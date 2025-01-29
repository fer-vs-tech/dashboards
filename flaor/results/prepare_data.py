import logging

logger = logging.getLogger(__name__)

import cm_dashboards.flaor.utils.db_helper as db_helper
import cm_dashboards.flaor.utils.helpers as helpers
from cm_dashboards.flaor.config.config import cache, timeout
from cm_dashboards.flaor.results.program_names import ProgramNames


@cache.memoize(timeout=timeout)
def get_data(
    wvr_paths,
    program_name,
    return_table_data=False,
):
    """
    Get table data from df
    :param wvr_path: dict of WVR paths
    :param program_name: ProgramName enum
    :return dataframe or tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    kics_path = wvr_paths.get("kics")
    base_path = wvr_paths.get("base")
    kics_model_name = "FLAOR_KICSRatio_Model"
    base_model_name = "Base"

    header_rows = []
    multi_index = True
    try:
        match program_name:
            case ProgramNames.SCHEMA:
                db = db_helper.ProjectedRiskRegulatory()
                result = helpers.get_df(db, kics_path, kics_model_name)

            case ProgramNames.SOLVENCY_OVERALL:
                db = db_helper.SolvencyOverall()
                result = helpers.get_df(db, kics_path, kics_model_name)
                result["KICS_Ratio"] = result["KICS_Ratio"].apply(lambda x: f"{x:.1f}%")

            case ProgramNames.REQUIRED_CAPITAL:
                db = db_helper.RequiredCapital()
                result = helpers.get_df(db, kics_path, kics_model_name)

            case ProgramNames.ASSET_PORTFOLIO:
                db = db_helper.AssetPortfolioIndividual()
                db_group = db_helper.AssetPortfolioGroup()
                db_unique = db_helper.AssetPortfolioUniqueData()

                result = helpers.get_df(db, base_path, base_model_name)
                result_group = helpers.get_df(db_group, base_path, base_model_name)
                result_unique = helpers.get_df(db_unique, base_path, base_model_name)

                result = helpers.update_unique_data(result, result_unique)
                result = helpers.add_group_data(result, result_group)

            case ProgramNames.PROJECTED_RISK_REGULATORY:
                db = db_helper.ProjectedRiskRegulatory()
                result = helpers.get_df(db, kics_path, kics_model_name)

            case ProgramNames.LIFE_AND_HEALTH_RISK:
                db = db_helper.LifeAndHealthRisk()
                result = helpers.get_df(db, kics_path, kics_model_name)

            case ProgramNames.MARKET_RISK:
                db = db_helper.MarketRisk()
                result = helpers.get_df(db, kics_path, kics_model_name)

            case ProgramNames.CREDIT_RISK:
                db = db_helper.CreditRisk()
                result = helpers.get_df(db, kics_path, kics_model_name)

            case _:
                message = f"Program name not found: {program_name}"
                logger.error(message)
                return Exception(message)

        if return_table_data:
            result = helpers.prepare_table_data(
                result, header_rows=header_rows, multi_index=multi_index
            )

        return result

    except Exception as e:
        return Exception(f"Error in get_data: {e}")
