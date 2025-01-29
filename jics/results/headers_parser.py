import logging

logger = logging.getLogger(__name__)

import cm_dashboards.jics.helpers.helpers as helpers
import cm_dashboards.utilities as utilities
from cm_dashboards.jics.config.config import cache, timeout


@cache.memoize(timeout=timeout)
def get_df(hader_name, df_output=False, template="HEADER", header=[0, 1], width=None):
    """
    Get header data based on dashboard_id
    :param output: Dataframe
    :param dashboard_id: Dashboard id (str)
    :param df_output: Return df output (bool) (default: False)
    :param template: Template name (str) (default: HEADER)
    :param header: Header rows (list) (default: [0, 1])
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable or df output
    """
    template_df = None
    try:
        template_df, _ = helpers.get_template_df(
            template, header=header, generate_header_rows=False
        )

    except Exception as error:
        raise utilities.add_exception_info(error, "Error while getting header DF")
    header_name = dict(header_name=hader_name)
    template_df = helpers.replace_header_values(template_df, header_name)
    if width is not None:
        template_df = template_df.iloc[:, 0:width]
    if df_output:
        template_df = template_df.fillna("")
        return template_df
    try:
        result = helpers.prepare_table_data(template_df, multi_index=True)
    except Exception as error:
        raise utilities.add_exception_info(error, "Error while preparing table data")

    return result
