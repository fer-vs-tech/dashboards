import logging

logger = logging.getLogger(__name__)

import json
import time

from dash import no_update
from dash.dependencies import Input, Output, State

import cm_dashboards.orsa.utils.helpers as helpers
import cm_dashboards.utilities as utilities
import cm_dashboards.wvr_data.wvr_functions as wvr_functions
from cm_dashboards.orsa.config.config import app
from cm_dashboards.orsa.results.prepare_chart import generate
from cm_dashboards.orsa.results.prepare_data import get_data
from cm_dashboards.orsa.results.program_names import ChartNames, ProgramNames


@app.callback(
    [
        Output("wvr_files", "data"),
        Output("prepared_data", "data"),
        Output("chart_data", "data"),
        Output("error-toast", "is_open"),
    ],
    Input("url", "search"),
)
def get_wvr_path(url_query_string):
    """
    Get wvr path from URL parameters
    :param url_query_string: URL parameters
    :return: WVR path value
    """
    is_open = False
    try:
        # decode_url = utilities.encode_and_decode_string(
        #     url_query_string, encoding=False
        # )
        # params = utilities.extract_url_params(decode_url)
        # downscale_factor = int(params.get("factor", ["100000"])[0])
        wvr_paths = utilities.get_wvr_path_from_url(url_query_string, multiple=True)
        logger.debug("FV:")
        logger.debug(wvr_paths)
        downscale_factor = 100000

        # Set default WVR paths manually (for development only)
        if wvr_paths is None or len(wvr_paths) == 0:
            logger.info("Setting default WVR paths manually...")
            aggregation_std = "C:/temp/dashboard/orsa/2023-07-20/SII_Aggregation_Std_Formula_Group.wvr"
            base_path = "C:/temp/dashboard/orsa/2023-07-20/ORSA_Run_1/"
            model_name = "SII_Company_ALM_FLAOR_Stress"

            base = f"{base_path}/SII_Company_ALM_FLAOR_Base.wvr"
            catastrophe = f"{base_path}/{model_name}_Life_Catastrophe.wvr"
            expense_wvr = f"{base_path}/{model_name}_Life_Expense.wvr"
            lapse_down = f"{base_path}/{model_name}_Life_Lapse_Down.wvr"
            lapse_mass = f"{base_path}/{model_name}_Life_Lapse_Mass.wvr"
            lapse_up = f"{base_path}/{model_name}_Life_Lapse_Up.wvr"
            longevity = f"{base_path}/{model_name}_Life_Longevity.wvr"
            morbidity = f"{base_path}/{model_name}_Life_Morbidity.wvr"
            mortality = f"{base_path}/{model_name}_Life_Mortality.wvr"
            equity_type_1_general = (
                f"{base_path}/{model_name}_Market_Equity_Type_1_General.wvr"
            )
            equity_type_2_general = (
                f"{base_path}/{model_name}_Market_Equity_Type_2_General.wvr"
            )
            interest_down = f"{base_path}/{model_name}_Market_Interest_Down.wvr"
            interest_up = f"{base_path}/{model_name}_Market_Interest_Up.wvr"
            property_p = f"{base_path}/{model_name}_Market_Property.wvr"
            spread_bond_infra_corp = (
                f"{base_path}/{model_name}_Market_Spread_Bond_Infra_Corp.wvr"
            )
            spread_bond_infra_invest = (
                f"{base_path}/{model_name}_Market_Spread_Bond_Infra_Invest.wvr"
            )
            spread_bond_no_infra = (
                f"{base_path}/{model_name}_Market_Spread_Bond_No_Infra.wvr"
            )
            fx_down = f"{base_path}/{model_name}_Market_FX_Down.wvr"
            fx_up = f"{base_path}/{model_name}_Market_FX_Up.wvr"

            # Map WVR files to dictionary for easy access in callbacks
            map_wvr_paths = {
                "aggregation_std": aggregation_std,
                "base": base,
                "catastrophe": catastrophe,
                "expense": expense_wvr,
                "lapse_down": lapse_down,
                "lapse_mass": lapse_mass,
                "lapse_up": lapse_up,
                "longevity": longevity,
                "morbidity": morbidity,
                "mortality": mortality,
                "equity_type_1_general": equity_type_1_general,
                "equity_type_2_general": equity_type_2_general,
                "interest_down": interest_down,
                "interest_up": interest_up,
                "property": property_p,
                "spread_bond_infra_corp": spread_bond_infra_corp,
                "spread_bond_infra_invest": spread_bond_infra_invest,
                "spread_bond_no_infra": spread_bond_no_infra,
                "fx_down": fx_down,
                "fx_up": fx_up,
            }
        else:
            logger.info("Setting WVR path from URL parameters...")
            # Check if all the required paths are present
            if len(wvr_paths) < 20:
                raise Exception("Invalid parameters, some WVR paths are missing")

            map_wvr_paths = utilities.set_orsa_wvr_paths(wvr_paths)

        logger.info(f"{json.dumps(map_wvr_paths, indent=4)}")

        # Get the data from the WVR files and perform any necessary calculations
        logger.info(f"Downscale factor: {downscale_factor}")
        common_data = get_data(
            map_wvr_paths,
            ProgramNames.FutureBSProjection,
            downscale_factor=downscale_factor,
        )
        chart_data = helpers.get_partial_data(common_data, start_row=1, end_row=7)
        chart_data = helpers.perform_calculations(chart_data)

        # Convert the results to dict to store in memory (session)
        chart_data_dict = helpers.convert_df(chart_data, to_dict=True)
        data_dict = helpers.convert_df(common_data, to_dict=True)

        # Append unique ID to the data as a key for easy access in callbacks
        unique_id = utilities.generate_unique_id(map_wvr_paths)
        data_dict = utilities.create_dict_with_unique_id(unique_id, data_dict)
        chart_data_dict = utilities.create_dict_with_unique_id(
            unique_id, chart_data_dict
        )

    except Exception as e:
        logger.error("Error occurred while getting WVR path and data: {}".format(e))
        is_open = True
        map_wvr_paths, data_dict, chart_data_dict = {}, {}, {}

    return map_wvr_paths, data_dict, chart_data_dict, is_open


@app.callback(
    [
        Output("future-bs-projection-table", "data"),
        Output("future-bs-projection-table", "columns"),
        Output("future-bs-projection-table", "style_data_conditional"),
    ],
    [
        Input("wvr_files", "data"),
        Input("prepared_data", "data"),
    ],
)
def update(wvr_files, prepared_data):
    """
    Update table
    :param wvr_files: Path to the WVR file
    :param prepared_data: dict of prepared data
    :return result: figure, data, column, style
    """
    result = no_update, no_update, no_update
    if (
        prepared_data is None
        or len(prepared_data) == 0
        or wvr_files is None
        or len(wvr_files) == 0
    ):
        logger.error("No prepared data or WVR files found")
        return result

    # Check if data is present
    unique_id = utilities.generate_unique_id(wvr_files)
    prepared_data = prepared_data.get(unique_id)
    if prepared_data is None:
        logger.error("No prepared data found")
        return no_update, no_update, no_update

    # Get figure and table data
    start_time = time.perf_counter()
    try:
        result = generate(wvr_files, ChartNames.FutureBSProjection, prepared_data)
    except Exception as e:
        logger.error(
            "Error generating chart {}: {}".format(
                ChartNames.FutureBSProjection.value, e
            )
        )
    end_time = time.perf_counter()
    logger.info("Time took to generate the chart: {}".format(end_time - start_time))
    return result


@app.callback(
    [
        Output("balance-sheet-graph", "figure"),
        Output("risk-distribution-graph", "figure"),
        Output("market-risk-distribution-graph", "figure"),
        Output("life-insurance-risk-distribution-graph", "figure"),
        Output("asset-mv-graph", "figure"),
        Output("market-risk-projected-graph", "figure"),
        Output("life-insurance-risk-projected-graph", "figure"),
    ],
    [
        Input("wvr_files", "data"),
        Input("chart_data", "data"),
    ],
)
def update(wvr_files, chart_data):
    """
    Update table
    :param wvr_files: Path to the WVR file
    :param prepared_data: dict of prepared data
    :return result: figure, data, column, style
    """
    if (
        chart_data is None
        or len(chart_data) == 0
        or wvr_files is None
        or len(wvr_files) == 0
    ):
        logger.error("No prepared data or WVR files found")
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
        )

    # Check if data is present
    unique_id = utilities.generate_unique_id(wvr_files)
    chart_data = chart_data.get(unique_id)
    if chart_data is None:
        logger.error("No prepared data found")
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
        )

    # Get figures
    start_time = time.perf_counter()
    prepared_data = helpers.convert_df(chart_data, to_dict=False)
    results = list()
    program_names = [
        ChartNames.BalanceSheet,
        ChartNames.RiskDistribution,
        ChartNames.MarketRiskDistribution,
        ChartNames.LifeInsuranceRiskDistribution,
        ChartNames.AssetMV,
        ChartNames.MarketRiskProjection,
        ChartNames.LifeInsuranceRiskProjection,
    ]

    # Establish connection to the database to speed up the process of getting data
    db_connection = wvr_functions.get_db_connection(
        wvr_files.get("aggregation_std"), "SII_Aggregation_Std_Formula_Group"
    )
    for program_name in program_names:
        try:
            result = generate(wvr_files, program_name, prepared_data, hide_title=True)
            results.append(result)
        except Exception as e:
            logger.error(f"Error generating 'Overview' ({program_name.value}): {e}")
            results.append(no_update)
    db_connection.close()
    end_time = time.perf_counter()
    logger.info("Time took to generate the chart: {}".format(end_time - start_time))

    return results


@app.callback(
    [
        Output("solvency-results-table", "data"),
        Output("solvency-results-table", "columns"),
        Output("solvency-results-table", "style_data_conditional"),
    ],
    [
        Input("wvr_files", "data"),
        Input("chart_data", "data"),
    ],
)
def update(wvr_files, prepared_data):
    """
    Update table
    :param wvr_files: Path to the WVR file
    :param prepared_data: dict of prepared data
    :return result: figure, data, column, style
    """
    result = no_update, no_update, no_update
    if (
        prepared_data is None
        or len(prepared_data) == 0
        or wvr_files is None
        or len(wvr_files) == 0
    ):
        logger.error("No prepared data or WVR files found")
        return result

    # Check if data is present
    unique_id = utilities.generate_unique_id(wvr_files)
    prepared_data = prepared_data.get(unique_id)
    if prepared_data is None:
        logger.error("No prepared data found")
        return no_update, no_update, no_update

    # Get figure and table data
    start_time = time.perf_counter()
    try:
        result = generate(wvr_files, ChartNames.SolvencyResults, prepared_data)
    except Exception as e:
        logger.error(
            "Error generating chart {}: {}".format(ChartNames.SolvencyResults.value, e)
        )
    end_time = time.perf_counter()
    logger.info("Time took to generate the chart: {}".format(end_time - start_time))
    return result


@app.callback(
    [
        Output("balance-sheet-figure", "figure"),
        Output("balance-sheet-table", "data"),
        Output("balance-sheet-table", "columns"),
        Output("balance-sheet-table", "style_data_conditional"),
        Output("risk-distribution-figure", "figure"),
        Output("risk-distribution-table", "data"),
        Output("risk-distribution-table", "columns"),
        Output("risk-distribution-table", "style_data_conditional"),
        Output("market-risk-distribution-figure", "figure"),
        Output("market-risk-distribution-table", "data"),
        Output("market-risk-distribution-table", "columns"),
        Output("market-risk-distribution-table", "style_data_conditional"),
        Output("life-insurance-risk-distribution-figure", "figure"),
        Output("life-insurance-risk-distribution-table", "data"),
        Output("life-insurance-risk-distribution-table", "columns"),
        Output("life-insurance-risk-distribution-table", "style_data_conditional"),
        Output("asset-portfolio-figure", "figure"),
        Output("asset-portfolio-table", "data"),
        Output("asset-portfolio-table", "columns"),
        Output("asset-portfolio-table", "style_data_conditional"),
        Output("asset-mv-figure", "figure"),
        Output("asset-mv-table", "data"),
        Output("asset-mv-table", "columns"),
        Output("asset-mv-table", "style_data_conditional"),
    ],
    [
        Input("wvr_files", "data"),
    ],
)
def update(wvr_files):
    """
    Update table
    :param wvr_files: Path to the WVR file
    :return result: figure, data, column, style
    """
    no_result = no_update, no_update, no_update, no_update
    if wvr_files is None or len(wvr_files) == 0:
        logger.error("No valid WVR files found")
        return no_result * 6

    # Get figure and table data
    program_names = [
        ChartNames.BalanceSheet,
        ChartNames.RiskDistribution,
        ChartNames.MarketRiskDistribution,
        ChartNames.LifeInsuranceRiskDistribution,
        ChartNames.AssetPortfolio,
        ChartNames.AssetMV,
    ]
    results = list()
    start_time = time.perf_counter()
    for program_name in program_names:
        try:
            result = generate(
                wvr_files, program_name, with_table_data=True, hide_title=True
            )
            results.extend(result)
        except Exception as e:
            logger.error("Error generating chart {}: {}".format(program_name.value, e))
            results.extend(result)
    end_time = time.perf_counter()
    logger.info("Time took to generate the chart: {}".format(end_time - start_time))
    return results


@app.callback(
    [
        Output("catastrophe-graph", "figure"),
        Output("expense-graph", "figure"),
        Output("longevity-graph", "figure"),
        Output("morbidity-graph", "figure"),
        Output("mortality-graph", "figure"),
        Output("lapse-graph", "figure"),
    ],
    [
        Input("wvr_files", "data"),
        Input("chart_data", "data"),
    ],
)
def update(wvr_files, chart_data):
    """
    Update table
    :param wvr_files: Path to the WVR file
    :param prepared_data: dict of prepared data
    :return result: figure, data, column, style
    """
    if (
        chart_data is None
        or len(chart_data) == 0
        or wvr_files is None
        or len(wvr_files) == 0
    ):
        logger.error("No prepared data or WVR files found")
        return no_update, no_update, no_update, no_update, no_update, no_update

    # Check if data is present
    unique_id = utilities.generate_unique_id(wvr_files)
    chart_data = chart_data.get(unique_id)
    if chart_data is None:
        logger.error("No prepared data found")
        return no_update, no_update, no_update, no_update, no_update, no_update

    # Get figure and table data
    start_time = time.perf_counter()
    results = list()
    program_names = [
        ChartNames.CatastropheRisk,
        ChartNames.ExpenseRisk,
        ChartNames.LongevityRisk,
        ChartNames.MorbidityRisk,
        ChartNames.MortalityRisk,
        ChartNames.LapseRisk,
    ]
    prepared_data = helpers.convert_df(chart_data, to_dict=False)
    for program_name in program_names:
        try:
            result = generate(wvr_files, program_name, prepared_data)
            results.append(result)
        except Exception as e:
            logger.error(
                f"Error generating 'Projected Life Insurance Risk Chart ({program_name.value}): {e}"
            )
            results.append(no_update)

    end_time = time.perf_counter()
    logger.info("Time took to generate the chart: {}".format(end_time - start_time))
    return results


@app.callback(
    [
        Output("equity-graph", "figure"),
        Output("interest-graph", "figure"),
        Output("property-graph", "figure"),
        Output("currency-graph", "figure"),
        Output("spread-graph", "figure"),
    ],
    [
        Input("wvr_files", "data"),
        Input("chart_data", "data"),
    ],
)
def update(wvr_files, chart_data):
    """
    Update table
    :param wvr_files: Path to the WVR file
    :param prepared_data: dict of prepared data
    :return result: figure, data, column, style
    """
    if (
        chart_data is None
        or len(chart_data) == 0
        or wvr_files is None
        or len(wvr_files) == 0
    ):
        logger.error("No prepared data or WVR files found")
        return no_update, no_update, no_update, no_update, no_update

    # Check if data is present
    unique_id = utilities.generate_unique_id(wvr_files)
    chart_data = chart_data.get(unique_id)
    if chart_data is None:
        logger.error("No prepared data found")
        return no_update, no_update, no_update, no_update, no_update

    # Get figure and table data
    start_time = time.perf_counter()
    results = list()
    program_names = [
        ChartNames.EquityRisk,
        ChartNames.InterestRisk,
        ChartNames.PropertyRisk,
        ChartNames.CurrencyRisk,
        ChartNames.SpreadRisk,
    ]
    prepared_data = helpers.convert_df(chart_data, to_dict=False)
    for program_name in program_names:
        try:
            result = generate(wvr_files, program_name, prepared_data)
            results.append(result)
        except Exception as e:
            logger.error(
                f"Error generating 'Projected Market Risk Chart ({program_name.value}): {e}"
            )
            results.append(no_update)

    end_time = time.perf_counter()
    logger.info("Time took to generate the chart: {}".format(end_time - start_time))
    return results


@app.callback(
    [
        Output("projected-market-risk-graph", "figure"),
        Output("projected-market-risk-table", "data"),
        Output("projected-market-risk-table", "columns"),
        Output("projected-market-risk-table", "style_data_conditional"),
        Output("projected-life-insurance-risk-graph", "figure"),
        Output("projected-life-insurance-risk-table", "data"),
        Output("projected-life-insurance-risk-table", "columns"),
        Output("projected-life-insurance-risk-table", "style_data_conditional"),
    ],
    [
        Input("wvr_files", "data"),
        Input("chart_data", "data"),
    ],
)
def update(wvr_files, chart_data):
    """
    Update table
    :param wvr_files: Path to the WVR file
    :param prepared_data: dict of prepared data
    :return result: figure, data, column, style
    """
    if (
        chart_data is None
        or len(chart_data) == 0
        or wvr_files is None
        or len(wvr_files) == 0
    ):
        logger.error("No prepared data or WVR files found")
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
        )

    # Check if data is present
    unique_id = utilities.generate_unique_id(wvr_files)
    chart_data = chart_data.get(unique_id)
    if chart_data is None:
        logger.error("No prepared data found")
        return (
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
            no_update,
        )

    # Get figure and table data
    start_time = time.perf_counter()
    results = list()
    program_names = [
        ChartNames.ProjectedLifeInsuranceRiskAgg,
        ChartNames.LifeInsuranceRiskAgg,
    ]
    prepared_data = helpers.convert_df(chart_data, to_dict=False)
    for program_name in program_names:
        try:
            result = generate(wvr_files, program_name, prepared_data)
            results.extend(result)
        except Exception as e:
            logger.error(
                f"Error generating 'Projected Risk (Agg) Chart ({program_name.value}): {e}"
            )
            results.append(no_update)

    end_time = time.perf_counter()
    logger.info("Time took to generate the chart: {}".format(end_time - start_time))
    return results
