import logging

logger = logging.getLogger(__name__)
import pandas as pd

import cm_dashboards.orsa.utils.db_helper as db_helper
import cm_dashboards.orsa.utils.helpers as helpers
from cm_dashboards.orsa.config.config import cache, timeout
from cm_dashboards.orsa.results.program_names import ProgramNames


@cache.memoize(timeout=timeout)
def get_data(wvr_files, program_name, return_table_data=False, downscale_factor=100000):
    """
    Get table data from df
    :param wvr_files: dict of WVR paths
    :param program_name: ProgramName enum
    :return dataframe or tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    # Declare params
    model_name = "SII_Company_ALM_FLAOR"
    agg_model_name = "SII_Aggregation_Std_Formula_Group"
    report_date = "2018-12-31"
    report_dates = [
        "2018-12-31",
        "2019-12-31",
        "2020-12-31",
        "2021-12-31",
        "2022-12-31",
        "2023-12-31",
    ]
    header_rows = list()
    result = None
    multi_index = False
    wvr_path = wvr_files.get("base")  # Default to base
    wvr_aggregation = wvr_files.get("aggregation_std")

    # Adjust DB query params accordingly
    try:
        match program_name:
            case ProgramNames.Schema:
                data_db = db_helper.FutureBSProjection(report_dates)
                result = helpers.get_df(data_db, wvr_path, model_name)

            case ProgramNames.FutureBSProjection:
                # Open DB connection to prevent opening/closing connection for each query as it is slow
                db_results = dict()

                # Get data from DB for each WVR output
                db_connection = helpers.get_db_connection(wvr_path, model_name)
                data_db = db_helper.FutureBSProjection(report_dates)
                for name, path in wvr_files.items():
                    # Skip aggregation_std as it is not needed
                    if name == "aggregation_std":
                        continue
                    current_result = helpers.get_df(data_db, path, model_name)
                    current_result["Report_Date"] = current_result[
                        "Report_Date"
                    ].astype(str)
                    current_result["Call_Date"] = current_result["Call_Date"].astype(
                        str
                    )
                    # Scale down values
                    current_result = current_result.apply(
                        lambda x: helpers.downscale_value(x, downscale_factor)
                    )
                    db_results[name] = current_result
                db_connection.close()

                # Get template
                result, _ = helpers.get_template_df(
                    "future_bs_projection", False, [0, 1]
                )
                result = helpers.replace_template_values(result, db_results)

            case ProgramNames.SolvencyResults:
                data_db = db_helper.RCInformation(report_date)
                db_result = helpers.get_df(data_db, wvr_aggregation, agg_model_name)
                result, header_rows = helpers.get_template_df("solvency_result")
                result = helpers.replace_template_values_ordinary(result, db_result)
                result = result.apply(
                    lambda x: helpers.downscale_value(x, downscale_factor)
                )

            case ProgramNames.BalanceSheet:
                data_db = db_helper.RCInformation(report_date)
                db_result = helpers.get_df(data_db, wvr_aggregation, agg_model_name)
                result, header_rows = helpers.get_template_df("balance_sheet", False)
                result = helpers.replace_template_values_ordinary(result, db_result)
                result = result.apply(
                    lambda x: helpers.downscale_value(x, downscale_factor)
                )

            case ProgramNames.RiskDistribution:
                data_db = db_helper.RCInformation(report_date)
                db_result = helpers.get_df(data_db, wvr_aggregation, agg_model_name)
                result, header_rows = helpers.get_template_df(
                    "risk_distribution", False
                )
                result = helpers.replace_template_values_ordinary(result, db_result)
                result = result.apply(
                    lambda x: helpers.downscale_value(x, downscale_factor)
                )

            case ProgramNames.MarketRiskDistribution:
                data_db = db_helper.RCInformation(report_date)
                db_result = helpers.get_df(data_db, wvr_aggregation, agg_model_name)
                result, header_rows = helpers.get_template_df("market_risk", False)
                result = helpers.replace_template_values_ordinary(result, db_result)
                result = result.apply(
                    lambda x: helpers.downscale_value(x, downscale_factor)
                )

            case ProgramNames.LifeInsuranceRiskDistribution:
                data_db = db_helper.RCInformation(report_date)
                db_result = helpers.get_df(data_db, wvr_aggregation, agg_model_name)
                result, header_rows = helpers.get_template_df("life_insurance", False)
                result = helpers.replace_template_values_ordinary(result, db_result)
                result = result.apply(
                    lambda x: helpers.downscale_value(x, downscale_factor)
                )

            case ProgramNames.AssetMV:
                data_db = db_helper.RebalanceInfoAtBase()
                comp_db = db_helper.RebalanceAtCompanyLevel()
                db_result = helpers.get_df(data_db, wvr_path, model_name)
                comp_result = helpers.get_df(comp_db, wvr_path, model_name)

                # Convert date columns to string
                db_result["ReportDate"] = db_result["ReportDate"].astype(str)
                db_result["CallDate"] = db_result["CallDate"].astype(str)
                comp_result["ReportDate"] = db_result["ReportDate"].astype(str)
                comp_result["CallDate"] = db_result["CallDate"].astype(str)

                # Insert actual output into template, perform needed calculations
                result, header_rows = helpers.get_template_df("asset_portfolio", False)
                result.iloc[0:4] = helpers.calculate_avg_value(
                    result.iloc[0:4], db_result
                )
                result.iloc[5:7] = helpers.calculate_avg_value(
                    result.iloc[5:7], comp_result
                )
                result = helpers.add_sum_row(result)
                result = result.apply(
                    lambda x: helpers.downscale_value(x, downscale_factor)
                )
                result = helpers.calculate_ratios(result)

            case _:
                logger.error("Program name not found: {}".format(program_name))
                return Exception("Program name not found: {}".format(program_name))

        # Check table data must be returned
        if return_table_data:
            result = helpers.prepare_table_data(
                result, header_rows=header_rows, multi_index=multi_index
            )

        return result

    except Exception as e:
        return Exception("Error in get_data: {}".format(e))
