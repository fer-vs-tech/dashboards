#demo_ifrs17/results/subledger.py
import logging

import json
import time
import os
import pandas as pd

import cm_dashboards.utilities as utilities
import cm_dashboards.demo_ifrs17.utils.helpers as helpers
logger = logging.getLogger(__name__)


def generate_subledger_table_b (r3s_vars):
    current_path = os.path.dirname(os.path.abspath(__file__))
    current_path = os.path.dirname(current_path)
    subdir = 'templates/Subledger'
    template_file = os.path.join(current_path, subdir, 'Subledger_Table_B.json')
    local_vars = {}
    with open(template_file) as data_file:
        schema = json.load(data_file)

    for var in r3s_vars:
        local_vars[str(var.get('Variable'))] = var.get('Value')

    bba_01 = 1
    paa_01 = 1
    rebba_01 = 1
    repaa_01 = 1
    bba_02 = 1
    paa_02 = 1
    rebba_02 = 1
    repaa_02 = 1


    for record in schema:
        var_id = ""
        code = "B."
        if record['Type'] != "" and record['Variable Name'] != "" and record['Sign on source'] != "":
            if "BBA" in str(record['Type']):
                var_id = "BBA_" + str(record['Variable Name'])
            if "PAA" in str(record['Type']):
                var_id = "PAA_" + str(record['Variable Name'])
        record['Var ID'] = var_id

        record['Value'] = local_vars.get(var_id)

        opening = False
        if record['Primary'] == "Balance_Opening":
            code = code + "01."
            opening = True
        else:
            code = code + "02."
            opening = False

        if record['Type'] == "Ins_BBA":
            if opening:
                code = code + "0" + str(bba_01) +  ".BBA"
                bba_01 = bba_01 + 1
            else:
                code = code + "0" + str(bba_02) +  ".BBA"
                bba_02 = bba_02 + 1
        if record['Type'] == "Reins_BBA":
            if opening:
                code = code + "0" + str(rebba_01) +  ".ReBBA"
                rebba_01 = rebba_01 + 1
            else:
                code = code + "0" + str(rebba_02) +  ".ReBBA"
                rebba_02 = rebba_02 + 1
        if record['Type'] == "Ins_PAA":
            if opening:
                code = code + "0" + str(paa_01) +  ".PAA"
                paa_01 = paa_01 + 1
            else:
                code = code + "0" + str(paa_02) +  ".RePAA"
                paa_02 = paa_02 + 1
        if record['Type'] == "Reins_PAA":
            if opening:
                code = code + "0" + str(repaa_01) +  ".PAA"
                repaa_01 = repaa_01 + 1
            else:
                code = code + "0" + str(repaa_02) +  ".RePAA"
                repaa_02 = repaa_02 + 1

        record['RNA SubLedger Code'] = code

    df = pd.DataFrame(schema)
    logger.debug(df)
    return schema



def generate_subledger_table_a (r3s_vars):
    current_path = os.path.dirname(os.path.abspath(__file__))
    current_path = os.path.dirname(current_path)
    subdir = 'templates/Subledger'
    template_file = os.path.join(current_path, subdir, 'Subledger_Table_A.json')
    #local_vars = {}
    with open(template_file) as data_file:
        schema = json.load(data_file)

    sel_gocs = []

    first_key = next(iter(r3s_vars))
    if first_key:
        groups = r3s_vars[first_key]
        for group in groups.keys():
            if group not in sel_gocs:
                sel_gocs.append(group)

    code_build = 0
    previous_amount = {}
    previous_var_name = ""
    previous_primary = ""

    bba = rebba = paa = repaa = 0

    for record in schema:
        var_id = ""

        if str(record['Primary']) == previous_primary:
            previous_cbuild = str(code_build)
            record['CodeBuild1'] = str(code_build)
        else:
            previous_cbuild = str(code_build)
            code_build = code_build + 1
            record['CodeBuild1'] = str(code_build)

        if str(record['Type']) == "Ins_BBA":
            var_id = "BBA_" + str(record['Variable Name'])
        if str(record['Type']) == "Reins_BBA":
            var_id = "BBA_" + str(record['Variable Name'])
        if str(record['Type']) == "Reins_PAA":
            var_id = "PAA_Reins_" + str(record['Variable Name'])
        if str(record['Type']) == "Ins_PAA":
            var_id = "PAA_" + str(record['Variable Name'])

        record['Var ID'] = var_id

        if record['Var ID'] == previous_var_name:
            record['CodeBuild2'] = ".01"
            record['CR/CD'] = "DR"
        else:
            record['CodeBuild2'] = ""
            record['CR/CD'] = "CR"

        if record["Variable Name"] == "CF_Recognised_In_OCI_Part_A":
            logger.debug("DEBUGI")

        previous_var_name = var_id

        if record['CodeBuild2'] == "":
            sign = 1
        else:
            sign = -1
            #record['Value'] = local_vars.get(var_id) if local_vars.get(var_id) else {}
        #else:
        temp = {}
        if r3s_vars.get(var_id):
            vals = r3s_vars.get(var_id)
            for k in vals.keys():
                if int(vals[k]) != 0:
                    temp[k] = vals[k] * sign
                else:
                    temp[k] = 0
            record['Value'] = temp
        else:
            record['Value'] = {}

        # if record['CodeBuild2'] == "":
        #     record['Value'] = local_vars.get(var_id) if local_vars.get(var_id) else {}
        # else:
        #     record['Value'] = local_vars.get(var_id) * -1 if local_vars.get(var_id) else {}

        if record['CR/CD'] == "CR":
            record["Cr"] = record['Value']
            record["Dr"] = {}
        else: #DR
            record["Cr"] = {}
            record["Dr"] = record['Value']

        temp_values = record['Value']
        temp_amounts = {}
        for goc in sel_gocs:
            temp_amounts[goc] = 0

        for goc in sel_gocs:
            cr = record["Cr"]
            dr = record["Dr"]
            if cr.get(goc):
                temp_amounts[goc] = temp_amounts[goc] + cr.get(goc)
            if dr.get(goc):
                temp_amounts[goc] = temp_amounts[goc] + dr.get(goc)
            if previous_amount.get(goc):
                temp_amounts[goc] = temp_amounts[goc] + previous_amount.get(goc)

        previous_amount = temp_amounts

        record["Amount"] = temp_amounts

        if record['Var ID'] == "BBA_CF_Premium_Reinsurance_Total":
            logger.debug("e")

        code = "F." + ("000" + str(record['CodeBuild1']))[-2:]

        if str(record['Type']) == "Ins_BBA":
            suffix = ".BBA"
            # counter = "." + ("000" + str(bba))[-2:]
            # code = code + str(counter) + str(record['CodeBuild2']) + ".BBA"
        if str(record['Type']) == "Reins_BBA":
            suffix = ".ReBBA"
        if str(record['Type']) == "Ins_PAA":
            suffix = ".PAA"
        if str(record['Type']) == "Reins_PAA":
            suffix = ".RePAA"

        minus = 1 if str(record['CodeBuild2']) == ".01" else 0

        if (str(record['Primary']) == previous_primary or previous_primary == ""):
            if str(record['Type']) == "Ins_BBA":
                bba = bba + 1
                counter = ("000" + str(bba - minus))[-2:]
                #counter = "01"
            if str(record['Type']) == "Reins_BBA":
                rebba = rebba + 1
                counter = ("000" + str(rebba - minus))[-2:]
            if str(record['Type']) == "Ins_PAA":
                paa = paa + 1
                counter = ("000" + str(paa - minus))[-2:]
            if str(record['Type']) == "Reins_PAA":
                repaa = repaa + 1
                counter = ("000" + str(repaa - minus))[-2:]
        else:
            bba = rebba = paa = repaa = 0
            if str(record['Type']) == "Ins_BBA":
                bba = bba + 1
            if str(record['Type']) == "Reins_BBA":
                rebba = rebba + 1
            if str(record['Type']) == "Ins_PAA":
                paa = paa + 1
            if str(record['Type']) == "Reins_PAA":
                repaa = repaa + 1
            counter = "01"
            #counter = ("000" + str(1 - minus))[-2:]


        code = code + "." + counter + record['CodeBuild2'] + suffix
        record['RNA SubLedger Code'] = code

        previous_primary = str(record['Primary'])

    #df = pd.DataFrame(schema)

    #df.to_excel("C:/temp/output.xlsx")

    return schema


def generate_subledger_logic (subledger_table_a, group, primary):
    current_path = os.path.dirname(os.path.abspath(__file__))
    current_path = os.path.dirname(current_path)
    subdir = 'templates/Subledger'
    template_file = os.path.join(current_path, subdir, 'subledger_logic.json')

    selected = []

    with open(template_file) as data_file:
        schema = json.load(data_file)

    for record in schema:
        if record["Primary - Secondary"] == primary:
            variable = record.get('Variable Name')
            type = record.get('Type')
            if "BBA" in type:
                variable = "BBA_" + str(variable)
            else:
                if "Reins_PAA" in type:
                    variable = "PAA_Reins_" + str(variable)
                else:
                    variable = "PAA_" + str(variable)

            positive = subledger_table_a.get(variable)
            negative = subledger_table_a.get(variable + ".01")

            positive_values = positive.get('Value')
            negative_values = negative.get('Value')
            pos_val = positive_values.get(str(group)) if positive_values and positive_values.get(str(group)) else "0"
            neg_val = negative_values.get(str(group)) if negative_values and negative_values.get(str(group)) else "0"

            type_positve = positive.get('Secondary')
            type_negative = negative.get('Secondary')
            record[type_positve] = pos_val
            record[type_negative] = neg_val

            record["BALANCE"] = "TRUE" if int(pos_val) + int(neg_val) == 0 else "FALSE"

            selected.append({
                "Type": type,
                "Variable": variable,
                "Change in LIC": record.get("LIC") if record.get("LIC") else "",
                "Change in PVCF": record.get("PVCF") if record.get("PVCF") else "",
                "Change in RA": record.get("RA") if record.get("RA") else "",
                "Change in CSM": record.get("CSM") if record.get("CSM") else "",
                "Cash This Year (inc Inv Income)": record.get("Cash Liability") if record.get("Cash Liability") else "",
                "Ins Revenue": record.get("Revenue") if record.get("Revenue") else "",
                "Ins Serv Exp": record.get("Expenses") if record.get("Expenses") else "",
                "IFIE, less Inv Income, less other exp": record.get("Financial") if record.get("Financial") else "",
                "Change in OCI": record.get("OCI") if record.get("OCI") else "",
                "Balance": record.get("BALANCE")
                             })
            #logger.debug(record.get("LIC"))


    return selected