import cm_dashboards.kics_cloud.db_helper as db_helper
import cm_dashboards.kics_cloud.helpers as helpers


def get_table_data(wvr_path):
    """
    Get table data from df
    :param wvr_path: path to WVR file
    :param model_name: name of model
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    # Initialize DB query
    model_name = "KICS4.3_DGB"  # KICS4.3_DGB-KICS_Ind_Risk_Asset
    journal_tables = db_helper.TableInfos()

    # Get data from wvr, unpack data (data, columns, conditional_style)
    df = helpers.get_df(journal_tables, wvr_path, model_name)

    # Prepare table data
    result = helpers.prepare_table_data(df)

    return result
