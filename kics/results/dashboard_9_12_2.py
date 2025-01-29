import cm_dashboards.kics.helpers.db_helper as db_helper
import cm_dashboards.kics.helpers.helpers as helpers
from cm_dashboards.kics.app_config import KICS_NAME, cache, timeout


@cache.memoize(timeout=timeout)
def get_table_data(wvr_path, model_name, report_date, journal_code):
    """
    Get table data from df
    :param wvr_path: path to wvr file
    :param model_name: name of the model
    :param report_date: report date to filter by (2022-01-01)
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """

    # Initialize DB instance
    table_name = helpers.get_table_name_by_journal_code(journal_code)
    data = db_helper.Journal(
        table_name=table_name,
        report_date=report_date,
    )
    # Get template df
    template_df, _ = helpers.get_template_df(
        journal_code, generate_header_rows=False, header=[0, 1, 2], kics_name=KICS_NAME
    )

    # Slice template df and insert output records into template df by applying filter as per requirement
    if journal_code == "9-12-5":
        # Get data from wvr
        output = helpers.get_df(data, wvr_path, model_name)

        # Evaluate conditional expression and add result to output df as new column (N)
        n1_result = output.eval(
            "CSCRT_TIER_1_CBS_USBT_YN == 'Y' & CSCRT_TIER_1_CBS_CNTA_YN == 'Y' & CSCRT_TIER_2_CBS_USBT_YN == 'Y' & CSCRT_TIER_2_CBS_CNTA_YN == 'Y'"
        )
        n2_result = output.eval(
            "CSCRT_TIER_1_CBS_OLAB_YN == 'Y' & CSCRT_TIER_1_CBS_AFOA_YN == 'Y' & CSCRT_TIER_2_CBS_OLAB_YN == 'Y' & CSCRT_TIER_2_CBS_AFOA_YN == 'Y'"
        )
        n3_result = output.eval("ILISS_UCNL_CPSC_YN == 'Y'")

        # Cast result to boolean
        output["N1"] = n1_result.astype(bool)
        output["N2"] = n2_result.astype(bool)
        output["N3"] = n3_result.astype(bool)

        template_df.iloc[0:5] = helpers.update_values_row_wise(
            template_df.iloc[0:5],
            output[output["CSCRT_KIND_NM"].str.startswith("누적적우선주")],
            start_row=0,
        )
        template_df.iloc[5:11] = helpers.update_values_row_wise(
            template_df.iloc[5:11],
            output[output["CSCRT_KIND_NM"].str.startswith("비누적적")],
            start_row=0,
        )
        template_df.iloc[11:16] = helpers.update_values_row_wise(
            template_df.iloc[11:16],
            output[output["CSCRT_KIND_NM"].str.startswith("상환 우선주")],
            start_row=0,
        )
        template_df.iloc[16:19] = helpers.update_values_row_wise(
            template_df.iloc[16:19],
            output[output["CSCRT_KIND_NM"].str.startswith("기타")],
            start_row=0,
        )

    # Dashboard 9-12-6
    else:
        # Get data from wvr
        output = helpers.get_df(data, wvr_path, model_name)

        # Evaluate conditional expression and add result to output df as new column (N, NN)
        n1_result = output.eval(
            "CSCRT_TIER_1_CBS_USBT_YN == 'Y' & CSCRT_TIER_1_CBS_CNTA_YN == 'Y' & CSCRT_TIER_2_CBS_USBT_YN == 'Y' & CSCRT_TIER_2_CBS_CNTA_YN == 'Y'"
        )
        n2_result = output.eval(
            "CSCRT_TIER_1_CBS_OLAB_YN == 'Y' & CSCRT_TIER_1_CBS_AFOA_YN == 'Y' & CSCRT_TIER_2_CBS_OLAB_YN == 'Y' & CSCRT_TIER_2_CBS_AFOA_YN == 'Y'"
        )

        # Cast result to boolean
        output["N1"] = n1_result.astype(bool)
        output["N2"] = n2_result.astype(bool)

        # Update values in template df by applying filter as per requirement
        template_df.iloc[0:10] = helpers.update_values_row_wise(
            template_df.iloc[0:10],
            output[output["CSCRT_KIND_NM"].str.startswith("신종자본증권")],
            start_row=0,
        )
        template_df.iloc[10:25] = helpers.update_values_row_wise(
            template_df.iloc[10:25],
            output[output["CSCRT_KIND_NM"].str.startswith("후순위채무")],
            start_row=0,
        )
    # Prepare table data (data, columns, conditional_style)
    results = helpers.prepare_table_data(
        template_df, multi_index=True, show_negative_numbers=True
    )
    return results
