import logging

import cm_dashboards.china_subledger.utils.helpers as helpers

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
        data_df = helpers.dict_to_df(data_dict)
        options = list(data_df[column_name].unique())
        if column_name == "Report_Date":
            options = sorted(options)
        label = column_name.replace("_", " ")
        result = helpers.prepare_dropdown_options(options, label)
    except Exception as e:
        logger.error(f"Error while generating dropdown options for {column_name}: {e}")
    return result
