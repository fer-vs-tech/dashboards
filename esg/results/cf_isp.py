import cm_dashboards.esg.db_helper as db_helper
import cm_dashboards.esg.helpers as helpers


def get_table_data(wvr_path, report_date):
    """
    Get table data from df
    :param wvr_path: path to WVR file
    :param report_date: report date
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    # Initialize DB instance
    model_name = "NSP"
    data = db_helper.CF_ISP()

    # Get output as DF
    df = helpers.get_df(data, wvr_path, model_name)
    df = helpers.calculate_and_add_needed_values(df)
    df = helpers.pivot_df(df)

    # Prepare table data
    result = helpers.prepare_table_data(df)

    return result
