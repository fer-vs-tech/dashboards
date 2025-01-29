#demo_ifrs17/results/common.py
import logging

import json
import os

logger = logging.getLogger(__name__)


def generate_bs_summary (breakdowns, table, option, group):
    results = []
    if breakdowns is None:
        return None

    current_path = os.path.dirname(os.path.abspath(__file__))
    current_path = os.path.dirname(current_path)

    if table == "BS_GMM":
        template_file = 'bba_summary.json'
        subdir = 'templates/BS_Summary'
    elif table == "BS_PAA":
        template_file = 'paa_summary.json'
        subdir = 'templates/BS_Summary'
    elif table == "REC_A":
        template_file = 'rec_a_summary.json'
        subdir = 'templates/BS_Summary'
    elif table == "REC_B":
        template_file = 'rec_b_summary.json'
        subdir = 'templates/BS_Summary'
    else:
        template_file = ""

    if template_file == "":
        return None

    full_template_file = os.path.join(current_path, subdir, template_file)

    with open(full_template_file) as data_file:
        schema = json.load(data_file)

    for record in schema:
        desc = ""
        temp_record = {}
        for header in record.keys():
            if header == 'Description':
                temp_record["Description"] = record[header]
            else:
                final_value = 0
                reference = record[header]
                refs = reference.get('Reference')
                ref_list = refs.split("|")
                if option.lower() == "net position":
                    for ref in ref_list:
                        val = breakdowns.get(ref)
                        if val:
                            for item in val.keys():
                                if item == group:
                                    final_value = final_value + val[item]
                elif option.lower() == "reinsurance only":
                    for ref in ref_list:
                        if str(ref).startswith("Re"):
                            val = breakdowns.get(ref)
                            if val:
                                for item in val.keys():
                                    if item == group:
                                        final_value = val[item]
                else: # insurance
                    for ref in ref_list:
                        if not str(ref).startswith("Re"):
                            val = breakdowns.get(ref)
                            if val:
                                for item in val.keys():
                                    if item == group:
                                        final_value = val[item]

                temp_record[header] = final_value
        results.append(temp_record)

    # for breakdown in breakdowns:
    #     bba_bk = breakdown.get("BBA_Breakdown")
    #     bba_bk_reins = breakdown.get("BBA_Reins_Breakdown")
    #     paa_bk = breakdown.get("PAA_Breakdown")
    #     paa_bk_reins = breakdown.get("PAA_Reins_Breakdown")
    #
    # if table == "BS_GMM":
    #     template_file = "C:/RnA/development/Reports/Disclosure_Std/bs_summary/bba_summary.json"
    #     ins = bba_bk
    #     reins = bba_bk_reins
    # elif table == "BS_PAA":
    #     template_file = "C:/RnA/development/Reports/Disclosure_Std/bs_summary/paa_summary.json"
    #     ins = paa_bk
    #     reins = paa_bk_reins
    # else:
    #     template_file = "C:/RnA/development/Reports/Disclosure_Std/bs_summary/bs_summary.json"
    #
    # with open(template_file) as data_file:
    #     schema = json.load(data_file)
    #
    # for record in schema:
    #     desc = ""
    #     temp_record = {}
    #     for header in record.keys():
    #         if header == 'Description':
    #             temp_record["Description"] = record[header]
    #         else:
    #             final_value = 0
    #             reference = record[header]
    #             refs = reference.get('Reference')
    #             ref_list = refs.split("|")
    #             if option.lower() == "net position":
    #                 for ref in ref_list:
    #                     val = helpers.get_dictio_value(ref, ins + reins)
    #                     if val:
    #                         for item in val.keys():
    #                             if item == group:
    #                                 final_value = final_value + val[item]
    #             elif option.lower() == "reinsurance only":
    #                 for ref in ref_list:
    #                     if str(ref).startswith("Re"):
    #                         val = helpers.get_dictio_value(ref, reins)
    #                         if val:
    #                             for item in val.keys():
    #                                 if item == group:
    #                                     final_value = val[item]
    #             else: # insurance
    #                 for ref in ref_list:
    #                     if not str(ref).startswith("Re"):
    #                         val = helpers.get_dictio_value(ref, ins)
    #                         if val:
    #                             for item in val.keys():
    #                                 if item == group:
    #                                     final_value = val[item]
    #
    #             temp_record[header] = final_value
    #     results.append(temp_record)
    return results
