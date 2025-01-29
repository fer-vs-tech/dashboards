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
    journal_code = "9-11"
    table = helpers.get_table_name_by_journal_code(
        journal_code, journal_type="with_selection"
    )
    data = db_helper.Journal(
        table_name=table["name"],
        select=table["columns"],
        report_date=report_date,
    )

    # Get template df
    template_df, header_rows = helpers.get_template_df(
        journal_code, header=[0, 1], kics_name=KICS_NAME
    )

    # Get data from wvr, and unpivot df
    output_df = helpers.get_df(data, wvr_path, model_name)

    # Format KICS_EXPI_MNCT value (year)
    output_df["KICS_EXPI_MNCT"] = output_df["KICS_EXPI_MNCT"].apply(
        lambda x: helpers.format_year_value(x)
    )

    # Keep track of column start and end indices
    # as it represents one credit rating unit (level)
    start_col = 0
    end_col = 5

    # Loop through 1-7 rating values, if any are exist in the output
    # pdate template values accordingly, otherwise empty values
    for credit_rating in range(1, 11):
        print("Current credit rating: {}".format(credit_rating))
        print("Start: {}, end: {}".format(start_col, end_col))

        # Filter out results for the current credit rating, reset index
        result = output_df[output_df["KICS_CRRT_NM"] == str(credit_rating)]
        result.reset_index(drop=True, inplace=True)

        # Update the first half of the template as it is needed per request
        template_df.iloc[1:11, start_col:end_col] = helpers.update_values_row_wise(
            template_df.iloc[1:11, start_col:end_col],
            result,
            start_row=0,
            output_start_row=0,
        )

        # Update the second half of the template as it is needed per request
        template_df.iloc[11:21, start_col:end_col] = helpers.update_values_row_wise(
            template_df.iloc[11:21, start_col:end_col],
            result,
            start_row=0,
            output_start_row=0,
        )

        # Adjust start and end column indices for the next iteration (or block of columns)
        start_col = end_col - 1
        end_col = start_col + 5

    # Prepare table data (data, columns, conditional_style)
    results = helpers.prepare_table_data(template_df, header_rows, multi_index=True)

    return results
