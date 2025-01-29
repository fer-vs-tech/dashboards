#demo_ifrs17/results/paa_disclosures.py
import logging

import cm_dashboards.demo_ifrs17.utils.helpers as helpers
from cm_dashboards.demo_ifrs17.results.prepare_components import generate_disclosures_sums, generate_disclosure_summaries

logger = logging.getLogger(__name__)

def paa_ins_disc (paa_ins_data, master_groups, disc_key_value={}):
    presentation = []
    cumulative = None

    sections_list = ["A_SUB_PAA", "ICL_A_PAA", "IFE_PAA", "ISE_PAA", "ALP_PAA", "IRV_PAA", "OCI_PAA", "UAC_PAA", "CEB_PAA", "SCE_PAA", "SFP_PAA", "SPL_PAA"]

    sub = {}
    icl = {}

    for section in sections_list:
        if section in ["A_SUB_PAA"]:
            sub, cumulative = helpers.calculate_disclosure(section=section, lookup_data=paa_ins_data, master_groups=master_groups, cumulative=cumulative)
        elif section in ["ICL_A_PAA"]:
            icl, cumulative = helpers.calculate_disclosure(section=section, lookup_data=paa_ins_data, master_groups=master_groups, cumulative=cumulative)
            presentation = generate_disclosures_sums(icl + sub, master_groups, presentation)
            disc_key_value = helpers.generate_report_key_value(icl + sub, 'RNA_Disc_Code', 'Value', disc_key_value)
        else:
            tempo, cumulative = helpers.calculate_disclosure(section=section, lookup_data=paa_ins_data, master_groups=master_groups, cumulative=cumulative)
            presentation = generate_disclosures_sums(tempo, master_groups, presentation)
            disc_key_value = helpers.generate_report_key_value(tempo, 'RNA_Disc_Code', 'Value', disc_key_value)

    return presentation, disc_key_value

def paa_reins_disc (paa_reins_data, master_groups, disc_key_value={}):
    presentation = []
    cumulative = None

    sections_list = ["A_SUB_PAA_Reins", "RCL_A_PAA_Reins", "RFE_PAA", "RSE_PAA", "ALP_PAA_Reins", "RRV_PAA", "ROCI_PAA", "RUAC_PAA",
                     "RCEB_PAA", "RCE_PAA", "RSFP_PAA", "RSPL_PAA"]

    sub = {}
    icl = {}

    for section in sections_list:
        if section in ["A_SUB_PAA_Reins"]:
            sub, cumulative = helpers.calculate_disclosure(section=section, lookup_data=paa_reins_data, master_groups=master_groups, cumulative=cumulative)
        elif section in ["RCL_A_PAA_Reins"]:
            icl, cumulative = helpers.calculate_disclosure(section=section, lookup_data=paa_reins_data, master_groups=master_groups, cumulative=cumulative)
            presentation = generate_disclosures_sums(icl + sub, master_groups, presentation)
            disc_key_value = helpers.generate_report_key_value(icl + sub, 'RNA_Disc_Code', 'Value', disc_key_value)
        else:
            tempo, cumulative = helpers.calculate_disclosure(section=section, lookup_data=paa_reins_data, master_groups=master_groups, cumulative=cumulative)
            presentation = generate_disclosures_sums(tempo, master_groups, presentation)
            disc_key_value = helpers.generate_report_key_value(tempo, 'RNA_Disc_Code', 'Value', disc_key_value)

    return presentation, disc_key_value
