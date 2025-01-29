import cm_dashboards.china_subledger.utils.db_helper as db_helper
import cm_dashboards.china_subledger.utils.helpers as helpers


def get_table_data(wvr_path, report_date, group_id):
    """
    Get table data from df
    :param wvr_path: path to WVR file
    :param report_date: report date
    :param group_id: group id
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    journal_tables = db_helper.PortfolioData(report_date, group_id)
    df = helpers.get_df(journal_tables, wvr_path, "IFRS_17")
    return df
