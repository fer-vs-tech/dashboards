import cm_dashboards.jics.helpers.db_helper as db_helper
import cm_dashboards.jics.helpers.helpers as helpers
from cm_dashboards.jics.config.config import cache, timeout


@cache.memoize(timeout=timeout)
def get_table_data(wvr_path, model_name):
    """
    Get table data from df
    :param wvr_path: path to WVR file
    :param model_name: name of model
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    journal_tables = db_helper.TableInfos()
    df = helpers.get_df(journal_tables, wvr_path, model_name)
    result = helpers.prepare_table_data(df)
    return result
