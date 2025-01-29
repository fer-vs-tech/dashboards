"""
@author: Kamoliddin Usmonov
@project: Dashboard Journal for SELIC POC
@description: Home page (entry point)
@date: 2022-08-04
"""
import io
import sys
import time
from datetime import datetime
from unittest import result

import pandas as pd
from flask import redirect, request, send_file
from sqlalchemy import column

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
import cm_dashboards.ifrs17_accounting_selic.journal_table as journal_table
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
external_scripts = ["../static/utils/tabs.js"]
external_stylesheets = ["../static/css/bootstrap.css", "../static/css/styles.css"]

# Apply our custome template
plt_io.templates["cloud_manager"] = custom_template

# App configuration and initialization
app = dash.Dash(
    name=PROJECT_NAME,
    title="IFRS17 Acounting Dashboard",
    update_title="IFRS17 Acounting Dashboard - updating...",
    server=server,
    eager_loading=True,
    url_base_pathname=f"/dash/{PROJECT_NAME}/",
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
                    children="Journals on Cloud Manager",
                ),
                html.Div(
                    children=[
                        dbc.Tabs(
                            children=[
                                dbc.Tab(
                                    id="tab-1",
                                    label="Primary (Life)",
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
                                                            children=[
                                                                dcc.Loading(
                                                                    id="primary-life-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        html.A(
                                                                            id="primary-life-download-link",
                                                                            target="_blank",
                                                                            children=html.Button(
                                                                                className="export",
                                                                                children="Download",
                                                                                name="primary_life",
                                                                                id="primary-life-download-button",
                                                                            ),
                                                                        ),
                                                                        html.Br(),
                                                                        html.Label(
                                                                            "GOC Journals"
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="primary-life-journals-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            style_cell={
                                                                                "textAlign": "center",
                                                                                "minWidth": 95,
                                                                                "maxWidth": 95,
                                                                                "width": 95,
                                                                            },
                                                                            hidden_columns=[
                                                                                "Document_Date",
                                                                                "Posting_Date",
                                                                                "Document_Header_Text",
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
                                    label="Primary (General)",
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
                                                            children=[
                                                                dcc.Loading(
                                                                    id="primary-generalgeneral-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        html.A(
                                                                            id="primary-general-download-link",
                                                                            target="_blank",
                                                                            children=html.Button(
                                                                                className="export",
                                                                                children="Download",
                                                                                name="primary_general",
                                                                                id="primary-general-download-button",
                                                                            ),
                                                                        ),
                                                                        html.Br(),
                                                                        html.Label(
                                                                            "GOC Journals"
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="primary-general-journals-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            style_cell={
                                                                                "textAlign": "center",
                                                                                "minWidth": 95,
                                                                                "maxWidth": 95,
                                                                                "width": 95,
                                                                            },
                                                                            hidden_columns=[
                                                                                "Document_Date",
                                                                                "Posting_Date",
                                                                                "Document_Header_Text",
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
                                    id="tab-3",
                                    label="Reinsurance (Life)",
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
                                                            children=[
                                                                dcc.Loading(
                                                                    id="reinsurance-life-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        html.A(
                                                                            id="reinsurance-life-download-link",
                                                                            target="_blank",
                                                                            children=html.Button(
                                                                                className="export",
                                                                                children="Download",
                                                                                name="reinsurance_life",
                                                                                id="reinsurance-life-download-button",
                                                                            ),
                                                                        ),
                                                                        html.Br(),
                                                                        html.Label(
                                                                            "GOC Journals"
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="reinsurance-life-journals-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            style_cell={
                                                                                "textAlign": "center",
                                                                                "minWidth": 95,
                                                                                "maxWidth": 95,
                                                                                "width": 95,
                                                                            },
                                                                            hidden_columns=[
                                                                                "Document_Date",
                                                                                "Posting_Date",
                                                                                "Document_Header_Text",
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
                                    id="tab-4",
                                    label="Reinsurance (General)",
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
                                                            children=[
                                                                dcc.Loading(
                                                                    id="reinsurance-general-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        html.A(
                                                                            id="reinsurance-general-download-link",
                                                                            target="_blank",
                                                                            children=html.Button(
                                                                                className="export",
                                                                                children="Download",
                                                                                name="reinsurance_general",
                                                                                id="reinsurance-general-download-button",
                                                                            ),
                                                                        ),
                                                                        html.Br(),
                                                                        html.Label(
                                                                            "GOC Journals"
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="reinsurance-general-journals-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            style_cell={
                                                                                "textAlign": "center",
                                                                                "minWidth": 95,
                                                                                "maxWidth": 95,
                                                                                "width": 95,
                                                                            },
                                                                            hidden_columns=[
                                                                                "Document_Date",
                                                                                "Posting_Date",
                                                                                "Document_Header_Text",
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
                                    id="tab-5",
                                    label="Primary (General/PAA)",
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
                                                            children=[
                                                                dcc.Loading(
                                                                    id="primary-general-paa-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        html.A(
                                                                            id="primary-general-paa-download-link",
                                                                            target="_blank",
                                                                            children=html.Button(
                                                                                className="export",
                                                                                children="Download",
                                                                                name="primary_general_paa",
                                                                                id="primary-general-paa-download-button",
                                                                            ),
                                                                        ),
                                                                        html.Br(),
                                                                        html.Label(
                                                                            "GOC Journals"
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="primary-general-paa-journals-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            style_cell={
                                                                                "textAlign": "center",
                                                                                "minWidth": 95,
                                                                                "maxWidth": 95,
                                                                                "width": 95,
                                                                            },
                                                                            hidden_columns=[
                                                                                "Document_Date",
                                                                                "Posting_Date",
                                                                                "Document_Header_Text",
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
                                    id="tab-6",
                                    label="Reinsurance (General/PAA)",
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
                                                            children=[
                                                                dcc.Loading(
                                                                    id="reinsurance-general-paa-loading",
                                                                    type="default",
                                                                    color="#2741BC",
                                                                    debug=True,
                                                                    children=[
                                                                        html.A(
                                                                            id="reinsurance-general-paa-download-link",
                                                                            target="_blank",
                                                                            children=html.Button(
                                                                                className="export",
                                                                                children="Download",
                                                                                name="reinsurance_general_paa",
                                                                                id="reinsurance-general-paa-download-button",
                                                                            ),
                                                                        ),
                                                                        html.Br(),
                                                                        html.Label(
                                                                            "GOC Journals"
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="reinsurance-general-paa-journals-table",
                                                                            style_table={
                                                                                "overflowX": "auto",
                                                                                "minWidth": "100%",
                                                                            },
                                                                            style_cell={
                                                                                "textAlign": "center",
                                                                                "minWidth": 95,
                                                                                "maxWidth": 95,
                                                                                "width": 95,
                                                                            },
                                                                            hidden_columns=[
                                                                                "Document_Date",
                                                                                "Posting_Date",
                                                                                "Document_Header_Text",
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
    Output("confirmed-wvr-path", "value"),
    [Input("url", "search")],
)
def get_wvr_path(input_url):
    """
    Get wvr path from URL parameters
    """
    global WVR_PATH, URL_PARAMETER
    print("input_url:", input_url)
    if input_url:
        WVR_PATH = utilities.get_wvr_path_from_url(input_url)
        URL_PARAMETER = input_url
    return WVR_PATH


"""
Generate download link for the table
"""


@app.callback(
    [
        Output("primary-life-download-link", "href"),
        Output("reinsurance-life-download-link", "href"),
        Output("primary-general-download-link", "href"),
        Output("reinsurance-general-download-link", "href"),
        Output("primary-general-paa-download-link", "href"),
        Output("reinsurance-general-paa-download-link", "href"),
    ],
    [
        Input("primary-life-download-button", "name"),
        Input("reinsurance-life-download-button", "name"),
        Input("primary-general-download-button", "name"),
        Input("reinsurance-general-download-button", "name"),
        Input("primary-general-paa-download-button", "name"),
        Input("reinsurance-general-paa-download-button", "name"),
    ],
)
def update_link(
    primary_life,
    primary_general,
    reinsurance_life,
    reinsurance_general,
    primary_general_paa,
    reinsurance_general_paa,
):
    links = [
        f"/dash/{PROJECT_NAME}/download/{str(primary_life)}/",
        f"/dash/{PROJECT_NAME}/download/{str(primary_general)}/",
        f"/dash/{PROJECT_NAME}/download/{str(reinsurance_life)}/",
        f"/dash/{PROJECT_NAME}/download/{str(reinsurance_general)}/",
        f"/dash/{PROJECT_NAME}/download/{str(primary_general_paa)}/",
        f"/dash/{PROJECT_NAME}/download/{str(reinsurance_general_paa)}/",
    ]
    return links


# Accounting Info Primary (Life)
@app.callback(
    [
        Output("primary-life-journals-table", "data"),
        Output("primary-life-journals-table", "columns"),
        # Output("primary-life-journals-table", "style_data_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_table(n_clicks):
    """
    Accounting Info Primary (Life) table
    """
    if WVR_PATH is None or WVR_PATH == "":
        return (
            no_update,
            no_update,
            no_update,
        )
    data, column, _ = journal_table.get_table_data(
        WVR_PATH, URL_PARAMETER, "primary_life"
    )

    # No update if no data
    if data is None or column is None:
        return (
            no_update,
            no_update,
        )

    return data, column


# Accounting Info Primary (General)
@app.callback(
    [
        Output("primary-general-journals-table", "data"),
        Output("primary-general-journals-table", "columns"),
        # Output("primary-general-journals-table", "style_data_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_table(n_clicks):
    """
    Accounting Info Primary (General) table
    """
    if WVR_PATH is None or WVR_PATH == "":
        return (
            no_update,
            no_update,
            no_update,
        )
    data, column, _ = journal_table.get_table_data(
        WVR_PATH, URL_PARAMETER, "primary_general"
    )

    # No update if no data
    if data is None or column is None:
        return (
            no_update,
            no_update,
        )

    return data, column


# Accounting Info Reinsurance (Life)
@app.callback(
    [
        Output("reinsurance-life-journals-table", "data"),
        Output("reinsurance-life-journals-table", "columns"),
        # Output("reinsurance-life-journals-table", "style_data_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_table(n_clicks):
    """
    Accounting Info Reinsurance (Life) table
    """
    if WVR_PATH is None or WVR_PATH == "":
        return (
            no_update,
            no_update,
            no_update,
        )
    data, column, _ = journal_table.get_table_data(
        WVR_PATH, URL_PARAMETER, "reinsurance_life"
    )

    # No update if no data
    if data is None or column is None:
        return (
            no_update,
            no_update,
        )

    return data, column


# Accounting Info Reinsurance (General)
@app.callback(
    [
        Output("reinsurance-general-journals-table", "data"),
        Output("reinsurance-general-journals-table", "columns"),
        # Output("reinsurance-general-journals-table", "style_data_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_table(n_clicks):
    """
    Accounting Info Reinsurance (General) table
    """
    if WVR_PATH is None or WVR_PATH == "":
        return (
            no_update,
            no_update,
            no_update,
        )
    data, column, _ = journal_table.get_table_data(
        WVR_PATH, URL_PARAMETER, "reinsurance_general"
    )

    # No update if no data
    if data is None or column is None:
        return (
            no_update,
            no_update,
        )
    return data, column


# Accounting Info Primary (General/PAA)
@app.callback(
    [
        Output("primary-general-paa-journals-table", "data"),
        Output("primary-general-paa-journals-table", "columns"),
        # Output("primary-general-journals-table", "style_data_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_table(n_clicks):
    """
    Accounting Info Primary (General/PAA) table
    """
    if WVR_PATH is None or WVR_PATH == "":
        return (
            no_update,
            no_update,
        )
    data, column, _ = journal_table.get_table_data(
        WVR_PATH, URL_PARAMETER, "primary_general_paa"
    )

    # No update if no data
    if data is None or column is None:
        return (
            no_update,
            no_update,
        )
    return data, column


# Accounting Info Reinsurance (General/PAA)
@app.callback(
    [
        Output("reinsurance-general-paa-journals-table", "data"),
        Output("reinsurance-general-paa-journals-table", "columns"),
        # Output("reinsurance-general-paa-journals-table", "style_data_conditional"),
    ],
    [Input("confirmed-wvr-path", "value")],
)
def update_table(n_clicks):
    """
    Accounting Info Reinsurance (General/PAA) table
    """
    if WVR_PATH is None or WVR_PATH == "":
        return (
            no_update,
            no_update,
        )
    data, column, _ = journal_table.get_table_data(
        WVR_PATH, URL_PARAMETER, "reinsurance_general_paa"
    )

    # No update if no data
    if data is None or column is None:
        return (
            no_update,
            no_update,
        )
    return data, column


@application.route(
    f"/dash/{PROJECT_NAME}/download/<string:journal_type>/all/<string:company_id>/"
)
def selic_poc_download_journal(journal_type, company_id):
    """
    Download Journal by Company ID and Journal Type
    """
    # Checking if the company_id is valid
    if (journal_type is None or journal_type == "") or (
        company_id is None or company_id == ""
    ):
        print("journal_type or company_id is empty")
        return redirect(f"/dash/{PROJECT_NAME}/{URL_PARAMETER}")

    # Define lazy evaluation for each journal
    lazy_results = []
    actual_cf_journal_df = dask.delayed(actual_cf_journal.get_data)(
        WVR_PATH, company_id, journal_type
    )
    expected_cf_journal_inforce_df = dask.delayed(expected_cf_journal.get_data)(
        WVR_PATH, company_id, journal_type
    )

    # Store lazy evaluation in a list
    lazy_results.append(actual_cf_journal_df)
    lazy_results.append(expected_cf_journal_inforce_df)

    # Evaluate all lazy evaluations
    try:
        results = dask.compute(lazy_results, scheduler="threads")
    except Exception as e:
        print(f"(download) Download failed with error: {e}")
        return redirect(f"/dash/{PROJECT_NAME}/{URL_PARAMETER}")

    # Data cleaning
    df = pd.concat(results[0], ignore_index=True)

    # Prepare the df for the CSV file
    df = helpers.prepere_df_for_download(df)

    # Calculate total debit and credit
    total_amount_summary = df.groupby("Record_Type")["Amount"].sum().to_frame()

    print(total_amount_summary)
    print("total_amount_debt", total_amount_summary.iloc[0])
    print("total_amount_credit", total_amount_summary.iloc[1])

    # Adjust column value length
    df = helpers.adjust_cell_data_length(df)
    # Generate header and footer data
    summary_info = helpers.create_footer_data(total_amount_summary)
    final_result = helpers.join_footer_to_body(df, summary_info)

    # Store data in a temporary file (in-memory buffer)
    execel_file = io.StringIO()
    final_result.to_csv(
        execel_file, index=False, header=False, float_format="%.2f", sep="\t"
    )
    mem = io.BytesIO()
    mem.write(execel_file.getvalue().encode("utf-8"))
    mem.seek(0)
    execel_file.close()

    # Send the file
    current_time = datetime.now().strftime("%Y_%m_%d-%H_%M_%S_%p")
    return send_file(
        mem,
        mimetype="text/csv",
        download_name=f"{journal_type.title()}_{company_id}_{current_time}.txt",
        as_attachment=True,
    )


@application.route(f"/dash/{PROJECT_NAME}/download/<string:journal_type>/")
def selic_poc_download_journals(journal_type):
    """
    Download All Journals as TXT file for SELIC POC
    """
    # Clean DF
    journals_df = journal_table.get_data(WVR_PATH, URL_PARAMETER, journal_type)
    journals_df.drop(columns=["Journal", "Download"], inplace=True)

    start_time = time.perf_counter()
    lazy_results = []
    for index, row in journals_df.iterrows():
        if row["GoC_Name"] == "ALL":
            continue

        print(f'{index} - {row["GoC_Name"]}')

        # Define lazy evaluation for each journal
        actual_cf_journal_df = dask.delayed(actual_cf_journal.get_data)(
            WVR_PATH, row["GoC_Name"], journal_type
        )
        expected_cf_journal_inforce_df = dask.delayed(expected_cf_journal.get_data)(
            WVR_PATH, row["GoC_Name"], journal_type
        )

        # Store lazy evaluation in a list
        lazy_results.append(actual_cf_journal_df)
        lazy_results.append(expected_cf_journal_inforce_df)

    # Evaluate all lazy evaluations
    try:
        results = dask.compute(lazy_results, scheduler="threads")
    except Exception as e:
        print(f"(download all) Download failed with error: {e}")
        return redirect(f"/dash/{PROJECT_NAME}/{URL_PARAMETER}")

    # Combine all results
    final_result = pd.concat(results[0], ignore_index=True)
    print(
        "Time: {:6.3f} seconds for {:d} rows".format(
            time.perf_counter() - start_time, final_result.shape[0]
        )
    )

    start_time = time.perf_counter()
    # Prepare the df for the CSV file
    df = helpers.prepere_df_for_download(final_result)

    # Calculate total debit and credit
    total_amount_summary = df.groupby("Record_Type")["Amount"].sum()
    total_amount_summary = total_amount_summary.to_frame()

    print(total_amount_summary)
    print("total_amount_debt", total_amount_summary.iloc[0])
    print("total_amount_credit", total_amount_summary.iloc[1])

    # Generate summary data
    summary_info = helpers.create_footer_data(total_amount_summary)

    # Adjust column value length
    df = helpers.adjust_cell_data_length(df)

    # Add summary data to the body
    final_result = helpers.join_footer_to_body(df, summary_info)

    # Store data in a temporary file (in-memory buffer)
    execel_file = io.StringIO()
    final_result.to_csv(
        execel_file, index=False, header=False, float_format="%.2f", sep="\t"
    )
    # final_result.to_csv(f'{journal_type.title()}.txt', index=False, header=False, float_format='%.2f', sep ='\t')
    mem = io.BytesIO()
    mem.write(execel_file.getvalue().encode("utf-8"))
    mem.seek(0)
    execel_file.close()
    print("Calculation time: {:6.3f} seconds".format(time.perf_counter() - start_time))

    # Send the file
    current_time = datetime.now().strftime("%Y_%m_%d-%H_%M_%S_%p")
    return send_file(
        mem,
        mimetype="text/csv",
        download_name=f"{journal_type.title()}_Journals_{current_time}.txt",
        as_attachment=True,
    )
