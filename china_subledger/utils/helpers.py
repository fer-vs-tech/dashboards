import datetime
import logging

import numpy as np
import pandas as pd

import cm_dashboards.dash_utils as dash_utils

logger = logging.getLogger(__name__)


def get_df(handler, wvr_path, model_name="IFRS_17", replace_na=None):
    """
    Get table data from wvr
    :param handler: DB handler
    :param wvr_path: path to wvr file
    :return: DataFrame
    """
    df = handler.get_wvr_data(wvr_path, model_name)
    # Replace NaN values if provided
    if replace_na is not None:
        df = df.replace(np.nan, 0)
    return df


def prepare_dropdown_options(option_names, name="Model", default=None):
    """
    Generate dropdown options
    :param option_names: List of option names
    :return: list of dictionaries (value, label, title) for dropdown options
    """
    # logger.info("Generating dropdown options: {}".format(option_names))
    if default is not None:
        if isinstance(default, list):
            option_names = default + option_names
        else:
            option_names.insert(0, default)

    # Loop through list of option names and create a list of dropdown options
    options = []
    for option_name in option_names:
        # Flat list if it exists
        if isinstance(option_name, list):
            option_name = option_name[0]

        # Format date if flag is set
        if name == "Report date" and not isinstance(option_name, str):
            title = option_name.strftime("Report date %d-%b-%Y")
        else:
            title = f"{name} '{option_name}'"

        # Generate new option
        option = {
            "label": option_name,
            "value": option_name,
            "title": title,
        }
        options.append(option)

    # logger.info("Dropdown options for {}: {}".format(name, options))
    return options


def prepare_table_data(
    df,
    header_rows=[],
    hidden_columns=[],
    filter_column_style=None,
    additional_header=[],
    replace_zero=None,
    multi_index=False,
    show_negative_numbers=True,
):
    """
    Prepare table data
    :param df: DataFrame
    :param header_rows: list of header rows
    :param hidden_columns: list of hidden columns
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    # Check if replacement is needed
    if replace_zero is not None:
        df = df.replace({0: replace_zero})
    if multi_index:
        table_data, columns = dash_utils.set_multi_index_column_names(
            df,
            show_negative_numbers=show_negative_numbers,
        )
    else:
        table_data = df.to_dict("records")
        table_columns = df.columns
        columns = dash_utils.set_column_names(
            table_columns,
            precision=0,
            hidden_columns=hidden_columns,
            show_negative_numbers=show_negative_numbers,
            additional_header=additional_header,
        )
    conditional_style = dash_utils.set_table_style_kics(
        columns, show_negative_numbers=show_negative_numbers
    )
    row_style = dash_utils.set_row_style(header_rows)
    style = conditional_style + row_style

    if filter_column_style is not None:
        result = dash_utils.set_conditional_style_by_filtering(
            column=filter_column_style
        )
        style = style + result

    return table_data, columns, style


def apply_formatting(cell_value, lookup_dict, perform_abs=False):
    """
    Apply formatting to cell value
    :param cell_value: cell value
    :param lookup_dict: lookup dictionary
    :return: formatted cell value with replacement value if applicable
    """
    if (
        pd.isna(cell_value)
        or pd.isnull(cell_value)
        or cell_value == ""
        or isinstance(cell_value, int)
    ):
        if str(cell_value).lower() == "true":
            return str(cell_value).upper()
        return cell_value

    # Remove substring from cell value if possible
    try:
        new_value = lookup_dict.get(cell_value, cell_value)
    except Exception as e:
        logger.info("Error occurred: {}".format(e))
        new_value = cell_value

    # Cast cell value to float if possible
    if not isinstance(new_value, (int, float, datetime.date)) and new_value.isdigit():
        new_value = float(new_value)

    # logger.info("Cell value: {}, new value: {}".format(cell_value, new_value))
    return new_value if new_value != 0 else "-"


def dashboards_list() -> dict:
    """
    Return list of dashboards
    """
    return {
        "variable_mapping": {
            "label": "R3S Variable Mapping",
        },
        "event_mapping": {
            "label": "Subledger Event Mapping",
        },
        "validation_subledger": {
            "label": "Validation Subledger",
        },
    }


def dict_to_df(input_dict: dict) -> pd.DataFrame:
    """
    Create a dataframe from a dictionary
    :param input_dict: input dictionary
    :return: dataframe
    """
    return pd.DataFrame(input_dict)
