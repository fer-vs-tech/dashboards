import cm_dashboards.kics.helpers.db_helper as db_helper
import cm_dashboards.kics.helpers.helpers as helpers
from cm_dashboards.kics.app_config import KICS_NAME, cache, timeout


@cache.memoize(timeout=timeout)
def get_table_data(wvr_path, model_name, report_date, journal_code):
    """
    Get table data from df
    :param wvr_path: path to wvr file
    :param report_date: report date to filter by (2022-01-01)
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    # Adjust parameters according to journal code
    match journal_code:
        case "2-4-1":
            # Initialize DB instance
            journal_code = "2-4-1"
            table_name = helpers.get_table_name_by_journal_code(
                journal_code, journal_type="mixed"
            )

            # Get data from DB for each program separately
            rc_data = db_helper.Journal(
                table_name=table_name["RC"]["name"],
                report_date=report_date,
            )

            lrt_data = db_helper.Journal(
                table_name=table_name["LIFE_RISK_TOT"]["name"],
                report_date=report_date,
                select=table_name["LIFE_RISK_TOT"]["columns"],
            )

            mr_data = db_helper.Journal(
                table_name=table_name["MARKET_RISK"]["name"],
                report_date=report_date,
                select=table_name["MARKET_RISK"]["columns"],
            )

            # Get data from wvr, and unpivot df
            rc_df = helpers.get_df(rc_data, wvr_path, model_name)
            lrt_df = helpers.get_df(lrt_data, wvr_path, model_name)
            mr_df = helpers.get_df(mr_data, wvr_path, model_name)

            # Join dfs
            rc_df = rc_df.join(lrt_df, how="outer")
            rc_df = rc_df.join(mr_df, how="outer")
            output = rc_df.to_dict(orient="records")[0]

            # Get template df
            template_df, header_rows = helpers.get_template_df(
                journal_code, kics_name=KICS_NAME
            )

        case "2-4-2":
            # Initialize DB instance
            journal_code = "2-4-2"
            table_name = helpers.get_table_name_by_journal_code(
                journal_code, journal_type="with_selection"
            )

            # Get data from DB for each program separately
            data = db_helper.Journal(
                table_name=table_name["name"],
                report_date=report_date,
                select=table_name["columns"],
            )
            # Get data from wvr, and unpivot df
            output = helpers.get_df(data, wvr_path, model_name)
            output = output.to_dict(orient="records")[0]

            # Get template df
            template_df, header_rows = helpers.get_template_df(
                journal_code, generate_header_rows=False, kics_name=KICS_NAME
            )

    # Insert actual values into template df from values df
    final_df = helpers.replace_template_values(template_df, output, use_applymap=True)

    # Prepare table data (data, columns, conditional_style)
    results = helpers.prepare_table_data(final_df, header_rows)

    return results
