#demo_ifrs17/results/bba_disclosures.py
import logging

import json
import os
import time
import pandas as pd

import cm_dashboards.utilities as utilities
import cm_dashboards.demo_ifrs17.utils.helpers as helpers
from cm_dashboards.demo_ifrs17.results.prepare_components import generate_disclosures_sums, netall_gen_presentation
logger = logging.getLogger(__name__)

def bba_ins_disc (bba_ins_data, master_groups, disc_key_value={}):
    presentation = []
    cumulative = None

    sections_list = ["B_SUB_BBA", "ICL_B_BBA", "A_SUB_BBA", "ICL_A_BBA", "IFE", "ISE", "ALP", "IRV", "OCI", "UAC", "CEB", "CIQ", "SFP", "SPL"]

    sub = {}
    icl = {}

    for section in sections_list:
        if section in ["A_SUB_BBA", "B_SUB_BBA"]:
            sub, cumulative = helpers.calculate_disclosure(section=section, lookup_data=bba_ins_data, master_groups=master_groups, cumulative=cumulative)
        elif section in ["ICL_A_BBA", "ICL_B_BBA"]:
            icl, cumulative = helpers.calculate_disclosure(section=section, lookup_data=bba_ins_data, master_groups=master_groups, cumulative=cumulative)
            presentation = generate_disclosures_sums(icl + sub, master_groups, presentation)
            disc_key_value = helpers.generate_report_key_value(icl + sub, 'RNA_Disc_Code', 'Value', disc_key_value)
        else:
            tempo, cumulative = helpers.calculate_disclosure(section=section, lookup_data=bba_ins_data, master_groups=master_groups, cumulative=cumulative)
            presentation = generate_disclosures_sums(tempo, master_groups, presentation)
            disc_key_value = helpers.generate_report_key_value(tempo, 'RNA_Disc_Code', 'Value', disc_key_value)

    return presentation, disc_key_value

def bba_reins_disc (bba_reins_data, master_groups, disc_key_value={}):
    presentation = []
    cumulative = None

    # sections_list = ["CSM_Reins", "RA_Reins", "DCF_Reins", "ICL_Reins", "LIC_Reins", "LRC_Reins", "LRC_EXC_Reins", "ICL_A_Reins",
    #                  "IFE_Reins", "ISE_Reins", "ALP_Reins", "IRV_Reins", "OCI_Reins", "UAC_Reins", "CEB_Reins", "CIQ_Reins", "SFP_Reins", "SPL_Reins"]

    sections_list = ["B_SUB_BBA_Reins", "ICL_B_BBA_Reins", "A_SUB_BBA_Reins", "ICL_A_BBA_Reins",
                     "IFE_Reins", "ISE_Reins", "ALP_Reins", "IRV_Reins", "OCI_Reins", "UAC_Reins", "CEB_Reins", "CIQ_Reins", "SFP_Reins", "SPL_Reins"]

    sub = {}
    icl = {}

    for section in sections_list:
        if section in ["A_SUB_BBA_Reins", "B_SUB_BBA_Reins"]:
            sub, cumulative = helpers.calculate_disclosure(section=section, lookup_data=bba_reins_data, master_groups=master_groups, cumulative=cumulative)
        elif section in ["ICL_A_BBA_Reins", "ICL_B_BBA_Reins"]:
            icl, cumulative = helpers.calculate_disclosure(section=section, lookup_data=bba_reins_data, master_groups=master_groups, cumulative=cumulative)
            presentation = generate_disclosures_sums(icl + sub, master_groups, presentation)
            disc_key_value = helpers.generate_report_key_value(icl + sub, 'RNA_Disc_Code', 'Value', disc_key_value)
        else:
            tempo, cumulative = helpers.calculate_disclosure(section=section, lookup_data=bba_reins_data, master_groups=master_groups, cumulative=cumulative)
            presentation = generate_disclosures_sums(tempo, master_groups, presentation)
            disc_key_value = helpers.generate_report_key_value(tempo, 'RNA_Disc_Code', 'Value', disc_key_value)

    return presentation, disc_key_value



def calculate_net_all (bba_ins_data, master_groups, disc_key_value={}):
    if not disc_key_value:
        return None

    presentation = []
    tempo, cumulative = helpers.calculate_disclosure(section="NET_ALL", lookup_data=disc_key_value, master_groups=master_groups, cumulative=disc_key_value)
    #presentation = generate_disclosures_sums(tempo, master_groups, presentation)
    presentation = netall_gen_presentation(tempo, master_groups)
    disc_key_value = helpers.generate_report_key_value(tempo, 'RNA_Disc_Code', 'Value', disc_key_value)


    return presentation, disc_key_value





    return None