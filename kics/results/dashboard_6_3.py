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
    journal_code = "6-3"
    data = db_helper.CreditRisk(journal_code, report_date, name=KICS_NAME)

    # Get data from wvr, and unpivot df
    output_df = helpers.get_df(data, wvr_path, model_name)

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

    # Add special case specific to HANA
    output_as_dict = None
    if KICS_NAME == "HANA":
        special_col_val = output_df["CRDGTCR_OAST_RCRVN_AMT"][0]
        output_as_dict = dict(CRDGTCR_OAST_RCRVN_AMT=special_col_val)

    # Replace template values with real values
    template_df = helpers.replace_template_values(
        template_df,
        output_as_dict,
        helper_df=output_df,
        product_sum=product_sum_df,
    )

    # Prepare table data (data, columns, conditional_style)
    results = helpers.prepare_table_data(template_df, header_rows, multi_index=True)

    return results
