"""
@author: Kamoliddin Usmonov
@project: K-ICS Cloud Dashboard 
@description: K-ICS Cloud Dashboards
@date: 2023-03-14
"""
import logging

logger = logging.getLogger(__name__)
import sys

sys.path.append("..")
import time

from dash import no_update
from dash.dependencies import Input, Output
from flask import redirect, render_template, request

import cm_dashboards.kics_cloud.results.prepare_chart as prepare_chart
import cm_dashboards.utilities as utilities
from cm_dashboards.kics_cloud.app_config import PROJECT_NAME, PROJECT_TITLE, app
from cm_dashboards.kics_cloud.results.program_names import ChartNames
from cm_dashboards.server import server as application


@app.callback(
    Output("kics-previous-wvr", "value"),
    Output("kics-volume-wvr", "value"),
    Output("kics-acturial-wvr", "value"),
    Output("kics-economic-wvr", "value"),
    Output("kics-current-wvr", "value"),
    Input("url", "search"),
)
def get_wvr_path(input_url):
    """
    Get wvr path from URL parameters
    :param input_url: Input URL to get .wvr path
    :return: WVR path value
    """
    global KICS_PREVIOUS_WVR
    global KICS_VOLUME_WVR
    global KICS_ACTURIAL_WVR
    global KICS_ECONOMIC_WVR
    global KICS_CURRENT_WVR

    # Get WVR path from URL parameters
    decode_url = utilities.encode_and_decode_string(input_url, encoding=False)
    logger.info("Decoded URL query: {}".format(decode_url))
    params = utilities.extract_url_params(decode_url)
    if len(params) > 0:
        logger.info("Setting WVR path from URL parameters...")
        wvr_paths = utilities.set_wvr_path(params)
        KICS_PREVIOUS_WVR = wvr_paths.get("previous")
        KICS_VOLUME_WVR = wvr_paths.get("volume")
        KICS_ACTURIAL_WVR = wvr_paths.get("acturial")
        KICS_ECONOMIC_WVR = wvr_paths.get("economic")
        KICS_CURRENT_WVR = wvr_paths.get("current")
    else:
        # Manually set WVR path for testing if needed
        logger.info("No WVR path found in URL parameters.")
        KICS_PREVIOUS_WVR = (
            "C:/temp/dashboard/kics_cloud/results_20230324/K-ICS_202112.wvr"
        )
        KICS_VOLUME_WVR = (
            "C:/temp/dashboard/kics_cloud/results_20230324/K-ICS_volume.wvr"
        )
        KICS_ACTURIAL_WVR = (
            "C:/temp/dashboard/kics_cloud/results_20230324/K-ICS_act.wvr"
        )
        KICS_ECONOMIC_WVR = (
            "C:/temp/dashboard/kics_cloud/results_20230324/K-ICS_202212.wvr"
        )
        KICS_CURRENT_WVR = (
            "C:/temp/dashboard/kics_cloud/results_20230324/K-ICS_202212.wvr"
        )

    logger.info(f"KICS_PREVIOUS_WVR - {KICS_PREVIOUS_WVR}")
    logger.info(f"KICS_VOLUME_WVR - {KICS_VOLUME_WVR}")
    logger.info(f"KICS_ACTURIAL_WVR - {KICS_ACTURIAL_WVR}")
    logger.info(f"KICS_ECONOMIC_WVR - {KICS_ECONOMIC_WVR}")
    logger.info(f"KICS_CURRENT_WVR - {KICS_CURRENT_WVR}")

    return (
        KICS_PREVIOUS_WVR,
        KICS_VOLUME_WVR,
        KICS_ACTURIAL_WVR,
        KICS_ECONOMIC_WVR,
        KICS_CURRENT_WVR,
    )


@app.callback(
    [
        Output("company-risk-figure", "figure"),
        Output("company-risk", "data"),
        Output("company-risk", "columns"),
        Output("company-risk", "style_data_conditional"),
    ],
    [
        Input("kics-current-wvr", "value"),
    ],
)
def update(wvr_path):
    """
    Update table
    :param wvr_path: Path to the wvr file
    :return result: figure, data, column, style
    """
    result = no_update, no_update, no_update, no_update
    if wvr_path is None:
        return result

    # Get figure and table data
    start_time = time.perf_counter()
    try:
        result = prepare_chart.generate(wvr_path, ChartNames.CompanyRisk)
    except Exception as e:
        logger.error(
            "Error generating chart {}: {}".format(ChartNames.CompanyRisk.value, e)
        )
    end_time = time.perf_counter()
    logger.info(
        "Time took to generate 'CompanyRisk' chart: {}".format(end_time - start_time)
    )
    return result


@app.callback(
    [
        Output("asset-info-figure", "figure"),
        Output("asset-info", "data"),
        Output("asset-info", "columns"),
        Output("asset-info", "style_data_conditional"),
    ],
    [
        Input("company-risk", "style_data_conditional"),
        Input("kics-current-wvr", "value"),
    ],
)
def update(_, wvr_path):
    """
    Update table
    :param wvr_path: Path to the wvr file
    :return result: figure, data, column, style
    """
    result = no_update, no_update, no_update, no_update
    if wvr_path is None:
        return result

    # Get figure and table data
    start_time = time.perf_counter()
    try:
        result = prepare_chart.generate(wvr_path, ChartNames.AssetInfo)
    except Exception as e:
        logger.error(
            "Error generating chart {}: {}".format(ChartNames.AssetInfo.value, e)
        )
    end_time = time.perf_counter()
    logger.info(
        "Time took to generate 'AssetInfo' chart: {}".format(end_time - start_time)
    )
    return result


@app.callback(
    [
        Output("market-risk-figure", "figure"),
        Output("market-risk", "data"),
        Output("market-risk", "columns"),
        Output("market-risk", "style_data_conditional"),
    ],
    [
        Input("asset-info", "style_data_conditional"),
        Input("kics-current-wvr", "value"),
    ],
)
def update(_, wvr_path):
    """
    Update table
    :param wvr_path: Path to the wvr file
    :return result: figure, data, column, style
    """
    result = no_update, no_update, no_update, no_update
    if wvr_path is None:
        return result

    # Get figure and table data
    start_time = time.perf_counter()
    try:
        result = prepare_chart.generate(wvr_path, ChartNames.MarketRisk)
    except Exception as e:
        logger.error(
            "Error generating chart {}: {}".format(ChartNames.MarketRisk.value, e)
        )
    end_time = time.perf_counter()
    logger.info(
        "Time took to generate 'MarketRisk' chart: {}".format(end_time - start_time)
    )
    return result


@app.callback(
    [
        Output("liability-info-figure", "figure"),
        Output("liability-info", "data"),
        Output("liability-info", "columns"),
        Output("liability-info", "style_data_conditional"),
    ],
    [
        Input("market-risk", "style_data_conditional"),
        Input("kics-current-wvr", "value"),
    ],
)
def update(_, wvr_path):
    """
    Update table
    :param wvr_path: Path to the wvr file
    :return result: figure, data, column, style
    """
    result = no_update, no_update, no_update, no_update
    if wvr_path is None:
        return result

    # Get figure and table data
    start_time = time.perf_counter()
    try:
        result = prepare_chart.generate(wvr_path, ChartNames.LiabilityInfo)
    except Exception as e:
        logger.error(
            "Error generating chart {}: {}".format(ChartNames.LiabilityInfo.value, e)
        )
    end_time = time.perf_counter()
    logger.info(
        "Time took to generate 'LiabilityInfo' chart: {}".format(end_time - start_time)
    )
    return result


@app.callback(
    [
        Output("risk-figure", "figure"),
        Output("insurance-risk-figure", "figure"),
        Output("market-risk-2-figure", "figure"),
        Output("product-info", "data"),
        Output("product-info", "columns"),
        Output("product-info", "style_data_conditional"),
    ],
    [
        Input("market-risk", "style_data_conditional"),
        Input("kics-current-wvr", "value"),
    ],
)
def update(_, wvr_path):
    """
    Update table
    :param wvr_path: Path to the wvr file
    :return result: figure, data, column, style
    """
    result = no_update, no_update, no_update, no_update, no_update, no_update
    if wvr_path is None:
        return result

    # Get figure and table data
    start_time = time.perf_counter()
    try:
        result = prepare_chart.generate(wvr_path, ChartNames.ProductInfo)
    except Exception as e:
        logger.error(
            "Error generating chart {}: {}".format(ChartNames.ProductInfo.value, e)
        )

    end_time = time.perf_counter()
    logger.info(
        "Time took to generate 'ProductInfo' chart: {}".format(end_time - start_time)
    )
    return result


@app.callback(
    [
        Output("bel-movement", "figure"),
        Output("risk-margin-movement", "figure"),
        Output("liability-movement", "data"),
        Output("liability-movement", "columns"),
        Output("liability-movement", "style_data_conditional"),
    ],
    [
        Input("kics-previous-wvr", "value"),
        Input("kics-volume-wvr", "value"),
        Input("kics-acturial-wvr", "value"),
        Input("kics-economic-wvr", "value"),
        Input("kics-current-wvr", "value"),
    ],
)
def update(*wvrs):
    """
    Update table
    :param previous_wvr: Path to the KICS Previous WVR file
    :param volume_wvr: Path to the KICS Volume WVR file
    :param acturial_wvr: Path to the KICS Acturial WVR file
    :param economic_wvr: Path to the KICS Economic WVR file
    :param current_wvr: Path to the KICS Current WVR file
    :return result: figure, data, column, style
    """
    result = no_update, no_update, no_update, no_update, no_update
    logger.info("WVR files: {}".format(wvrs))
    if len(wvrs) == 0:
        return result

    # Get figure and table data
    start_time = time.perf_counter()
    try:
        result = prepare_chart.generate(wvrs, ChartNames.LiabilityMovement)
    except Exception as e:
        logger.error(
            "Error generating chart {}: {}".format(
                ChartNames.LiabilityMovement.value, e
            )
        )
    end_time = time.perf_counter()
    logger.info(
        "Time took to generate 'LiabilityMovement' chart: {}".format(
            end_time - start_time
        )
    )
    return result


@app.callback(
    [
        Output("asset-movement-figure", "figure"),
        Output("asset-movement", "data"),
        Output("asset-movement", "columns"),
        Output("asset-movement", "style_data_conditional"),
    ],
    [
        Input("kics-previous-wvr", "value"),
        Input("kics-volume-wvr", "value"),
        Input("kics-acturial-wvr", "value"),
        Input("kics-economic-wvr", "value"),
        Input("kics-current-wvr", "value"),
    ],
)
def update(*wvrs):
    """
    Update table
    :param previous_wvr: Path to the KICS Previous WVR file
    :param volume_wvr: Path to the KICS Volume WVR file
    :param acturial_wvr: Path to the KICS Acturial WVR file
    :param economic_wvr: Path to the KICS Economic WVR file
    :param current_wvr: Path to the KICS Current WVR file
    :return result: figure, data, column, style
    """
    result = no_update, no_update, no_update, no_update
    logger.info("WVR files: {}".format(wvrs))
    if len(wvrs) == 0:
        return result

    # Get figure and table data
    start_time = time.perf_counter()
    try:
        result = prepare_chart.generate(wvrs, ChartNames.AssetMovement)
    except Exception as e:
        logger.error(
            "Error generating chart {}: {}".format(ChartNames.AssetMovement.value, e)
        )
    end_time = time.perf_counter()
    logger.info(
        "Time took to generate 'AssetMovement' chart: {}".format(end_time - start_time)
    )
    return result


@app.callback(
    [
        Output("required-capital-figure", "figure"),
        Output("required-capital", "data"),
        Output("required-capital", "columns"),
        Output("required-capital", "style_data_conditional"),
        Output("market-risk-movement-figure", "figure"),
        Output("market-risk-movement", "data"),
        Output("market-risk-movement", "columns"),
        Output("market-risk-movement", "style_data_conditional"),
        Output("insurance-risk-movement-figure", "figure"),
        Output("insurance-risk-movement", "data"),
        Output("insurance-risk-movement", "columns"),
        Output("insurance-risk-movement", "style_data_conditional"),
    ],
    [
        Input("kics-previous-wvr", "value"),
        Input("kics-current-wvr", "value"),
    ],
)
def update(*wvrs):
    """
    Update table
    :param previous_wvr: Path to the KICS Previous WVR file
    :param current_wvr: Path to the KICS Current WVR file
    :return result: figure, data, column, style
    """
    result = (
        no_update,
        no_update,
        no_update,
        no_update,
        no_update,
        no_update,
        no_update,
        no_update,
        no_update,
        no_update,
        no_update,
        no_update,
    )
    logger.info("WVR files: {}".format(wvrs))
    if len(wvrs) == 0:
        return result

    # Get figure and table data
    start_time = time.perf_counter()
    try:
        result = prepare_chart.generate(
            wvrs, ChartNames.CapitalAndIndividualRisksMovement
        )
    except Exception as e:
        logger.error(
            "Error generating chart {}: {}".format(
                ChartNames.CapitalAndIndividualRisksMovement.value, e
            )
        )
    end_time = time.perf_counter()
    logger.info(
        "Time took to generate 'CapitalAndIndividualRisksMovement' chart: {}".format(
            end_time - start_time
        )
    )
    return result


@app.callback(
    [
        Output("available-capital-figure", "figure"),
        Output("available-capital", "data"),
        Output("available-capital", "columns"),
        Output("available-capital", "style_data_conditional"),
    ],
    [
        Input("kics-previous-wvr", "value"),
        Input("kics-current-wvr", "value"),
    ],
)
def update(*wvrs):
    """
    Update table
    :param previous_wvr: Path to the KICS Previous WVR file
    :param current_wvr: Path to the KICS Current WVR file
    :return result: figure, data, column, style
    """
    result = no_update, no_update, no_update, no_update
    logger.info("WVR files: {}".format(wvrs))
    if len(wvrs) == 0:
        return result

    # Get figure and table data
    start_time = time.perf_counter()
    try:
        result = prepare_chart.generate(wvrs, ChartNames.AvailableCapital)
    except Exception as e:
        logger.error(
            "Error generating chart {}: {}".format(ChartNames.AvailableCapital.value, e)
        )
    end_time = time.perf_counter()
    logger.info(
        "Time took to generate 'AvailableCapital' chart: {}".format(
            end_time - start_time
        )
    )
    return result


@app.callback(
    [
        Output("tier-2-figure", "figure"),
        Output("tier-2", "data"),
        Output("tier-2", "columns"),
        Output("tier-2", "style_data_conditional"),
    ],
    [
        Input("kics-previous-wvr", "value"),
        Input("kics-acturial-wvr", "value"),
        Input("kics-economic-wvr", "value"),
        Input("kics-current-wvr", "value"),
    ],
)
def update(*wvrs):
    """
    Update table
    :param previous_wvr: Path to the KICS Previous WVR file
    :param current_wvr: Path to the KICS Current WVR file
    :return result: figure, data, column, style
    """
    result = no_update, no_update, no_update, no_update
    logger.info("WVR files: {}".format(wvrs))
    if len(wvrs) == 0:
        return result

    # Get figure and table data
    start_time = time.perf_counter()
    try:
        result = prepare_chart.generate(wvrs, ChartNames.TierTwo)
    except Exception as e:
        logger.error(
            "Error generating chart {}: {}".format(ChartNames.TierTwo.value, e)
        )
    end_time = time.perf_counter()
    logger.info(
        "Time took to generate 'TierTwo' chart: {}".format(end_time - start_time)
    )
    return result


@app.callback(
    [
        Output("tier-1-figure", "figure"),
        Output("tier-1", "data"),
        Output("tier-1", "columns"),
        Output("tier-1", "style_data_conditional"),
    ],
    [
        Input("kics-previous-wvr", "value"),
        Input("kics-current-wvr", "value"),
    ],
)
def update(*wvrs):
    """
    Update table
    :param previous_wvr: Path to the KICS Previous WVR file
    :param current_wvr: Path to the KICS Current WVR file
    :return result: figure, data, column, style
    """
    result = no_update, no_update, no_update, no_update
    logger.info("WVR files: {}".format(wvrs))
    if len(wvrs) == 0:
        return result

    # Get figure and table data
    start_time = time.perf_counter()
    try:
        result = prepare_chart.generate(wvrs, ChartNames.TierOne)
    except Exception as e:
        logger.error(
            "Error generating chart {}: {}".format(ChartNames.TierOne.value, e)
        )
    end_time = time.perf_counter()
    logger.info(
        "Time took to generate 'TierOne' chart: {}".format(end_time - start_time)
    )
    return result


@app.callback(
    [
        Output("insurance-risk-movement-2-figure", "figure"),
        Output("market-risk-movement-2-figure", "figure"),
        Output("insurance-risk-movement-2", "data"),
        Output("insurance-risk-movement-2", "columns"),
        Output("insurance-risk-movement-2", "style_data_conditional"),
    ],
    [
        Input("kics-previous-wvr", "value"),
        Input("kics-volume-wvr", "value"),
        Input("kics-acturial-wvr", "value"),
        Input("kics-economic-wvr", "value"),
        Input("kics-current-wvr", "value"),
    ],
)
def update(*wvrs):
    """
    Update table
    :param previous_wvr: Path to the KICS Previous WVR file
    :param volume_wvr: Path to the KICS Volume WVR file
    :param acturial_wvr: Path to the KICS Acturial WVR file
    :param economic_wvr: Path to the KICS Economic WVR file
    :param current_wvr: Path to the KICS Current WVR file
    :return result: figure, data, column, style
    """
    result = no_update, no_update, no_update, no_update, no_update
    logger.info("WVR files: {}".format(wvrs))
    if len(wvrs) == 0:
        return result

    # Get figure and table data
    start_time = time.perf_counter()
    try:
        result = prepare_chart.generate(wvrs, ChartNames.InsuranceAndMarketRisk)
    except Exception as e:
        logger.error(
            "Error generating chart {}: {}".format(
                ChartNames.InsuranceAndMarketRisk.value, e
            )
        )
    end_time = time.perf_counter()
    logger.info(
        "Time took to generate 'InsuranceAndMarketRisk' chart: {}".format(
            end_time - start_time
        )
    )
    return result


@app.callback(
    [
        Output("ratio-movement-figure", "figure"),
        Output("ratio-movement", "data"),
        Output("ratio-movement", "columns"),
        Output("ratio-movement", "style_data_conditional"),
    ],
    [
        Input("kics-previous-wvr", "value"),
        Input("kics-volume-wvr", "value"),
        Input("kics-acturial-wvr", "value"),
        Input("kics-economic-wvr", "value"),
        Input("kics-current-wvr", "value"),
    ],
)
def update(*wvrs):
    """
    Update table
    :param previous_wvr: Path to the KICS Previous WVR file
    :param volume_wvr: Path to the KICS Volume WVR file
    :param acturial_wvr: Path to the KICS Acturial WVR file
    :param economic_wvr: Path to the KICS Economic WVR file
    :param current_wvr: Path to the KICS Current WVR file
    :return result: figure, data, column, style
    """
    result = no_update, no_update, no_update, no_update
    logger.info("WVR files: {}".format(wvrs))
    if len(wvrs) == 0:
        return result

    # Get figure and table data
    start_time = time.perf_counter()
    try:
        result = prepare_chart.generate(wvrs, ChartNames.RatioMovement)
    except Exception as e:
        logger.error(
            "Error generating chart {}: {}".format(ChartNames.RatioMovement.value, e)
        )
    end_time = time.perf_counter()
    logger.info(
        "Time took to generate 'RatioMovement' chart: {}".format(end_time - start_time)
    )
    return result


@application.route(f"/dash/{PROJECT_NAME}/controllers", methods=["GET", "POST"])
def controllers():
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
            if any(
                [
                    k not in params
                    for k in ["previous", "volume", "acturial", "economic", "current"]
                ]
            ):
                logger.error("Invalid form data, some fields are missing")
                redirect_url = f"/dash/{PROJECT_NAME}/controllers?{old_params_decoded}"
                return redirect(redirect_url)

            # Remove the next key as it is not required
            params = {
                k: v[0]
                for k, v in params.items()
                if k in ["previous", "volume", "acturial", "economic", "current"]
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
        "controllers_screen.html",
        title=PROJECT_TITLE,
        wvrs=wvrs,
        auto_mode=auto_mode,
        query_string=encode_query_string,
    )
