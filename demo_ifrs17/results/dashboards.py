#demo_ifrs17/results/dashboards.py
import logging

import json
import os
import pandas as pd

import cm_dashboards.demo_ifrs17.results.prepare_components as prepare_components
logger = logging.getLogger(__name__)


def generate_pie_chart (pie, dictionary, type, w, h):
    results = []
    if dictionary is None:
        return None

    current_path = os.path.dirname(os.path.abspath(__file__))
    current_path = os.path.dirname(current_path)

    if pie == "ICL":
        template_file = 'chart_pie_icl.json'
        subdir = 'templates/Charts'
    elif pie == "BS_PAA":
        template_file = 'chart_pie_icl.json'
        subdir = 'templates/Charts'
    else:
        template_file = ""

    if template_file == "":
        return None

    full_template_file = os.path.join(current_path, subdir, template_file)

    with open(full_template_file) as data_file:
        schema = json.load(data_file)

    for record in schema:
        model = record.get('Model')
        final_value = 0
        for key in record.keys():
            if key == type:
                references = record.get(key)
                ref_list = references.split("|")
                for ref in ref_list:
                    if key == "Net Position":
                        value = dictionary.get(ref)
                        if str(model).lower() == "paa":
                            final_value = final_value + value['AGG. ALL']
                        else:
                            for k in value.keys():
                                if str(model).lower() in str(k).lower():
                                    final_value = final_value + value[k]
                    elif key == "Reinsurance":
                        value = dictionary.get(ref)
                        if str(model).lower() == "paa":
                            final_value = final_value + value['AGG. ALL']
                        else:
                            for k in value.keys():
                                if str(model).lower() in str(k).lower() and str(ref).startswith("Re"):
                                   final_value = final_value + value[k]
                    else: # insurance
                        value = dictionary.get(ref)
                        if str(model).lower() == "paa":
                            final_value = final_value + value['AGG. ALL']
                        else:
                            for k in value.keys():
                                if str(model).lower() in str(k).lower() and not str(ref).startswith("Re"):
                                   final_value = final_value + value[k]
        record['Value'] = final_value

    df_data = pd.DataFrame(schema)
    # Create chart and table data
    values, names = ("Value", "Model")
    cdm = {'BBA': 'lightcyan','BBA_Eff_Yield': 'cyan','BBA_Credit_Rate': 'royalblue','VFA': 'orange','PAA': 'darkblue'}
    color_discrete_map = ['royalblue', 'cyan', 'darkblue', 'gray', 'orange']
    chart = prepare_components.create_pie_chart(
        df = df_data,
        values=values,
        names=names,
        color_schema=color_discrete_map,
        size_width = w,
        size_height = w,
    )

    return schema, chart