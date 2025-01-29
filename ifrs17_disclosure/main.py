"""
@author: Kamoliddin Usmonov
@project: IFRS17 Disclosure
@description: Interactive dashboard for IFRS17 Disclosure
@date: 2022-09-06
"""
import logging

logger = logging.getLogger(__name__)

import sys

sys.path.append("..")

import json
import time

import dash_bootstrap_components as dbc
import plotly.io as plt_io
from dash import callback_context, dash_table, dcc, html, no_update
from dash.dependencies import ALL, Input, Output, State

import cm_dashboards.ifrs17_disclosure.dropdown_options as dropdown_options
import cm_dashboards.ifrs17_disclosure.helpers as helpers
import cm_dashboards.ifrs17_disclosure.results.calculate_results as calculate_results
import cm_dashboards.utilities as utilities
import cm_dashboards.wvr_data.wvr_functions as wvr_functions
from cm_dashboards.custom_template import custom_template
from cm_dashboards.ifrs17_disclosure.app_config import app

DB_ENGINE = None
DB_METADATA = None

# Apply our custome template
plt_io.templates["cloud_manager"] = custom_template

# Set up the layout
style_table = dict(overflowX="auto", minWidth="99%", maxHeight="43vh")
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
            style={"display": "none"},
            children=[
                dcc.Input(
                    id="wvr-path",
                    value="",
                ),
                dcc.Input(
                    id="model-name",
                    value="",
                ),
            ],
        ),
        html.Div(
            className="body-container",
            children=[
                html.Div(
                    className="title-container",
                    children=[
                        html.Div(
                            id="journal-title",
                            children="Journals on Cloud Manager",
                            style={"text-decoration": "none"},
                        ),
                    ],
                ),
                dcc.Loading(
                    type="default",
                    color="#2741BC",
                    children=[
                        dcc.Store(id="results", storage_type="session"),
                        dcc.Download(id="export-to-excel"),
                        html.Div(
                            children=[
                                dcc.Dropdown(
                                    id="journal-dropdown",
                                    placeholder="Select PTFLO ...",
                                    persistence=True,
                                    clearable=False,
                                ),
                                html.Br(),
                                dbc.Tabs(
                                    id="tabs",
                                    children=[
                                        dbc.Tab(
                                            id="tab-1",
                                            label="Primary Requirment (100)",
                                            tab_class_name="unactive-tab",
                                            label_class_name="unactive-tab-label",
                                            active_tab_class_name="active-tab",
                                            active_label_class_name="active-tab-label",
                                            children=[
                                                html.Div(
                                                    className="body-content",
                                                    style={"height": "57vh"},
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    className="one-half column mixed-table row",
                                                                    children=[
                                                                        html.Label(
                                                                            id="primary-100-label"
                                                                        ),
                                                                        html.Br(),
                                                                        html.A(
                                                                            target="_blank",
                                                                            download="yes",
                                                                            children=[
                                                                                html.Button(
                                                                                    "Export to Excel",
                                                                                    id={
                                                                                        "type": "export-data-button",
                                                                                        "index": "100_primary",
                                                                                    },
                                                                                    className="export",
                                                                                ),
                                                                            ],
                                                                        ),
                                                                        dash_table.DataTable(
                                                                            id="primary-100-table",
                                                                            is_focused=True,
                                                                            style_table=style_table,
                                                                            fixed_rows={
                                                                                "headers": True
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
                                        dbc.Tab(
                                            id="tab-2",
                                            label="Primary LRC (101)",
                                            tab_class_name="unactive-tab",
                                            label_class_name="unactive-tab-label",
                                            active_tab_class_name="active-tab",
                                            active_label_class_name="active-tab-label",
                                            children=[
                                                html.Div(
                                                    className="body-content",
                                                    style={"height": "57vh"},
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    className="one-half column mixed-table row",
                                                                    children=[
                                                                        html.Label(
                                                                            id="primary-101-label"
                                                                        ),
                                                                        html.A(
                                                                            target="_blank",
                                                                            download="yes",
                                                                            children=[
                                                                                html.Button(
                                                                                    "Export to Excel",
                                                                                    id={
                                                                                        "type": "export-data-button",
                                                                                        "index": "101_primary",
                                                                                    },
                                                                                    className="export",
                                                                                ),
                                                                            ],
                                                                        ),
                                                                        html.Br(),
                                                                        dash_table.DataTable(
                                                                            id="primary-101-table",
                                                                            is_focused=True,
                                                                            style_table=style_table,
                                                                            fixed_rows={
                                                                                "headers": True
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
        Output("wvr-path", "value"),
        Output("model-name", "value"),
        Output("journal-title", "children"),
        Output("tab-1", "label"),
        Output("tab-2", "label"),
    ],
    [Input("url", "search")],
)
def get_wvr_path(input_url):
    """
    Get wvr path from URL parameters
    """

    logger.info("Input_url: {}".format(input_url))

    # Get WVR path from URL parameters
    if input_url:
        # Dynamically set WVR PATH and JOURNAL_NAME
        wvr_path = utilities.get_wvr_path_from_url(input_url)
        model_name = wvr_functions.get_model_name_from_url(input_url)[0]
        journal_title = utilities.get_journal_title(model_name)
        tab_names = utilities.get_journal_tabs(model_name)
        logger.info(
            f"JOURNAL_NAME: {model_name}, JOURNAL_TITLE: {journal_title}, TAB_NAMES: {tab_names}"
        )
    else:
        # Manually set WVR PATH and JOURNAL_NAME for development
        logger.info("No input URL, using default values")
        wvr_path = "C:/temp/dashboard/Deves/2023-10-26/17_Move_Out_2022.wvr"  # 17_Move_Dir_2022, 17_Move_Out_2022, 17SC_At_Movement_Re_481-17SC_At_Movement_Dir_480
        model_name = "IFRS17_BBA_Reinsurance_Movement"  # IFRS17_BBA_Reinsurance_Movement-IFRS17_BBA_Primary_Movement
        journal_title = utilities.get_journal_title(model_name)
        tab_names = utilities.get_journal_tabs(model_name)

    return (
        wvr_path,
        model_name,
        journal_title,
        tab_names[0],
        tab_names[1],
    )


@app.callback(
    [
        Output("journal-dropdown", "options"),
        Output("journal-dropdown", "value"),
        Output("results", "data", allow_duplicate=True),
    ],
    [
        Input("wvr-path", "value"),
        Input("model-name", "value"),
    ],
    prevent_initial_call="initial_duplicate",
)
def update_table(wvr_path, model_name):
    """
    List of PTFLOs
    """
    results = {"100_primary": None, "101_primary": None}
    if wvr_path is None or wvr_path == "" or model_name is None or model_name == "":
        return no_update, no_update, results

    try:
        journals = dropdown_options.get_data(wvr_path, model_name)
        selected_journal = journals[0]["value"]
    except Exception as e:
        logger.error(f"Error while getting journals dropdown options: {e}")
        return no_update, no_update, results
    return journals, selected_journal, results


@app.callback(
    Output("results", "data"),
    [
        Input("journal-dropdown", "value"),
        State("wvr-path", "value"),
        State("model-name", "value"),
    ],
)
def calc_and_store_results(selected_journal, wvr_path, model_name):
    """
    Calculate results for selected journal
    """
    logger.info("Selected value: {}".format(selected_journal))
    if (
        wvr_path is None
        or wvr_path == ""
        or selected_journal is None
        or selected_journal == ""
        or model_name is None
        or model_name == ""
    ):
        logger.error("Invalid input for calculte and store results")
        return no_update
    # Keep track of time
    start_time = time.time()

    # Loop through each journal type and calculate results
    results = {"100_primary": None, "101_primary": None}
    for data_type in ["100_primary", "101_primary"]:
        try:
            result = calculate_results.get_table_data(
                wvr_path, selected_journal, model_name, data_type
            )
            results[data_type] = result
        except Exception as e:
            logger.error(f"Error while calculating {data_type} results: {e}")
            return no_update, no_update, no_update

    end_time = time.time()
    logger.info(f"Time took for {selected_journal} - {end_time - start_time}")
    return results


@app.callback(
    [
        Output("primary-100-table", "data"),
        Output("primary-100-table", "columns"),
        Output("primary-100-table", "style_data_conditional"),
        Output("primary-101-table", "data"),
        Output("primary-101-table", "columns"),
        Output("primary-101-table", "style_data_conditional"),
    ],
    [
        Input("results", "data"),
        State("model-name", "value"),
    ],
)
def update_table(stored_results, model_name):
    """
    Primary Requirement (100) Table
    Primary Requirement (101) Table
    """
    if (
        model_name is None
        or model_name == ""
        or stored_results is None
        or stored_results == ""
    ):
        logger.error("No update for primary tables")
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
        )
    # Keep track of time
    start_time = time.time()
    results = []
    for data_type in stored_results.keys():
        result = stored_results[data_type]
        table_data = calculate_results.prepare_table_data(result, model_name, data_type)
        results.extend([*table_data])

    end_time = time.time()
    logger.info(f"Time took to prepare table data - {end_time - start_time}")

    return results


@app.callback(
    Output("export-to-excel", "data"),
    [
        Input({"type": "export-data-button", "index": ALL}, "n_clicks"),
        State("results", "data"),
        State("journal-dropdown", "value"),
        State("model-name", "value"),
        State("tabs", "active_tab"),
    ],
    prevent_initial_call=True,
)
def export_to_excel(value, results, goc_name, model_name, active_tab):
    """
    Export to Excel
    """
    logger.info(f"Exporting to Excel: {value[0]} clicks")
    if results is None or results == "":
        logger.error("No update for export to excel")
        return no_update

    try:
        active_tab = int(active_tab.replace("tab-", ""))
        # Extract button id and get report type from it
        report_type = callback_context.triggered[0]["prop_id"].split(".")[0]
        report_type = json.loads(report_type)["index"]

        # Get label for the report type
        labels = utilities.get_journal_tabs(model_name)
        label = labels[active_tab]

        # Get data from results, convert it to df and export to excel
        logger.info(
            f"Generating excel for: GOC = {goc_name} / Record type = {report_type} / Labe = {label}"
        )
        data = results[report_type]
        return helpers.prepare_export_file(data, label, goc_name)
    except Exception as e:
        logger.error(f"Error while exporting to Excel: {e}")
        return no_update
