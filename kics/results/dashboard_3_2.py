import cm_dashboards.kics.helpers.db_helper as db_helper
import cm_dashboards.kics.helpers.helpers as helpers
from cm_dashboards.kics.app_config import KICS_NAME, cache, timeout


@cache.memoize(timeout=timeout)
def get_table_data(wvr_path, model_name, report_date, journal_code):
    """
    Get table data from df
    :param wvr_path: path to wvr file
    :param model_name: name of the model
    :param report_date: report date to filter by (2022-01-01)
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """

    # Initialize DB instance
    table_name = helpers.get_table_name_by_journal_code(journal_code)
    data = db_helper.Journal(table_name=table_name, report_date=report_date)

    # Get data from wvr, and unpivot df
    output = helpers.get_df(data, wvr_path, model_name)

    # Get template df
    template_df, header_rows = helpers.get_template_df(
        journal_code, kics_name=KICS_NAME
    )

    # Decrease header rows index by 1 to match with template df
    header_rows = [row_index - 1 for row_index in header_rows]

    # Extract additional headers, and new column names from template df
    headers = template_df.columns.to_list()
    headers = [helpers.remove_substring(header) for header in headers]
    new_columns = template_df.loc[0, :].fillna("").values.tolist()

    # # Update columns names amd drop unnecessary columns
    template_df.columns = new_columns
    template_df.drop([0], inplace=True)

    # Lookup for each value cell in template df and replace it with value from output df
    output_as_dict = output.to_dict(orient="records")[0]
    template_df = helpers.replace_template_values(template_df, output_as_dict)

    # Prepare table data (data, columns, conditional_style)
    results = helpers.prepare_table_data(
        template_df, header_rows, additional_header=headers
    )

    return results
