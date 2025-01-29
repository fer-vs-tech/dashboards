"""
@author: Kamoliddin Usmonov
@project: Dashboard Journal for SELIC POC
@description: Journal view page for SELIC POC
@date: 2022-08-04
"""

import sys

sys.path.append("..")

import dash
import dash_bootstrap_components as dbc
import plotly.io as plt_io
from dash import dash_table, dcc, html, no_update
from dash.dependencies import Input, Output

import cm_dashboards.custom_html_template as custom_html_template
import cm_dashboards.ifrs17_accounting_selic.journals.actual_cf_journal as actual_cf_journal
import cm_dashboards.utilities as utilities
from cm_dashboards.custom_template import custom_template
from cm_dashboards.server import server

DB_ENGINE = None
DB_METADATA = None
WVR_PATH = None
PROJECT_NAME = "ifrs17_accounting_selic"
Session = None

# External scripts and CSS stylesheets
external_scripts = ["../../static/utils/tabs.js"]
external_stylesheets = ["../../static/css/bootstrap.css", "../../static/css/styles.css"]

# Apply our custome template
plt_io.templates["cloud_manager"] = custom_template

# App configuration and initialization
app = dash.Dash(
    name=PROJECT_NAME,
    title="IFRS17 Acounting Dashboard",
    update_title="IFRS17 Acounting Dashboard - updating...",
    server=server,
    eager_loading=True,
    url_base_pathname=f"/dash/{PROJECT_NAME}/journal_view_paa/",
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    assets_folder="../assets",
    compress=server.config["COMPRESS_CONTENT"],
)

# Change the default favicon
app.index_string = custom_html_template.WM_TEMPLATE

# Enable dev mode if turned on in config
debug_mode = utilities.get_entry_from_config_file("dashboard", "debug_mode", False)
if debug_mode == "True":
    app.config.suppress_callback_exceptions = True
    app.enable_dev_tools(debug=True, dev_tools_ui=True, dev_tools_props_check=True)

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
            id="confirmed-wvr-path",
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
                        html.A(
                            id="journal-title",
                            children="Journals on Cloud Manager",
                            href=f"/dash/{PROJECT_NAME}/",
                            target="_blank",
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
                                    label="Journal",
                                    tab_class_name="unactive-tab",
                                    label_class_name="unactive-tab-label",
                                    active_tab_class_name="active-tab",
                                    active_label_class_name="active-tab-label",
                                    children=[
                                        html.Div(
                                            className="body-content",
                                            children=[
                                                html.Div(
                                                    className="row",
                                                    children=[
                                                        html.Div(
                                                            className="one-half column",
                                                            children=[
                                                                dcc.Loading(
                                                                    id="journal-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        html.A(
                                                                            id="journal-download-link",
                                                                            target="_blank",
                                                                            children=html.Button(
                                                                                className="export",
                                                                                children="Download",
                                                                                name="Actual_CF_Journal",
                                                                                id="journal-download-button",
                                                                            ),
                                                                        ),
                                                                        html.Br(),
                                                                        html.Label(id="journal-label"),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="journal-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            style_data={
                                                                                "minWidth": "100px",
                                                                                "width": "fit-content",
                                                                                "maxWidth": "220px",
                                                                                "overflow": "hidden",
                                                                                "textOverflow": "ellipsis",
                                                                            },
                                                                            hidden_columns=[
                                                                                "NB_IF",
                                                                                "GOC",
                                                                                "PTFLO_2",
                                                                                "PTFLO",
                                                                                "COHT",
                                                                                "Posting_Key",
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
        ),
    ],
)


@app.callback(
    [
        Output("confirmed-wvr-path", "value"),
        Output("journal-title", "children"),
        Output("journal-title", "href"),
        Output("journal-label", "children"),
    ],
    [Input("url", "search")],
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
    print("input_url:", input_url)

    # Get WVR path from URL parameters
    if input_url and "wvr" in input_url:
        WVR_PATH = utilities.get_wvr_path_from_url(input_url)
        # Get company ID from URL parameters
        COMPANY_ID = utilities.get_company_id_from_url(input_url)
        JOURNAL_TYPE = utilities.get_journal_type_from_url(input_url)
        JOURNAL_TITLE = utilities.get_journal_title(JOURNAL_TYPE)
        RETURN_URL = utilities.create_link_to_back(PROJECT_NAME, input_url)
        print(f"COMPANY_ID: {COMPANY_ID}, JOURNAL_TYPE: {JOURNAL_TYPE}, RETURN_URL: {RETURN_URL}")

    return (
        WVR_PATH,
        JOURNAL_TITLE,
        RETURN_URL,
        COMPANY_ID,
    )


# Gerenrate download links
@app.callback(
    [
        Output("journal-download-link", "href"),
    ],
    [
        Input("journal-download-button", "name"),
        Input("confirmed-wvr-path", "value"),
    ],
)
def update_link(actualcf, _):
    encode_wvr_path = utilities.encode_and_decode_string(WVR_PATH)
    links = [
        f"/dash/{PROJECT_NAME}/download/{COMPANY_ID}/{JOURNAL_TYPE}/journal/{str(actualcf)}/{encode_wvr_path}",
    ]
    return links


@app.callback(
    [
        Output("journal-table", "data"),
        Output("journal-table", "columns"),
        Output("journal-table", "style_data_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_table(n_clicks):
    """
    Journal table
    """
    if WVR_PATH is None or WVR_PATH == "":
        return (
            no_update,
            no_update,
            no_update,
        )
    result = actual_cf_journal.get_table_data(WVR_PATH, COMPANY_ID, JOURNAL_TYPE)
    return result
