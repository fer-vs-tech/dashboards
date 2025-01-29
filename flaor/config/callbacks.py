import logging

logger = logging.getLogger(__name__)

import json
import time

from dash import no_update
from dash.dependencies import Input, Output

import cm_dashboards.utilities as utilities
import cm_dashboards.wvr_data.wvr_functions as wvr_functions
from cm_dashboards.flaor.config.config import app
from cm_dashboards.flaor.results.prepare_chart import get_chart
from cm_dashboards.flaor.results.prepare_data import get_data
from cm_dashboards.flaor.results.program_names import ChartNames, ProgramNames


@app.callback(
    [
        Output("wvr_paths", "value"),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    Input("url", "search"),
    prevent_initial_call=True,
)
def set_wvr_path(input_url):
    """
    Get wvr path from URL parameters
    """
    logger.info("Setting WVR path ...")
    error_message = None
    logger.info(f"Input_url: {input_url}")

    # Manually set WVR path and JOURNAL_NAME
    if not input_url:
        wvr_paths = [
            "C:/temp/dashboard/flaor/2023-12-15/ModelResults/KICS_Future.wvr",
            "C:/temp/dashboard/flaor/2023-12-15/ModelResults/FLAOR_Shock_Batch.wvr",
        ]
    else:
        wvr_paths = utilities.get_wvr_path_from_url(input_url, multiple=True)
    logger.info(f"WVR path: {wvr_paths}")

    # Check if provided WVR file is valid
    try:
        # Unique model names for pattern matching
        model_names = ["FLAOR_KICSRatio_Model", "Base"]
        # Parse all WVR names
        identified_models = wvr_functions.identify_models(wvr_paths, model_names)
        # Check if needed models exist
        if not bool(identified_models):
            wvr_paths = None
            error_message = "The required model is missing or invalid output provided"
            return wvr_paths, error_message

        logger.info("Identified models: {}".format(identified_models))
        # Rename model names
        valid_paths = {
            "kics": identified_models.get("FLAOR_KICSRatio_Model"),
            "base": identified_models.get("Base"),
        }
    except Exception as e:
        logger.error(f"Error occured while getting WVR path: {e}")
        valid_paths = {}
        error_message = "WVR path is missing or invalid output provided"

    valid_paths = json.dumps(valid_paths)
    return valid_paths, error_message


@app.callback(
    Output("error-toast", "is_open"),
    Input("error-toast", "children"),
)
def open_toast(error_message):
    """
    Open toast with error message
    """
    return bool(error_message)


@app.callback(
    [
        Output("solvency-overall-table", "data"),
        Output("solvency-overall-table", "columns"),
        Output("solvency-overall-table", "style_data_conditional"),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    Input("wvr_paths", "value"),
    prevent_initial_call=True,
)
def update_solvency_overall_table(wvr_paths):
    """
    Update Solvency Overall table
    """
    wvr_paths = json.loads(wvr_paths)
    program_name = ProgramNames.SOLVENCY_OVERALL
    logger.info("Generating 'Solvency Overall' table")
    error_message = None
    if not wvr_paths or wvr_paths == "":
        return no_update, no_update, no_update, no_update

    try:
        results = get_data(wvr_paths, program_name, True)
    except Exception as e:
        error_message = f"Error occured while generating '{program_name}' table: {e}"
        logger.error(error_message)
        results = no_update, no_update, no_update

    return [*results, error_message]


@app.callback(
    [
        Output("solvency-overall-chart", "figure"),
        Output("available-capital-chart", "figure"),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    Input("solvency-overall-table", "data"),
    prevent_initial_call=True,
)
def update_solvency_overall_chart(data):
    """
    Update Solvency Overall chart
    """
    logger.info("Generating 'Solvency Overall' chart")
    error_message = None
    if not data or data == "":
        return no_update, no_update, no_update

    results = []
    charts = [ChartNames.SOLVENCY_OVERALL, ChartNames.AVAILABLE_CAPITAL]
    for name in charts:
        try:
            results.append(get_chart(name=name, prepared_data=data))
        except Exception as e:
            error_message = f"Error occured while generating '{name}' chart: {e}"
            logger.error(error_message)
            results.append(no_update)
    return [*results, error_message]


@app.callback(
    [
        Output("required-capital-table", "data"),
        Output("required-capital-table", "columns"),
        Output("required-capital-table", "style_data_conditional"),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    [
        Input("wvr_paths", "value"),
        Input("solvency-overall-table", "data"),
    ],
    prevent_initial_call=True,
)
def update_required_capital_table(wvr_paths, _):
    """
    Update Required Capital table
    """
    wvr_paths = json.loads(wvr_paths)
    program_name = ProgramNames.REQUIRED_CAPITAL
    logger.info(f"Generating '{program_name}' table")
    error_message = None
    if not wvr_paths or wvr_paths == "":
        return no_update, no_update, no_update, no_update

    try:
        results = get_data(wvr_paths, program_name, True)
    except Exception as e:
        error_message = f"Error occured while generating '{program_name}' table: {e}"
        logger.error(error_message)
        results = no_update, no_update, no_update
    return [*results, error_message]


@app.callback(
    [
        Output("required-capital-chart", "figure"),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    Input("required-capital-table", "data"),
    prevent_initial_call=True,
)
def update_available_capital_table(data):
    """
    Update Available Capital chart
    """
    program_name = ChartNames.REQUIRED_CAPITAL
    logger.info(f"Generating '{program_name}' chart")
    error_message = None
    if not data or data == "":
        return no_update, no_update

    try:
        results = get_chart(name=program_name, prepared_data=data)
    except Exception as e:
        error_message = f"Error occured while generating '{program_name}' chart: {e}"
        logger.error(error_message)
        results = no_update
    return results, error_message


@app.callback(
    [
        Output("asset-portfolio-chart", "figure"),
        Output("asset-portfolio-table", "data"),
        Output("asset-portfolio-table", "columns"),
        Output("asset-portfolio-table", "style_data_conditional"),
    ],
    [
        Input("wvr_paths", "value"),
    ],
)
def update_alm_results_table(wvr_paths):
    """
    Update Required Capital table
    """
    wvr_paths = json.loads(wvr_paths)
    program_name = ChartNames.ASSET_PORTFOLIO
    logger.info(f"Generating '{program_name}' table")
    if not wvr_paths or wvr_paths == "":
        return no_update, no_update, no_update, no_update

    try:
        results = get_chart(wvr_paths, program_name, with_table_data=True)
    except Exception as e:
        error_message = f"Error occured while generating '{program_name}' table: {e}"
        logger.error(error_message)
        results = no_update, no_update, no_update, no_update
    return results


@app.callback(
    [
        Output("projected-pap-rr-chart", "figure"),
        Output("projected-pap-liability-chart", "figure"),
        Output("projected-pap-table", "data"),
        Output("projected-pap-table", "columns"),
        Output("projected-pap-table", "style_data_conditional"),
    ],
    [
        Input("wvr_paths", "value"),
    ],
)
def update_projected_pap(wvr_paths):
    """
    Update Projected MV B/S under Risk Regulation table
    """
    wvr_paths = json.loads(wvr_paths)
    program_name = ChartNames.PROJECTED_RISK_REGULATORY
    logger.info(f"Generating '{program_name}' table")
    if not wvr_paths or wvr_paths == "":
        return no_update, no_update, no_update, no_update

    try:
        results = get_chart(wvr_paths, program_name, with_table_data=True)
    except Exception as e:
        error_message = f"Error occured while generating '{program_name}' table: {e}"
        logger.error(error_message)
        results = no_update, no_update, no_update, no_update
    return results


@app.callback(
    [
        Output("life-health-risk-table", "data"),
        Output("life-health-risk-table", "columns"),
        Output("life-health-risk-table", "style_data_conditional"),
    ],
    [
        Input("wvr_paths", "value"),
    ],
)
def update_life_health_risk_table(wvr_paths):
    """
    Update 'Life and Health Risk' table
    """
    wvr_paths = json.loads(wvr_paths)
    program_name = ProgramNames.LIFE_AND_HEALTH_RISK
    logger.info(f"Generating '{program_name}' table")
    if not wvr_paths or wvr_paths == "":
        return no_update, no_update, no_update, no_update

    try:
        results = get_data(wvr_paths, program_name, True)
    except Exception as e:
        error_message = f"Error occured while generating '{program_name}' table: {e}"
        logger.error(error_message)
        results = no_update, no_update, no_update, no_update
    return results


@app.callback(
    [
        Output("life-health-risk-chart", "figure"),
        Output("life-health-risk-overall-chart", "figure"),
        Output("mortality-risk-chart", "figure"),
        Output("longevity-risk-chart", "figure"),
        Output("morbitity-risk-chart", "figure"),
        Output("lapse-risk-chart", "figure"),
        Output("expense-risk-chart", "figure"),
        Output("catastrophe-risk-chart", "figure"),
    ],
    [
        Input("life-health-risk-table", "data"),
    ],
)
def update_life_health_risk_charts(data):
    """
    Update 'Life and Health Risk' charts
    """
    program_names = [
        ChartNames.LIFE_AND_HEALTH_INSURANCE_RISK,
        ChartNames.LIFE_AND_HEALTH_RISK_OVERALL,
        ChartNames.MORTALITY_RISK,
        ChartNames.LONGEVITY_RISK,
        ChartNames.MORBITITY_RISK,
        ChartNames.LAPSE_RISK,
        ChartNames.EXPENSE_RISK,
        ChartNames.CATASTROPHE_RISK,
    ]
    if not data or data == "":
        return [no_update] * len(program_name)
    results = []
    for program_name in program_names:
        logger.info(f"Generating '{program_name}' table")
        try:
            results.append(get_chart(name=program_name, prepared_data=data))
        except Exception as e:
            error_message = (
                f"Error occured while generating '{program_name}' chart: {e}"
            )
            logger.error(error_message)
            results.append(no_update)
            continue
    return results


@app.callback(
    [
        Output("market-risk-table", "data"),
        Output("market-risk-table", "columns"),
        Output("market-risk-table", "style_data_conditional"),
    ],
    [
        Input("wvr_paths", "value"),
    ],
)
def update_market_risk_table(wvr_paths):
    """
    Update 'Market Risk' table
    """
    wvr_paths = json.loads(wvr_paths)
    program_name = ProgramNames.MARKET_RISK
    logger.info(f"Generating '{program_name}' table")
    if not wvr_paths or wvr_paths == "":
        return no_update, no_update, no_update, no_update

    try:
        results = get_data(wvr_paths, program_name, True)
    except Exception as e:
        error_message = f"Error occured while generating '{program_name}' table: {e}"
        logger.error(error_message)
        results = no_update, no_update, no_update, no_update
    return results


@app.callback(
    [
        Output("market-risk-chart", "figure"),
        Output("market-risk-overall-chart", "figure"),
        Output("interest-risk-chart", "figure"),
        Output("equity-risk-chart", "figure"),
        Output("forex-risk-chart", "figure"),
        Output("property-risk-chart", "figure"),
        Output("concentration-risk-chart", "figure"),
    ],
    [
        Input("market-risk-table", "data"),
    ],
)
def update_marketrisk_charts(data):
    """
    Update 'Market Risk' charts
    """
    program_names = [
        ChartNames.MARKET_RISK,
        ChartNames.MARKET_RISK_OVERALL,
        ChartNames.INTEREST_RISK,
        ChartNames.EQUITY_RISK,
        ChartNames.FOREX_RISK,
        ChartNames.PROPERTY_RISK,
        ChartNames.CONCENTRATION_RISK,
    ]
    if not data or data == "":
        return [no_update] * len(program_name)
    results = []
    for program_name in program_names:
        logger.info(f"Generating '{program_name}' table")
        try:
            results.append(get_chart(name=program_name, prepared_data=data))
        except Exception as e:
            error_message = (
                f"Error occured while generating '{program_name}' chart: {e}"
            )
            logger.error(error_message)
            results.append(no_update)
            continue
    return results


@app.callback(
    [
        Output("credit-risk-table", "data"),
        Output("credit-risk-table", "columns"),
        Output("credit-risk-table", "style_data_conditional"),
    ],
    [
        Input("wvr_paths", "value"),
    ],
)
def update_credit_risk_table(wvr_paths):
    """
    Update 'Credit Risk' table
    """
    wvr_paths = json.loads(wvr_paths)
    program_name = ProgramNames.CREDIT_RISK
    logger.info(f"Generating '{program_name}' table")
    if not wvr_paths or wvr_paths == "":
        return no_update, no_update, no_update, no_update

    try:
        results = get_data(wvr_paths, program_name, True)
    except Exception as e:
        error_message = f"Error occured while generating '{program_name}' table: {e}"
        logger.error(error_message)
        results = no_update, no_update, no_update, no_update
    return results


@app.callback(
    [
        Output("credit-risk-chart", "figure"),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    Input("credit-risk-table", "data"),
    prevent_initial_call=True,
)
def update_credit_risk_chart(data):
    """
    Update 'Credit Risk' chart
    """
    program_name = ChartNames.CREDIT_RISK
    logger.info(f"Generating '{program_name}' chart")
    error_message = None
    if not data or data == "":
        return no_update, no_update

    try:
        results = get_chart(name=program_name, prepared_data=data)
    except Exception as e:
        error_message = f"Error occured while generating '{program_name}' chart: {e}"
        logger.error(error_message)
        results = no_update
    return results, error_message
