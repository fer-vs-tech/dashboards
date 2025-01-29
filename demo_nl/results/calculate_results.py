#nl/results/calculate_results.py

import logging

logger = logging.getLogger(__name__)

import numpy as np

import cm_dashboards.demo_nl.utils.db_helper as db_helper
import cm_dashboards.demo_nl.utils.helpers as helpers
import cm_dashboards.demo_nl.results.prepare_data as prepare_data
import cm_dashboards.demo_nl.layout.layout as layout

def populate_runoff (inputs, wvr_files):
    calc_results = {}
    try:
        wvr = wvr_files[inputs.model.lower()]
        df_data = prepare_data.get_triangleData(wvr, inputs.model.lower(), inputs.program, inputs.portfolio, inputs.method,
                                                inputs.component, inputs.reporting, inputs.dev, inputs.orig)
        force = None
        # force is triangle size limited, no matter if there are values
        # force [dev max, orig max]
        if inputs.component in (["Tri_Paid_Claims", "Tri_Case_Reserves", "Tri_Claim_Costs"]):
            force = [df_data["Dev_Period_Position"].max(), df_data["Origin_Period_Position"].max()]

        # FORMAT DATAFRAME TRIANGLE LIKE
        df_triangle = helpers.convert_df_to_triangle(df_data, ['Origin_Period_Position'], ['Dev_Period_Position'], ['returnValue'], force)

        columni = []
        for i in range(1, len(df_triangle.columns) + 1):
            columni.append(f"Dev {i}")
        df_triangle.columns = columni
        df_triangle.insert(0, 'Origin', range(1, len(df_triangle) + 1))

        calc_results = df_triangle.to_dict('records')
        df = df_data[df_data.returnValue.notnull()]

        data_table = layout.render_datatable(calc_results)
        chart = layout.render_chart(df)

    except Exception as e:
        error_message = f"Error occured while generating dashboard data: {e}"
        logger.error(error_message)

    return data_table, chart


def populate_ata_post (inputs, wvr_files, component):
    calc_results = {}
    try:
        wvr = wvr_files[inputs.model.lower()]
        if component == "post-data-analysis":
            df_stats = prepare_data.get_ATA_Post_Stats_Data(wvr, inputs.model.lower(), inputs.program, inputs.portfolio, inputs.method,
                                                    inputs.reporting, inputs.dev, inputs.orig)

            df_ratios = prepare_data.get_ATA_Post_LinkRatios_Data(wvr, inputs.model.lower(), inputs.program, inputs.portfolio, inputs.method,
                                                    inputs.reporting, inputs.dev, inputs.orig)
        else:
            df_stats = prepare_data.get_ATA_Pre_Stats_Data(wvr, inputs.model.lower(), inputs.program, inputs.portfolio, inputs.method,
                                                            inputs.reporting, inputs.dev, inputs.orig)

            df_ratios = prepare_data.get_ATA_Pre_LinkRatios_Data(wvr, inputs.model.lower(), inputs.program, inputs.portfolio, inputs.method,
                                                                  inputs.reporting, inputs.dev, inputs.orig)

        force = [df_ratios["Dev_Period_Position"].max(), df_ratios["Origin_Period_Position"].max()]

        df_triangle_ratios = helpers.convert_df_to_triangle(df_ratios, ['Origin_Period_Position'], ['Dev_Period_Position'], ['returnValue'], force)

        ratios_columns = []
        for i in range(1, len(df_triangle_ratios.columns) + 1):
            ratios_columns.append(f"Dev {i}")
        df_triangle_ratios.columns = ratios_columns
        df_triangle_ratios.insert(0, 'Origin', range(1, len(df_triangle_ratios) + 1))

        triangle_results = df_triangle_ratios.to_dict('records')

        #chart = layout.render_chart(df)

        df_data = df_stats.drop(columns=["Origin_Period_Position"], axis=1)
        df_table = df_data.transpose()
        if component == "post-data-analysis":
            df_table.insert(0, "Stats (Post-Outlier)", df_table.index)
            columns = ["Stats (Post-Outlier)"]
        else:
            df_table.insert(0, "Stats (Pre-Outlier)", df_table.index)
            columns = ["Stats (Pre-Outlier)"]
        df_table = df_table.iloc[1:]
        #columns = ["Stats (Post)"]
        for x in range(1, len(df_table.columns)):
            columns.append(f"Dev Year {df_table.columns[x]}")

        df_table.columns = columns

        calc_results = df_table.to_dict('records')
        # df = df_data[df_data.returnValue.notnull()]

        data_table = layout.render_datatable(triangle_results)
        data_table_stats = layout.render_datatable(calc_results)
        data_table.append(data_table_stats[0])

        #chart = layout.render_chart_ata(df)
        #df_chart = df_ratios[df_ratios.returnValue.notnull()]
        chart = layout.render_chart(df_ratios)

    except Exception as e:
        error_message = f"Error occured while generating dashboard data: {e}"
        logger.error(error_message)

    return data_table, chart


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
