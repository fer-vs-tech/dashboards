"""
@author: Kamoliddin Usmonov
@project: Dashboard Journals for IFRS17 Accounting
@description: Home page (entry point)
@date: 2022-07-27
"""

import logging

logger = logging.getLogger(__name__)
import sys
import time
from datetime import datetime

import pandas as pd
from flask import redirect, request, send_file

from cm_dashboards.server import server as application

sys.path.append("..")

import dash
import dash_bootstrap_components as dbc
import dask
import plotly.io as plt_io
from dash import dash_table, dcc, html, no_update
from dash.dependencies import Input, Output, State

import cm_dashboards.custom_html_template as custom_html_template
import cm_dashboards.ifrs17_accounting.generate_report as generate_report
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
QUERY_STRING = None
RETURN_URL = None
PROJECT_NAME = "accounting"

# External scripts and CSS stylesheets
external_scripts = ["../static/utils/tabs.js"]
external_stylesheets = ["../static/css/bootstrap.css", "../static/css/styles.css"]

# Apply our custome template
plt_io.templates["cloud_manager"] = custom_template

# App configuration for the Nonlife Dashboard
app = dash.Dash(
    name=PROJECT_NAME,
    title="IFRS17 Acounting Dashboard",
    update_title="(Updating) IFRS17 Acounting Dashboard",
    server=server,
    eager_loading=True,
    url_base_pathname=f"/dash/{PROJECT_NAME}/",
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    compress=server.config["COMPRESS_CONTENT"],
)

# Change the default favicon
app.index_string = custom_html_template.WM_TEMPLATE

# Enable dev mode if turned on in config
debug_mode = utilities.get_entry_from_config_file("dashboard", "debug_mode", False)
if debug_mode == "True":
    app.enable_dev_tools(debug=True, dev_tools_ui=True, dev_tools_props_check=True)

# Define app layout
style_table = {
    "overflowX": "auto",
    "minWidth": "100%",
}
style_data = {
    "minWidth": "100px",
    "width": "fit-content",
    "maxWidth": "220px",
    "overflow": "hidden",
    "textOverflow": "ellipsis",
}
hidden_columns = [
    "Document_Date",
    "Posting_Date",
    "Document_Header_Text",
]
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
                    id="url-query-string",
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
                    children="Journals on Cloud Manager",
                ),
                html.Div(
                    children=[
                        dbc.Tabs(
                            children=[
                                dbc.Tab(
                                    id="tab-1",
                                    label="Accounting Info Primary",
                                    tab_class_name="unactive-tab",
                                    label_class_name="unactive-tab-label",
                                    active_tab_class_name="active-tab",
                                    active_label_class_name="active-tab-label",
                                    children=[
                                        dcc.Loading(
                                            id="journals-loading",
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
                                                                            id="primary-journals-download-link",
                                                                            children=html.Button(
                                                                                className="export",
                                                                                children="Download",
                                                                                name="primary",
                                                                            ),
                                                                        ),
                                                                        html.A(
                                                                            id="reversed-primary-journals-download-link",
                                                                            children=html.Button(
                                                                                className="reverse",
                                                                                children="Reverse and Download",
                                                                                name="primary",
                                                                            ),
                                                                        ),
                                                                        html.Br(),
                                                                        html.Label(
                                                                            "GOC Journals"
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="journals-table",
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
                                    label="Accounting Info Reinsurance",
                                    tab_class_name="unactive-tab",
                                    label_class_name="unactive-tab-label",
                                    active_tab_class_name="active-tab",
                                    active_label_class_name="active-tab-label",
                                    children=[
                                        dcc.Loading(
                                            id="reins-journals-loading",
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
                                                                            id="reinsurance-journals-download-link",
                                                                            children=html.Button(
                                                                                className="export",
                                                                                children="Download",
                                                                                name="reinsurance",
                                                                            ),
                                                                        ),
                                                                        html.A(
                                                                            id="reversed-reinsurance-journals-download-link",
                                                                            children=html.Button(
                                                                                className="reverse",
                                                                                children="Reverse and Download",
                                                                                name="reinsurance",
                                                                            ),
                                                                        ),
                                                                        html.Br(),
                                                                        html.Label(
                                                                            "GOC Journals"
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="reins-journals-table",
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
        Output("url-query-string", "value"),
    ],
    Input("url", "search"),
)
def get_wvr_path(input_url):
    """
    Get wvr path from URL parameters
    """
    global WVR_PATH
    global QUERY_STRING
    global RETURN_URL
    logger.info(f"Input URL: {input_url}")
    if input_url:
        WVR_PATH = utilities.get_wvr_path_from_url(input_url)
        QUERY_STRING = input_url
        RETURN_URL = utilities.create_link_to_back("accounting", input_url)
    else:
        WVR_PATH = "C:/temp/dashboard/Deves/2024-01-17/Profit_Center_Allocation.wvr"
        QUERY_STRING = None
        RETURN_URL = f"/dash/{PROJECT_NAME}"
    return WVR_PATH, QUERY_STRING


@app.callback(
    [
        Output("journals-table", "data"),
        Output("journals-table", "columns"),
        Output("journals-table", "style_data_conditional"),
    ],
    [
        Input("wvr-path", "value"),
        State("url-query-string", "value"),
    ],
)
def update(wvr_path, query_string):
    """
    Accounting Journals table
    """
    result = (
        no_update,
        no_update,
        no_update,
    )
    if not wvr_path:
        return result
    try:
        result = journal_table.get_table_data(wvr_path, query_string, "primary")
    except Exception as error:
        logger.error(f"Error occured: {error}")
    return result


@app.callback(
    [
        Output("reins-journals-table", "data"),
        Output("reins-journals-table", "columns"),
        Output("reins-journals-table", "style_data_conditional"),
    ],
    [
        Input("wvr-path", "value"),
        State("url-query-string", "value"),
    ],
)
def update(wvr_path, query_string):
    """
    Reinsurance Journals table
    """
    result = (
        no_update,
        no_update,
        no_update,
    )
    if not wvr_path:
        return result
    try:
        result = journal_table.get_table_data(wvr_path, query_string, "reinsurance")
    except Exception as error:
        logger.error(f"Error occured: {error}")
    return result


@app.callback(
    [
        Output("primary-journals-download-link", "href"),
        Output("reinsurance-journals-download-link", "href"),
        Output("reversed-primary-journals-download-link", "href"),
        Output("reversed-reinsurance-journals-download-link", "href"),
    ],
    [
        Input("wvr-path", "value"),
    ],
)
def update_link(wvr_path):
    encode_wvr_path = utilities.encode_and_decode_string(wvr_path)
    logger.info(f"WVR path encoded: {encode_wvr_path}")
    links = [
        f"/dash/download/primary/?q={encode_wvr_path}",
        f"/dash/download/reinsurance/?q={encode_wvr_path}",
        f"/dash/download/primary/reverse/?q={encode_wvr_path}",
        f"/dash/download/reinsurance/reverse/?q={encode_wvr_path}",
    ]
    return links


@application.route("/dash/download/<string:journal_type>/")
@application.route("/dash/download/<string:journal_type>/<string:reverse>/")
def download_all_journals(journal_type, reverse=None):
    """
    Download all journals
    """
    reverse = reverse == "reverse" if reverse is not None else False
    try:
        encoded_path = request.args.get("q")
        decoded_path = utilities.encode_and_decode_string(encoded_path, encoding=False)
        logger.info(f"Downloading {journal_type} journals")
        logger.info(f"Reverse: {reverse}")
        logger.info(f"Encoded path: {encoded_path}")
        logger.info(f"Decoded path: {decoded_path}")
    except Exception as error:
        logger.error(f"Failed to get wvr path with error: {error}")
        return redirect(RETURN_URL)
    try:
        report_file = generate_report.main(decoded_path, journal_type, reverse)
        return report_file
    except Exception as error:
        logger.error(error)
        return redirect(RETURN_URL)


@application.route("/dash/download/<string:journal_type>/i/<string:company_id>/")
def download_journal_data(journal_type, company_id):
    """
    Download journal data
    """
    if (journal_type is None or journal_type == "") or (
        company_id is None or company_id == ""
    ):
        logger.info("Invalid company_id or journal_type, redirecting to home page")
        return redirect(RETURN_URL)

    try:
        encoded_path = request.args.get("q")
        decoded_path = utilities.encode_and_decode_string(encoded_path, encoding=False)
        logger.info(f"Downloading {company_id} {journal_type} jouurnals")
        logger.info(f"Encoded path: {encoded_path}")
        logger.info(f"Decoded path: {decoded_path}")
    except Exception as e:
        logger.error(f"Failed to get wvr path with error: {e}")
        return redirect(RETURN_URL)

    # Define lazy evaluation for each journal
    start_time = time.perf_counter()
    journal_connection = helpers.get_connection_string(WVR_PATH, "journal")
    mapping_connection = helpers.get_connection_string(WVR_PATH, "mapping")
    lazy_results = []

    # Define lazy evaluation for each journal, pass connection strings as parameters
    actual_data = dask.delayed(actual_journal.get_data)(
        company_id,
        journal_type,
        journal_connection=journal_connection,
        mapping_connection=mapping_connection,
    )
    expected_if_data = dask.delayed(expected_if_journal.get_data)(
        company_id,
        journal_type,
        journal_connection=journal_connection,
        mapping_connection=mapping_connection,
    )
    expected_nb_data = dask.delayed(expected_nb_journal.get_data)(
        company_id,
        journal_type,
        journal_connection=journal_connection,
        mapping_connection=mapping_connection,
    )
    lic_data = dask.delayed(lic_journal.get_data)(
        company_id,
        journal_type,
        journal_connection=journal_connection,
        mapping_connection=mapping_connection,
    )
    transition_data = dask.delayed(transition_journal.get_data)(
        company_id,
        journal_type,
        journal_connection=journal_connection,
        mapping_connection=mapping_connection,
    )

    # Store lazy evaluation in a list and compute them
    lazy_results.append(actual_data)
    lazy_results.append(expected_if_data)
    lazy_results.append(expected_nb_data)
    lazy_results.append(lic_data)
    lazy_results.append(transition_data)
    try:
        results = dask.compute(
            lazy_results, scheduler="synchronous", optimize_graph=True
        )
    except Exception as e:
        logger.error(f"Failed to get {company_id} data from DB with error: {e}")
        return redirect(RETURN_URL)
    finally:
        journal_connection.close()
        mapping_connection.close()

    df = pd.concat(results[0], ignore_index=True)
    if len(df) == 0:
        logger.info(f"No data found for company_id: {company_id}")
        return redirect(RETURN_URL)
    journal_df = journal_table.get_single_journal(
        WVR_PATH, journal_type, company_id, add_headnote=True
    )
    if journal_df is None:
        return redirect(RETURN_URL)
    result = helpers.prepere_df_for_download(
        df, journals_df=journal_df, calculate_as_block=True
    )
    if result is None:
        return redirect(RETURN_URL)

    export_file = helpers.generate_export_file(result)
    current_time = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    filename = f"{journal_type.title()}_{company_id}_({current_time}).txt"
    end_time = time.perf_counter()
    logger.info(f"Time took for {filename}: {end_time - start_time:6.3f} seconds")
    return send_file(
        export_file,
        mimetype="text/csv",
        download_name=filename,
        as_attachment=True,
    )
