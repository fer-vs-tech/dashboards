"""
@author: Kamoliddin Usmonov
@project: ESG
@description: ESG reporting dashboards
@date: 2023-02-27
"""
import logging

logger = logging.getLogger(__name__)
import sys

sys.path.append("..")
import time

import dash_bootstrap_components as dbc
import plotly.io as plt_io
from dash import dash_table, dcc, html, no_update
from dash.dependencies import Input, Output, State

import cm_dashboards.esg.dropdown_options as dropdown_options
import cm_dashboards.esg.results.cf_isp as cf_isp
import cm_dashboards.esg.results.funnel_plot as funnel_plot
import cm_dashboards.esg.results.schema as schema
import cm_dashboards.utilities as utilities
import cm_dashboards.wvr_data.wvr_functions as wvr_functions
from cm_dashboards.custom_template import custom_template
from cm_dashboards.esg.app_config import app

# Set WVR path globally for all dashboards
IFRS_PATH = None
NSP_PATH = None

# Apply our custome template
plt_io.templates["cloud_manager"] = custom_template

# Set up the layout
app.layout = dbc.Container(
    fluid="md",
    className="dbc",
    children=[
        dcc.Location(id="url", refresh=True),
        html.Div(
            className="logo-container",
            children=[
                html.Img(src="/dash/static/assets/wm_logo.svg"),
            ],
        ),
        dcc.Input(
            id="ifrs-wvr",
            value="",
            placeholder="C:\\temp\\results.wvr",
            style={"width": "50%", "display": "none"},
        ),
        dcc.Input(
            id="nsp-wvr",
            value="",
            placeholder="C:\\temp\\results.wvr",
            style={"width": "50%", "display": "none"},
        ),
        html.Div(
            className="body-container",
            children=[
                html.Div(
                    className="title-container",
                    children=[
                        html.Div(
                            id="journal-title",
                            children="ESG dashboards",
                            style={"text-decoration": "none"},
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        dbc.Toast(
                            id="flash-chart",
                            header="Error occurred",
                            is_open=False,
                            dismissable=True,
                            # duration=4000,
                            icon="danger",
                            style={
                                "position": "fixed",
                                "bottom": 120,
                                "right": 5,
                                "width": 300,
                                "zIndex": 10000,
                            },
                        ),
                        dbc.Toast(
                            id="flash-group",
                            header="Error occurred",
                            is_open=False,
                            dismissable=True,
                            # duration=4000,
                            icon="danger",
                            style={
                                "position": "fixed",
                                "bottom": 120,
                                "right": 5,
                                "width": 300,
                                "zIndex": 10000,
                            },
                        ),
                        dbc.Toast(
                            id="flash-wvr",
                            header="Error occurred 1",
                            is_open=False,
                            dismissable=True,
                            # duration=4000,
                            icon="danger",
                            style={
                                "position": "fixed",
                                "bottom": 120,
                                "right": 5,
                                "width": 300,
                                "zIndex": 10000,
                            },
                        ),
                        dbc.Tabs(
                            children=[
                                dbc.Tab(
                                    id="tab-1",
                                    label="Main",
                                    tab_class_name="unactive-tab",
                                    label_class_name="unactive-tab-label",
                                    active_tab_class_name="active-tab",
                                    active_label_class_name="active-tab-label",
                                    children=[
                                        html.Br(),
                                        dbc.Accordion(
                                            id="controllers",
                                            start_collapsed=False,
                                            children=[
                                                dbc.AccordionItem(
                                                    title="Controllers",
                                                    children=[
                                                        html.Div(
                                                            # style={"width": "50%"},
                                                            children=[
                                                                dbc.Row(
                                                                    children=[
                                                                        dbc.Col(
                                                                            children=[
                                                                                html.B(
                                                                                    "Reporting Date"
                                                                                ),
                                                                                dcc.Dropdown(
                                                                                    id="report-date-dropdown",
                                                                                    placeholder="Select report date ...",
                                                                                    persistence=True,
                                                                                    clearable=False,
                                                                                ),
                                                                                html.B(
                                                                                    "Scatter Plot Variable"
                                                                                ),
                                                                                dcc.Dropdown(
                                                                                    id="plot-variables-dropdown",
                                                                                    placeholder="Select variable ...",
                                                                                    persistence=True,
                                                                                    clearable=False,
                                                                                ),
                                                                            ],
                                                                        ),
                                                                        dbc.Col(
                                                                            children=[
                                                                                html.B(
                                                                                    "Grouping"
                                                                                ),
                                                                                dcc.Dropdown(
                                                                                    id="groups-dropdown",
                                                                                    placeholder="Select group ...",
                                                                                    persistence=True,
                                                                                    clearable=False,
                                                                                ),
                                                                                html.B(
                                                                                    "Graph max date"
                                                                                ),
                                                                                dcc.Dropdown(
                                                                                    id="max-date-dropdown",
                                                                                    placeholder="Select graph max date ...",
                                                                                    persistence=True,
                                                                                    clearable=False,
                                                                                ),
                                                                            ],
                                                                        ),
                                                                        dbc.Col(
                                                                            children=[
                                                                                html.B(
                                                                                    "Threshold"
                                                                                ),
                                                                                dbc.Input(
                                                                                    id="threshold",
                                                                                    type="number",
                                                                                    placeholder="4%",
                                                                                    value=4,
                                                                                    # min=0,
                                                                                    # max=100,
                                                                                    step=1,
                                                                                ),
                                                                                html.Br(),
                                                                                dbc.Button(
                                                                                    "Apply Settings",
                                                                                    id="apply-button",
                                                                                    className="me-2",
                                                                                    n_clicks=0,
                                                                                ),
                                                                                html.Br(),
                                                                            ],
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        dcc.Loading(
                                            id="main-loading",
                                            type="default",
                                            color="#2741BC",
                                            children=[
                                                html.Div(
                                                    className="body-content",
                                                    style={"height": "57vh"},
                                                    children=[
                                                        html.Div(
                                                            className="row",
                                                            children=[
                                                                html.Div(
                                                                    className="one-half column mixed-table row",
                                                                    children=[
                                                                        html.Label(
                                                                            id="main-label"
                                                                        ),
                                                                        html.Br(),
                                                                        dcc.Graph(
                                                                            config={
                                                                                "displaylogo": False
                                                                            },
                                                                            id="main-chart",
                                                                        ),
                                                                        # dash_table.DataTable(
                                                                        #     id="main-table",
                                                                        #     export_format="csv",
                                                                        #     is_focused=True,
                                                                        #     style_table={
                                                                        #         "overflowX": "auto",
                                                                        #         "minWidth": "100%",
                                                                        #         "maxHeight": "500px",
                                                                        #     },
                                                                        # ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                dbc.Tab(
                                    id="tab-2",
                                    label="NSP",
                                    tab_class_name="unactive-tab",
                                    label_class_name="unactive-tab-label",
                                    active_tab_class_name="active-tab",
                                    active_label_class_name="active-tab-label",
                                    children=[
                                        dcc.Loading(
                                            id="nsp-loading",
                                            type="default",
                                            color="#2741BC",
                                            children=[
                                                html.Div(
                                                    className="body-content",
                                                    style={"height": "57vh"},
                                                    children=[
                                                        html.Div(
                                                            className="row",
                                                            children=[
                                                                html.Div(
                                                                    className="one-half column mixed-table row",
                                                                    children=[
                                                                        html.Label(
                                                                            id="nsp-label",
                                                                            children="CF ISP chart",
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="cf-isp-table",
                                                                            export_format="csv",
                                                                            is_focused=True,
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                                "maxHeight": "500px",
                                                                                "height": "400px",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                dbc.Tab(
                                    id="tab-3",
                                    label="Schema",
                                    tab_class_name="unactive-tab",
                                    label_class_name="unactive-tab-label",
                                    active_tab_class_name="active-tab",
                                    active_label_class_name="active-tab-label",
                                    children=[
                                        dcc.Loading(
                                            id="schema-loading",
                                            type="default",
                                            color="#2741BC",
                                            children=[
                                                html.Div(
                                                    className="body-content",
                                                    style={"height": "57vh"},
                                                    children=[
                                                        html.Div(
                                                            className="row",
                                                            children=[
                                                                html.Div(
                                                                    className="one-half column mixed-table row",
                                                                    children=[
                                                                        html.Label(
                                                                            id="schema-label"
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="schema-table",
                                                                            export_format="csv",
                                                                            is_focused=True,
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                                "maxHeight": "500px",
                                                                                "height": "400px",
                                                                            },
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    [
        Output("ifrs-wvr", "value"),
        Output("nsp-wvr", "value"),
        Output("flash-wvr", "children"),
        Output("flash-wvr", "is_open"),
        Output("apply-button", "disabled"),
    ],
    Input("url", "search"),
)
def get_wvr_path(input_url):
    """
    Get wvr path from URL parameters
    """
    global IFRS_PATH
    global NSP_PATH
    flash_message = None
    show_flash = False
    disable_button = False

    logger.info("Input_url: {}".format(input_url))

    # Manually set WVR path and JOURNAL_NAME
    IFRS_PATH = "C:/Users/kamoliddin.usmonov/Documents/Development/ESG_package/NSP_APAC_Example/results/IFRS_Proj_Full.wvr"
    NSP_PATH = "C:/Users/kamoliddin.usmonov/Documents/Development/ESG_package/NSP_APAC_Example/results/NSP.wvr"

    # Get WVR path from URL parameters
    if input_url and "wvr" in input_url:
        # Unique model names for pattern matching
        model_names = ["IFRS", "NSP"]
        # Parse all WVR names
        wvr_paths = utilities.get_wvr_path_from_url(input_url, multiple=True)
        identified_models = wvr_functions.identify_models(wvr_paths, model_names)
        # Check if needed models exist
        if not bool(identified_models):
            flash_message = (
                "Some of the required models are missing or invalid output provided"
            )
            show_flash, disable_button = True, True
            return no_update, no_update, flash_message, show_flash, disable_button

        IFRS_PATH = identified_models.get("IFRS")
        NSP_PATH = identified_models.get("NSP")

    return IFRS_PATH, NSP_PATH, flash_message, show_flash, disable_button


@app.callback(
    [
        Output("report-date-dropdown", "options"),
        Output("report-date-dropdown", "value"),
    ],
    Input("ifrs-wvr", "value"),
)
def update_table(model_path):
    """
    Retrive report dates from output
    :param model_path: path to the model file
    :return result, default: List of dropdown options, and default value
    """
    logger.info("Report date dropdown - model path: {}".format(model_path))
    if IFRS_PATH is None or IFRS_PATH == "" or model_path == "" or model_path is None:
        return no_update, no_update

    # Get report dates from journal table
    result = dropdown_options.get_data(IFRS_PATH, type="report_date")
    default = result[0]["value"] if len(result) > 0 else None

    return result, default


@app.callback(
    [
        Output("plot-variables-dropdown", "options"),
        Output("plot-variables-dropdown", "value"),
    ],
    Input("ifrs-wvr", "value"),
)
def update_table(model_path):
    """
    Retrive plot variables
    :param report_date: The selected report date
    :return result, default: List of dropdown options, and default value
    """
    logger.info("Plot variable dropdown - model path: {}".format(model_path))
    if IFRS_PATH is None or IFRS_PATH == "" or model_path is None or model_path == "":
        return no_update, no_update

    # Get report dates from journal table
    result = dropdown_options.get_data(IFRS_PATH, type="variables")
    default = result[0]["value"] if len(result) > 0 else None

    return result, default


@app.callback(
    [
        Output("flash-group", "is_open"),
        Output("flash-group", "children"),
        Output("groups-dropdown", "options"),
        Output("groups-dropdown", "value"),
    ],
    [
        Input("report-date-dropdown", "value"),
        State("ifrs-wvr", "value"),
    ],
)
def update_table(report_date, model_path):
    """
    Retrive groups from output
    :param report_date: The selected report date
    :param model_path: The path to the model
    :return result, default: List of dropdown options, and default value
    """
    # logger.info("Selected date: {}".format(report_date))
    show_flash = True
    flash_message = "WVR file not found"
    result, default = no_update, no_update
    if model_path is None or model_path == "":
        return show_flash, flash_message, no_update, no_update

    # Get report dates from journal table
    try:
        flash_message = None
        result = dropdown_options.get_data(
            IFRS_PATH, type="groups", report_date=report_date
        )
        default = result[0]["value"] if len(result) > 0 else None
    except Exception as e:
        flash_message = "Error occurred while getting group dropdown data: {}".format(e)
        logger.error(flash_message)

    show_flash = bool(flash_message)
    return show_flash, flash_message, result, default


@app.callback(
    [
        Output("max-date-dropdown", "options"),
        Output("max-date-dropdown", "value"),
    ],
    [
        Input("report-date-dropdown", "value"),
        State("ifrs-wvr", "value"),
    ],
)
def update_table(report_date, model_path):
    """
    Retrive graph max date dropdown options
    :param report_date: The selected report date
    :param model_path: The path to the model
    :return result, default: List of dropdown options, and default value
    """
    # logger.info("Selected date: {}".format(report_date))
    if model_path is None or model_path == "":
        return no_update, no_update

    # Get report dates from journal table
    result = dropdown_options.get_data(
        IFRS_PATH, type="max_date", report_date=report_date
    )
    default = result[0]["value"] if len(result) > 0 else None

    return result, default


@app.callback(
    Output("threshold", "disabled"),
    Input("max-date-dropdown", "value"),
)
def update(max_date):
    """
    Disable the threshold input field if max date is not set to "Automatic calculation"
    :param report_date: The selected report date
    :return result, default: List of dropdown options, and default value
    """
    disabled = max_date != "AutoCalculate"
    logger.info("Selected max date: {} - {}".format(max_date, disabled))

    return disabled


@app.callback(
    [
        Output("flash-chart", "is_open"),
        Output("flash-chart", "children"),
        Output("main-chart", "figure"),
    ],
    [
        Input("apply-button", "n_clicks"),
        State("ifrs-wvr", "value"),
        State("report-date-dropdown", "value"),
        State("plot-variables-dropdown", "value"),
        State("groups-dropdown", "value"),
        State("max-date-dropdown", "value"),
        State("threshold", "value"),
    ],
)
def update_main(
    apply_button,
    model_path,
    report_date,
    plot_variable,
    group,
    max_date,
    threshold,
):
    """
    Update main chart
    :param IFRS_PATH: path to the WVR file
    :param report_date: Report date
    :param plot_variable: variable name to plot to the graph
    :param group: group name to filter
    :param senario: senario to filter
    :param max_date: max date to filter
    :param threshold: threshold value to filter
    :param start_collapsed: flag to collapse parent container
    :return data, colum, style_data, chart: Table data, column, style_data, and line chart
    """
    start_time = time.perf_counter()
    logger.info("Updating dashboard data ...")
    logger.info(
        "Report date: {}, plot variable: {}, group: {}, max date: {}, threshold: {}".format(
            report_date,
            plot_variable,
            group,
            max_date,
            threshold,
        )
    )

    show_flash = True
    flash_message = ""
    result = no_update

    # Check if parameters are valid
    if model_path is None:
        flash_message = "No wvr path specified"
        logger.error(flash_message)
        return show_flash, flash_message, result

    if report_date is None:
        flash_message = "No report date specified"
        show_flash = False
        logger.error(flash_message)
        return show_flash, flash_message, result

    # Get data
    try:
        flash_message = None
        result = funnel_plot.get_table_data(
            model_path, report_date, plot_variable, group, max_date, threshold
        )
    except Exception as e:
        flash_message = "Error occured while getting chart data: {}".format(e)
        logger.error(flash_message)

    show_flash = bool(flash_message)
    end_time = time.perf_counter()
    logger.info("Time took: {} seconds".format(end_time - start_time))

    return show_flash, flash_message, result


@app.callback(
    [
        Output("schema-table", "data"),
        Output("schema-table", "columns"),
        Output("schema-table", "style_data_conditional"),
    ],
    [
        Input("nsp-wvr", "value"),
        Input("report-date-dropdown", "value"),
    ],
)
def update_schema(model_path, report_date):
    """
    Update schema
    :param model_path: Path to the WVR file
    :param report_date: Selected report date
    :return: Schema
    """
    logger.info("Selected date: {}".format(report_date))
    result = no_update, no_update, no_update
    if model_path is None:
        logger.error("No wvr path specified")
        return result
    if report_date is None:
        logger.error("No report date specified")
        return result

    # Get schema
    try:
        result = schema.get_table_data(model_path, report_date, nsp=True)
    except Exception as e:
        logger.error("Error occured while getting schema information: {}".format(e))

    return result


@app.callback(
    [
        Output("cf-isp-table", "data"),
        Output("cf-isp-table", "columns"),
        Output("cf-isp-table", "style_data_conditional"),
    ],
    [
        Input("nsp-wvr", "value"),
        Input("report-date-dropdown", "value"),
    ],
)
def update(model_path, report_date):
    """
    Update CF-ISP chart
    :param model_path: Path to the WVR file
    :param report_date: Selected report date
    :return result: Table data
    """
    start_time = time.perf_counter()
    logger.info("Selected date: {}".format(report_date))
    result = no_update, no_update, no_update
    if model_path is None:
        logger.error("No wvr path specified")
        return result
    if report_date is None:
        logger.error("No report date specified")
        return result

    # Get data
    try:
        result = cf_isp.get_table_data(model_path, report_date)
    except Exception as e:
        logger.error("Error occured while getting CF ISP information: {}".format(e))

    end_time = time.perf_counter()
    logger.info("Time took: {} seconds".format(end_time - start_time))
    return result
