"""
@author: Kamoliddin Usmonov
@project: Dashboard Journal for SELIC POC
@description: Journal view page
@date: 2022-07-27
"""
import logging

logger = logging.getLogger(__name__)

import sys
import time
from datetime import datetime

from flask import redirect, send_file

from cm_dashboards.server import server as application

sys.path.append("..")

import dash
import dash_bootstrap_components as dbc
import plotly.io as plt_io
from dash import dash_table, dcc, html, no_update
from dash.dependencies import Input, Output, State

import cm_dashboards.custom_html_template as custom_html_template
import cm_dashboards.ifrs17_accounting.helpers as helpers
import cm_dashboards.ifrs17_accounting.journal_table as journal_table
import cm_dashboards.ifrs17_accounting.results.actual_journal as actual_journal
import cm_dashboards.ifrs17_accounting.results.expected_if_journal as expected_if_journal
import cm_dashboards.ifrs17_accounting.results.expected_nb_journal as expected_nb_journal
import cm_dashboards.ifrs17_accounting.results.lic_journal as lic_journal
import cm_dashboards.ifrs17_accounting.results.transition_journal as transition_journal
import cm_dashboards.utilities as utilities
from cm_dashboards.custom_template import custom_template
from cm_dashboards.server import server

DB_ENGINE = None
DB_METADATA = None
WVR_PATH = None
RETURN_URL = None
PROJECT_NAME = "accounting"

# External scripts and CSS stylesheets
external_scripts = ["../../static/utils/tabs.js"]
external_stylesheets = ["../../static/css/bootstrap.css", "../../static/css/styles.css"]
# Apply our custome template
plt_io.templates["cloud_manager"] = custom_template

# App configuration for the Nonlife Dashboard
app = dash.Dash(
    name=PROJECT_NAME,
    title="IFRS17 Acounting Dashboard - Journals",
    update_title="(Updating) IFRS17 Acounting Dashboard - Journals",
    server=server,
    eager_loading=True,
    url_base_pathname=f"/dash/{PROJECT_NAME}/journal_view/",
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    compress=server.config["COMPRESS_CONTENT"],
)

# Change the default favicon
app.index_string = custom_html_template.WM_TEMPLATE

# Enable dev mode if turned on in config
debug_mode = utilities.get_entry_from_config_file("dashboard", "debug_mode", False)
if debug_mode == "True":
    app.config.suppress_callback_exceptions = True
    app.enable_dev_tools(debug=True, dev_tools_ui=True, dev_tools_props_check=True)

# Define app layout
hidden_columns = [
    "NB_IF",
    "GOC",
    "CONTRACT_GROUP",
    "CONTRACT_CLASS",
    "PTFLO",
    "COHT",
    "Posting_Key",
    "Aggregates",
    "Branch",
    "Profit_Center_Code",
]

# Table data
style_data = {
    "minWidth": "100px",
    "width": "fit-content",
    "maxWidth": "220px",
    "overflow": "hidden",
    "textOverflow": "ellipsis",
}

style_table = {
    "overflowX": "auto",
    "minWidth": "100%",
}

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
        html.Div(
            style=dict(display="none"),
            children=[
                dcc.Input(
                    id="wvr-path",
                    value="",
                    placeholder="",
                ),
                dcc.Input(
                    id="company-id",
                    value="",
                    placeholder="",
                ),
                dcc.Input(
                    id="journal-type",
                    value="",
                    placeholder="",
                ),
            ],
        ),
        html.Div(
            className="body-container",
            children=[
                html.Div(
                    className="title-container",
                    children=[
                        html.A(
                            id="journal-title",
                            children="Journals on Cloud Manager",
                            href="/dash/accounting/",
                            style={"text-decoration": "none"},
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        dbc.Tabs(
                            children=[
                                dbc.Tab(
                                    id="tab-1",
                                    label="Actual CF Journal",
                                    tab_class_name="unactive-tab",
                                    label_class_name="unactive-tab-label",
                                    active_tab_class_name="active-tab",
                                    active_label_class_name="active-tab-label",
                                    children=[
                                        dcc.Loading(
                                            id="actualcf-journal-loading",
                                            type="default",
                                            color="#2741BC",
                                            debug=False,
                                            children=[
                                                html.Div(
                                                    className="body-content",
                                                    children=[
                                                        html.Div(
                                                            className="row",
                                                            children=[
                                                                html.Div(
                                                                    className="one-half column custom-table",
                                                                    children=[
                                                                        html.A(
                                                                            id="actualcf-journal-reverse-link",
                                                                            children=html.Button(
                                                                                className="reverse",
                                                                                children="Reverse",
                                                                                id="actualcf-journal-reverse-button",
                                                                            ),
                                                                        ),
                                                                        html.Br(),
                                                                        html.Label(
                                                                            id="actualcf-journal-label"
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="actualcf-journal-table",
                                                                            style_table=style_table,
                                                                            style_data=style_data,
                                                                            hidden_columns=hidden_columns,
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
                                    id="tab-2",
                                    label="Expected CF Journal (in-force)",
                                    tab_class_name="unactive-tab",
                                    label_class_name="unactive-tab-label",
                                    active_tab_class_name="active-tab",
                                    active_label_class_name="active-tab-label",
                                    children=[
                                        dcc.Loading(
                                            id="expected-journal-inforce-loading",
                                            type="default",
                                            color="#2741BC",
                                            debug=False,
                                            children=[
                                                html.Div(
                                                    className="body-content",
                                                    children=[
                                                        html.Div(
                                                            className="row",
                                                            children=[
                                                                html.Div(
                                                                    className="one-half column custom-table",
                                                                    children=[
                                                                        html.A(
                                                                            id="expected-journal-inforce-reverse-link",
                                                                            children=html.Button(
                                                                                className="reverse",
                                                                                children="Reverse",
                                                                                id="expected-journal-inforce-reverse-button",
                                                                            ),
                                                                        ),
                                                                        html.Br(),
                                                                        html.Label(
                                                                            id="expected-journal-inforce-label"
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="expected-journal-inforce-table",
                                                                            style_table=style_table,
                                                                            style_data=style_data,
                                                                            hidden_columns=hidden_columns,
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
                                    label="Expected CF Journal (NB)",
                                    tab_class_name="unactive-tab",
                                    label_class_name="unactive-tab-label",
                                    active_tab_class_name="active-tab",
                                    active_label_class_name="active-tab-label",
                                    children=[
                                        dcc.Loading(
                                            id="expected-journal-nb-loading",
                                            type="default",
                                            color="#2741BC",
                                            debug=False,
                                            children=[
                                                html.Div(
                                                    className="body-content",
                                                    children=[
                                                        html.Div(
                                                            className="row",
                                                            children=[
                                                                html.Div(
                                                                    className="one-half column custom-table",
                                                                    children=[
                                                                        html.A(
                                                                            id="expected-journal-nb-reverse-link",
                                                                            children=html.Button(
                                                                                className="reverse",
                                                                                children="Reverse",
                                                                                id="expected-journal-nb-reverse-button",
                                                                            ),
                                                                        ),
                                                                        html.Br(),
                                                                        html.Label(
                                                                            id="expected-journal-nb-label"
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="expected-journal-nb-table",
                                                                            style_table=style_table,
                                                                            style_data=style_data,
                                                                            hidden_columns=hidden_columns,
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
                                    id="tab-4",
                                    label="LIC CF Journal",
                                    tab_class_name="unactive-tab",
                                    label_class_name="unactive-tab-label",
                                    active_tab_class_name="active-tab",
                                    active_label_class_name="active-tab-label",
                                    children=[
                                        dcc.Loading(
                                            id="lic-cf-journal-loading",
                                            type="default",
                                            color="#2741BC",
                                            debug=False,
                                            children=[
                                                html.Div(
                                                    className="body-content",
                                                    children=[
                                                        html.Div(
                                                            className="row",
                                                            children=[
                                                                html.Div(
                                                                    className="one-half column custom-table",
                                                                    children=[
                                                                        html.A(
                                                                            id="lic-cf-journal-reverse-link",
                                                                            children=html.Button(
                                                                                className="reverse",
                                                                                children="Reverse",
                                                                                id="lic-cf-journal-reverse-button",
                                                                            ),
                                                                        ),
                                                                        html.Br(),
                                                                        html.Label(
                                                                            id="lic-cf-journal-label"
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="lic-cf-journal-table",
                                                                            style_table=style_table,
                                                                            style_data=style_data,
                                                                            hidden_columns=hidden_columns,
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
                                    id="tab-5",
                                    label="Transition Journal",
                                    tab_class_name="unactive-tab",
                                    label_class_name="unactive-tab-label",
                                    active_tab_class_name="active-tab",
                                    active_label_class_name="active-tab-label",
                                    children=[
                                        dcc.Loading(
                                            id="transition-journal-journal-loading",
                                            type="default",
                                            color="#2741BC",
                                            debug=False,
                                            children=[
                                                html.Div(
                                                    className="body-content",
                                                    children=[
                                                        html.Div(
                                                            className="row",
                                                            children=[
                                                                html.Div(
                                                                    className="one-half column custom-table",
                                                                    children=[
                                                                        html.A(
                                                                            id="transition-journal-reverse-link",
                                                                            children=html.Button(
                                                                                className="reverse",
                                                                                children="Reverse",
                                                                                id="transition-journal-reverse-button",
                                                                            ),
                                                                        ),
                                                                        html.Br(),
                                                                        html.Label(
                                                                            id="transition-journal-label"
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="transition-journal-table",
                                                                            style_table=style_table,
                                                                            style_data=style_data,
                                                                            hidden_columns=hidden_columns,
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
        Output("wvr-path", "value"),
        Output("company-id", "value"),
        Output("journal-type", "value"),
        Output("journal-title", "children"),
        Output("journal-title", "href"),
    ],
    Input("url", "search"),
)
def get_wvr_path(input_url):
    """
    Get wvr path from URL parameters
    """
    global WVR_PATH
    global COMPANY_ID
    global JOURNAL_TYPE
    global JOURNAL_TITLE
    global RETURN_URL
    logger.info("Input URL:{}".format(input_url))

    # Get WVR path from URL parameters
    WVR_PATH = "C:/temp/dashboard/Deves/2023-08-31/Profit_Center_688.wvr"
    if input_url and "wvr" in input_url:
        parsed_wvr = utilities.get_wvr_path_from_url(input_url)
        if utilities.get_wvr_path_from_url(input_url) is not None:
            WVR_PATH = parsed_wvr

    # Get company ID from URL parameters
    COMPANY_ID = utilities.get_company_id_from_url(input_url)
    JOURNAL_TYPE = utilities.get_journal_type_from_url(input_url)
    JOURNAL_TITLE = utilities.get_journal_title(JOURNAL_TYPE)
    RETURN_URL = utilities.create_link_to_back("accounting", input_url)
    logger.info(
        f"COMPANY_ID: {COMPANY_ID}, JOURNAL_TYPE: {JOURNAL_TYPE}, RETURN_URL: {RETURN_URL}"
    )

    return (
        WVR_PATH,
        COMPANY_ID,
        JOURNAL_TYPE,
        JOURNAL_TITLE,
        RETURN_URL,
    )


# Actual CF Journal
@app.callback(
    [
        Output("actualcf-journal-table", "data"),
        Output("actualcf-journal-table", "columns"),
        Output("actualcf-journal-table", "style_data_conditional"),
        Output("actualcf-journal-label", "children"),
    ],
    [
        Input("wvr-path", "value"),
        Input("actualcf-journal-reverse-button", "n_clicks"),
        State("company-id", "value"),
        State("journal-type", "value"),
    ],
)
def update(wvr_path, n_clicks, company_id, journal_type):
    """
    Actual CF Journal table
    """
    result = (
        no_update,
        no_update,
        no_update,
        no_update,
    )
    if (
        wvr_path is None
        or wvr_path == ""
        or company_id is None
        or company_id == ""
        or journal_type is None
        or journal_type == ""
    ):
        return result

    # Store the trigger ID to know which button was clicked
    ctx = dash.callback_context
    trigger_id = None
    # Get trigger ID
    if ctx.triggered:
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Set reverse flag
    is_reversed = n_clicks % 2 == 1 if n_clicks else False
    label_text = f"{company_id}" if not is_reversed else f"{company_id} (Reversed)"
    logger.info("n_clicks: {}".format(n_clicks))
    logger.info("reversed: {}".format(is_reversed))
    logger.info("trigger_id: {}".format(trigger_id))

    try:
        result = actual_journal.get_table_data(
            wvr_path, company_id, journal_type, reversed=is_reversed
        )
        return [*result, label_text]
    except Exception as e:
        logger.error(f"Error while getting Actual CF Journal table data: {e}")
        return result


@app.callback(
    [
        Output("expected-journal-inforce-table", "data"),
        Output("expected-journal-inforce-table", "columns"),
        Output("expected-journal-inforce-table", "style_data_conditional"),
        Output("expected-journal-inforce-label", "children"),
    ],
    [
        Input("wvr-path", "value"),
        Input("expected-journal-inforce-reverse-button", "n_clicks"),
        State("company-id", "value"),
        State("journal-type", "value"),
    ],
)
def update(wvr_path, n_clicks, company_id, journal_type):
    """
    Expected CF Journal (in-force) table
    """
    result = (
        no_update,
        no_update,
        no_update,
        no_update,
    )
    if (
        wvr_path is None
        or wvr_path == ""
        or company_id is None
        or company_id == ""
        or journal_type is None
        or journal_type == ""
    ):
        return result

    # Store the trigger ID to know which button was clicked
    ctx = dash.callback_context
    trigger_id = None
    # Get trigger ID
    if ctx.triggered:
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Set reverse flag
    is_reversed = n_clicks % 2 == 1 if n_clicks else False
    label_text = f"{company_id}" if not is_reversed else f"{company_id} (Reversed)"
    logger.info("n_clicks: {}".format(n_clicks))
    logger.info("is_reversed: {}".format(is_reversed))
    logger.info("trigger_id: {}".format(trigger_id))

    try:
        result = expected_if_journal.get_table_data(
            wvr_path, company_id, journal_type, reversed=is_reversed
        )
        return [*result, label_text]
    except Exception as e:
        logger.error(e)
        return result


@app.callback(
    [
        Output("expected-journal-nb-table", "data"),
        Output("expected-journal-nb-table", "columns"),
        Output("expected-journal-nb-table", "style_data_conditional"),
        Output("expected-journal-nb-label", "children"),
    ],
    [
        Input("wvr-path", "value"),
        Input("expected-journal-nb-reverse-button", "n_clicks"),
        State("company-id", "value"),
        State("journal-type", "value"),
    ],
)
def update(wvr_path, n_clicks, company_id, journal_type):
    """
    Expected CF Journal (nb) table
    """
    result = (
        no_update,
        no_update,
        no_update,
        no_update,
    )
    if (
        wvr_path is None
        or wvr_path == ""
        or company_id is None
        or company_id == ""
        or journal_type is None
        or journal_type == ""
    ):
        return result

    # Store the trigger ID to know which button was clicked
    ctx = dash.callback_context
    trigger_id = None
    # Get trigger ID
    if ctx.triggered:
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Set reverse flag
    is_reversed = n_clicks % 2 == 1 if n_clicks else False
    label_text = f"{company_id}" if not is_reversed else f"{company_id} (Reversed)"
    logger.info("n_clicks: {}".format(n_clicks))
    logger.info("is_reversed: {}".format(is_reversed))
    logger.info("trigger_id: {}".format(trigger_id))

    try:
        result = expected_nb_journal.get_table_data(
            wvr_path, company_id, journal_type, reversed=is_reversed
        )
        return [*result, label_text]
    except Exception as e:
        logger.error(e)
        return result


@app.callback(
    [
        Output("lic-cf-journal-table", "data"),
        Output("lic-cf-journal-table", "columns"),
        Output("lic-cf-journal-table", "style_data_conditional"),
        Output("lic-cf-journal-label", "children"),
    ],
    [
        Input("wvr-path", "value"),
        Input("lic-cf-journal-reverse-button", "n_clicks"),
        State("company-id", "value"),
        State("journal-type", "value"),
    ],
)
def update(wvr_path, n_clicks, company_id, journal_type):
    """
    LIC CF Journal table
    """
    result = (
        no_update,
        no_update,
        no_update,
        no_update,
    )
    if (
        wvr_path is None
        or wvr_path == ""
        or company_id is None
        or company_id == ""
        or journal_type is None
        or journal_type == ""
    ):
        return result

    # Store the trigger ID to know which button was clicked
    ctx = dash.callback_context
    trigger_id = None
    # Get trigger ID
    if ctx.triggered:
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Set reverse flag
    is_reversed = n_clicks % 2 == 1 if n_clicks else False
    label_text = f"{company_id}" if not is_reversed else f"{company_id} (Reversed)"
    logger.info("n_clicks: {}".format(n_clicks))
    logger.info("is_reversed: {}".format(is_reversed))
    logger.info("trigger_id: {}".format(trigger_id))

    try:
        result = lic_journal.get_table_data(
            wvr_path, company_id, journal_type, reversed=is_reversed
        )
        return [*result, label_text]
    except Exception as e:
        logger.error(e)
        return result


@app.callback(
    [
        Output("transition-journal-table", "data"),
        Output("transition-journal-table", "columns"),
        Output("transition-journal-table", "style_data_conditional"),
        Output("transition-journal-label", "children"),
    ],
    [
        Input("wvr-path", "value"),
        Input("transition-journal-reverse-button", "n_clicks"),
        State("company-id", "value"),
        State("journal-type", "value"),
    ],
)
def update(wvr_path, n_clicks, company_id, journal_type):
    """
    Traniition Journal table
    """
    result = (
        no_update,
        no_update,
        no_update,
        no_update,
    )
    if (
        wvr_path is None
        or wvr_path == ""
        or company_id is None
        or company_id == ""
        or journal_type is None
        or journal_type == ""
    ):
        return result

    # Store the trigger ID to know which button was clicked
    ctx = dash.callback_context
    trigger_id = None
    # Get trigger ID
    if ctx.triggered:
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Set reverse flag
    is_reversed = n_clicks % 2 == 1 if n_clicks else False
    label_text = f"{company_id}" if not is_reversed else f"{company_id} (Reversed)"
    logger.info("n_clicks: {}".format(n_clicks))
    logger.info("is_reversed: {}".format(is_reversed))
    logger.info("trigger_id: {}".format(trigger_id))

    try:
        result = transition_journal.get_table_data(
            wvr_path, company_id, journal_type, reversed=is_reversed
        )
        return [*result, label_text]
    except Exception as e:
        logger.error(e)
        return result
