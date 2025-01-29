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
    journal_code = "6-1"
    data = db_helper.CreditRiskTotal(report_date, name=KICS_NAME)

    helper_data = db_helper.CreditRisk(journal_code, report_date)

    # Get data from wvr, and unpivot df
    output = helpers.get_df(data, wvr_path, model_name)
    helper_output = helpers.get_df(helper_data, wvr_path, model_name)

    # Get template df
    template_df, header_rows = helpers.get_template_df(
        journal_code, kics_name=KICS_NAME
    )

    output_as_dict = output.to_dict(orient="records")[0]
    template_df = helpers.replace_template_values(
        template_df, output_as_dict, helper_df=helper_output
    )

    # Prepare table data (data, columns, conditional_style)
    results = helpers.prepare_table_data(template_df, header_rows)

    return results
