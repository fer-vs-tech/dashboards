#ifrs17_demo/results/prepare_results.py
import decimal
import logging

logger = logging.getLogger(__name__)

import pandas as pd
import os

replace_zero: str = None

from cm_dashboards.demo_ifrs17.config.config import cache, timeout
import cm_dashboards.demo_ifrs17.utils.db_helper as db_helper
import cm_dashboards.demo_ifrs17.utils.helpers as helpers
from decimal import *

@cache.memoize(timeout=timeout)
def get_step_dates(wvr, model_name):
    comp_db = db_helper.G_Step_Dates()
    comp_result = helpers.get_df(comp_db, wvr, model_name)
    return comp_result


@cache.memoize(timeout=timeout)
def get_variables(wvr, model_name, params, model_type, source):
    whole = None

    current_path = os.path.dirname(os.path.abspath(__file__))
    current_path = os.path.dirname(current_path)
    subdir = 'templates/Breakdowns'
    data_prepared_bdown = None

    goc_filters = helpers.filter_params_by_model(params.filter_goc, source)

    if source == "BBA":
        full_template_file = os.path.join(current_path, subdir, 'BBA_variables.json')
        field_list = helpers.build_select_list_agg(full_template_file)
        fields_grp, grpby_grp, where_grp = helpers.breakdown_query_builder(goc_filters)
    else:
        full_template_file = os.path.join(current_path, subdir, 'PAA_variables.json')
        field_list = helpers.build_select_list_agg(full_template_file)
        fields_grp, grpby_grp, where_grp = helpers.breakdown_query_builder(goc_filters)

    fields_total = "[Step Date] Step_Date, " + ','.join(field_list)
    grpby_total = "[Step Date]"
    where_total = f"[Step Date]='{params.step}'"
    comp_db_total = db_helper.G_Portfolio_Sum(fields_total, where_total, grpby_total, model_type)
    comp_result_total = helpers.get_df(comp_db_total, wvr, model_name)
    data_prepared = comp_result_total.set_index('Step_Date').T
    data_prepared = data_prepared.reset_index()
    data_prepared.columns = ["Variable", "Value"]

    #data_prepared["Value"] = np.ceil(data_prepared.Value).astype(float)
    # applying round
    # GOOD data_prepared["Value"] = data_prepared.Value.astype(float).round()
    data_prepared["Value"] = data_prepared.Value.astype(float).round(2)
    #data_prepared["Value"] = data_prepared.Value.astype(int).round()

    data_prepared.columns = ["Variable", "AGG. ALL"]

    if fields_grp:
        fields_str = "[Group_Identifier] Group_Identifier, " + ','.join(fields_grp) + "," + ','.join(field_list)
        grpby_str = "[Group_Identifier],  " + ', '.join(grpby_grp)
        where_str = f"[Step Date]='{params.step}'"
        if where_grp:
            where_str = where_str + " AND " + ' AND '.join(where_grp)
        comp_db_bdown = db_helper.G_Portfolio_Sum(fields_str, where_str, grpby_str, model_type)
        comp_result_bdown = helpers.get_df(comp_db_bdown, wvr, model_name)
        headers = ["Variable_Grp"]
        headers.extend(comp_result_bdown['Group_Identifier'])
        selected_filtered_groups = comp_result_bdown['Group_Identifier']
        # another_list = ['Group_Identifier']
        grpby_grp = list(map(lambda x: x.replace('[', '').replace(']', ''), grpby_grp))
        comp_result_bdown.drop(grpby_grp, axis=1, inplace=True)
        data_prepared_bdown = comp_result_bdown.set_index("Group_Identifier").T
        data_prepared_bdown = data_prepared_bdown.reset_index()
        data_prepared_bdown.columns = headers
        # applying round
        for item in selected_filtered_groups:
            data_prepared_bdown[item] = data_prepared_bdown[item].astype(float)
            # GOOD data_prepared_bdown[item] = data_prepared_bdown[item].astype(float).round()

    if data_prepared_bdown is not None:
        frames = [data_prepared, data_prepared_bdown]
        whole = pd.concat(frames, axis=1)
        whole.drop("Variable_Grp", axis=1, inplace=True)
    else:
        whole = data_prepared.copy()

    return whole


@cache.memoize(timeout=timeout)
def get_grouping(wvr, model_name, type):
    columns_db = db_helper.G_Portfolio_Columns()
    cols_results = helpers.get_enum_columns(columns_db, wvr, model_name)
    grouping = []
    for match in cols_results:
        options = ["Off", "Group By Value"]
        if match.endswith(" Value"):
            group_name = match.replace(" Value","")
            temp_db = db_helper.G_Portfolio_Distinct(match)
            results = helpers.get_df(temp_db, wvr, model_name)
            options.extend(results["grp"])
            element = {group_name:{"Variable_Name":str(match),
                        "Group_Values":options, "Group_Type":str(type), "Set_Value":"Off"}}
            grouping.append(element)
    return grouping


@cache.memoize(timeout=timeout)
def get_icl_by_model (wvr_files, step_date):

    comp_result_bba = None
    comp_result_paa = None
    try:
        if wvr_files.get("BBA"):
            bba = wvr_files.get("BBA")
            comp_db_bba = db_helper.G_ICL_Model_BBA(step_date)
            logger.debug(bba.get('path'))
            logger.debug(bba.get('model'))
            df_bba = helpers.get_df(comp_db_bba, bba.get('path'), bba.get('model'))
        if wvr_files.get("PAA"):
            paa = wvr_files.get("PAA")
            comp_db_paa = db_helper.G_ICL_Model_PAA(step_date)
            logger.debug(paa.get('path'))
            logger.debug(paa.get('model'))
            df_paa = helpers.get_df(comp_db_paa, paa.get('path'), paa.get('model'))

        data = []

        if df_bba is None and df_paa is None:
            return None

        if df_bba is not None and df_paa is not None:
            bba_records = df_bba.to_dict('records')
            paa_records = df_paa.to_dict('records')
            paa_ins = paa_reins = 0.0
            for record in paa_records:
                if record.get('Model_Value') == "PAA":
                    paa_ins = record.get('Totals')
                if record.get('Model_Value') == "PAA_Reins":
                    paa_reins = record.get('Totals')

            data.extend(bba_records)
            data.append({"Model_Value": "PAA", "Total_Ins": paa_ins, "Total_Reins": paa_ins, "Total_Net": paa_ins + paa_reins})
        elif df_bba is not None:
            bba_records = df_bba.to_dict('records')
            data.extend(bba_records)
        else:
            paa_records = df_bba.to_dict('records')
            paa_ins = paa_reins = 0.0
            for record in paa_records:
                if record.get('Model_Value') == "PAA":
                    paa_ins = record.get('Totals')
                if record.get('Model_Value') == "PAA_Reins":
                    paa_reins = record.get('Totals')
            data.append({"Model_Value": "PAA", "Total_Ins": paa_ins, "Total_Reins": paa_reins, "Total_Net": paa_ins + paa_reins})

        logger.debug(data)
    except Exception as e:
        logger.error("Error occurred while getting WVR path and data: {}".format(e))
        error_message = "Error occurred while getting WVR path and data: {}".format(e)
    return data
