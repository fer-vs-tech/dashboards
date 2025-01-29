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
    journal_code = "5-5"
    table_name = helpers.get_table_name_by_journal_code(journal_code)
    data = db_helper.Journal(
        table_name=table_name,
        report_date=report_date,
    )

    # Get data from wvr, and unpivot df
    output = helpers.get_df(data, wvr_path, model_name)

    # Get template df
    template_df, _ = helpers.get_template_df(
        journal_code,
        header=[0, 1, 2, 3, 4],
        generate_header_rows=False,
        kics_name=KICS_NAME,
    )

    # Insert actual data into template df
    template_df = helpers.update_common_rows_at_once(template_df, output)

    # Prepare table data (data, columns, conditional_style)
    results = helpers.prepare_table_data(
        template_df, multi_index=True, show_negative_numbers=True
    )
    return results
