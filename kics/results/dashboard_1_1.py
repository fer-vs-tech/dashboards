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
    journal_code = "1-1"
    table_name = helpers.get_table_name_by_journal_code(journal_code)
    data = db_helper.Journal(table_name=table_name, report_date=report_date)

    # Get data from wvr, and unpivot df
    results = helpers.get_df(data, wvr_path, model_name)
    results = results.to_dict(orient="records")[0]

    # Get template df
    template_df, header_rows = helpers.get_template_df(
        journal_code, kics_name=KICS_NAME
    )

    # Update template df with results df
    df = helpers.replace_template_values(template_df, results, use_applymap=True)

    # Prepare table data (data, columns, conditional_style)
    result = helpers.prepare_table_data(
        df,
        header_rows=header_rows,
        filter_column_style="총괄",
    )

    return result
