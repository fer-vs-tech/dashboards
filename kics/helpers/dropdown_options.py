import cm_dashboards.kics.helpers.db_helper as db_helper
import cm_dashboards.kics.helpers.helpers as helpers


def get_data(wvr_path, model_name, journal_code="1-1"):
    """
    Get table data from df
    :param wvr_path: path to wvr file
    :param journal_name: journal name to retrive table name from (AC)
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    # Initialize DB instance
    table_name = "A_RC"
    data = db_helper.JournalReportDates(table_name=table_name)

    # Get data from wvr (data, columns, conditional_style)
    df = helpers.get_df(data, wvr_path, model_name)
    result = helpers.prepare_dropdown_options(df)
    return result
