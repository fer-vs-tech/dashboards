import logging

logger = logging.getLogger(__name__)

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
    journal_code = "1-13"
    table_name = helpers.get_table_name_by_journal_code(journal_code)
    data = db_helper.Journal(table_name=table_name, report_date=report_date)
    header_info = db_helper.Journal(
        table_name="A_RC",
        select="ISS_CP_NM",
        report_date=report_date,
    )

    # Get data from wvr, and unpivot df
    results = helpers.get_df(data, wvr_path, model_name)
    header_df = helpers.get_df(header_info, wvr_path, model_name)
    logger.info(f"Header DF : {header_df}")

    # Get template df
    template_df, _ = helpers.get_template_df(journal_code, kics_name=KICS_NAME)

    # Get values from model output
    company_name = header_df["ISS_CP_NM"][0]
    applicable_tax_rate = results["ESMT_PTRAM_APPT_TXRT"][0].astype(float)
    applicable_tax_rate = helpers.add_sign_and_round(applicable_tax_rate)
    deferred_tax_assets = results["RPEA_DFCT_AST_MPRC_AMT"][0].astype(float)
    deferred_tax_liabilities = results["RPEA_DFCT_LAT_MPRC_AMT"][0].astype(float)
    logger.info("Results for 1-13 dashboard:")
    logger.info(f"Company name: {company_name}")
    logger.info(f"ESMT_PTRAM_APPT_TXRT: {applicable_tax_rate}")
    logger.info(f"RPEA_DFCT_AST_MPRC_AMT: {deferred_tax_assets}")
    logger.info(f"RPEA_DFCT_LAT_MPRC_AMT: {deferred_tax_liabilities}")

    # Update values in template df with results (by row and column index)
    template_df.iloc[0, 0] = company_name
    template_df.iloc[0, 3] = applicable_tax_rate
    template_df.iloc[0, 4] = deferred_tax_assets
    template_df.iloc[0, 5] = deferred_tax_liabilities

    # Last row
    template_df.iloc[2, 4] = deferred_tax_assets
    template_df.iloc[2, 5] = deferred_tax_liabilities

    # Prepare table data (data, columns, conditional_style)
    result = helpers.prepare_table_data(template_df)

    return result
