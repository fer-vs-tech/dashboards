import cm_dashboards.orsa.utils.db_helper as db_helper
import cm_dashboards.orsa.utils.helpers as helpers


def get_table_data(wvr_path):
    """
    Get table data from df
    :param wvr_path: path to WVR file
    :param model_name: name of model
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    # Initialize DB query
    model_name = "SII_Company_ALM_FLAOR"
    journal_tables = db_helper.TableInfos()

    # Get data from wvr, unpack data (data, columns, conditional_style)
    df = helpers.get_df(journal_tables, wvr_path, model_name)

    # Prepare table data
    result = helpers.prepare_table_data(df)

    return result
