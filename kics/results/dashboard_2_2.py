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
    journal_code = "2-2"
    table_name = helpers.get_table_name_by_journal_code(journal_code)
    data = db_helper.Journal(table_name=table_name, report_date=report_date)

    # Get data from wvr, and unpivot df
    results = helpers.get_df(data, wvr_path, model_name)

    # Get template df
    template_df, _ = helpers.get_template_df(
        journal_code, generate_header_rows=False, kics_name=KICS_NAME
    )
    # Extract variable names from template df
    r3s_variables = template_df.columns.tolist()
    r3s_variables.remove("")
    # Extract additional headers, and new column names from template df
    headers = template_df.loc[0, :].fillna("").values.tolist()
    new_columns = template_df.loc[1, :].fillna("").values.tolist()

    # Update columns names amd drop unnecessary columns
    template_df.columns = new_columns
    template_df.drop([0, 1], inplace=True)

    # Insert actual values
    final_df = helpers.insert_actual_values(
        template_df, results, r3s_variables, start_col_index=1
    )

    # Prepare table data (data, columns, conditional_style)
    result = helpers.prepare_table_data(final_df, additional_header=headers)

    return result
