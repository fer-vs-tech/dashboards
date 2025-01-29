"""
@author: Kamoliddin Usmonov
@project: Dashboard Journal for SELIC POC
@description: Journal view page for SELIC POC
@date: 2022-08-04
"""

import io
import sys
from datetime import datetime

import pandas as pd
from flask import redirect, send_file

from cm_dashboards.server import server as application

sys.path.append("..")

import dash
import dash_bootstrap_components as dbc
import dask
import plotly.io as plt_io
from dash import dash_table, dcc, html, no_update
from dash.dependencies import Input, Output

import cm_dashboards.custom_html_template as custom_html_template
import cm_dashboards.ifrs17_accounting_selic.helpers as helpers
import cm_dashboards.ifrs17_accounting_selic.journals.actual_cf_journal as actual_cf_journal
import cm_dashboards.ifrs17_accounting_selic.journals.expected_cf_journal as expected_cf_journal
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
    url_base_pathname=f"/dash/{PROJECT_NAME}/journal_view/",
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
                                    label="Actual CF Journal",
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
                                                                    id="actualcf-journal-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        html.A(
                                                                            id="actualcf-journal-download-link",
                                                                            target="_blank",
                                                                            children=html.Button(
                                                                                className="export",
                                                                                children="Download",
                                                                                name="Actual_CF_Journal",
                                                                                id="actualcf-journal-download-button",
                                                                            ),
                                                                        ),
                                                                        html.Br(),
                                                                        html.Label(id="actualcf-journal-label"),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="actualcf-journal-table",
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
                                dbc.Tab(
                                    id="tab-2",
                                    label="Expected CF Journal",
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
                                                                    id="expectedcf-journal-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        html.A(
                                                                            id="expectedcf-journal-download-link",
                                                                            target="_blank",
                                                                            children=html.Button(
                                                                                className="export",
                                                                                children="Download",
                                                                                name="Expected_CF_Journal",
                                                                                id="expectedcf-journal-download-button",
                                                                            ),
                                                                        ),
                                                                        html.Br(),
                                                                        html.Label(id="expectedcf-journal-label"),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="expectedcf-journal-table",
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
        Output("actualcf-journal-label", "children"),
        Output("expectedcf-journal-label", "children"),
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
        COMPANY_ID,
    )


@app.callback(
    [
        Output("actualcf-journal-table", "data"),
        Output("actualcf-journal-table", "columns"),
        Output("actualcf-journal-table", "style_data_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_table(n_clicks):
    """
    Actualcf CF Journal table
    """
    if WVR_PATH is None or WVR_PATH == "":
        return (
            no_update,
            no_update,
            no_update,
        )
    result = actual_cf_journal.get_table_data(WVR_PATH, COMPANY_ID, JOURNAL_TYPE)
    return result


@app.callback(
    [
        Output("expectedcf-journal-table", "data"),
        Output("expectedcf-journal-table", "columns"),
        Output("expectedcf-journal-table", "style_data_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_table(n_clicks):
    """
    Expected CF Journal table
    """
    if WVR_PATH is None or WVR_PATH == "":
        return (
            no_update,
            no_update,
            no_update,
        )
    result = expected_cf_journal.get_table_data(WVR_PATH, COMPANY_ID, JOURNAL_TYPE)
    return result


# Gerenrate download links
@app.callback(
    [
        Output("actualcf-journal-download-link", "href"),
        Output("expectedcf-journal-download-link", "href"),
    ],
    [
        Input("actualcf-journal-download-button", "name"),
        Input("expectedcf-journal-download-button", "name"),
        Input("confirmed-wvr-path", "value"),
    ],
)
def update_link(actualcf, expectedcf, _):
    links = [
        f"/dash/{PROJECT_NAME}/download/{COMPANY_ID}/{JOURNAL_TYPE}/journal/{str(actualcf)}",
        f"/dash/{PROJECT_NAME}/download/{COMPANY_ID}/{JOURNAL_TYPE}/journal/{str(expectedcf)}",
    ]
    return links


@application.route(f"/dash/{PROJECT_NAME}/download/<company_id>/<journal_type>/journal/<journal_name>")
@application.route(f"/dash/{PROJECT_NAME}/download/<company_id>/<journal_type>/journal/<journal_name>/<encoded_wvr_path>")
def selic_poc_download_file(company_id, journal_type, journal_name, encoded_wvr_path=None):
    """
    Download GOC journals as TXT file
    """
    if journal_type is None or journal_type == "" or journal_name is None or journal_name == "":
        print("journal_type or journal_name is empty")
        return redirect(RETURN_URL)

    if encoded_wvr_path:
        wvr_path = utilities.encode_and_decode_string(encoded_wvr_path, encoding=False)
    else:
        wvr_path = WVR_PATH

    lazy_results = []
    if journal_name == "Actual_CF_Journal":
        df = dask.delayed(actual_cf_journal.get_data)(wvr_path, company_id, journal_type)
    elif journal_name == "Expected_CF_Journal":
        df = dask.delayed(expected_cf_journal.get_data)(wvr_path, company_id, journal_type)
    else:
        return redirect(RETURN_URL)

    # Store lazy evaluation in a list
    lazy_results.append(df)

    # Evaluate all lazy evaluations
    try:
        results = dask.compute(lazy_results, scheduler="threads")
    except Exception as e:
        print(f"(download) Download failed with error: {e}")
        return redirect(RETURN_URL)

    # Data cleaning
    df = pd.concat(results[0], ignore_index=True)
    # Prepare the df for the CSV file
    df = helpers.prepere_df_for_download(df)

    # Calculate total debit and credit
    total_amount_summary = df.groupby("Record_Type")["Amount"].sum()
    total_amount_summary = total_amount_summary.to_frame()
    # total_amount_summary.to_csv(f'{journal_name}_summary.csv', index=True)

    # print(total_amount_summary)
    print("total_amount_debt", total_amount_summary.iloc[0])
    print("total_amount_credit", total_amount_summary.iloc[1])

    df = helpers.adjust_cell_data_length(df)
    summary_info = helpers.create_footer_data(total_amount_summary)
    result = helpers.join_footer_to_body(df, summary_info)

    # Store data in a temporary file (in-memory buffer)
    execel_file = io.StringIO()
    result.to_csv(execel_file, index=False, header=False, float_format="%.2f", sep="\t")
    # result.to_csv(f'{COMPANY_ID}_{journal_name}.txt', index=False, header=False, float_format='%.2f', sep ='\t')
    mem = io.BytesIO()
    mem.write(execel_file.getvalue().encode("utf-8"))
    mem.seek(0)
    execel_file.close()

    # Send the file
    current_time = datetime.now().strftime("%Y_%m_%d-%H_%M_%S_%p")
    return send_file(
        mem,
        mimetype="text/csv",
        download_name=f"{journal_type.title()}_{company_id}_{journal_name}_{current_time}.txt",
        as_attachment=True,
    )
