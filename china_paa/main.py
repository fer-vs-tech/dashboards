"""
:description: China PAA Dashboards
:author: Kamoliddin Usmonov
:date: 2023-11-20
"""

import logging
import sys

sys.path.append("..")

import time

from dash import no_update
from dash.dependencies import ALL, Input, Output, State

import cm_dashboards.china_paa.results.calculate_results as calculate_results
import cm_dashboards.china_paa.results.dropdown_options as dropdown_options
import cm_dashboards.china_paa.utils.helpers as helpers
import cm_dashboards.china_paa.utils.layout as layout
import cm_dashboards.utilities as utilities
import cm_dashboards.wvr_data.wvr_functions as wvr_functions
from cm_dashboards.china_paa.config.config import PROJECT_TITLE, app

logger = logging.getLogger(__name__)

app.layout = layout.generate_layout(PROJECT_TITLE)


@app.callback(
    [
        Output("wvr_path", "value"),
        Output("calculated-results", "clear_data"),
        Output("error-toast", "children"),
    ],
    Input("url", "search"),
)
def set_wvr_path(input_url):
    """
    Get wvr path from URL parameters
    """
    error_message = None
    clear_data = True
    logger.info(f"Input_url: {input_url}")

    wvr_path = (
        "C:/temp/dashboard/china/2024-03-04/R3S_IFRS_17/results/Grouping_Test.wvr"
    )
    if input_url:
        try:
            model_names = ["IFRS_17_PAA"]
            wvr_paths = utilities.get_wvr_path_from_url(input_url, multiple=True)
            identified_models = wvr_functions.identify_models(wvr_paths, model_names)
            if not bool(identified_models):
                wvr_path = None
                error_message = (
                    "The required model is missing or invalid output provided"
                )
                return wvr_path, clear_data, error_message
            logger.info(f"Identified models: {identified_models}")
            wvr_path = identified_models.get("IFRS_17_PAA")
        except Exception as e:
            logger.error(f"Error occured while getting WVR path: {e}")
            wvr_path = None
            error_message = "WVR path is missing or invalid output provided"
            return wvr_path, clear_data, error_message
    return wvr_path, clear_data, error_message


@app.callback(
    [
        Output("controllers-data", "data"),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    Input("wvr_path", "value"),
    prevent_initial_call=True,
)
def set_controllers_data(wvr_path):
    """
    Set controllers data
    :param wvr_path: path to the model file
    :return result: Data for controllers (dict)
    """
    logger.info("Setting controllers data")
    if not wvr_path:
        return no_update

    error_message = None
    data_for_controllers = {}
    try:
        data_for_controllers = dropdown_options.fetch_controllers_data(wvr_path)
    except Exception as e:
        error_message = f"Error occured while getting controllers data: {e}"
        logger.error(error_message)
    return data_for_controllers, error_message


@app.callback(
    [
        Output("report-date-dropdown", "options"),
        Output("report-date-dropdown", "value"),
        Output("model-dropdown", "options"),
        Output("model-dropdown", "value"),
        Output("portfolio-dropdown", "options"),
        Output("portfolio-dropdown", "value"),
        Output("risk-type-dropdown", "options"),
        Output("risk-type-dropdown", "value"),
        Output("grp-type-dropdown", "options"),
        Output("grp-type-dropdown", "value"),
        Output("inception-year-dropdown", "options"),
        Output("inception-year-dropdown", "value"),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    [
        Input("controllers-data", "data"),
    ],
    prevent_initial_call=True,
)
def set_openingdate_dropdown(controllers_data):
    """
    Set opening date value based on reporting date
    :param report_date: Selected report date
    :param wvr_path: path to the model file
    :return result, default: List of dropdown options, and default value
    """
    logger.info(f"Setting dropdown options ...")
    if not controllers_data:
        return [no_update] * 13

    error_message = None
    result = [no_update] * 12
    dropdowns = [
        "Report_Date",
        "Model",
        "Portfolio",
        "Risk_Type",
        "Grp_Type",
        "Inception_Year",
    ]
    for dropdown in dropdowns:
        try:
            options = dropdown_options.populate_dropdown(
                controllers_data,
                column_name=dropdown,
            )
            result[dropdowns.index(dropdown) * 2] = options
            if options:
                selected = options[0]["value"]
                result[dropdowns.index(dropdown) * 2 + 1] = selected
        except Exception as e:
            error_message = (
                f"Error occured while getting dropdown options for {dropdown}: {e}"
            )
            logger.error(error_message)
    return *result, error_message


@app.callback(
    [
        Output("open-date-dropdown", "options"),
        Output("open-date-dropdown", "value"),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    [
        Input("report-date-dropdown", "value"),
        Input("controllers-data", "data"),
    ],
    prevent_initial_call=True,
)
def set_openingdate_dropdown(report_date, controllers_data):
    """
    Set opening date value based on reporting date
    :param report_date: Selected report date
    :param wvr_path: path to the model file
    :return result, default: List of dropdown options, and default value
    """
    logger.info(f"Selected report date: {report_date}")
    if not report_date or not controllers_data:
        return [no_update] * 3

    error_message = None
    opening_dates = None
    opening_date = None
    try:
        report_dates = dropdown_options.populate_dropdown(
            controllers_data, column_name="Report_Date"
        )
        for i, current_report_date in enumerate(report_dates):
            if current_report_date["value"] == report_date:
                found_date = report_dates[i - 1 if i > 0 else 0]
                opening_dates = [found_date]
                opening_date = found_date["value"]
                break
            logger.warn(f"Opening date not found for {report_date}")
    except Exception as e:
        error_message = (
            f"Error occured while getting opening date dropdown options: {e}"
        )
        logger.error(error_message)
    return opening_dates, opening_date, error_message


@app.callback(
    output=[
        Output("calculated-results", "data"),
        Output("calculated-results", "clear_data", allow_duplicate=True),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    inputs=dict(
        button_clicks=Input("apply-button", "n_clicks"),
        input_data=dict(
            wvr=State("wvr_path", "value"),
            risk_type=State("risk-type-dropdown", "value"),
            report_date=State("report-date-dropdown", "value"),
            portfolio=State("portfolio-dropdown", "value"),
            grp_type=State("grp-type-dropdown", "value"),
            inception_year=State("inception-year-dropdown", "value"),
            model_value=State("model-dropdown", "value"),
        ),
    ),
    prevent_initial_call=True,
)
def calculate_and_store_results(button_clicks, input_data):
    """
    Calculate and store results
    :param button_clicks: Triggered button count
    :param input_data: Input data from dropdowns (dict)
    :return result: Calculated results (dict), clear data (bool), error message (str)
    """
    clear_data = True
    error_message = None
    if not input_data or button_clicks == 0:
        return no_update, no_update, error_message

    named_inputs = utilities.convert_dict_to_namedtuple(input_data)
    logger.info(f"Calculating results for: {named_inputs}")
    start_time = time.perf_counter()
    calc_result = {}
    try:
        calc_result = calculate_results.populate_results(named_inputs)
    except Exception as e:
        error_message = f"Error occured while generating dashboard data: {e}"
        logger.error(error_message)

    clear_data = not bool(calc_result)
    end_time = time.perf_counter()
    logger.info(f"Finished calculating results in {end_time - start_time:0.4f} seconds")
    logger.info(f"Clear data and disable button: {clear_data}")
    return calc_result, clear_data, error_message


@app.callback(
    [
        Output("dashboards", "children"),
        Output(
            {
                "type": "export-data-button",
                "index": "export-data-button",
            },
            "disabled",
            allow_duplicate=True,
        ),
    ],
    [
        Input("apply-button", "n_clicks"),
        Input("calculated-results", "data"),
    ],
    prevent_initial_call=True,
)
def show_results(n_clicks, calc_result):
    """
    Show results
    :param n_clicks: Triggered button count
    :param calc_result: Calculated results
    :return result: Dashboards layout and export button status
    """
    disabled = True
    if n_clicks == 0:
        return no_update, disabled
    if not bool(calc_result):
        message = "No results found"
        logger.error(message)
        return layout.render_error(message), disabled

    try:
        start_time = time.perf_counter()
        dashboard_resuls = calculate_results.generate_dashboard_data(calc_result[0])
        dashboards = layout.render_dashboards(dashboard_resuls)
        end_time = time.perf_counter()
        logger.info(
            f"Finished generating dashboard layout in {end_time - start_time:0.4f} seconds"
        )
        disabled = False
        return dashboards, disabled
    except Exception as e:
        message = f"Error occured while generating dashboard layout: {e}"
        logger.error(message)
        return layout.render_error(message), disabled


@app.callback(
    [
        Output("export-to-excel", "data"),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    inputs=dict(
        button_clicked=Input({"type": "export-data-button", "index": ALL}, "n_clicks"),
        data=State("calculated-results", "data"),
        input_data=dict(
            model_value=State("model-dropdown", "value"),
            report_date=State("report-date-dropdown", "value"),
            portfolio=State("portfolio-dropdown", "value"),
            risk_type=State("risk-type-dropdown", "value"),
            grp_type=State("grp-type-dropdown", "value"),
            inception_year=State("inception-year-dropdown", "value"),
        ),
    ),
    prevent_initial_call=True,
)
def export_to_excel(button_clicked, data, input_data):
    """
    Export results to excel file
    :param n_clicks: Triggered button count
    :param data: Calculated results
    :param report_date: Selected report date
    :param group_id: Selected group id
    :return result: Calculated results
    """
    error_message = None
    if button_clicked[0] is None:
        logger.info("No button clicked")
        return no_update, error_message

    named_inputs = utilities.convert_dict_to_namedtuple(input_data)
    try:
        logger.info(
            f"Exporting results to excel: {named_inputs.report_date} - {named_inputs.model_value}"
        )
        logger.info(f"Clicked button count: {button_clicked[0]}")
        prefix_name = [
            str(input_value) for input_value in input_data.values() if input_value
        ]
        prefix_name = "|".join(prefix_name)
        filename = utilities.generate_filename(
            extention="xlsx", prefix=prefix_name, add_timestamp=False
        )
        logger.info(f"Generated filename: {filename}")
        return (
            helpers.generate_report_file(data, filename, named_inputs.model_value),
            error_message,
        )
    except Exception as e:
        error_message = f"Error occured while exporting to excel: {e}"
        logger.error(error_message)
        return no_update, error_message


@app.callback(
    [
        Output("error-toast", "is_open"),
        Output("calculated-results", "clear_data", allow_duplicate=True),
        Output("apply-button", "disabled"),
    ],
    Input("error-toast", "children"),
    prevent_initial_call=True,
)
def show_error_message(message):
    """
    Show error message in toast if any error message is available
    :param message: Error message sent from other callbacks
    :return bool: Show/hide toast and disable/enable apply and export buttons
    """
    show_error_message = bool(message)
    clear_stored_data = show_error_message
    disable_apply_button = False

    if message is not None and "dropdown" in message:
        disable_apply_button = True
    return show_error_message, clear_stored_data, disable_apply_button
