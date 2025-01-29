import cm_dashboards.esg.db_helper as db_helper
import cm_dashboards.esg.helpers as helpers


def get_table_data(wvr_path, report_date, nsp=False):
    """
    Get table data from df
    :param wvr_path: path to WVR file
    :param report_date: report date
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    # Initialize DB instance
    journal_tables = db_helper.TableInfos()

    # Get output as DF
    if not nsp:
        model_name = helpers.get_date_dropdown_options(report_date=report_date)
        df = helpers.get_df(journal_tables, wvr_path, model_name)
    df = helpers.get_df(journal_tables, wvr_path, "NSP")

    # Prepare table data
    result = helpers.prepare_table_data(df)

    return result
