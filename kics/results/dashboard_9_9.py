import logging

import cm_dashboards.kics.helpers.db_helper as db_helper
import cm_dashboards.kics.helpers.helpers as helpers
from cm_dashboards.kics.app_config import KICS_NAME, cache, timeout

logger = logging.getLogger(__name__)


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
    journal_code = "9-9"
    table_name = helpers.get_table_name_by_journal_code(
        journal_code, journal_type="with_selection"
    )
    data = db_helper.Journal(
        table_name=table_name["name"],
        select=table_name["columns"],
        report_date=report_date,
    )

    # Get data from wvr
    output = helpers.get_df(data, wvr_path, model_name)

    # Add needed sum columns
    output["Int_Risk_Exposure_Total"] = output.eval(
        "IRRKEX_ASTT_BAS_CIRSRP_AMT + IRRKEX_LBTT_BAS_CIRSRP_AMT"
    )

    # Extract available currencies
    filter_currency = ["KRW"]  # default filter currency
    available_currencies = output["QISTR_GRPG_CKND_AMT"].unique().tolist()
    available_currencies = [x for x in available_currencies if x not in filter_currency]

    # Use this for percentage calculation and for total sum value
    total_sum = output.loc[
        ~output["QISTR_GRPG_CKND_AMT"].isin(filter_currency),
        "Int_Risk_Exposure_Total",
    ].sum()

    # Get template df
    template_df, header_rows = helpers.get_template_df(
        "9-9-2", header=[0, 1], kics_name=KICS_NAME
    )

    final_results = list()
    overview_results = dict()
    for i, currency in enumerate(available_currencies):
        title = "[통화 {}]".format(i + 1)
        logger.info("Currency: {} for dashboard-9-9-{}".format(currency, i + 2))

        # Select needed data row by currency
        currency_output = output[output["QISTR_GRPG_CKND_AMT"] == currency]

        # Lookup for each value cell in template df and replace it with value from output df
        output_as_dict = currency_output.to_dict(orient="records")[0]
        updated_df = helpers.replace_template_values(
            template_df, output_as_dict, use_applymap=True
        )

        # Rename specific columns dynamically
        updated_df = updated_df.rename(columns={"[통화 1]": title, "USD": currency})

        # Prepare table data (data, columns, conditional_style)
        results = helpers.prepare_table_data(updated_df, header_rows, multi_index=True)

        # Append results to final_results
        final_results.append(results)

        # Prepare overview table data
        current_total = output_as_dict["Int_Risk_Exposure_Total"]
        percentage = current_total / total_sum
        percentage = helpers.add_sign_and_round(percentage)

        # Add results
        overview_results.update(
            {
                title: [
                    currency,
                    output_as_dict["Int_Risk_Exposure_Total"],
                    percentage,
                ],
            }
        )

    # Get template df for overview table
    overview_df, header_rows = helpers.get_template_df("9-9-1", kics_name=KICS_NAME)

    # Add overview results as new column to overview template df (title, currency, total, percentage)
    for key, value in overview_results.items():
        overview_df = overview_df.assign(**{key: value})

    # Insert total sum value to matching cell
    overview_df.iloc[1, 1] = total_sum

    # Prepare overview table data (data, columns, conditional_style)
    overview_result = helpers.prepare_table_data(overview_df)
    final_results.insert(0, overview_result)  # Show as first dashboard table

    return final_results
