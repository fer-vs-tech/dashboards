from cm_dashboards.kics.app_config import cache, timeout
import cm_dashboards.kics.helpers.db_helper as db_helper
import cm_dashboards.kics.helpers.helpers as helpers


@cache.memoize(timeout=timeout)
def get_table_data(wvr_path, model_name):
    """
    Get table data from df
    :param wvr_path: path to WVR file
    :param model_name: name of model
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    # Initialize DB instance
    journal_tables = db_helper.TableInfos()

    # Get data from wvr, unpack data (data, columns, conditional_style
    df = helpers.get_df(journal_tables, wvr_path, model_name)

    # Prepare table data
    result = helpers.prepare_table_data(df)

    return result
