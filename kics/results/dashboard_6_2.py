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
    journal_code = "6-2"
    table_name = helpers.get_table_name_by_journal_code(
        journal_code, journal_type="mixed"
    )
    if table_name is None:
        raise ValueError(f"Table name not found for journal code {journal_code}")

    data = db_helper.Journal(
        table_name=table_name["CREDIT_RISK_TOT"]["name"],
        select=table_name["CREDIT_RISK_TOT"]["columns"],
        report_date=report_date,
    )
    helper_data = db_helper.CreditRisk(journal_code, report_date, name=KICS_NAME)

    # Get data from wvr, and unpivot df
    output = helpers.get_df(data, wvr_path, model_name)
    helper_output = helpers.get_df(helper_data, wvr_path, model_name)

    # Get template df
    template_df, header_rows = helpers.get_template_df(
        journal_code, header=[0, 1, 2], kics_name=KICS_NAME
    )

    # Get sumproduct df (contains values for sumproduct formulas per row)
    product_sum_df, _ = helpers.get_template_df(
        f"{journal_code}-sumproduct", header=[0, 1, 2], kics_name=KICS_NAME
    )
    # Replace NaN with 0
    product_sum_df.fillna(0, inplace=True)

    output_as_dict = output.to_dict(orient="records")[0]
    template_df = helpers.replace_template_values(
        template_df,
        output_as_dict,
        helper_df=helper_output,
        product_sum=product_sum_df,
    )

    # Prepare table data (data, columns, conditional_style)
    results = helpers.prepare_table_data(template_df, header_rows, multi_index=True)

    return results
