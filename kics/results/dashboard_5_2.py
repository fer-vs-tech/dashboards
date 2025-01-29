import pandas as pd

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
    journal_code = "5-2"
    table_name = helpers.get_table_name_by_journal_code(
        journal_code, journal_type="mixed"
    )

    # Get data from DB for each program separately
    er_data = db_helper.Journal(
        table_name=table_name["EQUITY_RISK"]["name"],
        report_date=report_date,
    )

    mr_data = db_helper.Journal(
        table_name=table_name["MARKET_RISK"]["name"],
        report_date=report_date,
    )

    # Get data from wvr, and unpivot df
    output_er = helpers.get_df(er_data, wvr_path, model_name)
    output_mr = helpers.get_df(mr_data, wvr_path, model_name)

    # Merge dataframes
    output = pd.merge(output_er, output_mr, on="Step Date", how="outer")

    # Get template df
    template_df, header_rows = helpers.get_template_df(
        journal_code, header=[0, 1, 2, 3], kics_name=KICS_NAME
    )

    # Lookup for each value cell in template df and replace it with value from output df
    output_as_dict = output.to_dict("records")[0]
    template_df = helpers.replace_template_values(
        template_df, output_as_dict, use_applymap=True
    )

    if KICS_NAME == "DGB":
        # Sum of selected pair of rows for each column
        row_indexes = [
            (1, 8),
            (2, 9),
            (3, 10),
            (4, 11),
            (5, 12),
            (6, 13),
            (7, 14),
        ]
        template_df = helpers.sum_specified_rows(
            template_df,
            row_indexes=row_indexes,
        )
        # Delete unnecessary rows after summatation as required
        template_df.drop([8, 9, 10, 11, 12, 13, 14], inplace=True)

    # Prepare table data (data, columns, conditional_style)
    results = helpers.prepare_table_data(
        template_df, header_rows=header_rows, multi_index=True
    )
    return results
