"""
@author: Kamoliddin Usmonov
@project: KICS
@description: K-ICS QIS reporting dashboards
@date: 2022-10-19
"""
import logging

logger = logging.getLogger(__name__)
import sys

sys.path.append("..")
import time

from dash import no_update
from dash.dependencies import Input, Output, State
from flask import redirect, render_template, request

import cm_dashboards.kics.helpers.dropdown_options as dropdown_options
import cm_dashboards.kics.helpers.helpers as helpers
import cm_dashboards.utilities as utilities
from cm_dashboards.kics.app_config import KICS_NAME, PROJECT_NAME, PROJECT_TITLE, app
from cm_dashboards.kics.layout.generate_layout import (
    generate_dashboard_layout,
    generate_main_layout,
)
from cm_dashboards.kics.layout.load_data import get_dashboard_data, get_dashboards_data
from cm_dashboards.server import server as application

# Dynamic app layout
dashbord_data = get_dashboards_data(KICS_NAME)
app.layout = generate_main_layout(dashbord_data)

# Set WVR path globally
KICS_PATH = None
TRANSITION_PATH = None
SENSITIVITY_PATH = None
KICS_MODEL_NAME = None
DB_CONNECTION = None


@app.callback(
    [
        Output("kics-name", "value"),
        Output("kics-path", "value"),
        Output("transition-path", "value"),
        Output("sensitivity-path", "value"),
        Output("kics-model-name", "value"),
    ],
    Input("url", "search"),
)
def get_wvr_path(input_url):
    """
    Get wvr path from URL parameters
    :param input_url: Input URL to get .wvr path
    :return: WVR path value
    """
    global KICS_PATH
    global TRANSITION_PATH
    global SENSITIVITY_PATH
    global KICS_MODEL_NAME
    global KICS_NAME
    global DB_CONNECTION

    # Default WVR path (only for development purposes)
    KICS_PATH = "C:/temp/dashboard/kics/2023-06-28/KICS.wvr"
    TRANSITION_PATH = (
        "C:/temp/dashboard/kics/2023-06-01/Transition_Measure/Transition_Measure.wvr"
    )
    SENSITIVITY_PATH = "C:/temp/dashboard/kics/2023-06-01/Sensitivity/Sensitivity.wvr"

    # Set WVR path from URL parameters based on KICS name
    logger.info(f"URL params: {input_url}")
    if KICS_NAME == "DGB":
        try:
            # Get WVR path from URL parameters
            decode_url = utilities.encode_and_decode_string(input_url, encoding=False)
            logger.info(f"Decoded URL query: {decode_url}")
            params = utilities.extract_url_params(decode_url)
            if len(params) > 0:
                logger.info("Setting WVR path from URL parameters...")
                wvr_paths = utilities.set_wvr_path(params)
                KICS_PATH = wvr_paths.get("main")
                TRANSITION_PATH = wvr_paths.get("transition")
                SENSITIVITY_PATH = wvr_paths.get("sensitivity")
            else:
                logger.info("No URL parameters found. Using default WVR path...")
        except Exception as e:
            logger.error(f"Error while setting WVR path from URL parameters: {e}")
            return no_update, no_update, no_update, no_update, no_update
    else:
        # Get WVR path from URL parameters normally
        kics_path = utilities.get_wvr_path_from_url(input_url)
        if kics_path is not None:
            KICS_PATH = kics_path
        TRANSITION_PATH = None
        SENSITIVITY_PATH = None

    logger.info(f"KICS_PATH - {KICS_PATH}")
    logger.info(f"TRANSITION_PATH - {TRANSITION_PATH}")
    logger.info(f"SENSTIVITY_PATH - {SENSITIVITY_PATH}")

    # Extract model name from output using WVR path
    KICS_MODEL_NAME = helpers.get_kics_model_name(KICS_PATH)

    # Do this only once for performance boost
    # DB_CONNECTION = helpers.get_db_connection(KICS_PATH, KICS_MODEL_NAME)
    return (
        KICS_NAME,
        KICS_PATH,
        TRANSITION_PATH,
        SENSITIVITY_PATH,
        KICS_MODEL_NAME,
    )


@app.callback(
    [
        Output("report-date-dropdown", "options"),
        Output("report-date-dropdown", "value"),
    ],
    [
        Input("kics-path", "value"),
        Input("kics-model-name", "value"),
    ],
)
def update_table(kics_path, kics_model_name):
    """
    Retrive report dates from given journal table
    :param n_clicks: A number of clicks for callback test
    :return: DDL options and value and the report dates list
    """
    if (
        kics_path is None
        or kics_path == ""
        or kics_model_name is None
        or kics_model_name == ""
    ):
        return no_update, no_update

    # Get report dates from journal table
    result = dropdown_options.get_data(kics_path, kics_model_name)
    default = result[0]["value"] if len(result) > 0 else None

    return result, default


@app.callback(
    Output("dashboard-data", "children"),
    [
        Input("report-date-dropdown", "value"),
        Input("tabs", "active_tab"),
        State("kics-name", "value"),
    ],
)
def update_table(report_date, active_tab, kics_name):
    """
    Update dashboard data
    :param report_date: Report date
    :param active_tab: Active tab
    :return: Dashboard data
    """
    logger.info("KICS name: {}".format(kics_name))
    logger.info("Report date: {})".format(report_date))
    logger.info("Active tab: {}".format(active_tab))
    logger.info("Model name: {}".format(KICS_MODEL_NAME))

    # Get dashboard data (label, dashboard count, handler)
    dashboard_data = get_dashboard_data(kics_name, active_tab)

    # Check if dashboard data is valid
    if (
        dashboard_data is None
        or len(dashboard_data) == 0
        or report_date is None
        or report_date == ""
    ):
        logger.info("No update for dashboard data")
        return no_update

    dashboard_id = dashboard_data.get("id")
    logger.info("Dashboard ID: {}".format(dashboard_id))

    # Keep track of time
    start_time = time.time()

    # Get dashboard results
    handler = dashboard_data.get("handler")
    child_dashboards = dashboard_data.get("child_dashboards")

    # Check if handler is valid
    if handler is None:
        logger.info(f"Handler is None for dashboard ID: {dashboard_id}")
        return no_update

    # Generate results
    results = generate_results(report_date, dashboard_id, handler, child_dashboards)

    # Execute dashboard results
    logger.info("Executing dashboard results")
    end_time = time.time()
    logger.info(f"Time taken for {dashboard_id} - {end_time - start_time}")

    # Generate layout for dashboard
    layout = generate_dashboard_layout(dashboard_data, results)

    return layout


def generate_results(report_date, dashboard_id, handler, child_dashboards):
    """
    Generate dynamic results for dashboard
    :param report_date: Report date (YYYY-MM-DD)
    :param dashboard_id: Dashboard ID (e.g. 2-4)
    :param handler: Handler object
    :param child_dashboards: Child dashboards (if any)
    :return: Results list (data, columns, style_data_conditional)
    """
    results = list()
    match dashboard_id:
        # Extraordinary dashboards with child dashboards
        case "2-4" | "3-2" | "5-1":
            for child_dash_id in child_dashboards.keys():
                result = handler.get_table_data(
                    KICS_PATH, KICS_MODEL_NAME, report_date, child_dash_id
                )
                results.append(result)

        case "2-6":
            results = handler.get_table_data(TRANSITION_PATH, report_date)

        case "9-12-(2)":
            for child_dash_id in child_dashboards.keys():
                result = handler.get_table_data(
                    KICS_PATH,
                    KICS_MODEL_NAME,
                    report_date,
                    child_dash_id,
                )
                results.append(result)

        case "9-12" | "9-12-(3)":
            # Get prepared common data
            prepared_output = handler.get_prepared_common_df(
                KICS_PATH, KICS_MODEL_NAME, report_date
            )
            not_common_dash_ids = ["9-12-7"]
            for child_dash_id in child_dashboards.keys():
                # Check if child dashboard consumes common data
                if child_dash_id not in not_common_dash_ids:
                    result = handler.get_table_data(
                        KICS_PATH,
                        KICS_MODEL_NAME,
                        report_date,
                        child_dash_id,
                        prepared_output=prepared_output,
                    )
                else:
                    result = handler.get_table_data(
                        KICS_PATH,
                        KICS_MODEL_NAME,
                        report_date,
                        child_dash_id,
                    )
                results.append(result)

        case "10-1":
            for child_dash_id in child_dashboards.keys():
                result = handler.get_table_data(
                    SENSITIVITY_PATH, report_date, child_dash_id
                )
                results.append(result)

        case "10-2":
            for child_dash_id in child_dashboards.keys():
                result = handler.get_table_data(
                    SENSITIVITY_PATH, report_date, child_dash_id
                )
                results.append(result)

        case _:
            # Ordinary dashboard without child dashboards
            results = handler.get_table_data(KICS_PATH, KICS_MODEL_NAME, report_date)

    return results


@application.route(f"/dash/{PROJECT_NAME}/controllers", methods=["GET", "POST"])
def kics_controllers():
    """
    Controller screen for the dash app
    """
    import urllib.parse

    if request.method == "POST":
        # Validate the form data
        params = request.form.to_dict(flat=False)
        old_params = params.get("next", [""])[0]
        old_params_decoded = utilities.encode_and_decode_string(old_params)
        auto_mode = params.get("auto_mode", ["false"])[0].lower() == "true"
        logger.info("Auto-mode: {}".format(auto_mode))
        # Check if it's auto-mode
        if auto_mode:
            # Check if all the required fields are present
            if any([k not in params for k in ["main", "transition", "sensitivity"]]):
                logger.error("Invalid form data, some fields are missing")
                redirect_url = f"/dash/{PROJECT_NAME}/controllers?{old_params_decoded}"
                return redirect(redirect_url)

            # Remove the next key as it is not required
            params = {
                k: v[0]
                for k, v in params.items()
                if k in ["main", "transition", "sensitivity"]
            }
            query_string = urllib.parse.urlencode(params)
            query_string = query_string.replace(".wvr", "")
            encode_query_string = utilities.encode_and_decode_string(
                query_string, encoding=True
            )
            logger.info("Encoded query string: {}".format(encode_query_string))
            logger.info("Query string: {}".format(query_string))
            redirect_url = f"/dash/{PROJECT_NAME}/?{encode_query_string}"
            return redirect(redirect_url)

        # Clean the params
        params = {
            k.replace("_path", ""): v[0]
            for k, v in params.items()
            if k.endswith("_path")
        }
        logger.info("Cleaned params: {}".format(params))
        wvrs = list(params.values())
        wvrs = utilities.validate_wvr_paths(wvrs)
        query_string = urllib.parse.urlencode(params)
        query_string = query_string.replace(".wvr", "")
        encode_query_string = utilities.encode_and_decode_string(
            query_string, encoding=True
        )
        redirect_url = f"/dash/{PROJECT_NAME}/?{encode_query_string}"
        logger.info("WVR files: {}".format(wvrs))
        logger.info("Query string: {}".format(query_string))

        return redirect(redirect_url)

    # Parse the URL query string
    query_string = "?" + request.query_string.decode("utf-8")
    query_string = query_string.replace(".wvr", "")
    params = utilities.extract_url_params(query_string)
    wvrs = params.get("wvr", [None])
    wvrs = utilities.validate_wvr_paths(wvrs)
    auto_mode = True
    if len(wvrs) == 0:
        wvrs = utilities.get_jobrun_folders()
        auto_mode = False
    encode_query_string = utilities.encode_and_decode_string(
        query_string, encoding=True
    )
    return render_template(
        "kics_controllers_screen.html",
        title=PROJECT_TITLE,
        wvrs=wvrs,
        auto_mode=auto_mode,
        query_string=encode_query_string,
    )
