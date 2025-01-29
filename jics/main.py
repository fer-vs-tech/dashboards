"""
@author: Kamoliddin Usmonov
@project: J-ICS Dashboards
@description: J-ICS Dashboards
@date: 2023-04-17
"""

import logging

logger = logging.getLogger(__name__)
import sys

sys.path.append("..")

import concurrent.futures
import time

from dash import dcc, no_update
from dash.dependencies import Input, Output, State

import cm_dashboards.custom_html_template as custom_html_template
import cm_dashboards.jics.helpers.helpers as helpers
import cm_dashboards.jics.results.data_generator as data_generator
import cm_dashboards.jics.results.dropdown_generator as dropdown_generator
import cm_dashboards.jics.results.headers_parser as headers_parser
import cm_dashboards.utilities as utilities
import cm_dashboards.wvr_data.wvr_functions as wvr_functions
from cm_dashboards.jics.config.config import PROJECT_TITLE, app
from cm_dashboards.jics.layout.data_loader import get_dashboard_info, get_dashboard_list
from cm_dashboards.jics.layout.layout_loader import (
    generate_dashboard_layout,
    generate_main_layout,
)

dashboard_data = get_dashboard_list()
app.index_string = custom_html_template.WM_TEMPLATE
app.layout = generate_main_layout(PROJECT_TITLE, dashboard_data)


@app.callback(
    [
        Output("wvr-path", "value"),
        Output("model-name", "value"),
        Output("error-toast", "children"),
    ],
    Input("url", "search"),
)
def get_wvr_path(input_url):
    """
    Get wvr path from URL parameters
    :param input_url: Input URL to get .wvr path
    :return: WVR path value
    """
    logger.info(f"URL params: {input_url}")
    wvr_path, model_name, message = None, None, None
    try:
        if input_url:
            wvr_path = utilities.get_wvr_path_from_url(input_url)
        else:
            wvr_path = r"C:\temp\dashboard\jics\2024-03-20\J-ICS_Calculations_v2.00\results\FT23_J-ICS_Std_Formula_Solo.wvr"
        model_names = wvr_functions.model_names_in_wvr(wvr_path)
        model_name = utilities.set_jics_model_name(model_names)
    except Exception as error:
        message = f"Error while getting WVR path: {error}"
        logger.error(message)
    return wvr_path, model_name, message


@app.callback(
    [
        Output("report-date-dropdown", "options"),
        Output("report-date-dropdown", "value"),
        Output("results-store", "data"),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    Input("wvr-path", "value"),
    Input("model-name", "value"),
    prevent_initial_call=True,
)
def update_table(wvr_path, model_name):
    """
    Retrive report dates from given journal table
    :param wvr_path: WVR file path
    :return: DDL options and value and the report dates list
    """
    if not wvr_path or not model_name:
        return no_update, no_update, no_update, no_update
    db_connection = utilities.get_db_connection(wvr_path, model_name)
    report_dates = dropdown_generator.get_data(wvr_path, model_name)
    report_date = report_dates[0]["value"] if len(report_dates) > 0 else None
    message = None
    logger.info(f"Report date: {report_date}")
    logger.info(f"Report dates: {report_dates}")
    if report_date is None:
        db_connection.close()
        message = "No valid report dates found"
        return no_update, no_update, no_update, message
    # Convert date object to string format to avoid serialization error
    report_date = report_date.strftime("%Y-%m-%d")
    data = {report_date: dict()}
    dashboard_list = get_dashboard_list()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = list()
        for tab_id in dashboard_list.keys():
            future = executor.submit(
                data_generator.get_common_output,
                wvr_path,
                model_name,
                report_date,
                tab_id,
                True,
            )
            future_eval = [tab_id, future]
            futures.append(future_eval)
        for tab_id, future in futures:
            logger.info(f"Evaluated tab data: {tab_id}")
            try:
                result = future.result()
                data[report_date][tab_id] = result
            except Exception as error:
                message = f"Error while fetching data for tab: {tab_id}. {error}"
                logger.error(message)
                continue
    db_connection.close()
    return report_dates, report_date, data, message


@app.callback(
    Output("dashboard-data", "children"),
    [
        Input("report-date-dropdown", "value"),
        Input("tabs", "active_tab"),
        State("wvr-path", "value"),
        State("model-name", "value"),
        State("results-store", "data"),
    ],
)
def update_table(report_date, active_tab, wvr_path, model_name, data):
    """
    Update dashboard data
    :param report_date: Report date
    :param active_tab: Active tab
    :return: Dashboard data
    """
    logger.info(f"Report date: {report_date}")
    logger.info(f"Active tab: {active_tab}")
    logger.info(f"Model name: {model_name}")
    dashboard_info = get_dashboard_info(active_tab)
    if dashboard_info is None or report_date is None:
        logger.info("No update for dashboard data")
        return no_update
    logger.info("Executing dashboard results")
    start_time = time.time()
    results = list()
    error_messages = list()
    label = dashboard_info.get("label")
    child_dashboards = dashboard_info.get("child_dashboards")
    common_output = data[report_date].get(active_tab)
    if common_output is None:
        common_output = data_generator.get_common_output(
            wvr_path, model_name, report_date, active_tab
        )
    for child_dash_id in child_dashboards.keys():
        try:
            # If child dashboard is a header, get header data, else get table data
            if child_dash_id == "HEADER":
                result = headers_parser.get_df(label)
            else:
                result, header_rows = data_generator.generate_df(
                    common_output,
                    child_dash_id,
                )
                result = data_generator.prepare_table_data(result, header_rows)
        except Exception as error:
            error_message = (f"Dashboard - {child_dash_id}", str(error))
            error_messages.append(error_message)
            logger.error(": ".join(error_message))
            continue
        results.append([child_dash_id, result])
    end_time = time.time()
    logger.info(f"Time taken for {active_tab} - {end_time - start_time}")
    layout = generate_dashboard_layout(dashboard_info, results, error_messages)
    return layout


@app.callback(
    Output("export-to-excel", "data"),
    [
        Input("export-link-button", "n_clicks"),
        Input("report-date-dropdown", "value"),
        Input("results-store", "data"),
    ],
)
def generate_report(n_clicks, report_date, data):
    """
    Export dashboard data to Excel file
    :param params: URL query string
    :return: Excel file
    """
    logger.info(f"Exporting to Excel, number of clicks: {n_clicks}")
    if n_clicks is None:
        return no_update
    data = data[report_date]
    start_time = time.perf_counter()
    results = dict()
    dashboard_list = get_dashboard_list()
    for tab_id, dashboards in dashboard_list.items():
        sheet_name = dashboards.get("label")
        child_dashboards = dashboards.get("child_dashboards", {})
        child_dashboard_ids = list(child_dashboards.keys())
        dashboards_count = len(child_dashboards)
        results[sheet_name] = dict()
        results[sheet_name]["dashboard_ids"] = child_dashboard_ids
        logger.info(f"Tab ID: {tab_id}, sheet name: {sheet_name}")
        logger.info(f"Dashboards count: {dashboards_count}")
        results[sheet_name]["data"] = data[tab_id]
    try:
        file_name = utilities.generate_filename(extention="xlsx", prefix="J-ICS_")
        output = helpers.generate_report_file(results)
    except Exception as error:
        end_time = time.perf_counter()
        logger.info(f"Time taken: {end_time - start_time:.4f}")
        logger.error(f"Error while generating Excel file: {error}")
        return no_update
    end_time = time.perf_counter()
    logger.info(
        f"Time taken to generate '{file_name}' file: {end_time - start_time:.4f} seconds"
    )
    return dcc.send_bytes(output.getvalue(), file_name)


@app.callback(
    [
        Output("error-toast", "is_open"),
        Output("results-store", "clear_data", allow_duplicate=True),
        Output("export-link-button", "disabled", allow_duplicate=True),
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
    disable_export_button = show_error_message
    logger.info(f"Message: {message}")
    logger.info(f"Show error message: {show_error_message}")
    logger.info(f"Clear stored data: {clear_stored_data}")
    logger.info(f"Disable export button: {disable_export_button}")
    return show_error_message, clear_stored_data, disable_export_button
