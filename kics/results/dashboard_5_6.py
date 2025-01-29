import cm_dashboards.kics.helpers.db_helper as db_helper
import cm_dashboards.kics.helpers.helpers as helpers
from cm_dashboards.kics.app_config import KICS_NAME, cache, timeout


@cache.memoize(timeout=timeout)
def get_table_data(wvr_path, model_name, report_date):
    """
    Get table data from df
    :param wvr_path: path to wvr file
    :param model_name: name of the model
    :param report_date: report date to filter by (2022-01-01)
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """

    # Initialize DB instance
    journal_code = "5-6"
    table_name = helpers.get_table_name_by_journal_code(
        journal_code, journal_type="mixed"
    )
    grg_data = db_helper.ConcenRiskGroupG(
        report_date=report_date, scenario=1, name=KICS_NAME
    )
    prg_data = db_helper.ConcenRiskGroupP(
        report_date=report_date, scenario=1, name=KICS_NAME
    )
    mr_data = db_helper.Journal(
        table_name=table_name["MARKET_RISK"]["name"],
        select=table_name["MARKET_RISK"]["columns"],
        report_date=report_date,
        scenario=1,
    )

    # Get data from wvr, and unpivot df
    output_1 = helpers.get_df(grg_data, wvr_path, model_name)
    output_2 = helpers.get_df(prg_data, wvr_path, model_name)
    output_3 = helpers.get_df(mr_data, wvr_path, model_name)

    # Calculate ranks using defined logic
    output_1 = helpers.calculate_ranks(
        output_1, ["ASFRS_SGRP_RSKA", "ASFRS_SGRP_EXPS_AMT"]
    )
    output_2 = helpers.calculate_ranks(
        output_2, ["PPPT_ASFC_RSKEP_AMT", "PPPT_ASFC_RSKA"]
    )

    # Get template df
    template_df, _ = helpers.get_template_df(
        journal_code, header=[0, 1], generate_header_rows=False, kics_name=KICS_NAME
    )

    # Insert MARKET_RISK output records into template df
    market_risk_as_dict = output_3.to_dict(orient="records")[0]
    template_df = helpers.replace_template_values(
        template_df, market_risk_as_dict, use_applymap=True
    )

    # Insert G_RISK_GROUP output records into template df
    template_df.iloc[1:17] = helpers.update_values_row_wise(
        template_df.iloc[1:17], output_1
    )

    # Insert P_RISK_GROUP output records into template df
    end_row_index = 28
    if KICS_NAME == "HANA":
        end_row_index = 44
    template_df.iloc[17:end_row_index] = helpers.update_values_row_wise(
        template_df.iloc[17:end_row_index], output_2
    )

    # Prepare table data (data, columns, conditional_style)
    results = helpers.prepare_table_data(
        template_df, multi_index=True, show_negative_numbers=True
    )
    return results
