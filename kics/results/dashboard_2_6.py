import cm_dashboards.kics.helpers.db_helper as db_helper
import cm_dashboards.kics.helpers.helpers as helpers
from cm_dashboards.kics.app_config import KICS_NAME, cache, timeout


@cache.memoize(timeout=timeout)
def get_table_data(wvr_path, report_date):
    """
    Get table data from df
    :param wvr_path: path to wvr file
    :param report_date: report date to filter by (2022-01-01)
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    # Get template df
    journal_code = "2-6"
    template_df, _ = helpers.get_template_df(
        journal_code, generate_header_rows=False, header=[0, 1], kics_name=KICS_NAME
    )

    # Initialize DB handlers
    db_handler_1 = db_helper.TransitionMeasure(
        report_date=report_date, switch_query=True
    )
    db_handler_2 = db_helper.TransitionMeasure(
        report_date=report_date, switch_query=False
    )

    # Define model names and handlers to use dynamically
    model_names = {
        "KICS10.0_DGB_DB": {
            "handler": db_handler_1,
            "column_name": "경과조치 적용 전 지급여력비율",
        },
        "KICS10.0_DGB_DB_TIR": {
            "handler": db_handler_2,
            "column_name": "장수위험,사업비위험,해지위험 및 대재해위험 경과조치 적용 후 지급여력비율",
        },
        "KICS10.0_DGB_DB_TER": {
            "handler": db_handler_2,
            "column_name": "주식위험 경과조치 적용 후 지급여력비율",
        },
        "KICS10.0_DGB_DB_TIR_TER": {
            "handler": db_handler_2,
            "column_name": "경과조치 적용 후 지급여력비율",
        },
    }

    # Get data for each model and add its results to the needed column in the template df
    common_values = dict()
    for model_name, data in model_names.items():
        db_handler = data["handler"]
        column_name = data["column_name"]
        output = helpers.get_df(db_handler, wvr_path, model_name)
        output_as_dict = output.to_dict(orient="records")[0]
        # Save common values for calculation of formula cells
        if model_name == "KICS10.0_DGB_DB":
            common_values = output_as_dict

        # Replace template values with output values
        partial_df = template_df.loc[:, [column_name]]
        template_df.loc[:, [column_name]] = helpers.replace_template_values(
            partial_df, output_as_dict, use_applymap=True
        )

    # Calculate formula cells
    template_df = helpers.replace_template_values(template_df, common_values)

    # Prepare table data (data, columns, conditional_style)
    results = helpers.prepare_table_data(
        template_df, multi_index=True, show_negative_numbers=True
    )

    return results
