"""
:description: China Subledger Dashboards
:author: Kamoliddin Usmonov
:date: 2024-04-01
"""

import logging
import sys

sys.path.append("..")

import json

from dash import dcc, no_update
from dash.dependencies import ALL, MATCH, Input, Output, State

import cm_dashboards.alchemy_db as db
import cm_dashboards.china_subledger.results.calculate_results as calculate_results
import cm_dashboards.china_subledger.results.dropdown_options as dropdown_options
import cm_dashboards.china_subledger.utils.helpers as helpers
import cm_dashboards.china_subledger.utils.layout_loader as layout_loader
import cm_dashboards.utilities as utilities
import cm_dashboards.wvr_data.wvr_functions as wvr_functions
from cm_dashboards.china_subledger.config.config import PROJECT_TITLE, app

logger = logging.getLogger(__name__)
app.layout = layout_loader.generate_layout(PROJECT_TITLE)


@app.callback(
    [
        Output("wvr_path", "value"),
        Output("previous-report-date-dropdown", "placeholder"),
        Output("report-date-dropdown", "placeholder"),
        Output("assumptions", "data"),
        Output("dashboards", "children", allow_duplicate=True),
    ],
    Input("url", "search"),
    prevent_initial_call=True,
)
@utilities.timeit(is_callback=True)
def set_wvr_path(input_url):
    """
    Get WVR path from URL parameters, read runtime parameters, and load assumptions from DB
    """
    logger.info(f"Input_url: {input_url}")
    wvr_paths = r"C:\temp\dashboard\china_subledger\2024-04-16\China_IFRS17_Subledger\results\Subledger.wvr"
    previous_report_date = None
    report_date = None
    assumptions = None
    jobrun_id = None
    error_message = no_update
    try:
        model_name = "IFRS_17"
        if input_url:
            jobrun_id = utilities.get_jobrun_id_from_url(input_url)
            wvr_paths = utilities.get_wvr_path_from_url(input_url)

        if not wvr_paths:
            raise ValueError("WVR file does not exist")
        identified_models = wvr_functions.identify_models(wvr_paths, model_name)

        if not bool(identified_models):
            raise ValueError("No valid models found")
        wvr_path = identified_models.get(model_name)
        runtime_params = wvr_functions.read_jobrun_params(wvr_path)
        logger.info(f"Runtime params: {json.dumps(runtime_params, indent=4)}")
        assumption_name = runtime_params.get("Subledger_Assumption")
        if not assumption_name:
            raise ValueError("Assumption name is missing in runtime params")

        report_date = runtime_params.get("Reporting_Date")
        previous_report_date = runtime_params.get("Previous_Reporting_Date")
        if not report_date or not previous_report_date:
            raise ValueError(
                "'Report Date' and 'Previous Report Date' could not be found in run time paramaters"
            )

        previous_report_date = wvr_functions.from_r3s_date(previous_report_date)
        report_date = wvr_functions.from_r3s_date(report_date)
        assumptions = db.get_assumption_set_data(assumption_name, jobrun_id)
    except Exception as error:
        logger.error(f"Error occured while getting WVR path: {error}")
        error_message = layout_loader.render_error(str(error))
        wvr_path = None

    finally:
        return (
            wvr_path,
            previous_report_date,
            report_date,
            assumptions,
            error_message,
        )


@app.callback(
    [
        Output("model_results", "data"),
        Output(
            {"type": "export-data-button", "index": ALL},
            "disabled",
            allow_duplicate=True,
        ),
    ],
    [
        Input("wvr_path", "value"),
        Input("previous-report-date-dropdown", "placeholder"),
        Input("report-date-dropdown", "placeholder"),
    ],
    prevent_initial_call=True,
)
@utilities.timeit(is_callback=True)
def populate_dashboard_data(wvr_path, previous_report_date, report_date):
    """
    Populate dashboard data
    """
    result = None
    disabled_button = [True]
    try:
        if not wvr_path:
            raise ValueError("WVR path is missing")
        if not previous_report_date:
            raise ValueError("Previous report date is missing")
        if not report_date:
            raise ValueError("Report date is missing")

        result = calculate_results.populate_results(
            wvr_path, previous_report_date, report_date
        )
        disabled_button = [False]
    except Exception as e:
        logger.error(f"Error occured while getting controllers data: {e}")

    finally:
        return result, disabled_button


@app.callback(
    [
        Output("group-id-dropdown", "options"),
        Output("group-id-dropdown", "value"),
        Output("group-id-dropdown", "disabled"),
        Output("apply-button", "disabled"),
    ],
    [
        Input("model_results", "data"),
    ],
)
@utilities.timeit(is_callback=True)
def update_dropdowns(model_results):
    """
    Update dropdowns
    """
    result = [no_update] * 4
    try:
        if not model_results:
            raise Exception("Model results are missing")
        dropdowns = [
            "Group_ID",
        ]

        for dropdown in dropdowns:
            try:
                options = dropdown_options.populate_dropdown(
                    model_results,
                    column_name=dropdown,
                )
                result[dropdowns.index(dropdown) * 2] = options
                if options:
                    selected = options[0]["value"]
                    result[dropdowns.index(dropdown) * 2 + 1] = selected
                    result[dropdowns.index(dropdown) * 2 + 2] = False

            except Exception as e:
                error_message = (
                    f"Error occured while getting dropdown options for {dropdown}: {e}"
                )
                logger.error(error_message)

        result[-1] = False

    except Exception as e:
        logger.error(f"Error occured while updating dropdowns: {e}")

    finally:
        return result


@app.callback(
    [
        Output("dashboards", "children"),
        Output("apply-button", "disabled", allow_duplicate=True),
    ],
    inputs=dict(
        n_clicks=Input("apply-button", "n_clicks"),
        input_data=dict(
            previous_report_date=State("previous-report-date-dropdown", "placeholder"),
            report_date=State("report-date-dropdown", "placeholder"),
            group_id=State("group-id-dropdown", "value"),
            assumptions=State("assumptions", "data"),
            model_results=State("model_results", "data"),
        ),
    ),
    prevent_initial_call=True,
)
@utilities.timeit(is_callback=True)
def generate_dashboard_result(n_clicks, input_data):
    """
    Generate dashboards
    """
    is_button_disabled = False
    result = no_update
    try:
        if not n_clicks or n_clicks < 1:
            return result

        inputs = utilities.convert_dict_to_namedtuple(input_data)
        logger.info(f"Report date: {inputs.report_date}, Group ID: {inputs.group_id}")
        if not inputs.report_date or not inputs.previous_report_date:
            raise ValueError("Report date and previous report date are missing")
        if not inputs.group_id:
            raise ValueError("Group ID is required to select")
        if not inputs.assumptions:
            raise ValueError("Assumptions are missing")
        if not inputs.model_results:
            raise ValueError("No data found in the model output")

        model_results = helpers.dict_to_df(inputs.model_results)
        model_results = model_results[model_results["Group_ID"] == inputs.group_id]
        if model_results.empty:
            raise ValueError("No data found for the selected report date and group ID")
        variable_mappings, event_mappings = calculate_results.get_mapping_tables(
            inputs.assumptions, model_results
        )
        if variable_mappings.empty:
            raise ValueError("No valid data found in variable mappings")
        if event_mappings.empty:
            raise ValueError("No valid data found in event mappings")

        dashboard_results = calculate_results.generate_dashboard_data(
            variable_mappings,
            event_mappings,
            model_results,
            inputs.previous_report_date,
            inputs.report_date,
        )
        result = layout_loader.render_dashboards(dashboard_results)

    except ValueError as error:
        logger.error(f"Invalid input: {error}")
        result = layout_loader.render_error(str(error))

    except Exception as error:
        message = f"Error occured while generating dashboards: {error}"
        logger.error(message)
        result = layout_loader.render_error(message)

    return result, is_button_disabled


@app.callback(
    [
        Output("export-to-excel", "data"),
        Output(
            {"type": "export-data-button", "index": ALL},
            "disabled",
            allow_duplicate=True,
        ),
    ],
    inputs=dict(
        button_click=Input({"type": "export-data-button", "index": ALL}, "n_clicks"),
        input_data=dict(
            previous_report_date=State("previous-report-date-dropdown", "placeholder"),
            report_date=State("report-date-dropdown", "placeholder"),
            model_results=State("model_results", "data"),
            assumptions=State("assumptions", "data"),
        ),
    ),
    prevent_initial_call=True,
)
@utilities.timeit(is_callback=True)
def export_data_to_excel(button_click, input_data):
    """
    Export data to Excel
    """
    is_button_disabled = [True]
    result = None
    try:
        inputs = utilities.convert_dict_to_namedtuple(input_data)
        logger.info(
            f"Report date: {inputs.report_date}, previous report date: {inputs.previous_report_date}"
        )
        if not inputs.report_date or not inputs.previous_report_date:
            raise ValueError("Report date and previous report date are missing")
        if not inputs.model_results:
            raise ValueError("No data found in the model output")
        if not inputs.assumptions:
            raise ValueError("Assumptions are missing")

        model_results = helpers.dict_to_df(inputs.model_results)
        result_df = calculate_results.generate_export_file(
            model_results,
            inputs.assumptions,
            inputs.previous_report_date,
            inputs.report_date,
        )
        if not result_df:
            raise ValueError("Cannot generate export file")

        filename = utilities.generate_filename("xlsx", "ChinaSubledger", True)
        result = dcc.send_bytes(
            result_df,
            filename,
            index=False,
        )
        is_button_disabled = [False]

    except ValueError as error:
        logger.info(f"Invalid input provided: {error}")

    except Exception as error:
        logger.info(f"Failed to export data to Excel: {error}")

    finally:
        return result, is_button_disabled


@app.callback(
    Output(
        {"type": "export-data-button", "index": MATCH}, "disabled", allow_duplicate=True
    ),
    Input({"type": "export-data-button", "index": MATCH}, "n_clicks"),
    prevent_initial_call=True,
)
def disabled_export_button(n_clicks):
    """
    Make sure the button stays disabled while data is being prepared
    """
    logger.info(f"Disable export button callback is triggered: {n_clicks} times")
    return True
