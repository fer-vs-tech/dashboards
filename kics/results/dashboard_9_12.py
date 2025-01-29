import logging

logger = logging.getLogger(__name__)

import cm_dashboards.kics.helpers.db_helper as db_helper
import cm_dashboards.kics.helpers.helpers as helpers
from cm_dashboards.kics.app_config import KICS_NAME, cache, timeout


@cache.memoize(timeout=timeout)
def get_table_data(
    wvr_path, model_name, report_date, dashboard_id, prepared_output=None
):
    """
    Get table data from df
    :param wvr_path: path to wvr file
    :param model_name: name of the model
    :param report_date: report date to filter by (2022-01-01)
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """

    journal_code = "9-12"  # applies to most of the dashboards
    multi_index = False
    variable_in_header = False
    generate_header_rows = False
    update_elementwise = True
    mixed_journal = False
    use_applymap = True
    show_negative_numbers = False

    # Adjust parameters according to journal code
    match dashboard_id:
        case "9-12-1" | "9-12-2":
            header = [0, 1]
            multi_index = True
            variable_in_header = True
        case "9-12-4":
            multi_index = True
            header = [0, 1, 2]
            variable_in_header = True
        case "9-12-7":
            journal_code = "9-12-7"
            multi_index = True
            mixed_journal = True
            header = [0, 1]
        case "9-12-8":
            multi_index = True
            use_applymap = False
            header = [0, 1, 2]
        case "9-12-9":
            multi_index = True
            header = [0, 1, 2]
            variable_in_header = True
        case "9-12-10" | "9-12-11" | "9-12-12":
            multi_index = True
            show_negative_numbers = True
            header = [0, 1]
            variable_in_header = True
        case _:
            header = [0]

    # Initialize DB instance
    if mixed_journal:
        table_name = helpers.get_table_name_by_journal_code(
            journal_code, journal_type="mixed"
        )
        data_ac = db_helper.Journal(
            table_name=table_name["AC"]["name"],
            select=table_name["AC"]["columns"],
            report_date=report_date,
        )
        data_kics = db_helper.Journal(
            table_name=table_name["KICS"]["name"],
            select=table_name["KICS"]["columns"],
            report_date=report_date,
        )

        # Get data from wvr
        output_ac = helpers.get_df(data_ac, wvr_path, model_name)
        output_kics = helpers.get_df(data_kics, wvr_path, model_name)

        # Convert results to dict and merge them
        output_ac = output_ac.to_dict("records")[0]
        output_kics = output_kics.to_dict("records")[0]
        output_as_dict = {**output_ac, **output_kics}

    elif prepared_output is not None:
        logger.info("Using prepared output for dashboard {}".format(dashboard_id))
        output = prepared_output
        output_as_dict = prepared_output.to_dict(orient="records")[0]
    else:
        logger.info("Using DB to retrive data for dashboard {}".format(dashboard_id))
        table_name = helpers.get_table_name_by_journal_code(journal_code)
        data = db_helper.Journal(
            table_name=table_name,
            report_date=report_date,
        )
        # Get data from wvr
        output = helpers.get_df(data, wvr_path, model_name)
        output_as_dict = output.to_dict(orient="records")[0]

    # Get template df
    template_df, header_rows = helpers.get_template_df(
        dashboard_id,
        generate_header_rows=generate_header_rows,
        header=header,
        kics_name=KICS_NAME,
    )

    # Lookup for each value cell in template df and replace it with value from output df
    if update_elementwise:
        template_df = helpers.replace_template_values(
            template_df, output_as_dict, use_applymap=use_applymap
        )
    else:
        template_df = helpers.update_values_row_wise(template_df, output, start_row=0)

    # Replace column names with values from output df
    if variable_in_header:
        template_df = helpers.replace_header_values(template_df, output_as_dict)

    # Prepare table data (data, columns, conditional_style)
    results = helpers.prepare_table_data(
        template_df,
        header_rows,
        multi_index=multi_index,
        show_negative_numbers=show_negative_numbers,
    )

    return results


@cache.memoize(timeout=timeout)
def get_prepared_common_df(wvr_path, model_name, report_date):
    """
    Get prepared common df for the dashboard
    :return: df
    """
    logger.info("Preparing common DB output")
    journal_code = "9-12"
    table_name = helpers.get_table_name_by_journal_code(journal_code)
    data = db_helper.Journal(
        table_name=table_name,
        report_date=report_date,
    )
    header_info = db_helper.Journal(
        table_name="A_RC",
        select="ISS_CP_NM, [Step Date] as Step_Date",
        report_date=report_date,
    )

    # Get data from wvr
    output = helpers.get_df(data, wvr_path, model_name)
    header_info = helpers.get_df(header_info, wvr_path, model_name)

    output = output.merge(header_info, on="Step_Date", how="left")
    return output
