#demo_ifrs17/config/callbacks.py
import logging

import dash
from flask import json, jsonify, render_template
import json
import time
import pandas as pd
from collections import OrderedDict

from dash import no_update
import cm_dashboards.utilities as utilities
from dash.dependencies import Input, Output, State
from cm_dashboards.demo_ifrs17.config.config import app
import cm_dashboards.demo_ifrs17.utils.helpers as helpers
import cm_dashboards.demo_ifrs17.results.prepare_results as prepare_results
import cm_dashboards.demo_ifrs17.results.prepare_components as prepare_components
import cm_dashboards.demo_ifrs17.results.bba_disclosures as bba_disclosures
import cm_dashboards.demo_ifrs17.results.paa_disclosures as paa_disclosures
import cm_dashboards.demo_ifrs17.results.subledger as subledger
import cm_dashboards.demo_ifrs17.results.common as common
import cm_dashboards.demo_ifrs17.results.dashboards as dashboards
import cm_dashboards.demo_ifrs17.results.example as example
import cm_dashboards.demo_ifrs17.utils.debugger_test as debugger_test

logger = logging.getLogger(__name__)

@app.callback(
    Output("error-toast", "is_open"),
    Input("error-toast", "children"),
    prevent_initial_call=True,
)
def show_error_message(message):
    """
    Show error message in toast if any error message is available
    :param message: Error message sent from other callbacks
    :return bool: Show/hide toast and disable/enable apply and export buttons
    """
    show_error_message = bool(message)
    return show_error_message

# 01 LOAD REPORT -> SET RESULTS PATHS RECEIVED
@app.callback(
    [
        Output("wvr_files", "data"),
        Output("menu-tabs","active_tab"),
        Output("dashboard-tabs","active_tab"),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    Input("url", "search"),
    prevent_initial_call = True
)
def load_report(url_query_string):
    """
    Get wvr path from URL parameters
    :param url_query_string: URL parameters
    :return: WVR path value
    """
    try:
        error_message = None
        params = utilities.extract_url_params(url_query_string)

        logger.debug(f"params received: {params}")

        # validate input params received.

        #not valid parameters in request
        if "jobrun" not in params and "wvr" not in params:
            error_message = "Invalid parameters found in the request: missing jobrun and wvr"
            return dash.no_update, "tab-0", "tab-1", error_message

        # mismatch between param count received
        if len(list(params['jobrun'])) != len(list(params['wvr'])):
            logger.error(f"mismatch between jobruns {len(list(params['jobrun']))} and wvrs {len(list(params['wvr']))}")
            error_message = f"mismatch between jobruns {len(list(params['jobrun']))} and wvrs {len(list(params['wvr']))}"
            return dash.no_update, "tab-0", "tab-1", error_message

        wvr_paths = utilities.get_wvr_path_from_url(url_query_string, multiple=True)

        logger.debug(f"Params mapped to files {wvr_paths}")

        # Set default WVR paths manually (for development only)
        if wvr_paths is None or len(wvr_paths) == 0:
            logger.info("Setting default WVR paths manually to default single batch results file...")

            base_path = "G:/My Drive/z_technical/SII_Reporting/R3S_IFRS_17_202310/R3S_IFRS_17/results"

            bba = f"{base_path}/IFRS_17_(Discounting)_2019_YE.wvr"
            paa = f"{base_path}/IFRS_17_PAA_2019_YE.wvr"

            # Map WVR files to dictionary for easy access in callbacks
            map_wvr_paths = {
                "BBA": { "path" : bba, "model" : "IFRS_17_(Discounting)"},
                "PAA": { "path" : paa, "model" : "IFRS_17_PAA"},
            }
        else:
            logger.info("Setting WVR path from URL parameters...")
            map_wvr_paths = helpers.set_wvr_nl_paths(wvr_paths)


    except Exception as e:
        logger.error("Error occurred while getting WVR path and data: {}".format(e))
        error_message = "Error occurred while getting WVR path and data: {}".format(e)
    logger.debug("retornando")
    logger.debug(map_wvr_paths)
    return map_wvr_paths, "tab-0", "tab-1", error_message

# 02 RESULTS PATHS RECEIVED  -> POPULATE MODELS DROPDOWNS
@app.callback(
    [
        Output("bba-model-dropdown", "options"),
        Output("bba-model-dropdown", "value"),
        Output("paa-model-dropdown", "options"),
        Output("paa-model-dropdown", "value"),
    ],
    Input("wvr_files", "data"),
)
def load_models_dropdowns (wvr_files):
    models = []
    bba = wvr_files.get('BBA')
    paa = wvr_files.get('PAA')
    bba_model = no_update
    paa_model = no_update

    if bba:
        bba_model = bba.get('model')
        models.append(bba_model)

    if paa:
        paa_model = paa.get('model')
        models.append(paa_model)

    return models, bba_model, models, paa_model


# 03 MODELS SELECTED -> LOAD & PREPARE PARAMETERS
@app.callback(
    [
        Output("steps-dropdown", "options", allow_duplicate=True),
        Output("steps-dropdown", "value", allow_duplicate=True),
        Output("params-goc-table", "data", allow_duplicate=True),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    [
     Input("bba-model-dropdown", "value"),
     Input("paa-model-dropdown", "value"),
     State("wvr_files", "data"),
     ],
    prevent_initial_call=True,
)
def prepare_parameters(bba_selected, paa_selected, wvr_files):
    error_message = None
    parameters_goc = None
    grouping_bba = []
    grouping_paa = []
    default_step = ""
    if wvr_files is None:
        error_message = "No models found or selected"
        #return no_update, no_update, parameters_goc, error_message
        return no_update, no_update, no_update, error_message

    steps = []

    if bba_selected:
        bba = wvr_files.get('BBA')
        df_steps_bba = prepare_results.get_step_dates(wvr=bba.get('path'), model_name=bba.get('model'))
        #grouping_bba = prepare_results.get_grouping(wvr=bba.get('path'), model_name=bba.get('model'), type="BBA")
        for step in df_steps_bba['Step_Date']:
            steps.append(str(step))

    if paa_selected:
        paa = wvr_files.get('PAA')
        df_steps_paa = prepare_results.get_step_dates(wvr=paa.get('path'), model_name=paa.get('model'))
        #grouping_paa = prepare_results.get_grouping(wvr=paa.get('path'), model_name=paa.get('model'), type="PAA")
        for step in df_steps_paa['Step_Date']:
            if str(step) not in steps:
                steps.append(str(step))

    steps.sort()
    if steps:
        default_step = steps[0]

    #parameters_goc = grouping_bba + grouping_paa

    #return steps, default_step, parameters_goc, error_message
    return steps, default_step, None, error_message

# 04 PARAMETERS CALCULATED -> BUILD PARAMETERS TABLE
# @app.callback(
#     Output("params-goc-table","data"),
#     [
#         Input("parameters_goc", "data"),
#         State("params-goc-table", "data"),
#     ],
#     prevent_initial_call=True,
# )
# def populate_grouping_table (parameters_goc, filtered_gocs):
#     data = None
#     if parameters_goc is None:
#         return no_update
#
#     table_data = []
#
#     for group in parameters_goc:
#         group_name = list(group.keys())[0]
#         group_details = list(group.values())[0]
#         type = group_details.get('Group_Type')
#         set_value = group_details.get('Set_Value')
#         if filtered_gocs:
#             for goc in filtered_gocs:
#                 if type == goc.get('Model') and group_name == goc.get('GoC'):
#                     set_value = goc.get('Value')
#         # if type == "PAA" and paa_filter:
#         #     for param in paa_filter:
#         #         if list(param.keys())[0] == group_name:
#         #             set_value = str(list(param.values())[0])
#
#         table_data.append({"Model": str(type), "Group": str(group_name), "Value": set_value})
#
#     return table_data

# 05 LOAD GOC OPTIONS BASED ON GOC SELECTED
# @app.callback(
#     [
#         Output('goc-options-dropdown', 'options'),
#         Output('goc-options-dropdown', 'value')
#     ],
#     [
#         Input("params-goc-table", "active_cell"),
#         State("parameters_goc", "data"),
#         State("params-goc-table", "data")
#     ],
#     prevent_initial_call=True,
# )
# def load_goc_options(active_cell, parameters_goc, goc_table):
#     if goc_table is None or active_cell is None:
#         return no_update, no_update
#
#     model_selected = goc_table[active_cell['row']]['Model']
#     group_selected = goc_table[active_cell['row']]['Group']
#     value_selected = goc_table[active_cell['row']]['Value']
#
#     logger.debug(f"model type is {model_selected} group is {group_selected} with value {value_selected}")
#
#     options = []
#
#     for goc in parameters_goc:
#         group_name = list(goc.keys())[0]
#         group_details = list(goc.values())[0]
#         if group_name == group_selected and model_selected == group_details.get('Group_Type'):
#             options = group_details.get('Group_Values')
#
#     active = value_selected if value_selected in options else ""
#
#     return options, active
#
# # 06 REFRESH GOC PARAMETERS TABLE
# @app.callback(
#         Output("params-goc-table", "data", allow_duplicate=True),
#     [
#         Input('goc-options-dropdown', 'value'),
#         Input('params-goc-table', 'active_cell'),
#         State('params-goc-table', 'data')
#     ],
#     prevent_initial_call=True,
# )
# def update_group_table (selected_value, active_cell, goc_table):
#     if selected_value is None or active_cell is None or goc_table is None:
#         return no_update
#
#     goc_table[active_cell['row']]['Value'] = selected_value
#
#     return goc_table

@app.callback([
          #Output("parameters_goc", "data", allow_duplicate=True),
          Output("params-goc-table", "data", allow_duplicate=True),
          Output("params-goc-table", "columns", allow_duplicate=True),
          Output("params-goc-table", "dropdown_conditional", allow_duplicate=True),
],
    [
        Input("modal-filters", "is_open"),
        State("wvr_files", "data"),
        State("params-goc-table", "data"),
    ],
    prevent_initial_call=True
)
def load_filters_if_not(is_open, wvr_files, parameters_goc_table):
    if not is_open or wvr_files is None:
        return no_update, no_update, no_update

    goc = []
    columns = [
                  {'id': 'model', 'name': 'Model', 'editable': False},
                  {'id': 'group', 'name': 'Group', 'editable': False},
                  {'id': 'value', 'name': 'Value', 'presentation': 'dropdown', 'editable': True}
              ]
    grouping_bba = []
    grouping_paa = []
    table_data = []

    drop_conditional = []

    if not parameters_goc_table:
        bba = wvr_files.get('BBA')
        paa = wvr_files.get('PAA')
        if bba:
            grouping_bba = prepare_results.get_grouping(wvr=bba.get('path'), model_name=bba.get('model'), type="BBA")
            for iterr in grouping_bba:
                for t in iterr.keys():
                    testo = iterr[t]
                    testo['Group_Values'] = helpers.update_type_for_options(testo['Group_Values'])

        if paa:
            grouping_paa = prepare_results.get_grouping(wvr=paa.get('path'), model_name=paa.get('model'), type="PAA")
            for iterr in grouping_paa:
                for t in iterr.keys():
                    testo = iterr[t]
                    testo['Group_Values'] = helpers.update_type_for_options(testo['Group_Values'])


        groups = grouping_bba + grouping_paa

        if groups:
            for grp in groups:
                for k in grp.keys():
                    extended_info = grp[k]
                    table_data.append({"model": extended_info['Group_Type'], "group": k, "value": "Off"})
                    options = extended_info['Group_Values']
                    test = [{'label': str(i), 'value': str(i)} for i in options]
                    drop_conditional.append({'if': {'column_id':'value',
                                          'filter_query': '{model} eq "' + extended_info['Group_Type'] + '" and {group} eq "' + k + '"'
                                          },
                                   'options': test,
                                   'clearable': False,
                    },)

        logger.debug(table_data)
        logger.debug(drop_conditional)
        #
        # if grouping_paa:
        #     for groups in grouping_paa:
        #         for k in groups.keys():
        #             table_data.append({"model":"PAA", "group": k, "value": "Off"})
    else:
        return no_update, no_update, no_update
        #table_data = parameters_goc_table



    # if filtered_gocs:
    #     for group in filtered_gocs:
    #         group_name = list(group.keys())[0]
    #         group_details = list(group.values())[0]
    #         type = group_details.get('Group_Type')
    #         set_value = group_details.get('Set_Value')
    #         # if filtered_gocs:
    #         #     for goc in filtered_gocs:
    #         #         if type == goc.get('Model') and group_name == goc.get('GoC'):
    #         #             set_value = goc.get('Value')
    #         # if type == "PAA" and paa_filter:
    #         #     for param in paa_filter:
    #         #         if list(param.keys())[0] == group_name:
    #         #             set_value = str(list(param.values())[0])
    #
    #         table_data.append({"Model": str(type), "Group": str(group_name), "Value": set_value})

    return table_data, columns, drop_conditional

# AUTO SELECT THE FIRST SUB-MENU TAB
@app.callback(
    [
        Output("variable-options-tabs", "active_tab"),
        Output("breakdown-options-tabs", "active_tab"),
        Output("disclosure-options-tabs", "active_tab")
    ],
    [
        Input("menu-tabs", "active_tab")
    ]
)
def tab_content(main_tab):
    empty = no_update
    active_tab = "tab-0"
    if main_tab is None:
        return empty, empty, empty

    if main_tab == "tab-1": #variables
        return active_tab, empty, empty
    elif main_tab == "tab-2": #breakdowns
        return empty, active_tab, empty
    elif main_tab == "tab-4": #disclosures
        return empty, empty, active_tab
    else:
        return empty, empty, empty


# 07 APPLY GOC PARAMETERS FILTER
@app.callback(
        [
            #Output("filtered_gocs", "data"),
            Output("filter-count", "children", allow_duplicate=True),
            Output ("row-filters", "children", allow_duplicate=True),
            Output("modal-filters", "is_open", allow_duplicate=True),
        ],
        [
            Input("apply-filters", "n_clicks"),
            State("modal-filters", "is_open"),
            State("params-goc-table", "data"),
        ],
        prevent_initial_call=True,
)
def update_filter_labels (apply_click, is_open, goc_table):
    if not is_open or goc_table is None:
        return no_update, no_update, no_update

    goc_filters = []
    if apply_click > 0:
        filter_count = 0
        for filter in goc_table:
            if filter.get('value') not in ["Off", None]:
                filter_count = filter_count + 1

        child = prepare_components.return_filter_indicators(goc_table)

        if not child:
            child = no_update
        # for item in goc_table:
        #     goc_filters.append({"Model": item.get('Model'), "GoC": item.get('Group'), "Value": item.get('Value')})
        # return goc_filters, False
        return filter_count, child, False
    else:
        return no_update, no_update, no_update

# 08 DISPLAY FILTERS APPLIED
# @app.callback(
#     [
#         Output("filter-count", "children", allow_duplicate=True),
#         Output ("row-filters", "children", allow_duplicate=True),
#     ],
#     [
#         Input("filtered_gocs", "data"),
#     ],
#     prevent_initial_call=True
# )
# def display_filtered_gocs (filtered_gocs):
#     filter_count = 0
#     if not filtered_gocs:
#         return str(filter_count), no_update
#
#     for filter in filtered_gocs:
#         value = filter.get('Value')
#         if value != "Off":
#             filter_count = filter_count + 1
#
#     child = prepare_components.return_filter_indicators(filtered_gocs)
#
#     if not child:
#         child = no_update
#     return str(filter_count), child

# 09 APPLY QUERY -> CALCULATE VARIABLES AND BREAKDOWNS -> READY FOR DISCLOSURES
@app.callback(
    output=[
        Output("table-r3s-bba-variables", "data"),
        Output("table-r3s-paa-variables", "data"),
        #Output("table-BS-Ins-BBA-VFA", "data"),
        Output("BS-Ins-BBA-VFA-tab", "children"),
        Output("BS-Reins-BBA-tab", "children"),
        Output("BS-Ins-PAA-tab", "children"),
        Output("BS-Reins-PAA-tab", "children"),
        Output("variables_key_value", "data"),
        Output("breakdowns_key_value", "data"),
        Output("error-toast", "children", allow_duplicate=True),
    ],
    inputs=dict(
        button_clicks=Input("apply-button", "n_clicks"),
        wvr_files=State("wvr_files", "data"),
        input_data=dict(
            bba=State("bba-model-dropdown", "value"),
            paa=State("paa-model-dropdown", "value"),
            step=State("steps-dropdown", "value"),
            filter_goc=State("params-goc-table", "data"),
        ),
    ),
    prevent_initial_call=True,
)
def prepare_variables_breakdowns(button_clicks, wvr_files, input_data):
    if button_clicks < 1:
        return None, None, None, None
    full_variables_bba = None
    full_variables_paa = None
    bba_ins_render = no_update
    bba_reins_render = no_update
    paa_ins_render = no_update
    paa_reins_render = no_update
    bd_k_v = {}
    var_k_v = None
    error_message = None
    try:
        named_inputs = utilities.convert_dict_to_namedtuple(input_data)
        bba = wvr_files.get('BBA')
        paa = wvr_files.get('PAA')

        if bba:
            bba_variables = prepare_results.get_variables(wvr=bba.get('path'), model_name=bba.get('model'), params=named_inputs, model_type=None, source="BBA")
            #full_variables_bba = bba_variables.to_dict('records')
            full_variables_bba = helpers.generate_variables_presentation(bba_variables)
            table_data_bba = bba_variables.to_dict('records')
            bba_bscode = helpers.populate_R3S_BSCode(table_data_bba, "BBA")
            bba_ins_data, groups_bba = helpers.populate_Breakdowns(bba_bscode, "BBA_Ins")
            bba_reins_data, groups_bba = helpers.populate_Breakdowns(bba_bscode, "BBA_Reins")
            # render breakdowns
            #bba_ins_render = helpers.breakdown_generate_presentation(bba_ins_data, groups_bba)
            bba_ins_render = prepare_components.breakdown_gen_presentation(bba_ins_data, groups_bba)
            #bba_reins_render = helpers.breakdown_generate_presentation(bba_reins_data, groups_bba)
            bba_reins_render = prepare_components.breakdown_gen_presentation(bba_reins_data, groups_bba)
            bd_k_v = helpers.generate_report_key_value(bba_ins_data, 'RNA BS Code', 'value', bd_k_v)
            bd_k_v = helpers.generate_report_key_value(bba_reins_data, 'RNA BS Code', 'value', bd_k_v)
        if paa:
            paa_variables = prepare_results.get_variables(wvr=paa.get('path'), model_name=paa.get('model'), params=named_inputs, model_type="PAA", source="PAA")
            paa_reins_variables = prepare_results.get_variables(wvr=paa.get('path'), model_name=paa.get('model'), params=named_inputs, model_type="PAA_Reins", source="PAA")
            var_paa_ins = helpers.generate_variables_presentation(paa_variables)
            var_paa_reins = helpers.generate_variables_presentation(paa_reins_variables)
            full_variables_paa = var_paa_ins + var_paa_reins
            #full_variables_paa = paa_variables.to_dict('records') + paa_reins_variables.to_dict('records')
            table_data_paa_ins = paa_variables.to_dict('records')
            table_data_paa_reins = paa_reins_variables.to_dict('records')
            paa_bscode = helpers.populate_R3S_BSCode(table_data_paa_ins, "PAA")
            paa_reins_bscode = helpers.populate_R3S_BSCode(table_data_paa_reins, "PAA")
            paa_ins_data, groups_paa = helpers.populate_Breakdowns(paa_bscode, "PAA_Ins")
            paa_reins_data, groups_paa = helpers.populate_Breakdowns(paa_reins_bscode, "PAA_Reins")
            # render breakdowns
            paa_ins_render = prepare_components.breakdown_gen_presentation(paa_ins_data, groups_bba)
            paa_reins_render = prepare_components.breakdown_gen_presentation(paa_reins_data, groups_bba)
            bd_k_v = helpers.generate_report_key_value(paa_ins_data, 'RNA BS Code', 'value',  bd_k_v)
            bd_k_v = helpers.generate_report_key_value(paa_reins_data, 'RNA BS Code', 'value',  bd_k_v)

        #bd_k_v = helpers.generate_breakdown_key_value (bba_ins_data, bba_reins_data, paa_ins_data, paa_reins_data)

        #breakdowns = [{"BBA_Breakdown": bba_ins_data, "BBA_Reins_Breakdown": bba_reins_data, "PAA_Breakdown": paa_ins_data, "PAA_Reins_Breakdown": paa_reins_data}]

    except Exception as e:
        logger.error("Error occurred while getting WVR path and data: {}".format(e))
        error_message = "Error occurred while getting WVR path and data: {}".format(e)

    if full_variables_bba and full_variables_paa:
        full_vars = full_variables_bba + full_variables_paa
    elif full_variables_bba:
        full_vars = full_variables_bba
    else:
        full_vars = full_variables_paa
    if full_vars:
        var_k_v = {}
        for var in full_vars:
            tempo_values = {}
            for k in var.keys():
                if k != "Variable":
                    tempo_values[k] = var[k]
            var_k_v[str(var.get('Variable'))] = tempo_values


    return full_variables_bba, full_variables_paa, bba_ins_render, bba_reins_render, paa_ins_render, paa_reins_render, var_k_v, bd_k_v, error_message


# 10 CALCULATE DISCLOSURES -> READY FOR SUMMARIES AND CHARTS
@app.callback(
    [
        Output("disclosure-ins-bba-vfa-tab", "children"),
        Output("disclosure-reins-bba-tab", "children"),
        Output("disclosure-ins-paa-tab", "children"),
        Output("disclosure-reins-paa-tab", "children"),
        Output("disclosures_key_value", "data"),
        #Output("table-net-all-debug", "data"),
        Output("disclosure-net-all-tab", "children"),
        Output("key-summ-col", "children"),
        Output("key-openings-col", "children"),
        # Output("acc-reins", "children"), #ACCORDION VERSION
        Output("error-toast", "children", allow_duplicate=True),
    ],
    [
        Input("breakdowns_key_value", "data"),
        State("table-r3s-bba-variables", "data"),
        State("table-r3s-paa-variables", "data"),
        State("variables_key_value", "data")
    ],
    prevent_initial_call=True,
)
def prepare_disclosures (breakdowns, r3s_bba_vars, r3s_paa_vars, var_k_v):
    error_message = None
    returned = no_update
    returned_reins = no_update
    returned_paa = no_update
    returned_paa_reins = no_update
    net_all = no_update
    key_summary = no_update
    key_openings = no_update
    subledger_b = no_update
    disc_k_v = {}

    try:
        if breakdowns:
            bba_gocs = helpers.get_filtered_results_groups(breakdowns, "BBA")
            #returned, disc_k_v = bba_disclosures.bba_insurance_disclosure(breakdowns, bba_gocs, disc_k_v)
            returned, disc_k_v = bba_disclosures.bba_ins_disc(breakdowns, bba_gocs, disc_k_v)
            bba_gocs = helpers.get_filtered_results_groups(breakdowns, "BBA")
            #returned_reins, disc_k_v = bba_disclosures.bba_reinsurance_disclosure(breakdowns, bba_gocs, disc_k_v)
            returned_reins, disc_k_v = bba_disclosures.bba_reins_disc(breakdowns, bba_gocs, disc_k_v)

            paa_gocs = helpers.get_filtered_results_groups(breakdowns, "PAA")
            #returned_paa, disc_k_v = paa_disclosures.paa_insurance_disclosure(breakdowns, paa_gocs, disc_k_v)
            returned_paa, disc_k_v = paa_disclosures.paa_ins_disc(breakdowns, paa_gocs, disc_k_v)
            paa_gocs = helpers.get_filtered_results_groups(breakdowns, "RePAA")
            #returned_paa_reins, disc_k_v = paa_disclosures.paa_reinsurance_disclosure(breakdowns, paa_gocs, disc_k_v)
            returned_paa_reins, disc_k_v = paa_disclosures.paa_reins_disc(breakdowns, paa_gocs, disc_k_v)


            net_all, disc_k_v = bba_disclosures.calculate_net_all(breakdowns, paa_gocs, disc_k_v)
            key_summary = prepare_components.generate_key_summary(disc_k_v)
            key_openings = prepare_components.generate_key_openings(disc_k_v)


    except Exception as e:
        logger.error("Error occurred while getting WVR path and data: {}".format(e))
        error_message = "Error occurred while getting WVR path and data: {}".format(e)

    # OLD GOOD return returned, returned_reins, returned_paa, returned_paa_reins, disc_k_v, error_message
    return returned, returned_reins, returned_paa, returned_paa_reins, disc_k_v, net_all, key_summary, key_openings, error_message

@app.callback(
    Output("subledger-table", "data"),
    [
        State("variables_key_value", "data"),
        Input("subledger-groups", "value"),
        Input("subledger-primary", "value")
    ]
)
def render_subledger_logic (var_k_v, group, primary):
    subledger_table_b_presentation = []
    skv_dict = {}
    s_logic = no_update
    if var_k_v is not None and group is not None:
        subledger_results = subledger.generate_subledger_table_a(var_k_v)
        for record in subledger_results:
            #internal k-v dictionary
            skv_dict[str(record.get('Var ID')) + str(record.get('CodeBuild2'))] = {"Value": record.get('Value'), "Primary": record.get('Primary'), "Secondary": record.get('Secondary')}
            #presentation
            dr = record.get("Dr")
            dr_value = dr.get(str(group)) if dr and dr.get(str(group)) else ""
            cr = record.get("Cr")
            cr_value = cr.get(str(group)) if cr and cr.get(str(group)) else ""
            amount = record.get("Amount")
            subledger_table_b_presentation.append({"Var ID": record.get('Var ID'), "RNA SubLedger Code": record.get('RNA SubLedger Code'),
                                "Dr": dr_value, "Cr" : cr_value,
                                "Amount": amount.get(str(group)) if amount.get(str(group)) else ""})
        if skv_dict and group and primary:
            s_logic = subledger.generate_subledger_logic(skv_dict, group, primary)

    #return subledger_table_b_presentation
    return s_logic

# 11 POPUATE GOC DROPDOWNS BASED ON BREAKDOWNS
@app.callback(
    [
        Output("summary-groups", "options"),
        Output("summary-groups", "value"),
        Output("subledger-groups", "options"),
        Output("subledger-groups", "value"),
    ],
    Input("breakdowns_key_value", "data")
)
def pupulate_goc_combos (breakdowns):
    unified_list = []
    if breakdowns:
        bba_gocs = helpers.get_filtered_results_groups(breakdowns, "BBA")
        if bba_gocs:
            for goc in bba_gocs:
                if goc not in unified_list:
                    unified_list.append(goc)
        paa_gocs = helpers.get_filtered_results_groups(breakdowns, "PAA")
        if paa_gocs:
            for goc in paa_gocs:
                if goc not in unified_list:
                    unified_list.append(goc)
        paa_reins_gocs = helpers.get_filtered_results_groups(breakdowns, "RePAA")
        if paa_reins_gocs:
            for goc in paa_reins_gocs:
                if goc not in unified_list:
                    unified_list.append(goc)

        return unified_list, unified_list[0], unified_list, unified_list[0]
    else:
        return no_update, no_update, no_update, no_update

# 12 CALCULATE AND RENDER SUMMARIES BASED ON BREAKDOWNS + DISCLOSURES
@app.callback(
        Output("summary-bs-container", "children"),
    [
        State("breakdowns_key_value", "data"),
        State("disclosures_key_value", "data"),
        Input("summary-options", "value"),
        Input("summary-groups", "value"),
]
)
def render_bs_summaries (breakdowns, disclosures, option, group):
    compo = []

    if not breakdowns:
        return no_update

    bs_gmm = common.generate_bs_summary(breakdowns, "BS_GMM", option, group)
    bs_paa = common.generate_bs_summary(breakdowns, "BS_PAA", option, group)
    rec_a = common.generate_bs_summary(disclosures, "REC_A", option, group)
    rec_b = common.generate_bs_summary(disclosures, "REC_B", option, group)

    compo.extend(prepare_components.generate_bs_summary(bs_gmm, "Balance Sheet Under GMM/VFA"))
    compo.extend(prepare_components.generate_bs_summary(bs_paa, "Balance Sheet Under PAA"))
    compo.extend(prepare_components.generate_bs_summary(rec_a, "Reconciliation A: LRC & LIC for Insurance Contracts"))
    compo.extend(prepare_components.generate_bs_summary(rec_b, "Reconciliation B: Components of Insurance Contracts (under GMM/VFA)"))

    return compo

# 12 CALCULATE AND RENDER CHARTS BASED ON BREAKDOWNS + DISCLOSURES
@app.callback(
    [
        Output("first-pie-icl", "figure"),
        Output("second-pie-icl", "figure"),
        Output("third-pie-icl", "figure"),
    ],
    [
        State("breakdowns_key_value", "data"),
        State("wvr_files", "data"),
        State("steps-dropdown", "value"),
        Input("dashboards-options", "value"),
        Input("first-chart-slider", "value"),
        Input("second-chart-slider", "value"),
        Input("third-chart-slider", "value"),
]
)
def render_pie_charts(bdowns, wvr_files, step_date, type, size_first, size_second, size_third):

    if wvr_files is None or step_date is None:
        return no_update, no_update, no_update

    if size_first is None:
        size_first_w = size_first_h = 200
    else:
        size_first_w = size_first_h = size_first
    if size_second is None:
        size_second_w = size_second_h = 200
    else:
        size_second_w = size_second_h = size_second
    if size_third is None:
        size_third_w = size_third_h = 200
    else:
        size_third_w = size_third_h = size_third

    figurina = example.get_charts(wvr_files, step_date, size_first_w, size_first_h, "Total_Ins")

    if bdowns and type:
        test, chart_first = dashboards.generate_pie_chart("ICL", bdowns, type, size_first_w, size_first_h)
        test, chart_second = dashboards.generate_pie_chart("ICL", bdowns, type, size_second_w, size_second_h)
        test, chart_third = dashboards.generate_pie_chart("ICL", bdowns, type, size_third_w, size_third_h)
        return figurina, chart_second, chart_third
    else:
        return no_update, no_update, no_update


def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("modal-filters", "is_open", allow_duplicate=True),
    Input("btn-filters", "n_clicks"),
    State("modal-filters", "is_open"),
    prevent_initial_call=True,
)
def show_modal_filters(click, is_open):
    if click > 0:
        return not is_open

# app.callback(
#         Output("modal-filters", "is_open"),
#     [
#         Input("group-switch", "value"),
#         Input("apply-filters", "n_clicks"),
#     ],
#     [State("modal-filters", "is_open")],
#     prevent_initial_call=True,
# )(toggle_modal)







# # @server.route('/dash/ifrs17')
# # def index():
# #     messages = [{'title': 'Message One',
# #                  'content': 'Message One Content'},
# #                 {'title': 'Message Two',
# #                  'content': 'Message Two Content'}
# #                 ]
# #     return render_template('"../templates/ifrs17_templates/index.html', messages=messages)
# #
# @app.callback(
#     #Output("body-container", "children", allow_duplicate=True),
#     [
#     Output("table_variables", "data", allow_duplicate=True),
#     Output("table_variables", "columns", allow_duplicate=True),
#     Output("dropdown_per_row", "data", allow_duplicate=True)
#     ],
#     Input("url", "search"),
#     prevent_initial_call = True
# )
# def render_json(url_query_string):
#     try:
#
#         df_per_row_dropdown = pd.DataFrame(OrderedDict([
#             ('City', ['NYC', 'Montreal', 'Los Angeles']),
#             ('Neighborhood', ['Brooklyn', 'Mile End', 'Venice']),
#             ('Temperature (F)', [70, 60, 90]),
#         ]))
#
#         data = {
#             "2021|ANNTY|NP_Annuity|No|BBA": ["2021|TERM|NP_CIC|No|BBA", "2021|TERM|NP_TA|No|BBA", "2021|UL_End|Universal_Life|No|BBA_Effective_Yield", "2021|UWP|UWP|No|VFA",
#                                              "2021|WP_END|WP_End_New|No|VFA", "2021|WP_END|WP_LCEndow|No|VFA", "2021|WP_END|WP_WoL|No|VFA"],
#             "274.5964557": ["1267.090027", "1013.631535", "1668.827183", "2702.499754", "961.7139228", "1145.536137", "957.969174"],
#             "-3894307.463": ["-2235401.951", "-884189.0796", "-802065.986", "250386.2991", "200827.8556", "-320153.2487", "74428.85644"],
#             "-3627125.521": ["-1992113.658", "-766104.3568", "-728937.6132", "250779.8327", "199533.6508", "-263986.7108", "93958.56945"]
#         }
#
#         df = pd.DataFrame(data)
#
#         df.columns= ['Group', 'Amortized_DAC', 'Cash_Balance', 'Cash_Balance_Opening']
#
#         df2 = df.set_index('Group').T
#         df2[''] = df2.index
#         logger.debug(df2)
#
#         bba_variables = helpers.bba_build_select_list('C:/RnA/development/Reports/Disclosure_Std/BBA_variables.json')
#
#         # for item in bba_variables:
#         #     logger.debug(item)
#
#
#         return df2.to_dict('records'), [{"name": i, "id": i} for i in df2.columns], df_per_row_dropdown.to_dict('records')
#
#
#         # #logger.error("query string {]".format(url_query_string))
#         # logger.debug("query string")
#         # with open('c:/temp/variables.json', 'r') as myfile:
#         #     data = json.load(myfile)
#         #
#         # df = pd.json_normalize(data)
#         # df.drop("field_type", axis=1, inplace=True)
#         #
#         # return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], df_per_row_dropdown.to_dict('records')
#         #
#         # ret = ""
#         # for item_list in data:
#         #     logger.debug(item_list["name"])
#         #     ret = ret + str(item_list["name"]) + " "
#         #     # for key in item_list:
#         #     #     logger.debug(key)
#         #     #     logger.debug(item_list[key])
#         #     #logger.debug("The key and value are ({}) = ({})".format(key, value))
#         #
#         #
#         #
#         # return ret
#         # #return render_template('templates/index.html', messages=messages)
#     except Exception as e:
#         logger.error("Error while loading json: {}".format(e))
#
#     return no_update