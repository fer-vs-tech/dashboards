import logging

logger = logging.getLogger(__name__)

import cm_dashboards.jics.helpers.db_helper as db_helper
import cm_dashboards.jics.helpers.helpers as helpers
from cm_dashboards.jics.config.config import cache, timeout


@cache.memoize(timeout=timeout)
def get_data(wvr_path, model_name):
    """
    Get table data from df
    :param wvr_path: path to wvr file
    :param journal_name: journal name to retrive table name from (AC)
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    table_name = "A_ESR"
    data = db_helper.JournalReportDates(table_name=table_name)
    df = helpers.get_df(data, wvr_path, model_name)
    result = helpers.prepare_dropdown_options(df)
    return result
