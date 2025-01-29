import logging

logger = logging.getLogger(__name__)

import numpy as np

import cm_dashboards.china_paa.utils.db_helper as db_helper
import cm_dashboards.china_paa.utils.helpers as helpers


def populate_results(named_inputs):
    """
    Get table data from df
    :param named_inputs: wvr, report_date, portfolio, grp_type, inception_year, risk_type, model_value
    :return: tuple (data, columns, conditional_style)
    """
    db_query = db_helper.GroupData(
        named_inputs.report_date,
        named_inputs.grp_type,
        named_inputs.inception_year,
        named_inputs.risk_type,
        named_inputs.portfolio,
        named_inputs.model_value,
    )
    data = helpers.get_df(db_query, named_inputs.wvr)
    data = data.select_dtypes(include=[np.number]).sum().to_frame().T
    data = data.to_dict("records")
    return data


def generate_dashboard_data(results_dict):
    """
    Generate dashboard data based on the results dictionary and dashboard id
    """
    # Initialize results dictionary and dashboard list
    results = {}
    dashboards = helpers.dashboards_list()

    # Loop through dashboards and generate data
    for dash_id, dash_data in dashboards.items():
        template = helpers.get_template_df(dash_id, header=dash_data.get("header"))
        # Replace template values with actual values
        df = helpers.replace_template_values(template, results_dict)

        # Prepare table data
        multi_index = len(dash_data.get("header")) > 1
        result = helpers.prepare_table_data(
            df, multi_index=multi_index, header_rows=dash_data.get("header_rows")
        )
        results[dash_id] = result

    return results
