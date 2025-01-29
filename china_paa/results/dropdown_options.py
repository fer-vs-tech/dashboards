import logging

import pandas as pd

import cm_dashboards.china_paa.utils.db_helper as db_helper
import cm_dashboards.china_paa.utils.helpers as helpers

logger = logging.getLogger(__name__)


def populate_dropdown(data_dict, column_name):
    """
    Generate dropdown options
    :param wvr_path: path to wvr file
    :param journal_name: journal name to retrive table name from (AC)
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    result = []
    try:
        data_df = dict_to_df(data_dict)
        options = list(data_df[column_name].unique())
        label = column_name.replace("_", " ")
        # Add empty option as default for optional dropdowns
        if column_name not in ["Report_Date", "Model"]:
            options.insert(0, "")
        result = helpers.prepare_dropdown_options(options, label)
    except Exception as e:
        logger.error(f"Error while generating dropdown options for {column_name}: {e}")
    return result


def fetch_controllers_data(wvr_path):
    """
    Get table data from df
    :param wvr_path: path to WVR file
    :param report_date: report date
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    journal_tables = db_helper.ControllersData()
    df = helpers.get_df(journal_tables, wvr_path, "IFRS_17_PAA")
    result = df.to_dict("records")
    return result


def dict_to_df(input_dict):
    """
    Create a dataframe from a dictionary
    :param input_dict: input dictionary
    :return: dataframe
    """
    df = pd.DataFrame(input_dict)
    return df
