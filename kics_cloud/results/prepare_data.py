import logging

logger = logging.getLogger(__name__)
import pandas as pd

import cm_dashboards.kics_cloud.db_helper as db_helper
import cm_dashboards.kics_cloud.helpers as helpers
from cm_dashboards.kics_cloud.app_config import cache, timeout
from cm_dashboards.kics_cloud.results.program_names import ProgramNames


@cache.memoize(timeout=timeout)
def get_data(wvr_path, program_name, return_table_data=False):
    """
    Get table data from df
    :param wvr_path: path to WVR file
    :param program_name: ProgramName enum
    :return dataframe or tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    # Declare params
    model_name = "KICS4.3_DGB"
    asset_risk_model_name = "KICS_Ind_Risk_Asset"
    report_date = "2022-12-31"
    report_date_pre = "2021-12-31"
    result = None

    # Adjust DB query params accordingly
    match program_name:
        case ProgramNames.ProductLevelLifeRisk:
            data_db = db_helper.ProductLevelLifeRisk(report_date)
            result = helpers.get_df(data_db, wvr_path, model_name)

        case ProgramNames.CompanyLevelLifeRiskTotal:
            data_db = db_helper.CompanyLevelLifeRiskTotal(report_date)
            result = helpers.get_df(data_db, wvr_path, model_name)

        case ProgramNames.ProductLevelLifeRiskTotal:
            data_db = db_helper.ProductLevelLifeRiskTotal(report_date)
            result = helpers.get_df(data_db, wvr_path, model_name)

        case ProgramNames.OperationRiskTotal:
            data_db = db_helper.OperationRiskTotal(report_date)
            result = helpers.get_df(data_db, wvr_path, model_name)

        case ProgramNames.CompanyLevelAssetRisk | ProgramNames.MarketRisk:
            data_db = db_helper.CompanyLevelAssetRisk(report_date)
            result = helpers.get_df(data_db, wvr_path, model_name)

        case ProgramNames.ProductLevelAssetRisk:
            data_db = db_helper.ProductLevelAssetRisk(report_date)
            result = helpers.get_df(data_db, wvr_path, model_name)

        case ProgramNames.AssetInfo:
            data_db = db_helper.AssetInfo(report_date)
            result = helpers.get_df(data_db, wvr_path, asset_risk_model_name)

        case ProgramNames.LiabilityMovement:
            data = db_helper.LiabilityMovement(report_date)
            data_pre = db_helper.LiabilityMovement(report_date_pre)
            previous, volume, acturial, economic, current = wvr_path
            previous_df = helpers.get_df(data_pre, previous, model_name)
            volume_df = helpers.get_df(data, volume, model_name)
            acturial_df = helpers.get_df(data, acturial, model_name)
            economic_df = helpers.get_df(data, economic, model_name)
            current_df = helpers.get_df(data, current, model_name)

            # Join each of the results
            result = pd.concat(
                [previous_df, volume_df, acturial_df, economic_df, current_df]
            )
            result.reset_index(inplace=True, drop=True)
            result = helpers.calculate_difference(result)
            names = helpers.get_data_structure(ProgramNames.LiabilityMovement.value)
            result = helpers.add_column(result, names)
            result.rename(
                columns={"Δ Best_Estimate_Liability": "Δ BEL", "Δ Risk_Margin": "Δ RM"},
                inplace=True,
            )

        case ProgramNames.AssetMovement:
            data = db_helper.AssetMovement(report_date)
            data_pre = db_helper.AssetMovement(report_date_pre)
            previous, volume, acturial, economic, current = wvr_path
            previous_df = helpers.get_df(data_pre, previous, model_name)
            volume_df = helpers.get_df(data, volume, model_name)
            acturial_df = helpers.get_df(data, acturial, model_name)
            economic_df = helpers.get_df(data, economic, model_name)
            current_df = helpers.get_df(data, current, model_name)

            # Join each of the results
            result = helpers.join_dfs(
                [previous_df, volume_df, acturial_df, economic_df, current_df]
            )
            result = helpers.calculate_difference(result)
            names = helpers.get_data_structure(ProgramNames.AssetMovement.value)
            result = helpers.add_column(result, names)

        case ProgramNames.InsuranceAndMarketRisk:
            data = db_helper.InsuranceAndMarketRisk(report_date)
            data_pre = db_helper.InsuranceAndMarketRisk(report_date_pre)
            previous, volume, acturial, economic, current = wvr_path
            previous_df = helpers.get_df(data_pre, previous, model_name)
            volume_df = helpers.get_df(data, volume, model_name)
            acturial_df = helpers.get_df(data, acturial, model_name)
            economic_df = helpers.get_df(data, economic, model_name)
            current_df = helpers.get_df(data, current, model_name)

            # Join each of the results
            result = helpers.join_dfs(
                [previous_df, volume_df, acturial_df, economic_df, current_df]
            )
            result = helpers.calculate_difference(result)
            names = helpers.get_data_structure(
                ProgramNames.InsuranceAndMarketRisk.value
            )
            result = helpers.add_column(result, names)

        case ProgramNames.RatioMovement:
            data = db_helper.RatioMovement(report_date)
            data_pre = db_helper.RatioMovement(report_date_pre)
            previous, volume, acturial, economic, current = wvr_path
            previous_df = helpers.get_df(data_pre, previous, model_name)
            volume_df = helpers.get_df(data, volume, model_name)
            acturial_df = helpers.get_df(data, acturial, model_name)
            economic_df = helpers.get_df(data, economic, model_name)
            current_df = helpers.get_df(data, current, model_name)

            # Join each of the results
            result = helpers.join_dfs(
                [previous_df, volume_df, acturial_df, economic_df, current_df]
            )
            names = helpers.get_data_structure(ProgramNames.RatioMovement.value)
            result = helpers.add_column(result, names)

        case ProgramNames.CapitalAndIndividualRisksMovement:
            data = db_helper.CapitalAndIndividualRisksMovement(report_date)
            data_pre = db_helper.CapitalAndIndividualRisksMovement(report_date_pre)
            previous, current = wvr_path
            previous_df = helpers.get_df(data_pre, previous, model_name)
            current_df = helpers.get_df(data, current, model_name)

            # Join each of the results
            result = helpers.join_dfs([previous_df, current_df])
            names = helpers.get_data_structure(
                ProgramNames.CapitalAndIndividualRisksMovement.value
            )
            result = helpers.add_column(result, names)

        case ProgramNames.InterestRateSensitivity:
            data = db_helper.InterestRateSensitivity(report_date)
            model_names = [
                "BEL02_Base",
                "BEL02_Down",
                "BEL02_Up",
            ]
            df_base = helpers.get_df(data, wvr_path, model_names[0])
            df_down = helpers.get_df(data, wvr_path, model_names[1])
            df_up = helpers.get_df(data, wvr_path, model_names[2])

            # Join each of the results
            result = pd.merge(df_base, df_down, on="Group_ID", how="left")
            result = pd.merge(result, df_up, on="Group_ID", how="left")

            # Calculate ratios
            result["100bp_Down"] = result.apply(
                lambda x: helpers.calc_ratio(x=x["BEL_Base_y"], y=x["BEL_Base_x"]),
                axis=1,
            )
            result["100bp_Up"] = result.apply(
                lambda x: helpers.calc_ratio(x=x["BEL_Base"], y=x["BEL_Base_x"]),
                axis=1,
            )

        case ProgramNames.AvailableCapital:
            data = db_helper.AvailableCapital(report_date)
            data_pre = db_helper.AvailableCapital(report_date_pre)
            previous, current = wvr_path
            previous_df = helpers.get_df(data_pre, previous, model_name)
            current_df = helpers.get_df(data, current, model_name)

            # Join each of the results
            result = helpers.join_dfs([previous_df, current_df])
            names = helpers.get_data_structure(ProgramNames.AvailableCapital.value)
            result = helpers.add_column(result, names)

        case ProgramNames.TierTwo:
            data = db_helper.TierTwo(report_date)
            data_pre = db_helper.TierTwo(report_date_pre)
            previous, acturial, economic, current = wvr_path
            previous_df = helpers.get_df(data_pre, previous, model_name)
            acturial_df = helpers.get_df(data, acturial, model_name)
            economic_df = helpers.get_df(data, economic, model_name)
            current_df = helpers.get_df(data, current, model_name)

            # Join each of the results
            result = helpers.join_dfs(
                [previous_df, acturial_df, economic_df, current_df]
            )
            result = helpers.calculate_difference(result)
            names = helpers.get_data_structure(ProgramNames.TierTwo.value)
            result = helpers.add_column(result, names)

        case ProgramNames.TierOne:
            data = db_helper.TierOne(report_date)
            data_pre = db_helper.TierOne(report_date_pre)
            capital_data = db_helper.AvailableCapital(report_date)
            capital_data_pre = db_helper.AvailableCapital(report_date_pre)

            previous, current = wvr_path
            previous_df = helpers.get_df(data_pre, previous, model_name)
            current_df = helpers.get_df(data, current, model_name)

            capital_previous_df = helpers.get_df(capital_data_pre, previous, model_name)
            capital_current_df = helpers.get_df(capital_data, current, model_name)

            # Join each of the results
            result = helpers.join_dfs([previous_df, current_df])
            result_capital = helpers.join_dfs([capital_previous_df, capital_current_df])

            # Add needed data
            bs_adjustment = (
                result_capital.Adjustment_Reserve.iloc[1]
                - result_capital.Adjustment_Reserve.loc[0]
            )
            capital_adjust = (
                result_capital.Capital.iloc[1] - result_capital.Capital.loc[0]
            )
            current = result.Tier_1.iloc[1]
            result.loc[1] = bs_adjustment
            result.loc[2] = capital_adjust
            result.loc[3] = current
            result = result.sort_index().reset_index(drop=True)

            names = helpers.get_data_structure(ProgramNames.TierOne.value)
            result = helpers.add_column(result, names)

        case _:
            return result

    # Check table data must be returned
    if return_table_data:
        result = helpers.prepare_table_data(result)

    return result
