import logging

logger = logging.getLogger(__name__)

import cm_dashboards.jics.helpers.db_helper as db_helper
import cm_dashboards.jics.helpers.helpers as helpers
import cm_dashboards.utilities as utilities
from cm_dashboards.jics.config.config import cache, timeout


@cache.memoize(timeout=timeout)
def get_common_output(wvr_path, model_name, report_date, journal_code, as_dict=False):
    table_name = helpers.get_table_name_by_journal_code(journal_code)
    data = db_helper.Journal(table_name=table_name, report_date=report_date)
    output = helpers.get_df(data, wvr_path, model_name)
    if output.empty:
        logger.error("Output is empty")
    if as_dict:
        output = output.to_dict(orient="records")[0]
    return output


@cache.memoize(timeout=timeout)
def generate_df(output, dashboard_id):
    """
    Generate df for dashboard based on dashboard_id
    :param output: Dictionary with output values (dict)
    :param dashboard_id: Dashboard id (str)
    :return: DataFrame and list of header row ids (tuple)
    """
    # logger.info(f"Getting data for dashboard: {dashboard_id}")
    header = [0, 1]
    generate_header_rows = True
    variable_in_header = False
    numeric_format = False
    match dashboard_id:
        case "T5" | "T44":
            generate_header_rows = False

        case "T9" | "T12" | "T13" | "T29" | "T30" | "T59" | "T61":
            header = [0, 1, 2]

        case "T9-2" | "T9-3" | "T9-4" | "T9-5":
            header = [0]
            variable_in_header = True
            numeric_format = True

        case "T10":
            header = [0, 1, 2]
            generate_header_rows = False

        case "T42" | "T43" | "T45" | "T46":
            header = [0, 1, 2]

        case "T50" | "T51":
            header = [0, 1, 2]
            variable_in_header = True

        case "T52" | "T53" | "T54" | "T55" | "T56":
            variable_in_header = True

        case "T60":
            header = [0, 1, 2]
            generate_header_rows = False

        case "T64":
            header = [0, 1, 2]
            generate_header_rows = False
            variable_in_header = True
            numeric_format = True

        case "T66":
            header = [0, 1, 2]
            generate_header_rows = False
            variable_in_header = True
            numeric_format = True

        case (
            "T77"
            | "T80"
            | "T82"
            | "T68"
            | "T69"
            | "T70"
            | "T71"
            | "T72"
            | "T73"
            | "T74"
        ):
            generate_header_rows = False

        case "T25":
            header = [0]
            generate_header_rows = False

        case "T26":
            header = [0, 1, 2]
            generate_header_rows = False

        case "T27":
            header = [0, 1, 2, 3, 4]
            generate_header_rows = False
            variable_in_header = True

        case "T28":
            header = [0, 1, 2, 3]
            generate_header_rows = False

        case "T65":
            header = [0, 1, 2, 3]
            generate_header_rows = False
            variable_in_header = True
            numeric_format = True

        case "T67":
            header = [0, 1, 2]
            variable_in_header = True

        case "T79":
            generate_header_rows = False

        case "T84" | "T85":
            header = [0, 1]
            generate_header_rows = False

        case "T86" | "T87":
            header = [0, 1, 2]

        case _:
            pass
    try:
        template_df, header_rows = helpers.get_template_df(
            dashboard_id, header=header, generate_header_rows=generate_header_rows
        )
    except Exception as error:
        raise utilities.add_exception_info(error, "Error while getting template df")
    try:
        template_df = helpers.replace_template_values(
            template_df, output, perform_abs=False
        )
        if variable_in_header:
            template_df = helpers.replace_header_values(
                template_df, output, numeric_format=numeric_format
            )
    except Exception as error:
        raise utilities.add_exception_info(
            error, "Error while replacing template values"
        )
    template_df = template_df.fillna("")
    return template_df, header_rows


@cache.memoize(timeout=timeout)
def prepare_table_data(template_df, header_rows):
    """
    Get table data from df
    :param output: Dataframe
    :param dashboard_id: Dashboard id (str)
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    try:
        result = helpers.prepare_table_data(
            template_df, multi_index=True, header_rows=header_rows
        )
    except Exception as error:
        raise utilities.add_exception_info(error, "Error while preparing table data")
    return result
