import warnings

# Suppress warnings from pandas
warnings.simplefilter(action="ignore", category=Warning)

from cm_dashboards.demo_ifrs17.utils.abstract_handler import GenericHandler
import cm_dashboards.wvr_data.wvr_functions as wvr_functions
import pandas as pd
from timeit import default_timer as timer
import json
import logging
import os
import ast
import numpy as np
import math

logger = logging.getLogger(__name__)


def bba_build_select_list (json_path):
    bba_variables = []
    with open(json_path) as data_file:
        data = json.load(data_file)
        for v in data:
            bba_variables.append("[" + v['Output Variables Name'] + "] as [" + v['Var ID'] + "]")
    return bba_variables


def build_select_list_agg (json_path):
    bba_variables = []
    with open(json_path) as data_file:
        data = json.load(data_file)
        for v in data:
            bba_variables.append("SUM([" + v['Output Variables Name'] + "]) as [" + v['Var ID'] + "]")
    return bba_variables

def get_enum_columns (self, wvr_path, model):
    """
    Get R3S data from wvr
    """
    # Check if DF already exists
    query = self.get_db_query()
    connect_string = wvr_functions.get_wvr_connection_url(wvr_path, model)
    # logger.info("Connect string: {}".format(connect_string))
    con = wvr_functions.get_connection(connect_string)

    start_query = timer()
    df = pd.read_sql(query, con)
    end_query = timer()
    logger.info(
        "Query for {0} execution took {1}s".format(model, end_query - start_query)
    )
    con.close()
    # Add extra calculated columns
    df = self.set_df(df)
    columns = []
    for item in df.columns:
        columns.append(item)

    return columns


def get_df(handler: GenericHandler, wvr_path: str, model_name: str) -> pd.DataFrame:
    """
    Get table data from wvr
    :param handler: DB handler
    :param wvr_path: path to wvr file
    :return: DataFrame
    """
    df = handler.get_wvr_data(wvr_path, model_name)
    return df


def get_wvr_data(self, wvr_path, model):
    """
    Get R3S data from wvr
    """
    # Check if DF already exists
    query = self.get_db_query()
    connect_string = wvr_functions.get_wvr_connection_url(wvr_path, model)
    # logger.info("Connect string: {}".format(connect_string))
    con = wvr_functions.get_connection(connect_string)

    start_query = timer()
    df = pd.read_sql(query, con)
    end_query = timer()
    logger.info(
        "Query for {0} execution took {1}s".format(model, end_query - start_query)
    )
    con.close()
    # Add extra calculated columns
    df = self.set_df(df)
    return df


def generate_variables_presentation (variables):
    results = []
    groups = list(variables.columns)
    groups.remove("Variable")
    groups.remove("AGG. ALL")
    if len (groups) > 0:
        variables["Total_Filter"] = 0
        for group in groups:
            variables["Total_Filter"] = variables["Total_Filter"] + variables[group]

    if "Total_Filter" in variables.columns:
        new_cols = ["Variable", "AGG. ALL", "Total_Filter"]
        for group in groups:
            new_cols.append(group)
        variables = variables.reindex(columns=new_cols)

    local = variables.to_dict('records')

    return local

# maps r3s output bba.vfa results to var - bscode
def populate_R3S_BSCode (data_r3s, data_type):
    mydict = {}
    for var in data_r3s:
        mydict[var['Variable']] = None
        valdict ={}
        for k in var.keys():
            if k != "Variable":
                valdict[k] = var[k]
        mydict[var['Variable']] = valdict

    current_path = os.path.dirname(os.path.abspath(__file__))
    current_path = os.path.dirname(current_path)
    subdir = 'templates/Breakdowns'

    if data_type == "BBA":
        file_template = os.path.join(current_path, subdir, 'BBA_BSCode.json')
    else:
        file_template = os.path.join(current_path, subdir, 'PAA_BSCode.json')

    with open(file_template) as data_file:
        data = json.load(data_file)
        for variable_record in data:
            if variable_record['Var ID'] in mydict.keys():
                di = mydict[variable_record['Var ID']]
                di['RNA_BS_Code'] = variable_record['RNA BS Code']
                di['Var_ID'] = variable_record['Var ID']
                mydict[variable_record['Var ID']] = di
    return mydict

# calculate var - bscode to breakdown outputs
def populate_Breakdowns (r3s_bscode, data_type):
    first_value = next(iter(r3s_bscode.values()), None)
    keys = first_value.keys()
    master_groups = []
    empty_dict_value = {}
    current_path = os.path.dirname(os.path.abspath(__file__))
    current_path = os.path.dirname(current_path)
    subdir = 'templates/Breakdowns'
    for group in keys:
        if group not in ["RNA_BS_Code", "Var_ID"]:
            if len(master_groups) == 1: #already agg.all but still iterating, so added filtered groups total
                master_groups.append("Total_Filter")
                empty_dict_value["Total_Filter"] = ""
            master_groups.append(group)
            empty_dict_value[str(group)] = ""
    #df_results = pd.DataFrame(r3s_bscode)
    miracle_df = pd.DataFrame.from_dict(r3s_bscode, orient='index')
    #df_results.columns = ["Var_ID", "RNA_BS_Code", "Value"]

    filtered_groups = list(miracle_df.columns)
    filtered_groups.remove("AGG. ALL")
    filtered_groups.remove("RNA_BS_Code")
    filtered_groups.remove("Var_ID")

    if len(filtered_groups) > 0:
        miracle_df["Total_Filter"] = 0
        for item in filtered_groups:
            miracle_df["Total_Filter"] = miracle_df["Total_Filter"] + miracle_df[item]

    if data_type == "BBA_Ins":
        template_file = 'BBA_Ins.json'
    elif data_type == "BBA_Reins":
        template_file = 'BBA_Reins.json'
    elif data_type == "PAA_Ins":
        template_file = 'PAA_Ins.json'
    elif data_type == "PAA_Reins":
        template_file = 'PAA_Reins.json'
    else:
        return None, None

    full_template_file = os.path.join(current_path, subdir, template_file)

    with open(full_template_file) as data_file:
        data = json.load(data_file)

    for variable_record in data:
        if variable_record['Source'] == 'R3S' and variable_record['Sign on Source'] != '':
            lookup_value = str(variable_record['RNA BS Code'])
            #res = miracle_df.loc[miracle_df["RNA_BS_Code"] == lookup_value, 'Value'].sum()
            support_dict = {}
            for group in master_groups:
                #if group not in ["RNA_BS_Code", "Var_ID"]:
                result = miracle_df.loc[miracle_df["RNA_BS_Code"] == lookup_value, group].sum()
                # GOOD support_dict[group] = int(result * int(variable_record['Sign on Source']))
                support_dict[group] = round(float(result * float(variable_record['Sign on Source'])))
            variable_record['value'] = support_dict
            #result = df_results.loc[df_results["RNA_BS_Code"] == str(variable_record['RNA BS Code']), 'Value'].sum()
            #variable_record['value'] = int(result * int(variable_record['Sign on Source']))
        if variable_record['Source'] == "":
            variable_record['value'] = empty_dict_value


    data = breakdown_calculate_ref_variables(data)

    return data, master_groups



def breakdown_generate_presentation (data, master_groups):
    presentation = []

    for record in data:
        line = {"BS Code": record['RNA BS Code'], "Item": record['description']}
        dict = record['value']
        if dict:
            for key in dict.keys():
                #new_key = "AGG. ALL" if key == "Value" else key
                if dict[key] != "":
                    line[key] = math.trunc(dict[key])
                else:
                    line[key] = ""
                #multiplier = 10 ** 2
                #line[key] = int(dict[key] * multiplier) / multiplier
                # line[key] = math.trunc(dict[key])
                # GOOD line[key] = dict[key]
        else:
            for group in master_groups:
                line[group] = "-"
        presentation.append(line)
    return presentation

def disclosure_generate_presentation (data, master_groups):
    presentation = []

    for record in data:
        line = {"Record_Type": record['Record_Type'], "RNA Disc Code": record['RNA_Disc_Code'], "Item": record['Description']}
        dict = record['Value']
        if dict and dict!='0':
            for key in dict.keys():
                line[key] = dict[key]
        else:
            for group in master_groups:
                line[group] = "-"
        presentation.append(line)
    return presentation

def breakdown_calculate_ref_variables (data):
    x = 0
    while x < 3:
        for record in data:
            if record['Source'] == 'REF':
                lookup_value = record['RNA BS Code']
                if lookup_value != "":
                    valor = {}
                    for aux in data:
                        if aux['Ref Item'] == lookup_value:
                            temp = aux['value']
                            if temp is not None:
                                for k in temp.keys():
                                    if k in valor.keys():
                                        valor[k] = float(temp[k]) + float(valor[k])
                                    else:
                                        valor[k] = int(temp[k])
                        if aux['Ref Item'] == "(-)" + str(lookup_value):
                            temp_neg = aux['value']
                            if temp_neg is not None:
                                for k in temp_neg.keys():
                                    if k in valor.keys():
                                        valor[k] = float(valor[k]) - float(temp_neg[k])
                                    else:
                                        valor[k] = 0 - float(temp_neg[k])
                    record['value'] = valor
        x = x + 1
    return data

def calc_ref (row, data_df):
    try:
        if row['Source'] == 'REF':
            # result = data_df.loc[data_df['Ref Item'] == str(row['RNA BS Code']), 'value'].sum()
            result = data_df.loc[data_df['Ref Item'] == str(row['RNA BS Code']), 'value']
            result_neg = data_df.loc[data_df['Ref Item'] == "(-)" + str(row['RNA BS Code']), 'value']
            # result_neg = data_df.loc[data_df['Ref Item'] == "(-)" + str(row['RNA BS Code']), 'value'].sum()
            #res = ast.literal_eval(str(result))
            res1 = result.iloc[0]
            res2 = result_neg.iloc[0]
            for k in res1.keys():
                res1[k] = int(res1[k]) - res2[k]
            return [res1]
        else:
            return row['value']
    except Exception as e:
        logger.error("Error!!: {}".format(e))

def get_disclosure_template (section):
    template_file = ""
    #BBA INS
    #template_file = os.path.join(current_path, "templates", template_file)
    current_path = os.path.dirname(os.path.abspath(__file__))
    current_path = os.path.dirname(current_path)
    if section == "B_SUB_BBA":
        template_file = 'BBA_Reconciliation_B_Sections.json'
        subdir = 'templates/Disclosures/BBA/Ins'
    elif section == "ICL_B_BBA":
        template_file = 'BBA_Disc_Insurance_Contract_Liability_B.json'
        subdir = 'templates/Disclosures/BBA/Ins'
    elif section == "A_SUB_BBA":
        template_file = 'BBA_Reconciliation_A_Sections.json'
        subdir = 'templates/Disclosures/BBA/Ins'
    elif section == "ICL_A_BBA":
        template_file = 'BBA_Disc_Insurance_Contract_Liability_A.json'
        subdir = 'templates/Disclosures/BBA/Ins'
    elif section == "IFE":
        template_file = 'BBA_Disc_Insurance_Insurance_Finance_Expenses.json'
        subdir = 'templates/Disclosures/BBA/Ins'
    elif section == "ISE":
        template_file = 'BBA_Disc_Insurance_Insurance_Service_Expenses.json'
        subdir = 'templates/Disclosures/BBA/Ins'
    elif section == "ALP":
        template_file = 'BBA_Disc_Insurance_Alternative_Presentation.json'
        subdir = 'templates/Disclosures/BBA/Ins'
    elif section == "IRV":
        template_file = 'BBA_Disc_Insurance_Insurance_Revenue.json'
        subdir = 'templates/Disclosures/BBA/Ins'
    elif section == "OCI":
        template_file = 'BBA_Disc_Insurance_Statement_Other_Comprehensive_Income.json'
        subdir = 'templates/Disclosures/BBA/Ins'
    elif section == "UAC":
        template_file = 'BBA_Disc_Insurance_Balance_Unrecovered_Acquisition_Costs.json'
        subdir = 'templates/Disclosures/BBA/Ins'
    elif section == "CEB":
        template_file = 'BBA_Disc_Insurance_Cash_Equity_Balance.json'
        subdir = 'templates/Disclosures/BBA/Ins'
    elif section == "CIQ":
        template_file = 'BBA_Disc_Insurance_Statement_Change_In_Equity.json'
        subdir = 'templates/Disclosures/BBA/Ins'
    elif section == "SFP":
        template_file = 'BBA_Disc_Insurance_Statement_Financial_Position.json'
        subdir = 'templates/Disclosures/BBA/Ins'
    elif section == "SPL":
        template_file = 'BBA_Disc_Insurance_Statement_Profit_Loss.json'
        subdir = 'templates/Disclosures/BBA/Ins'
    #BBA REINS
    elif section == "B_SUB_BBA_Reins":
        template_file = 'BBA_Reconciliation_B_Sections_Reins.json'
        subdir = 'templates/Disclosures/BBA/Reins'
    elif section == "ICL_B_BBA_Reins":
        template_file = 'BBA_Disc_Reinsurance_Contract_Liability_B_Reins.json'
        subdir = 'templates/Disclosures/BBA/Reins'
    elif section == "A_SUB_BBA_Reins":
        template_file = 'BBA_Reconciliation_A_Sections_Reins.json'
        subdir = 'templates/Disclosures/BBA/Reins'
    elif section == "ICL_A_BBA_Reins":
        template_file = 'BBA_Disc_Reinsurance_Contract_Liability_A_Reins.json'
        subdir = 'templates/Disclosures/BBA/Reins'
    elif section == "IFE_Reins":
        template_file = 'BBA_Disc_Reinsurance_Reinsurance_Finance_Expenses.json'
        subdir = 'templates/Disclosures/BBA/Reins'
    elif section == "ISE_Reins":
        template_file = 'BBA_Disc_Reinsurance_Reinsurance_Service_Expenses.json'
        subdir = 'templates/Disclosures/BBA/Reins'
    elif section == "ALP_Reins":
        template_file = 'BBA_Disc_Reinsurance_Alternative_Presentation.json'
        subdir = 'templates/Disclosures/BBA/Reins'
    elif section == "IRV_Reins":
        template_file = 'BBA_Disc_Reinsurance_Reinsurance_Revenue.json'
        subdir = 'templates/Disclosures/BBA/Reins'
    elif section == "OCI_Reins":
        template_file = 'BBA_Disc_Reinsurance_Statement_Other_Comprehensive_Income_Reins.json'
        subdir = 'templates/Disclosures/BBA/Reins'
    elif section == "UAC_Reins":
        template_file = 'BBA_Disc_Reinsurance_Balance_Unrecovered_Acquisition_Costs_Reins.json'
        subdir = 'templates/Disclosures/BBA/Reins'
    elif section == "CEB_Reins":
        template_file = 'BBA_Disc_Reinsurance_Cash_Equity_Balance_Reins.json'
        subdir = 'templates/Disclosures/BBA/Reins'
    elif section == "CIQ_Reins":
        template_file = 'BBA_Disc_Reinsurance_Statement_Change_In_Equity_Reins.json'
        subdir = 'templates/Disclosures/BBA/Reins'
    elif section == "SFP_Reins":
        template_file = 'BBA_Disc_Reinsurance_Statement_Financial_Position_Reins.json'
        subdir = 'templates/Disclosures/BBA/Reins'
    elif section == "SPL_Reins":
        template_file = 'BBA_Disc_Reinsurance_Statement_Profit_Loss_Reins.json'
        subdir = 'templates/Disclosures/BBA/Reins'
    #PAA INS
    elif section == "A_SUB_PAA":
        template_file = 'PAA_Reconciliation_A_Sections.json'
        subdir = 'templates/Disclosures/PAA/Ins'
    elif section == "ICL_A_PAA":
        template_file = 'PAA_Insurance_Contract_Liability_A.json'
        subdir = 'templates/Disclosures/PAA/Ins'
    elif section == "IFE_PAA":
        template_file = 'PAA_Insurance_Finance_Expenses.json'
        subdir = 'templates/Disclosures/PAA/Ins'
    elif section == "ISE_PAA":
        template_file = 'PAA_Insurance_Service_Expenses.json'
        subdir = 'templates/Disclosures/PAA/Ins'
    elif section == "ALP_PAA":
        template_file = 'PAA_Insurance_Alternative_Presentation.json'
        subdir = 'templates/Disclosures/PAA/Ins'
    elif section == "IRV_PAA":
        template_file = 'PAA_Insurance_Revenue.json'
        subdir = 'templates/Disclosures/PAA/Ins'
    elif section == "OCI_PAA":
        template_file = 'PAA_Insurance_Other_Comprehensive_Income.json'
        subdir = 'templates/Disclosures/PAA/Ins'
    elif section == "UAC_PAA":
        template_file = 'PAA_Insurance_Balance_Unrecovered_Acquisition_Costs.json'
        subdir = 'templates/Disclosures/PAA/Ins'
    elif section == "CEB_PAA":
        template_file = 'PAA_Insurance_Cash_Equity_Balance.json'
        subdir = 'templates/Disclosures/PAA/Ins'
    elif section == "SCE_PAA":
        template_file = 'PAA_Insurance_Statement_Change_Equity.json'
        subdir = 'templates/Disclosures/PAA/Ins'
    elif section == "SFP_PAA":
        template_file = 'PAA_Insurance_Statement_Final_Position.json'
        subdir = 'templates/Disclosures/PAA/Ins'
    elif section == "SPL_PAA":
        template_file = 'PAA_Insurance_Statement_Profit_Loss.json'
        subdir = 'templates/Disclosures/PAA/Ins'
    #PAA REINS
    elif section == "A_SUB_PAA_Reins":
        template_file = 'PAA_Reconciliation_A_Sections_Reins.json'
        subdir = 'templates/Disclosures/PAA/Reins'
    elif section == "RCL_A_PAA_Reins":
        template_file = 'PAA_Reinsurance_Contract_Liability_A_Reins.json'
        subdir = 'templates/Disclosures/PAA/Reins'
    elif section == "RFE_PAA":
        template_file = 'PAA_Reinsurance_Finance_Expenses.json'
        subdir = 'templates/Disclosures/PAA/Reins'
    elif section == "RSE_PAA":
        template_file = 'PAA_Reinsurance_Service_Expenses.json'
        subdir = 'templates/Disclosures/PAA/Reins'
    elif section == "ALP_PAA_Reins":
        template_file = 'PAA_Reinsurance_Alternative_Presentation.json'
        subdir = 'templates/Disclosures/PAA/Reins'
    elif section == "RRV_PAA":
        template_file = 'PAA_Reinsurance_Revenue.json'
        subdir = 'templates/Disclosures/PAA/Reins'
    elif section == "ROCI_PAA":
        template_file = 'PAA_Reinsurance_Other_Comprehensive_Income.json'
        subdir = 'templates/Disclosures/PAA/Reins'
    elif section == "RUAC_PAA":
        template_file = 'PAA_Reinsurance_Balance_Unrecovered_Acquisition_Costs.json'
        subdir = 'templates/Disclosures/PAA/Reins'
    elif section == "RCEB_PAA":
        template_file = 'PAA_Reinsurance_Cash_Equity_Balance.json'
        subdir = 'templates/Disclosures/PAA/Reins'
    elif section == "RCE_PAA":
        template_file = 'PAA_Reinsurance_Statement_Change_Equity.json'
        subdir = 'templates/Disclosures/PAA/Reins'
    elif section == "RSFP_PAA":
        template_file = 'PAA_Reinsurance_Statement_Final_Position.json'
        subdir = 'templates/Disclosures/PAA/Reins'
    elif section == "RSPL_PAA":
        template_file = 'PAA_Reinsurance_Statement_Profit_Loss.json'
        subdir = 'templates/Disclosures/PAA/Reins'
    elif section == "NET_ALL":
        template_file = 'Disclosure_Net_All.json'
        subdir = 'templates/Disclosures'
    else:
        return None
    full_template_file = os.path.join(current_path, subdir, template_file)
    return full_template_file

def calculate_disclosure (section, lookup_data, master_groups, cumulative):
    try:
        schema = None
        if cumulative is None:
            cumulative = {}
        template_file = get_disclosure_template(section)

        with open(template_file) as data_file:
            schema = json.load(data_file)

        schema, cumulative = self_calculate_dictionary_value("Sum_External", schema, lookup_data, master_groups, cumulative=cumulative)
        schema, cumulative = self_calculate_dictionary_value("Sum_Sub", schema, lookup_data, master_groups, cumulative=cumulative)
        schema, cumulative = self_calculate_dictionary_value("Sum_External_Disc", schema, lookup_data, master_groups, cumulative=cumulative)
        schema, cumulative = self_calculate_dictionary_value("Sum_Disc_Local", schema, lookup_data, master_groups, cumulative=cumulative)


        min, max = get_dictio_limits(schema)

        while min <= max:
            schema, cumulative = self_calculate_dictionary_value("Local", schema, lookup_data, master_groups, calc_level=min, cumulative=cumulative)
            min = min + 1

        return schema, cumulative

    except Exception as e:
        logger.error("Error!!: {}".format(e))


def self_calculate_dictionary_value (calc_type, schema, lookup_data, master_groups, calc_level=None, cumulative=None):
    #miracle_df = pd.DataFrame.from_dict(lookup_data, orient='index')
    empty_values = {}
    if not cumulative:
        cumulative = {}
    for group in master_groups:
        empty_values[group] = 0

    for variable_record in schema:
        if variable_record['Ref_Type'] == calc_type:
            signal = 1
            lookup_value = str(variable_record['Reference'])
            if lookup_value[:1] == '-':
                signal = -1
                lookup_value = lookup_value[1:]

            # Sum External
            if variable_record['Ref_Type'] == "Sum_External":
                if variable_record['RNA_Disc_Code'] == "Net_D.PL.2.3":
                    logger.debug("STOPPPP")
                lookup_values = lookup_value.split("|")
                if lookup_values[0] == '':
                    variable_record['Value'] = empty_values
                else:
                    return_value = {}
                    for ref in lookup_values:
                        sub_signal = -1 if str(ref).startswith("(-)") else 1
                        ref_clean = str(ref).replace("(-)","")
                        if lookup_data.get(ref_clean):
                            val = lookup_data.get(ref_clean)
                        else:
                            val = None
                        if val:
                            for val_k in val.keys():
                                if int(val[val_k]) != 0:
                                    sub_signal = -1 if str(ref).startswith("(-)") else 1
                                    if val_k in return_value.keys():
                                        return_value[val_k] = (return_value[val_k]) + (val[val_k] * sub_signal)
                                    else:
                                        return_value[val_k] = (val[val_k] * sub_signal)
                                else:
                                    if val_k in return_value.keys():
                                        return_value[val_k] = return_value[val_k]
                                    else:
                                        return_value[val_k] = 0
                        else:
                            variable_record['Value'] = empty_values
                    for k in return_value.keys():
                        return_value[k] = return_value[k] * signal
                    variable_record['Value'] = return_value
                cumulative[variable_record['RNA_Disc_Code']] = return_value

            # Sum local and External Disc Reference
            if variable_record['Ref_Type'] == "Sum_Disc_Local":
                if variable_record['RNA_Disc_Code'] == "ReBBA_D.CEQ.7":
                    logger.debug("STOPPPP")
                lookup_values = lookup_value.split("|")
                if lookup_values[0] == '':
                    variable_record['Value'] = empty_values
                else:
                    return_value = {}
                    for ref in lookup_values:
                        sub_signal = -1 if str(ref).startswith("(-)") else 1
                        ref_clean = str(ref).replace("(-)","")
                        isDisc = True if "_D." in ref else False
                        if isDisc:
                            if cumulative.get(ref_clean):
                                val = cumulative.get(ref_clean)
                            else:
                                val = None
                        else:
                            if lookup_data.get(ref_clean):
                                val = lookup_data.get(ref_clean)
                            else:
                                val = None
                        if val:
                            for val_k in val.keys():
                                if int(val[val_k]) != 0:
                                    signed_val = (val[val_k]) * -1 if sub_signal == -1 else (val[val_k])
                                    if val_k in return_value.keys():
                                        return_value[val_k] = (return_value[val_k]) + signed_val
                                    else:
                                        return_value[val_k] = signed_val
                                else:
                                    if val_k in return_value.keys():
                                        return_value[val_k] = return_value[val_k]
                                    else:
                                        return_value[val_k] = 0
                variable_record['Value'] = return_value
                cumulative[variable_record['RNA_Disc_Code']] = return_value
            # Sum External Previous Disclosure
            if variable_record['Ref_Type'] == "Sum_External_Disc":
                if variable_record['RNA_Disc_Code'] == "BBA_D.ICL_A.3.2.1":
                    logger.debug("STOPPPP")
                lookup_values = lookup_value.split("|")
                if lookup_values[0] == '':
                    variable_record['Value'] = empty_values
                else:
                    return_value = {}
                    for ref in lookup_values:
                        sub_signal = -1 if str(ref).startswith("(-)") else 1
                        ref_clean = str(ref).replace("(-)", "")
                        if cumulative.get(ref_clean):
                            val = cumulative.get(ref_clean)
                        else:
                            val = None
                        if val:
                            for val_k in val.keys():
                                if int(val[val_k]) != 0:
                                    signed_val = (val[val_k]) * -1 if sub_signal == -1 else (val[val_k])
                                    if val_k in return_value.keys():
                                        return_value[val_k] = (return_value[val_k]) + signed_val
                                    else:
                                        return_value[val_k] = signed_val
                                else:
                                    if val_k in return_value.keys():
                                        return_value[val_k] = return_value[val_k]
                                    else:
                                        return_value[val_k] = 0
                        else:
                            variable_record['Value'] = empty_values
                    for k in return_value.keys():
                        return_value[k] = return_value[k] * signal
                    variable_record['Value'] = return_value
                cumulative[variable_record['RNA_Disc_Code']] = return_value
            # Sum Sub
            if variable_record['Ref_Type'] == "Sum_Sub":
                return_value = {}
                value_top = {}
                value_bottom = {}
                if variable_record['RNA_Disc_Code']=="ReBBA_D.DCF_B.4.3":
                    logger.debug("DEBUG")
                if str(lookup_value).startswith("-"):
                    masterNegative = True
                else:
                    masterNegative = False
                if "minus" in lookup_value:
                    lookup_values = lookup_value.split("minus")
                    top = str(lookup_values[0]).split("|")
                    bottom = str(lookup_values[1]).split("|")
                    if top[0] == "" and bottom[0] == "":
                        variable_record['Value'] = empty_values
                    else:
                        # return_value = {}
                        # value_top = {}
                        # value_bottom = {}
                        for ref in top:
                            sub_signal = -1 if str(ref).startswith("(-)") else 1
                            ref_clean = str(ref).replace("(-)", "")
                            if lookup_data.get(ref_clean):
                                val = lookup_data.get(ref_clean)
                            else:
                                val = None
                            if val:
                                for val_k in val.keys():
                                    if int(val[val_k]) != 0:
                                        signed_val = (val[val_k]) * -1 if sub_signal == -1 else (val[val_k])
                                        if val_k in value_top.keys():
                                            value_top[val_k] = (value_top[val_k]) + signed_val
                                        else:
                                            value_top[val_k] = signed_val
                                    else:
                                        if val_k in value_top.keys():
                                            value_top[val_k] = value_top[val_k]
                                        else:
                                            value_top[val_k] = 0
                            else:
                                value_top = value_top
                                #value_top = empty_values

                        for ref in bottom:
                            sub_signal = -1 if str(ref).startswith("(-)") else 1
                            ref_clean = str(ref).replace("(-)", "")
                            if lookup_data.get(ref_clean):
                                val = lookup_data.get(ref_clean)
                            else:
                                val = None
                            if val:
                                for val_k in val.keys():
                                    if int(val[val_k]) != 0:
                                        signed_val = (val[val_k]) * -1 if sub_signal == -1 else (val[val_k])
                                        if val_k in value_bottom.keys():
                                            value_bottom[val_k] = (value_bottom[val_k]) + signed_val
                                        else:
                                            value_bottom[val_k] = signed_val
                                    else:
                                        if val_k in value_bottom.keys():
                                            value_bottom[val_k] = value_bottom[val_k]
                                        else:
                                            value_bottom[val_k] = 0
                            else:
                                value_bottom = value_bottom
                                #value_bottom = empty_values

                        if value_top and value_bottom:
                            for final in value_top.keys():
                                value_top[final] = (value_top[final] - value_bottom[final]) * signal
                                value_top[final] = value_top[final] * -1 if masterNegative else value_top[final]
                            variable_record['Value'] = value_top
                            cumulative[variable_record['RNA_Disc_Code']] = value_top
                        elif value_top:
                            for final in value_top.keys():
                                value_top[final] = value_top[final] * signal
                                value_top[final] = value_top[final] * -1 if masterNegative else value_top[final]
                            variable_record['Value'] = value_top
                            cumulative[variable_record['RNA_Disc_Code']] = value_top
                        elif value_bottom:
                            for final in value_bottom.keys():
                                value_bottom[final] = value_bottom[final] * signal
                                value_bottom[final] = value_bottom[final] * -1 if masterNegative else value_bottom[final]
                            variable_record['Value'] = value_bottom
                            cumulative[variable_record['RNA_Disc_Code']] = value_bottom
                        else:
                            variable_record['Value'] = empty_values
                else:
                    variable_record['Value'] = empty_values
                    #variable_record['Value'] = value_top
            # Local
            if variable_record['Ref_Type'] == "Local" and variable_record['Level_Calc'] == str(calc_level):
                if variable_record['RNA_Disc_Code'] == "BBA_D.RA_B.3":
                    logger.debug("STOPPPP")
                if variable_record['RNA_Disc_Code'] == "BBA_D.RA_B.3.2":
                    logger.debug("STOPPPP2")
                lookup_values = lookup_value.split("|")
                if lookup_values[0] == '':
                    variable_record['Value'] = empty_values
                else:
                    return_value = {}
                    for ref in lookup_values:
                        sub_signal = -1 if str(ref).startswith("(-)") else 1
                        ref_clean = str(ref).replace("(-)", "")
                        if cumulative.get(ref_clean):
                            val = cumulative.get(ref_clean)
                        else:
                            val = None
                        if val:
                            for val_k in val.keys():
                                if int(val[val_k]) != 0:
                                    signed_val = (val[val_k]) * -1 if sub_signal == -1 else (val[val_k])
                                    if val_k in return_value.keys():
                                        return_value[val_k] = (return_value[val_k]) + signed_val
                                    else:
                                        return_value[val_k] = signed_val
                                else:
                                    if val_k in return_value.keys():
                                        return_value[val_k] = return_value[val_k]
                                    else:
                                        return_value[val_k] = 0
                        else:
                            variable_record['Value'] = empty_values
                    for k in return_value.keys():
                        return_value[k] = return_value[k] * signal
                    variable_record['Value'] = return_value
                cumulative[variable_record['RNA_Disc_Code']] = return_value
    return schema, cumulative

# def get_value_of_item (lookup_value, dictio):
#     value = None
#     if lookup_value:
#         item = dictio[lookup_value]
#         if item:
#             value = item.get('value')
#     return value

def get_dictio_value(lookup_value, dictio):
    value = None
    for item in dictio:
        if item.get('RNA BS Code') == lookup_value:
            value = item.get('value')
            return value
    return value

def get_dictio_key_value(lookup_value, dictio):
    value = None
    for item in dictio:
        if item.get('RNA_Disc_Code') == lookup_value:
            value = item.get('Value')
            return value
    return value

def get_dictio_limits(dictio):
    min = 0
    max = 0
    for item in dictio:
        if item.get('Level_Calc') != "":
            found = int(item.get('Level_Calc'))
            if found > max:
                max = found
            if found < min:
                min = found
    return min, max


def breakdown_query_builder (parameters):
    fields = []
    where = []
    group = []
    for param in parameters:
        if param.get('value') not in ["Off", None]:
            fields.append("[" + param.get('group') + " Value]")
            group.append("[" + param.get('group') + " Value]")
            if param.get('value') != "Group By Value":
                where.append(f"[{param.get('group')} Value]='{param.get('value')}'")
    return fields, group, where

# def filter_params_by_model (parameters, source):
#     filtered_params = []
#     for param in parameters:
#         if param.get('Model') == source and param.get('Value') != "Off":
#             filtered_params.append(param)
#     return filtered_params

def update_type_for_options (options_list):
    updated_list = []
    for option in options_list:
        if isinstance(option, float) or isinstance(option, int):
            updated_list.append(str(int(option)))
        else:
            updated_list.append(option)
    return updated_list

def filter_params_by_model (parameters, source):
    filtered_params = []
    if parameters:
        for param in parameters:
            if param.get('model') == source and param.get('value') not in ["Off",None]:
                filtered_params.append(param)
    return filtered_params

def get_filtered_results_groups (data, mask):
    master_groups = []
    if data:
        for key in data.keys():
            if str(key).startswith(mask):
                groups = data[key]
                for group in groups.keys():
                    master_groups.append(group)
                return master_groups
    return master_groups

def generate_report_key_value (dictio, key, value, bk_key_value = {}):

    for record in dictio:
        if record.get(key) != "":
            bk_key_value[record.get(key)] = record.get(value)

    return bk_key_value

# def create_goc_parameters (goc_data):
#
#     listeja = []
#     for parameter in goc_data:
#         group_name = parameter.get('Group')
#
#     temp_db = db_helper.G_Portfolio_Distinct(match)
#     results = helpers.get_df(temp_db, wvr, model_name)
#     options.extend(results["grp"])
#     element = {group_name: {"Variable_Name": str(match),
#                             "Group_Values": options, "Group_Type": str(type), "Set_Value": "Off"}}
#     listeja.append(element)