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
    journal_code = "5-4"
    table_name = helpers.get_table_name_by_journal_code(
        journal_code, journal_type="mixed"
    )
    header_data = db_helper.Journal(
        table_name=table_name["MARKET_RISK"]["name"],
        select=table_name["MARKET_RISK"]["columns"],
        report_date=report_date,
    )

    data = db_helper.Journal(
        table_name=table_name["FOREX_RISK_GROUP"]["name"],
        select=table_name["FOREX_RISK_GROUP"]["columns"],
        report_date=report_date,
    )

    # Get data from wvr, and unpivot df
    header = helpers.get_df(header_data, wvr_path, model_name)
    output = helpers.get_df(data, wvr_path, model_name)

    # Get template df
    template_df, _ = helpers.get_template_df(
        journal_code, generate_header_rows=False, kics_name=KICS_NAME
    )
    # Replace "Unnamed" columns with empty string
    columns = template_df.columns.tolist()
    columns = [helpers.remove_substring(column) for column in columns]
    template_df.columns = columns

    # Lookup for each value cell in template df and replace it with value from output df
    header_as_dict = header.to_dict(orient="records")[0]
    template_df = helpers.replace_template_values(template_df, header_as_dict)

    # Update values row-wise based on output df values
    template_df = helpers.update_values_row_wise(template_df, output)

    # Prepare table data (data, columns, conditional_style)
    results = helpers.prepare_table_data(template_df)

    return results
