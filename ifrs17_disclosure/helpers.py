import logging

logger = logging.getLogger(__name__)

import io
import time

import pandas as pd
from dash import dcc
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

import cm_dashboards.ifrs17_accounting.dash_utils as dash_utils


def convert_to_int(df):
    """
    Helper function to convert DF columns to int values while ignoring errors
    :param df: DF to convert
    :return df: converted DF with int values
    """
    df = df.astype(int, errors="ignore")
    return df


def get_df(handler, wvr_path, model):
    """
    Get table data from wvr
    """
    table_data_df = handler.get_wvr_data(wvr_path, model)
    return table_data_df


def prepare_dropdown_options(df):
    """
    Generate dropdown options
    """
    # Make sure that the first option is "ALL"
    options = []
    for name in df["PTFLO"]:
        option = {"label": name, "value": name}
        if option not in options:
            options.append({"label": name, "value": name})
    options.append({"label": "ALL", "value": "ALL"})
    return options


def prepare_table_data(table_data_df, header_rows=[], hidden_columns=[]):
    table_data = table_data_df.to_dict("records")
    columns = dash_utils.set_column_names(
        table_data_df.columns, precision=0, hidden_columns=hidden_columns
    )
    conditional_style = dash_utils.set_table_style(columns)
    row_style = dash_utils.set_row_style(header_rows)
    style = conditional_style + row_style
    return table_data, columns, style


def get_table_name_by_journal_type(journal_type, journal="individual"):
    """
    Get table name by journal type
    """
    tables = {
        "individual": {
            "IFRS17_BBA_Reinsurance_Movement": "I_BBA_OUT_Reinsurance",
            "IFRS17_BBA_Primary_Movement": "I_BBA_Primary",
        },
        "grouped": {
            "IFRS17_BBA_Reinsurance_Movement": "G_BBA_OUT_Reinsurance",
            "IFRS17_BBA_Primary_Movement": "G_BBA_Primary",
        },
        "aggregated": {
            "IFRS17_BBA_Reinsurance_Movement": "A_BBA_OUT_Reinsurance",
            "IFRS17_BBA_Primary_Movement": "A_BBA_Primary",
        },
    }
    result = None
    try:
        result = tables[journal][journal_type]
    except KeyError:
        pass
    logger.info(
        f"Selected journal: {journal}, type: {journal_type}, table name: {result}"
    )
    return result


def format_number(x):
    """
    Helper function to format numbers
    :param x: number to format
    :return x: formatted number
    """
    if isinstance(x, (int, float)):
        if x < 0:
            return "({:,.6f})".format(abs(x))
        else:
            return "{:,.6f}".format(x)
    else:
        return x


def convert_to_decimal(df, use_int=False):
    """
    Helper function to convert DF columns to decimal values while ignoring errors
    :param df: DF to convert
    :return df: converted DF with decimal values
    """
    if not use_int:
        df = df.applymap(format_number)
    else:
        df = df.applymap(lambda x: int(x) if isinstance(x, (int, float)) else x)
    return df


def convert_to_df(records):
    """
    Convert records to DF
    """
    df = pd.DataFrame(records)
    return df


def prepare_export_file(data, label, goc_name):
    """
    Prepare export file
    :param data: Records to export
    :param label: Label to use in the filename
    :param goc_name: GOC name to use in the filename
    :return: Export file in CSV format
    """
    df = convert_to_df(data)
    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{goc_name}_{label}_({current_time}).xlsx".replace(" ", "_")

    wb = Workbook()
    ws = wb.active

    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    # Apply color to header row
    for cell in ws["1:1"]:
        cell.font = cell.font.copy(bold=True)
        cell.border = cell.border.copy(top=None, bottom=None)

    # # Assign column widths manually
    ws.column_dimensions["A"].width = 95
    ws.column_dimensions["B"].width = 25
    ws.column_dimensions["C"].width = 25
    ws.column_dimensions["D"].width = 25
    ws.column_dimensions["E"].width = 25

    # Update sheet title
    ws.title = f"{goc_name}_{label}"

    # Save workbook to a BytesIO object
    in_mem_file = io.BytesIO()
    wb.save(in_mem_file)
    in_mem_file.seek(0)

    return dcc.send_bytes(in_mem_file.getvalue(), filename)
