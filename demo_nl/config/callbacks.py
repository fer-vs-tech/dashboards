import logging

import dash

logger = logging.getLogger(__name__)

import json
import time

from dash import no_update
from dash.dependencies import Input, Output, State

import cm_dashboards.demo_nl.utils.helpers as helpers
import cm_dashboards.demo_nl.utils.constants as constants
import cm_dashboards.demo_nl.layout.layout as layout
import cm_dashboards.utilities as utilities
import cm_dashboards.wvr_data.wvr_functions as wvr_functions
from cm_dashboards.demo_nl.config.config import app
from cm_dashboards.demo_nl.results.prepare_chart import generate
from cm_dashboards.demo_nl.results.prepare_data import get_programs, get_portfolios, get_triangleSize, get_triangleData, get_report_dates
from cm_dashboards.demo_nl.results.program_names import ChartNames, ProgramNames
from cm_dashboards.demo_nl.results import calculate_results
import cm_dashboards.demo_nl.results.ultimate_development_factors as ultimate_development_factors
import cm_dashboards.demo_nl.results.cumulative_incurred_claims as cumulative_incurred_claims
import cm_dashboards.demo_nl.results.box_plot_outliers as box_plot_outliers


@app.callback(
    output=[
        # Output("calculated-results", "data"),
        # Output("calculated-results", "clear_data", allow_duplicate=True),
        # Output("raw-data", "children"),
        # Output("data-chart", "children"),
        Output("ult-development-factors-chart", "figure"),
        Output("ult-development-factors-table", "data"),
        #Output("ult-development-factors-table", "columns"),
        #Output("ult-development-factors-table", "style_cell_conditional"),
        Output("controllers", "active_item"),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    inputs=dict(
        button_clicks=Input("lic-apply-button", "n_clicks"),
        wvr_files=Input("wvr_files", "data"),
        input_data=dict(
            program=State("lic-program-dropdown", "value"),
            portfolio=State("lic-portfolio-dropdown", "value"),
            method=State("lic-method-dropdown", "value"),
            model=State("lic-section-dropdown", "value"),
            section=State("lic-section-dropdown", "value"),
            component=State("lic-component-dropdown", "value"),
            titlename=State("lic-component-dropdown", "options"),
            reporting=State("lic-date-dropdown", "value"),
            dev=State("lic-slider-dev", "value"),
            orig=State("lic-slider-origin", "value"),
        ),
    ),
    prevent_initial_call=True,
)
def calculate_and_store_results(button_clicks, wvr_files, input_data):
    """
    Calculate and store results
    :param button_clicks: Triggered button count
    :param input_data: Input data from dropdowns (dict)
    :return result: Calculated results (dict), clear data (bool), error message (str)
    """
    clear_data = True
    error_message = None
    chart_fig = dash.no_update
    data_table_fig = dash.no_update
    columns = dash.no_update
    conditional_style = dash.no_update
    data_table = None
    chart = None

    if not input_data or button_clicks == 0:
        return no_update, no_update, "acc-filters", error_message

    named_inputs = utilities.convert_dict_to_namedtuple(input_data)

    title = [x['label'] for x in named_inputs.titlename if x['value'] == named_inputs.component]

    logger.info(f"Calculating results for: {named_inputs}")
    start_time = time.perf_counter()
    try:
        if named_inputs.section == "Run-Off Triangles":
            chart_fig, data_table_fig, columns, conditional_style = cumulative_incurred_claims.get_chart(named_inputs, wvr_files, title[0])
            #data_table_fig = dash.no_update
            # columns = dash.no_update
            #conditional_style = dash.no_update
            #data_table, chart = calculate_results.populate_runoff(named_inputs, wvr_files)
        elif named_inputs.section == "Age-To-Age Factors":
            data_table, chart = calculate_results.populate_ata_post(named_inputs, wvr_files, named_inputs.component)
        elif named_inputs.section == "Dev Factor":
            chart_fig, data_table_fig, columns, conditional_style = ultimate_development_factors.get_chart(wvr_files, "Ultimate Dev factors")
        elif named_inputs.section == "Data Analysis":
            #chart_fig, data_table_fig, columns, conditional_style = ultimate_development_factors.get_chart(wvr_files, "Ultimate Dev factors")
            chart_fig, data_table_fig, columns, conditional_style = box_plot_outliers.get_chart(named_inputs, wvr_files, title[0])
        else:
            x = 2
        end_time = time.perf_counter()
        logger.info(f"Finished calculating results in {end_time - start_time:0.4f} seconds")
        logger.info(f"Clear data and disable button: {clear_data}")
    except Exception as e:
        error_message = f"Error occured while generating dashboard data: {e}"
        logger.error(error_message)

    return chart_fig, data_table_fig, ["acc-filters", "acc-chart"], error_message
    # calc_results = {}
    # try:
    #     df_triangle, df_data = calculate_results.populate_results(named_inputs, wvr_files)
    #     calc_results = df_triangle.to_dict('records')
    #     df_data = df_data[df_data.returnValue.notnull()]
    #     logger.debug(df_data)
    #     # generate layout for data
    #     data_table = layout.render_datatable(calc_results)
    #     chart = layout.render_chart(df_data)
    #     #chart = helpers.create_line_chart(df=df_data, x="Origin_Period_Position", y="returnValue", title="prueba")
    #
    # except Exception as e:
    #     error_message = f"Error occured while generating dashboard data: {e}"
    #     logger.error(error_message)
    #
    # # clear_data = not bool(calc_result)
    # clear_data = True if calc_results is None else False
    # end_time = time.perf_counter()
    # logger.info(f"Finished calculating results in {end_time - start_time:0.4f} seconds")
    # logger.info(f"Clear data and disable button: {clear_data}")




# @app.callback(
#     [
#         Output("dashboards", "children"),
#     ],
#     [
#         Input("data_calculated", "data"),
#     ],
#     prevent_initial_call=True
# )
# def show_results(n_clicks, calc_result):
#     if n_clicks == 0:
#         return no_update
#     try:
#         start_time = time.perf_counter()
#         test = {}
#         test = calc_result
#         dashboards = layout.render_custom_triangle(test)
#         end_time = time.perf_counter()
#         logger.info(
#             f"Finished generating dashboard layout in {end_time - start_time:0.4f} seconds"
#         )
#         return dashboards
#     except Exception as e:
#         message = f"Error occured while generating dashboard layout: {e}"
#         logger.error(message)
#         return layout.render_error(message)

#
#
# @app.callback(
#     [
#         Output("data_calculated", "data"),
#         Output("calculated-results", "clear_data", allow_duplicate=True),
#     ],
#     [
#         Input("triangle-apply-button", "n_clicks"),
#         Input("wvr_files", "data")
#     ]
# )
# def show_triangle_results (nclicks, wvr_paths):
#     if nclicks == 0:
#         return dash.no_update
#     #     return layout.render_content("lerele " + str(nclicks))
#     df_data = get_triangleData(wvr_paths, "NL_LIC_Model", "Chain_Ladder", "Grp1", "BCL", "Tri_Paid_Claims_By_Year")
#     df2 = helpers.convert_df_to_triangle(df_data, ['Origin_Period_Position'], ['Dev_Period_Position'], ['returnValue'])
#
#     return (df2.to_dict("records"))
@app.callback(
    [
        Output("error-toast", "is_open"),
        Output("calculated-results", "clear_data", allow_duplicate=True),
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

    if message is not None and "dropdown" in message:
        disable_apply_button = True
    return show_error_message, clear_stored_data


@app.callback(
    [
        Output("wvr_files", "data"),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    Input("url", "search"),
    prevent_initial_call = True
)
def get_wvr_path(url_query_string):
    """
    Get wvr path from URL parameters
    :param url_query_string: URL parameters
    :return: WVR path value
    """
    try:
        error_message = None
        params = utilities.extract_url_params(url_query_string)

        logger.debug(f"params received: {params}")

        # validate input params received.

        #not valid parameters in request
        if "jobrun" not in params and "wvr" not in params:
            error_message = "Invalid parameters found in the request: missing jobrun and wvr"
            return dash.no_update, error_message

        # mismatch between param count received
        if len(list(params['jobrun'])) != len(list(params['wvr'])):
            logger.error(f"mismatch between jobruns {len(list(params['jobrun']))} and wvrs {len(list(params['wvr']))}")
            error_message = f"mismatch between jobruns {len(list(params['jobrun']))} and wvrs {len(list(params['wvr']))}"
            return dash.no_update, error_message

        # Invalid number of params allowed (1 or 4)
        if len(list(params['jobrun'])) > 4:
            logger.debug(f"Invalid number of models received: {len(params)}:")
            logger.debug(f"It must be 1 for batch runs or 4 for independent runs")
            error_message = f"Invalid number of models received: {len(params)}: It must be 1 for batch runs or 4 for independent runs"
            return dash.no_update, error_message

        wvr_paths = utilities.get_wvr_path_from_url(url_query_string, multiple=True)

        logger.debug(f"Params mapped to files {wvr_paths}")

        # Set default WVR paths manually (for development only)
        if wvr_paths is None or len(wvr_paths) == 0:
            logger.info("Setting default WVR paths manually to default single batch results file...")

            base_path = "C:/Program Files/RNA Analytics/WorkflowManager/Data/jobruns/Batch_NL_12497/"

            data_prep = f"{base_path}/Non-Life_WM.wvr"
            nl_lic = f"{base_path}/Non-Life_WM.wvr"
            nl_lrc_fit = f"{base_path}/Non-Life_WM.wvr"
            nl_lrc_eval = f"{base_path}/Non-Life_WM.wvr"

            # Map WVR files to dictionary for easy access in callbacks
            map_wvr_paths = {
                "NL_Data_Prep": data_prep,
                "NL_LIC_Model": nl_lic,
                "NL_LRC_Fit": nl_lrc_fit,
                "NL_LRC_Eval": nl_lrc_eval,
            }
        else:
            logger.info("Setting WVR path from URL parameters...")
            map_wvr_paths = helpers.set_wvr_nl_paths(wvr_paths)

    except Exception as e:
        logger.error("Error occurred while getting WVR path and data: {}".format(e))
        error_message = "Error occurred while getting WVR path and data: {}".format(e)

    return map_wvr_paths, error_message

@app.callback(
    [
        Output("programs", "data"),
        Output("portfolios", "data"),
        Output("methods", "data"),
        Output("dates", "data"),
        Output("dev-periods", "data"),
        Output("origin-periods", "data"),
        Output("lic-tab", "disabled"),
        Output("lrc-fit-tab", "disabled"),
        Output("lrc-eval-tab", "disabled"),
        Output("error-toast", "is_open", allow_duplicate=True),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    [
     #Input("triangle-model-dropdown", "value"),
     Input("wvr_files", "data"),
     ],
    prevent_initial_call=True,
)
def pre_load_data(wvr_files):
    no_update = dash.no_update
    programs = None
    portfolios = []
    methods = []
    dates = []
    error_message = ""
    logger.debug("received session wvr_files")
    logger.debug(constants.MENU_MODELS["LIC Model"])
    logger.debug(wvr_files)
    logger.debug(wvr_files[constants.MENU_MODELS["LIC Model"]])
    #tabs disabled by default, only enabled if model received
    tab_lic = tab_lrc_fit = tab_lrc_eval = True

    if constants.MENU_MODELS["LIC Model"] in wvr_files:
        tab_lic = False
        programs, portfolios, methods, dates, dev, orig = generate_filter_options(wvr_files[constants.MENU_MODELS["LIC Model"]], constants.MENU_MODELS["LIC Model"])
    else:
        error_message = str(error_message) + "LIC model not found. "

    if constants.MENU_MODELS["LRC Fit Model"] in wvr_files:
        tab_lrc_fit = False
        if not programs:
            programs, portfolios, methods, dates, dev, orig = generate_filter_options(wvr_files[constants.MENU_MODELS["LIC Model"]], constants.MENU_MODELS["LIC Model"])
    else:
        error_message = str(error_message) + "LRC Fit model not found. "

    if constants.MENU_MODELS["LRC Eval Model"] in wvr_files:
        tab_lrc_eval = False
        if not programs:
            programs, portfolios, methods, dates, dev, orig = generate_filter_options(wvr_files[constants.MENU_MODELS["LIC Model"]], constants.MENU_MODELS["LIC Model"])
    else:
        str(error_message) + "LRC Eval model not found. "

    # df_programs = get_programs(wvr_files[model_value], model_value)
    #
    # programs = df_programs['program_name']
    # programs = list(filter(None, programs))
    #
    # if model_value.lower() == "nl_lic_model":
    #     options = NL_LIC_SECTIONS
    # elif model_value.lower() == "nl_lrc_fit":
    #     options = NL_LRC_FIT_SECTIONS
    # elif model_value.lower() == "nl_lrc_eval":
    #     options = NL_LRC_EVAL_SECTIONS
    # elif model_value.lower() == "nl_data_prep":
    #     options = NL_LRC_EVAL_SECTIONS
    # else:
    #     options = None

    return programs, portfolios, methods, dates, dev, orig, tab_lic, tab_lrc_fit, tab_lrc_eval, error_message, error_message

@app.callback(
    [
        Output("lic-apply-button", "disabled"),
        Output("lic-section-dropdown", "options"),
        Output("lic-section-dropdown", "value"),
    ],
    [
     Input("lic-tab", "disabled"),
     ],
    prevent_initial_call=True,
)
def load_lic_sections(lic_tab_disabled):
    disabled = True
    no_update = dash.no_update

    if lic_tab_disabled:
        return disabled, no_update, no_update
    else:
        options = list(constants.NL_LIC_SECTIONS.keys())
        return not disabled, options, options[0]


@app.callback(
    [
        Output("lic-type-dropdown", "options"),
        Output("lic-type-dropdown", "value"),
    ],
    [
     Input("lic-section-dropdown", "value"),
     ],
    prevent_initial_call=True,
)
def load_lic_types(selected_section):
    no_update = dash.no_update
    types = list(constants.NL_LIC_SECTIONS[selected_section].keys())
    return types, types[0]

@app.callback(
    [
        Output("lic-component-dropdown", "options"),
        Output("lic-component-dropdown", "value"),
    ],
    [
     Input("lic-type-dropdown", "value"),
     State("lic-section-dropdown", "value"),
     ],
    prevent_initial_call=True,
)
def load_lic_outputs(selected_type, sel_section):
    no_update = dash.no_update
    types = constants.NL_LIC_SECTIONS[sel_section]
    test = types[selected_type]
    return test, test[0]

@app.callback(
    [
        Output("lic-program-dropdown", "options"),
        Output("lic-program-dropdown", "value"),
        Output("lrc-fit-program-dropdown", "options"),
        Output("lrc-fit-program-dropdown", "value"),
        Output("lrc-eval-program-dropdown", "options"),
        Output("lrc-eval-program-dropdown", "value"),
    ],
    [
     Input("programs", "data"),
     ],
    prevent_initial_call=True,
)
def load_programs(programs):
    return programs, programs[0], programs, programs[0], programs, programs[0]


@app.callback(
    [
        Output("lic-portfolio-dropdown", "options"),
        Output("lic-portfolio-dropdown", "value"),
        Output("lrc-fit-portfolio-dropdown", "options"),
        Output("lrc-fit-portfolio-dropdown", "value"),
        Output("lrc-eval-portfolio-dropdown", "options"),
        Output("lrc-eval-portfolio-dropdown", "value"),
    ],
    [
     Input("portfolios", "data"),
     ],
    prevent_initial_call=True,
)
def load_portfolios(portfolios):
    return portfolios, portfolios[0], portfolios, portfolios[0], portfolios, portfolios[0]

@app.callback(
    [
        Output("lic-method-dropdown", "options"),
        Output("lic-method-dropdown", "value"),
        Output("lrc-fit-method-dropdown", "options"),
        Output("lrc-fit-method-dropdown", "value"),
        Output("lrc-eval-method-dropdown", "options"),
        Output("lrc-eval-method-dropdown", "value"),
    ],
    [
     Input("methods", "data"),
     ],
    prevent_initial_call=True,
)
def load_methods(methods):
    return methods, methods[0], methods, methods[0], methods, methods[0]

@app.callback(
    [
        Output("lic-date-dropdown", "options"),
        Output("lic-date-dropdown", "value"),
        Output("lrc-fit-date-dropdown", "options"),
        Output("lrc-fit-date-dropdown", "value"),
        Output("lrc-eval-date-dropdown", "options"),
        Output("lrc-eval-date-dropdown", "value"),
    ],
    [
     Input("dates", "data"),
     ],
    prevent_initial_call=True,
)
def load_rep_dates(dates):
    return dates, dates[0], dates, dates[0], dates, dates[0]


@app.callback(
    [
        Output("lic-slider-dev", "min"),
        Output("lic-slider-dev", "max"),
        Output("lic-slider-dev", "marks"),
        Output("lic-slider-dev", "value"),
        Output("lrc-fit-slider-dev", "min"),
        Output("lrc-fit-slider-dev", "max"),
        Output("lrc-fit-slider-dev", "marks"),
        Output("lrc-fit-slider-dev", "value"),
        Output("lrc-eval-slider-dev", "min"),
        Output("lrc-eval-slider-dev", "max"),
        Output("lrc-eval-slider-dev", "marks"),
        Output("lrc-eval-slider-dev", "value"),
    ],
    [
     Input("dev-periods", "data"),
     ],
    prevent_initial_call=True,
)
def load_dev_periods(devs):
    min = 1
    marksDev = {i: {'label': str(i)} for i in range(1, devs + min)}
    return min, devs, marksDev, [min, devs], min, devs, marksDev, [min, devs], min, devs, marksDev, [min, devs]


@app.callback(
    [
        Output("lic-slider-origin", "min"),
        Output("lic-slider-origin", "max"),
        Output("lic-slider-origin", "marks"),
        Output("lic-slider-origin", "value"),
        Output("lrc-fit-slider-origin", "min"),
        Output("lrc-fit-slider-origin", "max"),
        Output("lrc-fit-slider-origin", "marks"),
        Output("lrc-fit-slider-origin", "value"),
        Output("lrc-eval-slider-origin", "min"),
        Output("lrc-eval-slider-origin", "max"),
        Output("lrc-eval-slider-origin", "marks"),
        Output("lrc-eval-slider-origin", "value"),
    ],
    [
     Input("origin-periods", "data"),
     ],
    prevent_initial_call=True,
)
def load_origin_periods(orig):
    min = 1
    marksOrig = {i: {'label': str(i)} for i in range(1, orig + min)}
    return min, orig, marksOrig, [min, orig], min, orig, marksOrig, [min, orig], min, orig, marksOrig, [min, orig]

# @app.callback(
#     [
#         Output("lic-component-dropdown", "options"),
#         Output("lic-component-dropdown", "value"),
#         Output("error-toast", "is_open", allow_duplicate=True),
#     ],
#     [Input("lic-type-dropdown", "value"),
#      ],
#     prevent_initial_call=True,
# )
# def load_options(option_value):
#     options = None
#     noupdate = dash.no_update
#     default_variable = dash.no_update
#     if option_value == "":
#         return noupdate, noupdate, False
#
#     if option_value.lower() == "run-off triangles":
#         options = constants.NL_RUN_OFF
#         logger.debug("FER CHANGED")
#         logger.debug(constants.NL_RUN_OFF[1])
#         default_variable = constants.NL_RUN_OFF[1].get("value")
#     elif option_value.lower() == "data analysis":
#         options = constants.NL_DATA_ANALYSIS
#     elif option_value.lower() == "age-to-age factors":
#         options = constants.NL_AGE_2_AGE
#         default_variable = constants.NL_AGE_2_AGE[0].get("value")
#     elif option_value.lower() == "dev factor":
#         options = constants.NL_DEV_FACTORS
#     elif option_value.lower() == "proj. results":
#         options = constants.NL_PROJ_RESULTS
#     elif option_value.lower() == "lic summary":
#         options = constants.NL_LIC_SUMMARY
#     else:
#         options = [""]
#
#     return options, default_variable, False


# Generate all the dropdown options (program, portfolio, method, dates and dev & origin positions
def generate_filter_options (path, model):

    programs = None
    portfolios = []
    methods = []

    logger.debug(f"received {model} and {path}")

    df_programs = get_programs(path, model)
    programs = df_programs['program_name']
    programs = list(filter(None, programs))
    df_portfolios = get_portfolios(path, model, programs[0])
    for item in df_portfolios['portfolio']:
        if item[:item.find('_')] not in portfolios:
            portfolios.append(item[:item.find('_')])
        if item[item.find('_') + 1:] not in methods:
            methods.append(item[item.find('_') + 1:])
    df_dates = get_report_dates(path, model, programs[0])
    dates = df_dates['report_date']
    dates = list(filter(None, dates))
    triangle_size = get_triangleSize(path, model, programs[0])
    dev = int(triangle_size['dev'])
    orig = int(triangle_size['origin'])

    return programs, portfolios, methods, dates, dev, orig