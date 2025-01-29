import logging

import cm_dashboards.kics.helpers.db_helper as db_helper
import cm_dashboards.kics.helpers.helpers as helpers
from cm_dashboards.kics.app_config import KICS_NAME, cache, timeout

logger = logging.getLogger(__name__)


@cache.memoize(timeout=timeout)
def get_table_data(wvr_path, report_date, journal_code):
    """
    Get table data from df
    :param wvr_path: path to wvr file
    :param report_date: report date to filter by (2022-01-01)
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    # Initialize DB handlers
    db_handler_1 = db_helper.Sensitivity(
        journal_code, report_date=report_date, switch_query=True
    )
    db_handler_2 = db_helper.Sensitivity(
        journal_code, report_date=report_date, switch_query=False
    )

    # Adjust header indexes based on journal_code
    match journal_code:
        case "10-1-1":
            header_indexes = [0, 1, 2]
            model_names = {
                "KICS10.0_DGB_DB": {
                    "handler": db_handler_1,
                    "column_name": ("22/12월말", "22/12월말 금리 적용시", "22/12월말 금리 적용시"),
                    "needed_variables": ["AVCPT_TTL_AMT_NAST_VAL"],
                },
                "KICS10.0_DGB_DB_001": {
                    "handler": db_handler_2,
                    "column_name": ("22/12월말", "금리변동시", "+100bp"),
                    "needed_variables": ["NAST_VAL"],
                },
                "KICS10.0_DGB_DB_002": {
                    "handler": db_handler_2,
                    "column_name": ("22/12월말", "금리변동시", "-100bp"),
                    "needed_variables": ["NAST_VAL"],
                },
            }
        case "10-1-2":
            header_indexes = [0, 1]
            model_names = {
                "KICS10.0_DGB_DB": {
                    "handler": db_handler_1,
                    "needed_variables": ["CRRK_DIRTY_DDAF_AMT", "ORSK_TOT_AMT"],
                },
                "KICS10.0_DGB_DB_001": {
                    "handler": db_handler_2,
                    "column_name": ("위험액", "+100bp"),
                },
                "KICS10.0_DGB_DB_002": {
                    "handler": db_handler_2,
                    "column_name": ("위험액", "-100bp"),
                },
            }

        case "10-1-3":
            header_indexes = [0, 1]
            model_names = {
                "KICS10.0_DGB_DB_001": {
                    "handler": db_handler_2,
                    "column_name": ("생명장기손해보험위험액", "+100bp"),
                },
                "KICS10.0_DGB_DB_002": {
                    "handler": db_handler_2,
                    "column_name": ("생명장기손해보험위험액", "-100bp"),
                },
            }

        case "10-1-4":
            header_indexes = [0, 1]
            model_names = {
                "KICS10.0_DGB_DB": {
                    "handler": db_handler_2,
                    "column_name": ("시장위험액", "+100bp"),
                    "needed_variables": [
                        "STK_RSKA",
                        "PPRSKA_AMT",
                        "FRSAM_TOT_AMT",
                        "ASFC_RSKA_TOT_AMT",
                    ],
                },
            }

        case _:
            logger.error(f"Invalid journal_code: {journal_code}")
            raise ValueError(f"Invalid journal_code: {journal_code}")

    # Get template df
    template_df, _ = helpers.get_template_df(
        journal_code,
        generate_header_rows=False,
        header=header_indexes,
        kics_name=KICS_NAME,
    )

    # Get data for each model and add its results to the needed column in the template df
    common_values = dict()
    for i, (model_name, data) in enumerate(model_names.items()):
        db_handler = data["handler"]
        column_name = data.get("column_name")
        needed_variables = data.get("needed_variables")
        output = helpers.get_df(db_handler, wvr_path, model_name)
        output_as_dict = output.to_dict(orient="records")[0]
        # Save common values to use in formula cells
        if needed_variables is not None:
            for variable in needed_variables:
                # If key already exists, rename it to avoid overwriting
                key_name = variable
                if variable in common_values.keys():
                    key_name = f"{variable}_{i}"
                common_values[key_name] = output_as_dict[variable]

        # Skip replacing template values if column_name is not provided
        if column_name is None:
            continue

        # Replace template values with output values
        partial_df = template_df.loc[:, [column_name]]
        template_df.loc[:, [column_name]] = helpers.replace_template_values(
            partial_df,
            output_as_dict,
            use_applymap=True,
        )

    # Calculate formula cells using common values
    template_df = helpers.replace_template_values(template_df, common_values)

    # Prepare table data (data, columns, conditional_style)
    multi_index = True if len(header_indexes) > 1 else False
    results = helpers.prepare_table_data(
        template_df, multi_index=multi_index, show_negative_numbers=True
    )

    return results
