"""
@author: Kamoliddin Usmonov
@date: 2022-09-14
@description: This file contains formulas to calculate IFRS17 disclosure
"""

COLUMN_NAMES = {
    "IFRS17_BBA_Primary_Movement": {
        "100_primary": [
            "Description",
            "Excluding_Loss_Component",
            "Loss_Component",
            "LIC",
            "Total",
        ],
        "101_primary": [
            "Description",
            "Future_cash_flows",
            "Risk_adjustment",
            "CSM",
            "Total",
        ],
    },
    "IFRS17_BBA_Reinsurance_Movement": {
        "100_primary": [
            "Description",
            "Excluding_loss_recovery",
            "Loss_recovery",
            "AIC",
            "Total",
        ],
        "101_primary": [
            "Description",
            "Future_cash_flows",
            "Risk_adjustment",
            "CSM",
            "Total",
        ],
    },
}

DESCRIPTIONS = {
    "IFRS17_BBA_Primary_Movement": {
        "100_primary": [
            "Opening insurance contract liabilities",
            "Opening insurance contract assets",
            "Net balance",
            "Insurance revenue",
            "Insurance service expenses",
            "Incurred claims and other directly attributable expenses",
            "Other pre-recognition cash flows assets derecognised at the date of initial recognition",
            "Changes that relate to past service - changes in the FCF related to the LIC",
            "Losses on onerous contracts and reversal of those losses",
            "Insurance acquisition cash flows amortisation",
            "Insurance service expenses (2)",
            "Insurance service result",
            "Finance expenses from insurance contracts issued",
            "Other changes",
            "Total amounts recognised in comprehensive income",
            "Investment components",
            "Other changes (2)",
            "Cash flows",
            "Premiums received",
            "Claims and other directly attributable expenses paid",
            "Insurance acquisition cash flows",
            "Total cash flows",
            "Net balance as at 31 December",
            "Closing insurance contract liabilities",
            "Closing insurance contract assets",
            "Net balance as at 31 December (2)",
        ],
        "101_primary": [
            "Opening insurance contract liabilities",
            "Opening insurance contract assets",
            "Opening net balance",
            "Changes that relate to current service",
            "CSM recognised in profit or loss for the services provided",
            "Change in the risk adjustment for non-financial risk for the risk expired",
            "Experience adjustments - relating to insurance service expenses",
            "Changes that relate to future service",
            "Changes in estimates that adjust the CSM",
            "Changes in estimates that result in onerous contract losses or reversal of losses",
            "Contracts initially recognised in the period",
            "Experience adjustments - arising from premiums received in the period that relate to future service",
            "Changes that relate to past service",
            "Changes that relate to past service - changes in the FCF related to the LIC",
            "Experience adjustments - arising from premiums received in the period that relate to past service",
            "Insurance service result",
            "Finance (income) expenses from insurance contracts issued",
            "Other changes",
            "Total amounts recognised in comprehensive income",
            "Other changes (2)",
            "Cash flows",
            "Premiums received",
            "Claims and other directly attributable expenses paid",
            "Insurance acquisition cash flows",
            "Total cash flows",
            "Closing net balance",
            "Closing insurance contract liabilities",
            "Closing insurance contract assets",
            "Closing net balance (2)",
        ],
    },
    "IFRS17_BBA_Reinsurance_Movement": {
        "100_primary": [
            "Opening reinsurance contract assets",
            "Opening reinsurance contract liabilities",
            "Net balance as at 1 January",
            "Net income (expenses) from reinsurance contracts held",
            "Reinsurance expenses",
            "Other incurred directly attributable expenses",
            "Incurred claims recovery",
            "Changes that relate to past service - changes in the FCF relating to incurred claims recovery",
            "Income on initial recognition of onerous underlying contracts",
            "Reversals of a loss-recovery component other than changes in the FCF of reinsurance contracts held",
            "Changes in the FCF of reinsurance contracts held from onerous underlying contracts",
            "Effect of changes in the risk of reinsurers",
            "Cost of retroactive cover for reinsurance contracts held",
            "Net income (expenses) from reinsurance contracts held (2)",
            "Finance income (expenses) from reinsurance contracts held",
            "Other changes",
            "Total amounts recognised in comprehensive income",
            "Investment components",
            "Other changes (2)",
            "Cash flows",
            "Premiums paid net of ceding commissions and other directly attributable expenses paid",
            "Recoveries from reinsurance",
            "Total cash flows",
            "Net balance as at 31 December",
            "Closing reinsurance contract assets",
            "Closing reinsurance contract liabilities",
            "Net balance as at 31 December (2)",
        ],
        "101_primary": [
            "Opening reinsurance contract assets",
            "Opening reinsurance contract liabilities",
            "Opening net balance",
            "Changes that relate to current service",
            "CSM recognised in profit or loss for the services received",
            "Change in the risk adjustment for non-financial risk for the risk expired",
            "Experience adjustments - relating to incurred claims and other directly attributable expenses recovery",
            "Changes that relate to future service",
            "Changes in estimates that adjust the CSM",
            "Contracts initially recognised in the period",
            "CSM adjustment for income on initial recognition of onerous underlying contracts",
            "Reversals of a loss-recovery component other than changes in the FCF of reinsurance contracts held",
            "Changes in the FCF of reinsurance contracts held from onerous underlying contracts",
            "Experience adjustments - arising from ceded premiums paid in the period that relate to future service",
            "Changes that relate to past service",
            "Changes that relate to past service - changes in the FCF relating to incurred claims recovery",
            "Changes in estimates relate to losses on onerous contracts and reversal of those losses",
            "Experience adjustments - arising from ceded premiums paid in the period that relate to past service",
            "Effect of changes in the risk of reinsurers",
            "Cost of retroactive cover for reinsurance contracts held",
            "Net income (expenses) from reinsurance contracts held",
            "Finance income (expenses) from reinsurance contracts held",
            "Other changes",
            "Total amounts recognised in comprehensive income",
            "Other changes (2)",
            "Cash flows",
            "Premiums paid net of ceding commissions and other directly attributable expenses paid to reinsurer",
            "Recoveries from reinsurance",
            "Total cash flows",
            "Closing net balance",
            "Closing reinsurance contract assets",
            "Closing reinsurance contract liabilities",
            "Closing net balance (2)",
        ],
    },
}

FORMULAS = {
    "IFRS17_BBA_Primary_Movement": {
        "100_primary": {
            "Opening insurance contract liabilities": {
                "LRC": {
                    "calculate": "OPEN_CURR_BEL_OTH+OPEN_CURR_RA_OTH+OPEN_CSM",
                    "expression": {"condition": ">= 0", "replace": "sum"},
                },
                "LC": {
                    "calculate": "OPEN_CURR_BEL_LOSS + OPEN_CURR_RA_LOSS",
                },
                "LIC": {
                    "calculate": "OPEN_CURR_BEL_CASE_CY + OPEN_CURR_BEL_CASE_PY + OPEN_CURR_BEL_IBNR_CY + OPEN_INIT_BEL_IBNR_PY + OPEN_CURR_BEL_LAE_CY + OPEN_INIT_BEL_LAE_PY + OPEN_CURR_RA_CASE_CY + OPEN_CURR_RA_CASE_PY + OPEN_CURR_RA_IBNR_CY + OPEN_INIT_RA_IBNR_PY + OPEN_CURR_RA_LAE_CY + OPEN_INIT_RA_LAE_PY + OPEN_AOCI_RVNU_BEL_IBNR_PY + OPEN_AOCI_RVNU_BEL_LAE_PY + OPEN_AOCI_RVNU_RA_IBNR_PY + OPEN_AOCI_RVNU_RA_LAE_PY + OPEN_AOCI_EXPNS_BEL_IBNR_PY + OPEN_AOCI_EXPNS_BEL_LAE_PY + OPEN_AOCI_EXPNS_RA_IBNR_PY + OPEN_AOCI_EXPNS_RA_LAE_PY",
                },
                "TOTAL": None,
            },
            "Opening insurance contract assets": {
                "LRC": {
                    "calculate": "OPEN_CURR_BEL_OTH + OPEN_CURR_RA_OTH + OPEN_CSM",
                    "expression": {
                        "condition": "< 0",
                        "replace": "sum",
                        "positive": True,
                    },
                },
                "LC": None,
                "LIC": None,
                "TOTAL": None,
            },
            "Net balance": {
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[0]['Excluding_Loss_Component'] - result_df.iloc[1]['Excluding_Loss_Component']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[0]['Loss_Component'] - result_df.iloc[1]['Loss_Component']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[0]['LIC'] - result_df.iloc[1]['LIC']",
                },
                "TOTAL": None,
            },
            "Insurance revenue": {
                "index": 3,
                "LRC": {
                    "calculate": "-(EXP_CLM_INSRC_OTH_RSP_WAP+EXP_DIR_ACQ_NPR_OTH_RSP_WAP+EXP_DIR_MNTNC_OTH_RSP_WAP+EXP_DIR_LAE_OTH_RSP_WAP+EXP_DIR_INVST_FEE_OTH_RSP_WAP+EXP_RA_AMORT_OTH_RSP_WAP+CSM_AMORT+DAC_AMORT+PV_DIR_ACQ_PR_AMORT)",
                },
                "LC": None,
                "LIC": None,
                "TOTAL": None,
            },
            "Insurance service expenses": None,
            "Other pre-recognition cash flows assets derecognised at the date of initial recognition": None,
            "Incurred claims and other directly attributable expenses": {
                "LRC": None,
                "LC": None,
                "LIC": {
                    "calculate": "CLOS_INIT_BEL_CASE_CY + CLOS_INIT_BEL_IBNR_CY + CLOS_INIT_BEL_LAE_CY + CLOS_INIT_RA_CASE_CY + CLOS_INIT_RA_IBNR_CY + CLOS_INIT_RA_LAE_CY - ACTCF_CLM_INSRC_CY - ACTCF_DIR_LAE_CY - ACTCF_DIR_MNTNC",
                },
                "TOTAL": None,
            },
            "Changes that relate to past service - changes in the FCF related to the LIC": {
                "LRC": None,
                "LC": None,
                "LIC": {
                    "calculate": "ADJ_BEL_IBNR_PY + ADJ_BEL_CASE_PY + ADJ_BEL_LAE_PY + ADJ_RA_IBNR_PY + ADJ_RA_CASE_PY + ADJ_RA_LAE_PY - ((EXPCF_CLM_CASE_CY + EXPCF_CLM_CASE_PY) + (EXPCF_CLM_IBNR_CY + EXPCF_CLM_IBNR_PY) + (EXPCF_LOSS_ADJ_EXPNS_CY+ EXPCF_LOSS_ADJ_EXPNS_PY) + (EXP_RA_AMORT_IBNR_CY + EXP_RA_AMORT_IBNR_PY) + (EXP_RA_AMORT_CASE_CY + EXP_RA_AMORT_CASE_PY) + (EXP_RA_AMORT_LAE_CY + EXP_RA_AMORT_LAE_PY)) -ACTCF_CLM_INSRC_PY - ACTCF_DIR_LAE_PY",
                },
                "TOTAL": None,
            },
            "Losses on onerous contracts and reversal of those losses": {
                "LRC": {
                    "calculate": "-(CLOS_LC_ALLC_RESET_BEL + CLOS_LC_ALLC_RESET_RA) - SUBS_LOSS_REVRSL + SUBS_LOSS_TRNSFR",
                    # "negative": True,
                },
                "LC": {
                    "calculate": "CLOS_LC_ALLC_RESET_BEL + CLOS_LC_ALLC_RESET_RA -(EXP_CLM_INSRC_LOSS_RSP_WAP+EXP_DIR_ACQ_NPR_LOSS_RSP_WAP+EXP_DIR_MNTNC_LOSS_RSP_WAP+EXP_DIR_LAE_LOSS_RSP_WAP+EXP_DIR_INVST_FEE_LOSS_RSP_WAP+EXP_RA_AMORT_LOSS_RSP_WAP+EXP_DIR_ACQ_PR_LOSS_RSP_WAP) + (INIT_BEL_LOSS_QDP - INIT_BEL_LOSS_RDP) + (INIT_RA_LOSS_QDP - INIT_RA_LOSS_RDP) + (INIT_BEL_LOSS_PAP - INIT_BEL_LOSS_QDP) + (INIT_RA_LOSS_PAP - INIT_RA_LOSS_QDP) + INCPT_INIT_BEL_LOSS_WAP_NB + INCPT_INIT_RA_LOSS_WAP_NB",
                },
                "LIC": None,
                "TOTAL": None,
            },
            "Insurance acquisition cash flows amortisation": {
                "LRC": {
                    "calculate": "DAC_AMORT + PV_DIR_ACQ_PR_AMORT",
                },
                "LC": None,
                "LIC": None,
                "TOTAL": None,
            },
            "Insurance service expenses (2)": {
                "index": 10,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[4]['Excluding_Loss_Component'] + result_df.iloc[5]['Excluding_Loss_Component'] + result_df.iloc[6]['Excluding_Loss_Component'] + result_df.iloc[7]['Excluding_Loss_Component'] + result_df.iloc[8]['Excluding_Loss_Component'] + result_df.iloc[9]['Excluding_Loss_Component']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[4]['Loss_Component'] + result_df.iloc[5]['Loss_Component'] + result_df.iloc[6]['Loss_Component'] + result_df.iloc[7]['Loss_Component'] + result_df.iloc[8]['Loss_Component'] + result_df.iloc[9]['Loss_Component']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[4]['LIC'] + result_df.iloc[5]['LIC'] + result_df.iloc[6]['LIC'] + result_df.iloc[7]['LIC'] + result_df.iloc[8]['LIC'] + result_df.iloc[9]['LIC']",
                },
                "TOTAL": None,
            },
            "Insurance service result": {
                "index": 11,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[3]['Excluding_Loss_Component'] + result_df.iloc[10]['Excluding_Loss_Component']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[3]['Loss_Component'] + result_df.iloc[10]['Loss_Component']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[3]['LIC'] + result_df.iloc[4]['LIC'] + result_df.iloc[10]['LIC']",
                },
                "TOTAL": None,
            },
            "Finance expenses from insurance contracts issued": {
                "LRC": {
                    "calculate": "(INTRST_EXPNS_RESET_BEL_RSP_WAP - INTRST_EXPNS_RESET_BEL_LOSS_RSP_WAP) + (INTRST_EXPNS_RESET_RA_RSP_WAP - INTRST_EXPNS_RESET_RA_LOSS_RSP_WAP) + CSM_UNWND",
                },
                "LC": {
                    "calculate": "INTRST_EXPNS_RESET_BEL_LOSS_RSP_WAP + INTRST_EXPNS_RESET_RA_LOSS_RSP_WAP",
                },
                "LIC": {
                    "calculate": "(INTRST_EXPNS_BEL_IBNR_CY + INTRST_EXPNS_BEL_IBNR_PY) + (INTRST_EXPNS_BEL_CASE_CY + INTRST_EXPNS_BEL_CASE_PY) + (INTRST_EXPNS_BEL_LAE_CY + INTRST_EXPNS_BEL_LAE_PY) + (INTRST_EXPNS_RA_IBNR_CY + INTRST_EXPNS_RA_IBNR_PY) + (INTRST_EXPNS_RA_CASE_CY + INTRST_EXPNS_RA_CASE_PY) + (INTRST_EXPNS_RA_LAE_CY + INTRST_EXPNS_RA_LAE_PY)",
                },
                "TOTAL": None,
            },
            "Other changes": {
                "LRC": {
                    "calculate": "(CLOS_AOCI_EXPNS_BEL_OTH + CLOS_AOCI_RVNU_BEL_OTH) + (CLOS_AOCI_EXPNS_RA_OTH + CLOS_AOCI_RVNU_RA_OTH) -( OPEN_AOCI_EXPNS_BEL_OTH + OPEN_AOCI_RVNU_BEL_OTH + OPEN_AOCI_EXPNS_RA_OTH + OPEN_AOCI_RVNU_RA_OTH)",
                },
                "LC": {
                    "calculate": "(CLOS_AOCI_EXPNS_BEL_LOSS + CLOS_AOCI_RVNU_BEL_LOSS) + (CLOS_AOCI_EXPNS_RA_LOSS + CLOS_AOCI_RVNU_RA_LOSS) - (OPEN_AOCI_EXPNS_BEL_LOSS + OPEN_AOCI_RVNU_BEL_LOSS + OPEN_AOCI_EXPNS_RA_LOSS + OPEN_AOCI_RVNU_RA_LOSS)",
                },
                "LIC": {
                    "calculate": "CLOS_AOCI_EXPNS_BEL_IBNR_PY + CLOS_AOCI_RVNU_BEL_IBNR_PY + CLOS_AOCI_EXPNS_BEL_CASE_PY + CLOS_AOCI_RVNU_BEL_CASE_PY + CLOS_AOCI_EXPNS_BEL_LAE_PY + CLOS_AOCI_RVNU_BEL_LAE_PY + CLOS_AOCI_EXPNS_RA_IBNR_PY + CLOS_AOCI_RVNU_RA_IBNR_PY + CLOS_AOCI_EXPNS_RA_CASE_PY + CLOS_AOCI_RVNU_RA_CASE_PY + CLOS_AOCI_EXPNS_RA_LAE_PY + CLOS_AOCI_RVNU_RA_LAE_PY + CLOS_AOCI_EXPNS_BEL_IBNR_CY + CLOS_AOCI_RVNU_BEL_IBNR_CY + CLOS_AOCI_EXPNS_BEL_CASE_CY + CLOS_AOCI_RVNU_BEL_CASE_CY + CLOS_AOCI_EXPNS_BEL_LAE_CY + CLOS_AOCI_RVNU_BEL_LAE_CY + CLOS_AOCI_EXPNS_RA_IBNR_CY + CLOS_AOCI_RVNU_RA_IBNR_CY + CLOS_AOCI_EXPNS_RA_CASE_CY + CLOS_AOCI_RVNU_RA_CASE_CY + CLOS_AOCI_EXPNS_RA_LAE_CY + CLOS_AOCI_RVNU_RA_LAE_CY - (OPEN_AOCI_EXPNS_BEL_CASE_CY + OPEN_AOCI_EXPNS_BEL_CASE_PY + OPEN_AOCI_EXPNS_BEL_IBNR_CY + OPEN_AOCI_EXPNS_BEL_IBNR_PY + OPEN_AOCI_EXPNS_BEL_LAE_CY + OPEN_AOCI_EXPNS_BEL_LAE_PY + OPEN_AOCI_EXPNS_RA_CASE_CY + OPEN_AOCI_EXPNS_RA_CASE_PY + OPEN_AOCI_EXPNS_RA_IBNR_CY + OPEN_AOCI_EXPNS_RA_IBNR_PY + OPEN_AOCI_EXPNS_RA_LAE_CY + OPEN_AOCI_EXPNS_RA_LAE_PY + OPEN_AOCI_RVNU_BEL_CASE_CY + OPEN_AOCI_RVNU_BEL_CASE_PY + OPEN_AOCI_RVNU_BEL_IBNR_CY + OPEN_AOCI_RVNU_BEL_LAE_CY + OPEN_AOCI_RVNU_BEL_IBNR_PY + OPEN_AOCI_RVNU_BEL_LAE_PY + OPEN_AOCI_RVNU_RA_CASE_CY + OPEN_AOCI_RVNU_RA_CASE_PY + OPEN_AOCI_RVNU_RA_IBNR_CY + OPEN_AOCI_RVNU_RA_LAE_CY + OPEN_AOCI_RVNU_RA_IBNR_PY + OPEN_AOCI_RVNU_RA_LAE_PY)",
                },
                "TOTAL": None,
            },
            "Total amounts recognised in comprehensive income": {
                "index": 14,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[11]['Excluding_Loss_Component'] + result_df.iloc[12]['Excluding_Loss_Component'] + result_df.iloc[13]['Excluding_Loss_Component']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[11]['Loss_Component'] + result_df.iloc[12]['Loss_Component'] + result_df.iloc[13]['Loss_Component']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[11]['LIC'] + result_df.iloc[12]['LIC'] + result_df.iloc[13]['LIC']",
                },
                "TOTAL": None,
            },
            "Investment components": None,
            "Other changes (2)": None,
            "Cash flows": {
                "index": 17,
            },
            "Premiums received": {
                "LRC": {
                    "calculate": "ACTCF_PREM",
                },
                "LC": None,
                "LIC": None,
                "TOTAL": None,
            },
            "Claims and other directly attributable expenses paid": {
                "LRC": None,
                "LC": None,
                "LIC": {
                    "calculate": "ACTCF_CLM_INSRC_PY + ACTCF_DIR_LAE_PY + ACTCF_CLM_INSRC_CY + ACTCF_DIR_LAE_CY + ACTCF_DIR_MNTNC",
                },
                "TOTAL": None,
            },
            "Insurance acquisition cash flows": {
                "LRC": {
                    "calculate": "ACTCF_DIR_ACQ_PR",
                },
                "LC": None,
                "LIC": None,
                "TOTAL": None,
            },
            "Total cash flows": {
                "index": 21,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[18]['Excluding_Loss_Component'] + result_df.iloc[19]['Excluding_Loss_Component'] + result_df.iloc[20]['Excluding_Loss_Component']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[18]['Loss_Component'] + result_df.iloc[19]['Loss_Component'] + result_df.iloc[20]['Loss_Component']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[19]['LIC'] + result_df.iloc[20]['LIC']",
                },
                "TOTAL": None,
            },
            "Net balance as at 31 December": {
                "index": 22,
            },
            "Closing insurance contract liabilities": {
                "LRC": {
                    "calculate": "(CLOS_CURR_BEL_OTH+CLOS_CURR_RA_OTH+CLOS_CSM)",
                    "expression": {"condition": ">= 0", "replace": "zero"},
                },
                "LC": {
                    "calculate": "CLOS_CURR_BEL_LOSS +CLOS_CURR_RA_LOSS",
                },
                "LIC": {
                    "calculate": "(CLOS_CURR_BEL_CASE_PY + CLOS_CURR_BEL_IBNR_PY + CLOS_CURR_BEL_LAE_PY + CLOS_CURR_RA_CASE_PY + CLOS_CURR_RA_IBNR_PY + CLOS_CURR_RA_LAE_PY) + (CLOS_CURR_BEL_CASE_CY + CLOS_CURR_BEL_IBNR_CY + CLOS_CURR_BEL_LAE_CY + CLOS_CURR_RA_CASE_CY + CLOS_CURR_RA_IBNR_CY + CLOS_CURR_RA_LAE_CY)",
                },
                "TOTAL": None,
            },
            "Closing insurance contract assets": {
                "LRC": {
                    "calculate": "(CLOS_CURR_BEL_OTH+CLOS_CURR_RA_OTH+CLOS_CSM)",
                    "expression": {
                        "condition": "< 0",
                        "replace": "sum",
                        "negative": True,
                    },
                    "negative": True,
                },
                "LC": None,
                "LIC": None,
                "TOTAL": None,
            },
            "Net balance as at 31 December (2)": {
                "index": 25,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[23]['Excluding_Loss_Component'] - result_df.iloc[24]['Excluding_Loss_Component']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[23]['Loss_Component'] - result_df.iloc[24]['Loss_Component']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[23]['LIC']  - result_df.iloc[24]['LIC']",
                },
                "TOTAL": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[23]['Total'] - result_df.iloc[24]['Total']",
                },
            },
        },
        "101_primary": {
            "Opening insurance contract liabilities": {
                "LRC": {
                    "calculate": "OPEN_CURR_BEL",
                    "expression": {
                        "condition": ">= 0",
                        "add_max": "OPEN_CURR_BEL_CASE_CY + OPEN_CURR_BEL_CASE_PY + OPEN_CURR_BEL_IBNR_CY + OPEN_INIT_BEL_IBNR_PY + OPEN_CURR_BEL_LAE_CY + OPEN_INIT_BEL_LAE_PY + OPEN_AOCI_RVNU_BEL_IBNR_PY + OPEN_AOCI_RVNU_BEL_LAE_PY + OPEN_AOCI_EXPNS_BEL_IBNR_PY + OPEN_AOCI_EXPNS_BEL_LAE_PY",
                    },
                },
                "LC": {
                    "calculate": "OPEN_CURR_RA",
                    "expression": {
                        "condition": ">= 0",
                        "add_max": "OPEN_CURR_RA_CASE_CY + OPEN_CURR_RA_CASE_PY + OPEN_CURR_RA_IBNR_CY + OPEN_INIT_RA_IBNR_PY + OPEN_CURR_RA_LAE_CY + OPEN_INIT_RA_LAE_PY + OPEN_AOCI_RVNU_RA_IBNR_PY + OPEN_AOCI_RVNU_RA_LAE_PY + OPEN_AOCI_EXPNS_RA_IBNR_PY + OPEN_AOCI_EXPNS_RA_LAE_PY",
                    },
                },
                "LIC": {
                    "calculate": "OPEN_CSM",
                },
                "TOTAL": None,
            },
            "Opening insurance contract assets": {
                "LRC": {
                    "calculate": "OPEN_CURR_BEL",
                    "expression": {
                        "condition": "< 0",
                        "add_max": "-(OPEN_CURR_BEL_CASE_CY + OPEN_CURR_BEL_CASE_PY + OPEN_CURR_BEL_IBNR_CY + OPEN_INIT_BEL_IBNR_PY + OPEN_CURR_BEL_LAE_CY + OPEN_INIT_BEL_LAE_PY + OPEN_AOCI_RVNU_BEL_IBNR_PY + OPEN_AOCI_RVNU_BEL_LAE_PY + OPEN_AOCI_EXPNS_BEL_IBNR_PY + OPEN_AOCI_EXPNS_BEL_LAE_PY)",
                    },
                },
                "LC": {
                    "calculate": "OPEN_CURR_RA",
                    "expression": {
                        "condition": "< 0",
                        "add_max": " -( OPEN_CURR_RA_CASE_CY + OPEN_CURR_RA_CASE_PY + OPEN_CURR_RA_IBNR_CY + OPEN_INIT_RA_IBNR_PY + OPEN_CURR_RA_LAE_CY + OPEN_INIT_RA_LAE_PY + OPEN_AOCI_RVNU_RA_IBNR_PY + OPEN_AOCI_RVNU_RA_LAE_PY + OPEN_AOCI_EXPNS_RA_IBNR_PY + OPEN_AOCI_EXPNS_RA_LAE_PY )",
                    },
                },
                "LIC": None,
                "TOTAL": None,
            },
            "Opening net balance": {
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[0]['Future_cash_flows'] - result_df.iloc[1]['Future_cash_flows']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[0]['Risk_adjustment'] - result_df.iloc[1]['Risk_adjustment']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[0]['CSM'] - result_df.iloc[1]['CSM']",
                },
                "TOTAL": None,
            },
            "Changes that relate to current service": {
                "header": True,
                "index": 3,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[4]['Future_cash_flows'] + result_df.iloc[5]['Future_cash_flows'] + result_df.iloc[6]['Future_cash_flows']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[4]['Risk_adjustment'] + result_df.iloc[5]['Risk_adjustment'] + result_df.iloc[6]['Risk_adjustment']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[4]['CSM'] + result_df.iloc[5]['CSM'] + result_df.iloc[6]['CSM']",
                },
                "TOTAL": None,
            },
            "CSM recognised in profit or loss for the services provided": {
                "LRC": None,
                "LC": None,
                "LIC": {
                    "calculate": "-CSM_AMORT",
                },
                "TOTAL": None,
            },
            "Change in the risk adjustment for non-financial risk for the risk expired": {
                "LRC": None,
                "LC": {
                    "calculate": "-EXP_RA_AMORT_OTH_RSP_WAP - EXP_RA_AMORT_LOSS_RSP_WAP",
                },
                "LIC": None,
                "TOTAL": None,
            },
            "Experience adjustments - relating to insurance service expenses": {
                "LRC": {
                    "calculate": "-(EXP_CLM_INSRC_OTH_RSP_WAP + EXP_DIR_ACQ_NPR_OTH_RSP_WAP + EXP_DIR_MNTNC_OTH_RSP_WAP + EXP_DIR_LAE_OTH_RSP_WAP + EXP_DIR_INVST_FEE_OTH_RSP_WAP+EXP_CLM_INSRC_LOSS_RSP_WAP + EXP_DIR_ACQ_NPR_LOSS_RSP_WAP + EXP_DIR_MNTNC_LOSS_RSP_WAP + EXP_DIR_LAE_LOSS_RSP_WAP + EXP_DIR_INVST_FEE_LOSS_RSP_WAP + EXP_DIR_ACQ_PR_LOSS_RSP_WAP) + CLOS_INIT_BEL_CASE_CY + CLOS_INIT_BEL_IBNR_CY + CLOS_INIT_BEL_LAE_CY -( ACTCF_CLM_INSRC_CY + ACTCF_DIR_LAE_CY) - (EXPCF_CLM_CASE_CY + EXPCF_CLM_IBNR_CY + EXPCF_LOSS_ADJ_EXPNS_CY) - ACTCF_DIR_MNTNC",
                },
                "LC": {
                    "calculate": "CLOS_INIT_RA_CASE_CY + CLOS_INIT_RA_IBNR_CY + CLOS_INIT_RA_LAE_CY - ( EXP_RA_AMORT_IBNR_CY +  EXP_RA_AMORT_CASE_CY + EXP_RA_AMORT_LAE_CY)",
                },
                "LIC": None,
                "TOTAL": None,
            },
            "Changes that relate to future service": {
                "header": True,
                "index": 7,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[8]['Future_cash_flows'] + result_df.iloc[9]['Future_cash_flows'] + result_df.iloc[10]['Future_cash_flows'] + result_df.iloc[11]['Future_cash_flows']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[8]['Risk_adjustment'] + result_df.iloc[9]['Risk_adjustment'] + result_df.iloc[10]['Risk_adjustment'] + result_df.iloc[11]['Risk_adjustment']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[8]['CSM'] + result_df.iloc[9]['CSM'] + result_df.iloc[10]['CSM'] + result_df.iloc[11]['CSM']",
                },
                "TOTAL": None,
            },
            "Changes in estimates that adjust the CSM": {
                "LRC": {
                    "calculate": "-INIT_BEL_OTH_RDP + INIT_BEL_OTH_PAP",
                },
                "LC": {
                    "calculate": "-INIT_RA_OTH_RDP + INIT_RA_OTH_PAP",
                },
                "LIC": {
                    "calculate": "-(-INIT_BEL_OTH_RDP + INIT_BEL_OTH_PAP - INIT_RA_OTH_RDP + INIT_RA_OTH_PAP)",
                },
                "TOTAL": None,
            },
            "Changes in estimates that result in onerous contract losses or reversal of losses": {
                "LRC": {
                    "calculate": "- INIT_BEL_LOSS_RDP + INIT_BEL_LOSS_PAP",
                },
                "LC": {
                    "calculate": "- INIT_RA_LOSS_RDP + INIT_RA_LOSS_PAP",
                },
                "LIC": {
                    "calculate": "-SUBS_LOSS_REVRSL + SUBS_LOSS_TRNSFR",
                },
                "TOTAL": None,
            },
            "Contracts initially recognised in the period": {
                "LRC": {
                    "calculate": "INCPT_INIT_BEL_LOSS_WAP_NB + INCPT_INIT_BEL_OTH_WAP_NB",
                },
                "LC": {
                    "calculate": "INCPT_INIT_RA_OTH_WAP_NB + INCPT_INIT_RA_LOSS_WAP_NB",
                },
                "LIC": {
                    "calculate": "INIT_CSM_WAP_NB",
                },
                "TOTAL": None,
            },
            "Experience adjustments - arising from premiums received in the period that relate to future service": {
                "LRC": {
                    "calculate": "-EXP_PREM_RSP_WAP - EXP_DIR_ACQ_PR_OTH_RSP_WAP",
                },
                "LC": None,
                "LIC": {
                    "calculate": "EXP_PREM_RSP_WAP + EXP_DIR_ACQ_PR_OTH_RSP_WAP",
                },
                "TOTAL": None,
            },
            "Changes that relate to past service": {
                "header": True,
                "index": 12,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[13]['Future_cash_flows'] + result_df.iloc[14]['Future_cash_flows']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[13]['Risk_adjustment'] + result_df.iloc[14]['Risk_adjustment']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[13]['CSM'] + result_df.iloc[14]['CSM']",
                },
                "TOTAL": None,
            },
            "Changes that relate to past service - changes in the FCF related to the LIC": {
                "LRC": {
                    "calculate": "ADJ_BEL_IBNR_PY + ADJ_BEL_CASE_PY + ADJ_BEL_LAE_PY - ( EXPCF_CLM_CASE_PY + EXPCF_CLM_IBNR_PY + EXPCF_LOSS_ADJ_EXPNS_PY)  - (ACTCF_CLM_INSRC_PY + ACTCF_DIR_LAE_PY)",
                },
                "LC": {
                    "calculate": "ADJ_RA_IBNR_PY + ADJ_RA_CASE_PY + ADJ_RA_LAE_PY - (EXP_RA_AMORT_IBNR_PY + EXP_RA_AMORT_CASE_PY + EXP_RA_AMORT_LAE_PY)",
                },
                "LIC": None,
                "TOTAL": None,
            },
            "Experience adjustments - arising from premiums received in the period that relate to past service": None,
            "Insurance service result": {
                "header": True,
                "index": 15,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[16]['Future_cash_flows'] + result_df.iloc[17]['Future_cash_flows']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[16]['Risk_adjustment'] + result_df.iloc[17]['Risk_adjustment']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[16]['CSM'] + result_df.iloc[17]['CSM']",
                },
                "TOTAL": None,
            },
            "Finance (income) expenses from insurance contracts issued": {
                "LRC": {
                    "calculate": "INTRST_EXPNS_RESET_BEL_RSP_WAP - INTRST_EXPNS_RESET_BEL_LOSS_RSP_WAP + INTRST_EXPNS_RESET_BEL_LOSS_RSP_WAP + (INTRST_EXPNS_BEL_IBNR_CY + INTRST_EXPNS_BEL_IBNR_PY) + (INTRST_EXPNS_BEL_CASE_CY + INTRST_EXPNS_BEL_CASE_PY) + (INTRST_EXPNS_BEL_LAE_CY + INTRST_EXPNS_BEL_LAE_PY)",
                },
                "LC": {
                    "calculate": "INTRST_EXPNS_RESET_RA_RSP_WAP - INTRST_EXPNS_RESET_RA_LOSS_RSP_WAP + INTRST_EXPNS_RESET_RA_LOSS_RSP_WAP + (INTRST_EXPNS_RA_IBNR_CY + INTRST_EXPNS_RA_IBNR_PY) + (INTRST_EXPNS_RA_CASE_CY + INTRST_EXPNS_RA_CASE_PY) + (INTRST_EXPNS_RA_LAE_CY + INTRST_EXPNS_RA_LAE_PY)",
                },
                "LIC": {
                    "calculate": "CSM_UNWND",
                },
                "TOTAL": None,
            },
            "Other changes": {
                "LRC": {
                    "calculate": "(CLOS_AOCI_EXPNS_BEL_OTH + CLOS_AOCI_RVNU_BEL_OTH) - (OPEN_AOCI_EXPNS_BEL_OTH + OPEN_AOCI_RVNU_BEL_OTH) + (CLOS_AOCI_EXPNS_BEL_LOSS + CLOS_AOCI_RVNU_BEL_LOSS) - (OPEN_AOCI_EXPNS_BEL_LOSS + OPEN_AOCI_RVNU_BEL_LOSS) + CLOS_AOCI_EXPNS_BEL_IBNR_PY + CLOS_AOCI_RVNU_BEL_IBNR_PY + CLOS_AOCI_EXPNS_BEL_CASE_PY + CLOS_AOCI_RVNU_BEL_CASE_PY + CLOS_AOCI_EXPNS_BEL_LAE_PY + CLOS_AOCI_RVNU_BEL_LAE_PY + CLOS_AOCI_EXPNS_BEL_IBNR_CY + CLOS_AOCI_RVNU_BEL_IBNR_CY + CLOS_AOCI_EXPNS_BEL_CASE_CY + CLOS_AOCI_RVNU_BEL_CASE_CY + CLOS_AOCI_EXPNS_BEL_LAE_CY + CLOS_AOCI_RVNU_BEL_LAE_CY - (OPEN_AOCI_EXPNS_BEL_CASE_CY + OPEN_AOCI_EXPNS_BEL_CASE_PY + OPEN_AOCI_EXPNS_BEL_IBNR_CY + OPEN_AOCI_EXPNS_BEL_IBNR_PY + OPEN_AOCI_EXPNS_BEL_LAE_CY + OPEN_AOCI_EXPNS_BEL_LAE_PY + OPEN_AOCI_RVNU_BEL_CASE_CY + OPEN_AOCI_RVNU_BEL_CASE_PY + OPEN_AOCI_RVNU_BEL_IBNR_CY + OPEN_AOCI_RVNU_BEL_LAE_CY + OPEN_AOCI_RVNU_BEL_IBNR_PY + OPEN_AOCI_RVNU_BEL_LAE_PY)",
                },
                "LC": {
                    "calculate": " (CLOS_AOCI_EXPNS_RA_OTH + CLOS_AOCI_RVNU_RA_OTH) - (OPEN_AOCI_EXPNS_RA_OTH + OPEN_AOCI_RVNU_RA_OTH) + (CLOS_AOCI_EXPNS_RA_LOSS + CLOS_AOCI_RVNU_RA_LOSS) - (OPEN_AOCI_EXPNS_RA_LOSS + OPEN_AOCI_RVNU_RA_LOSS) + CLOS_AOCI_EXPNS_RA_IBNR_PY + CLOS_AOCI_RVNU_RA_IBNR_PY + CLOS_AOCI_EXPNS_RA_CASE_PY + CLOS_AOCI_RVNU_RA_CASE_PY + CLOS_AOCI_EXPNS_RA_LAE_PY + CLOS_AOCI_RVNU_RA_LAE_PY + CLOS_AOCI_EXPNS_RA_IBNR_CY + CLOS_AOCI_RVNU_RA_IBNR_CY + CLOS_AOCI_EXPNS_RA_CASE_CY + CLOS_AOCI_RVNU_RA_CASE_CY + CLOS_AOCI_EXPNS_RA_LAE_CY + CLOS_AOCI_RVNU_RA_LAE_CY - (OPEN_AOCI_EXPNS_RA_CASE_CY + OPEN_AOCI_EXPNS_RA_CASE_PY + OPEN_AOCI_EXPNS_RA_IBNR_CY + OPEN_AOCI_EXPNS_RA_IBNR_PY + OPEN_AOCI_EXPNS_RA_LAE_CY + OPEN_AOCI_EXPNS_RA_LAE_PY + OPEN_AOCI_RVNU_RA_CASE_CY + OPEN_AOCI_RVNU_RA_CASE_PY + OPEN_AOCI_RVNU_RA_IBNR_CY + OPEN_AOCI_RVNU_RA_LAE_CY + OPEN_AOCI_RVNU_RA_IBNR_PY + OPEN_AOCI_RVNU_RA_LAE_PY)",
                },
                "LIC": None,
                "TOTAL": None,
            },
            "Total amounts recognised in comprehensive income": {
                "header": True,
                "index": 18,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[15]['Future_cash_flows'] + result_df.iloc[12]['Future_cash_flows'] + result_df.iloc[7]['Future_cash_flows'] + result_df.iloc[3]['Future_cash_flows']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[15]['Risk_adjustment'] + result_df.iloc[12]['Risk_adjustment'] + result_df.iloc[7]['Risk_adjustment'] + result_df.iloc[3]['Risk_adjustment']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[15]['CSM'] + result_df.iloc[12]['CSM'] + result_df.iloc[7]['CSM'] + result_df.iloc[3]['CSM']",
                },
                "TOTAL": None,
            },
            "Other changes (2)": None,
            "Cash flows": {
                "header": True,
                "index": 20,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[21]['Future_cash_flows'] + result_df.iloc[22]['Future_cash_flows'] + result_df.iloc[23]['Future_cash_flows']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[21]['Risk_adjustment'] + result_df.iloc[22]['Risk_adjustment'] + result_df.iloc[23]['Risk_adjustment']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[21]['CSM'] + result_df.iloc[22]['CSM'] + result_df.iloc[23]['CSM']",
                },
                "TOTAL": None,
            },
            "Premiums received": {
                "LRC": None,
                "LC": None,
                "LIC": {
                    "calculate": "ACTCF_PREM",
                },
                "TOTAL": None,
            },
            "Claims and other directly attributable expenses paid": {
                "LRC": {
                    "calculate": "ACTCF_CLM_INSRC_PY + ACTCF_DIR_LAE_PY + ACTCF_CLM_INSRC_CY + ACTCF_DIR_LAE_CY + ACTCF_DIR_MNTNC",
                },
                "LC": None,
                "LIC": None,
                "TOTAL": None,
            },
            "Insurance acquisition cash flows": {
                "LRC": None,
                "LC": None,
                "LIC": {
                    "calculate": "ACTCF_DIR_ACQ_PR",
                },
                "TOTAL": None,
            },
            "Total cash flows": {
                "header": True,
                "index": 24,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[20]['Future_cash_flows']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[20]['Risk_adjustment']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[20]['CSM']",
                },
                "TOTAL": None,
            },
            "Closing net balance": {
                "index": 25,
            },
            "Closing insurance contract liabilities": {
                "LRC": {
                    "calculate": "(CLOS_CURR_BEL_OTH + CLOS_CURR_BEL_LOSS)",
                    "expression": {
                        "condition": ">= 0",
                        "add_max": "CLOS_CURR_BEL_CASE_PY + CLOS_CURR_BEL_IBNR_PY + CLOS_CURR_BEL_LAE_PY + CLOS_CURR_BEL_CASE_CY + CLOS_CURR_BEL_IBNR_CY + CLOS_CURR_BEL_LAE_CY",
                    },
                },
                "LC": {
                    "calculate": "(CLOS_CURR_RA_OTH + CLOS_CURR_RA_LOSS)",
                    "expression": {
                        "condition": ">= 0",
                        "add_max": "CLOS_CURR_RA_CASE_PY + CLOS_CURR_RA_IBNR_PY + CLOS_CURR_RA_LAE_PY + CLOS_CURR_RA_CASE_CY + CLOS_CURR_RA_IBNR_CY + CLOS_CURR_RA_LAE_CY",
                    },
                },
                "LIC": {
                    "calculate": "CLOS_CSM",
                },
                "TOTAL": None,
            },
            "Closing insurance contract assets": {
                "LRC": {
                    "calculate": "(CLOS_CURR_BEL_OTH + CLOS_CURR_BEL_LOSS)",
                    "expression": {
                        "condition": "< 0",
                        "add_max": "-(CLOS_CURR_BEL_CASE_PY + CLOS_CURR_BEL_IBNR_PY + CLOS_CURR_BEL_LAE_PY + CLOS_CURR_BEL_CASE_CY + CLOS_CURR_BEL_IBNR_CY + CLOS_CURR_BEL_LAE_CY)",
                    },
                },
                "LC": {
                    "calculate": "(CLOS_CURR_RA_OTH + CLOS_CURR_RA_LOSS)",
                    "expression": {
                        "condition": "< 0",
                        "add_max": "-(CLOS_CURR_RA_CASE_PY + CLOS_CURR_RA_IBNR_PY + CLOS_CURR_RA_LAE_PY + CLOS_CURR_RA_CASE_CY + CLOS_CURR_RA_IBNR_CY + CLOS_CURR_RA_LAE_CY)",
                    },
                },
                "LIC": {
                    "auto-fill": "",
                },
                "TOTAL": None,
            },
            "Closing net balance (2)": {
                "index": 28,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[26]['Future_cash_flows'] - result_df.iloc[27]['Future_cash_flows']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[26]['Risk_adjustment'] - result_df.iloc[27]['Risk_adjustment']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[26]['CSM'] - result_df.iloc[27]['CSM']",
                },
                "TOTAL": None,
            },
        },
    },
    "IFRS17_BBA_Reinsurance_Movement": {
        "100_primary": {
            "Opening reinsurance contract assets": {
                "LRC": {
                    "calculate": " -(OPEN_CURR_BEL_OTH + OPEN_CURR_CRDT_RISK_OTH + OPEN_INIT_RA_OTH - OPEN_AOCI_RVNU_RA_OTH + OPEN_AOCI_EXPNS_RA_OTH + OPEN_CSM)",
                    "expression": {
                        "condition": "> 0",
                    },
                },
                "LC": None,
                "LIC": {
                    "calculate": "( OPEN_CURR_RE_BEA_CASE_CY + OPEN_CURR_RE_BEA_CASE_PY + OPEN_CURR_RE_BEA_IBNR_CY + OPEN_INIT_RE_BEA_IBNR_PY + OPEN_CURR_RE_BEA_LAE_CY + OPEN_INIT_RE_BEA_LAE_PY - (OPEN_CURR_RE_CRDT_RISK_CASE_CY + OPEN_CURR_RE_CRDT_RISK_CASE_PY + OPEN_CURR_RE_CRDT_RISK_IBNR_CY + OPEN_INIT_RE_CRDT_RISK_IBNR_PY + OPEN_CURR_RE_CRDT_RISK_LAE_CY + OPEN_INIT_RE_CRDT_RISK_LAE_PY) + OPEN_CURR_RE_RA_CASE_CY + OPEN_CURR_RE_RA_CASE_PY + OPEN_CURR_RE_RA_IBNR_CY + OPEN_INIT_RE_RA_IBNR_PY + OPEN_CURR_RE_RA_LAE_CY + OPEN_INIT_RE_RA_LAE_PY + OPEN_AOCI_RVNU_RE_BEA_IBNR_PY + OPEN_AOCI_RVNU_RE_BEA_LAE_PY - OPEN_AOCI_RVNU_RE_CRDT_RISK_IBNR_PY - OPEN_AOCI_RVNU_RE_CRDT_RISK_LAE_PY + OPEN_AOCI_RVNU_RE_RA_IBNR_PY + OPEN_AOCI_RVNU_RE_RA_LAE_PY + OPEN_AOCI_EXPNS_RE_BEA_IBNR_PY + OPEN_AOCI_EXPNS_RE_BEA_LAE_PY - OPEN_AOCI_EXPNS_RE_CRDT_RISK_IBNR_PY - OPEN_AOCI_EXPNS_RE_CRDT_RISK_LAE_PY + OPEN_AOCI_EXPNS_RE_RA_IBNR_PY + OPEN_AOCI_EXPNS_RE_RA_LAE_PY)",
                    "expression": {
                        "condition": "> 0",
                    },
                },
                "TOTAL": None,
            },
            "Opening reinsurance contract liabilities": {
                "LRC": {
                    "calculate": "(OPEN_CURR_BEL_OTH + OPEN_CURR_CRDT_RISK_OTH + OPEN_INIT_RA_OTH - OPEN_AOCI_RVNU_RA_OTH + OPEN_AOCI_EXPNS_RA_OTH + OPEN_CSM)",
                    "expression": {
                        "condition": "> 0",
                    },
                },
                "LC": None,
                "LIC": {
                    "calculate": "- ( OPEN_CURR_RE_BEA_CASE_CY + OPEN_CURR_RE_BEA_CASE_PY + OPEN_CURR_RE_BEA_IBNR_CY + OPEN_INIT_RE_BEA_IBNR_PY + OPEN_CURR_RE_BEA_LAE_CY + OPEN_INIT_RE_BEA_LAE_PY - (OPEN_CURR_RE_CRDT_RISK_CASE_CY + OPEN_CURR_RE_CRDT_RISK_CASE_PY + OPEN_CURR_RE_CRDT_RISK_IBNR_CY + OPEN_INIT_RE_CRDT_RISK_IBNR_PY + OPEN_CURR_RE_CRDT_RISK_LAE_CY + OPEN_INIT_RE_CRDT_RISK_LAE_PY) + OPEN_CURR_RE_RA_CASE_CY + OPEN_CURR_RE_RA_CASE_PY + OPEN_CURR_RE_RA_IBNR_CY + OPEN_INIT_RE_RA_IBNR_PY + OPEN_CURR_RE_RA_LAE_CY + OPEN_INIT_RE_RA_LAE_PY + OPEN_AOCI_RVNU_RE_BEA_IBNR_PY + OPEN_AOCI_RVNU_RE_BEA_LAE_PY - OPEN_AOCI_RVNU_RE_CRDT_RISK_IBNR_PY - OPEN_AOCI_RVNU_RE_CRDT_RISK_LAE_PY + OPEN_AOCI_RVNU_RE_RA_IBNR_PY + OPEN_AOCI_RVNU_RE_RA_LAE_PY + OPEN_AOCI_EXPNS_RE_BEA_IBNR_PY + OPEN_AOCI_EXPNS_RE_BEA_LAE_PY - OPEN_AOCI_EXPNS_RE_CRDT_RISK_IBNR_PY - OPEN_AOCI_EXPNS_RE_CRDT_RISK_LAE_PY + OPEN_AOCI_EXPNS_RE_RA_IBNR_PY + OPEN_AOCI_EXPNS_RE_RA_LAE_PY)",
                    "expression": {
                        "condition": "> 0",
                    },
                },
                "TOTAL": None,
            },
            "Net balance as at 1 January": {
                "index": 2,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[0]['Excluding_loss_recovery'] - result_df.iloc[1]['Excluding_loss_recovery']",
                },
                "LC": None,
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[0]['AIC'] - result_df.iloc[1]['AIC']",
                },
                "TOTAL": None,
            },
            "Net income (expenses) from reinsurance contracts held": {
                "header": True,
                "index": 3,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[4]['Excluding_loss_recovery'] + result_df.iloc[5]['Excluding_loss_recovery'] + result_df.iloc[6]['Excluding_loss_recovery'] + result_df.iloc[7]['Excluding_loss_recovery'] + result_df.iloc[8]['Excluding_loss_recovery'] + result_df.iloc[9]['Excluding_loss_recovery'] + result_df.iloc[10]['Excluding_loss_recovery'] + result_df.iloc[11]['Excluding_loss_recovery'] + result_df.iloc[12]['Excluding_loss_recovery']",
                },
                "LC": None,
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[4]['AIC'] + result_df.iloc[5]['AIC'] + result_df.iloc[6]['AIC'] + result_df.iloc[7]['AIC'] + result_df.iloc[8]['AIC'] + result_df.iloc[9]['AIC'] + result_df.iloc[10]['AIC'] + result_df.iloc[11]['AIC'] + result_df.iloc[12]['AIC']",
                },
                "TOTAL": None,
            },
            "Reinsurance expenses": {
                "LRC": {
                    "calculate": "EXP_CLM_INSRC_RNC_RWU + EXP_LAE_OTH_RNC_RWU + EXP_CRDT_LOSS_RNC_RWU - EXP_RA_AMORT_OTH_RNC_RWU + CSM_AMORT",
                },
                "LC": None,
                "LIC": None,
                "TOTAL": None,
            },
            "Other incurred directly attributable expenses": {
                "LRC": None,
                "LC": None,
                "LIC": {
                    "calculate": "( CLOS_INIT_RE_BEA_CASE_CY + CLOS_INIT_RE_BEA_IBNR_CY + CLOS_INIT_RE_BEA_LAE_CY - CLOS_INIT_RE_CRDT_RISK_CASE_CY - CLOS_INIT_RE_CRDT_RISK_IBNR_CY - CLOS_INIT_RE_CRDT_RISK_LAE_CY + CLOS_INIT_RE_RA_CASE_CY + CLOS_INIT_RE_RA_IBNR_CY + CLOS_INIT_RE_RA_LAE_CY ) + ACTCF_CLM_INSRC_CY",
                },
                "TOTAL": None,
            },
            "Incurred claims recovery": None,
            "Changes that relate to past service - changes in the FCF relating to incurred claims recovery": {
                "LRC": None,
                "LC": None,
                "LIC": {
                    "calculate": "ADJ_RE_BEA_IBNR_PY + ADJ_RE_BEA_CASE_PY + ADJ_RE_BEA_LAE_PY + - ADJ_RE_CRDT_RISK_IBNR_PY + - ADJ_RE_CRDT_RISK_CASE_PY + - ADJ_RE_CRDT_RISK_LAE_PY + ADJ_RE_RA_IBNR_PY + ADJ_RE_RA_CASE_PY + ADJ_RE_RA_LAE_PY + -( EXPCF_CLM_IBNR_CY + EXPCF_CLM_IBNR_PY ) + -( EXPCF_CLM_CASE_CY + EXPCF_CLM_CASE_PY ) + -( EXPCF_LOSS_ADJ_EXPNS_CY + EXPCF_LOSS_ADJ_EXPNS_PY ) + ( EXPCF_CRDT_LOSS_IBNR_CY + EXPCF_CRDT_LOSS_IBNR_PY ) + ( EXPCF_CRDT_LOSS_CASE_CY + EXPCF_CRDT_LOSS_CASE_PY ) + ( EXPCF_CRDT_LOSS_LAE_CY + EXPCF_CRDT_LOSS_LAE_PY) + -( EXP_RA_AMORT_IBNR_CY + EXP_RA_AMORT_IBNR_PY ) + -( EXP_RA_AMORT_CASE_CY + EXP_RA_AMORT_CASE_PY ) + -( EXP_RA_AMORT_LAE_CY + EXP_RA_AMORT_LAE_PY ) + ACTCF_CLM_INSRC_PY",
                },
                "TOTAL": None,
            },
            "Income on initial recognition of onerous underlying contracts": None,
            "Reversals of a loss-recovery component other than changes in the FCF of reinsurance contracts held": None,
            "Changes in the FCF of reinsurance contracts held from onerous underlying contracts": None,
            "Effect of changes in the risk of reinsurers": {
                "LRC": {
                    "calculate": "- (RESET_CRDT_RISK_OTH_RPA - EXP_CLOS_RESET_CRDT_RISK_OTH_RNC_RWU)",
                },
                "LC": None,
                "LIC": None,
                "TOTAL": None,
            },
            "Cost of retroactive cover for reinsurance contracts held": None,
            "Net income (expenses) from reinsurance contracts held (2)": {
                "header": True,
                "index": 13,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[14]['Excluding_loss_recovery'] + result_df.iloc[15]['Excluding_loss_recovery']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[14]['Loss_recovery'] + result_df.iloc[15]['Loss_recovery']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[14]['AIC'] + result_df.iloc[15]['AIC']",
                },
                "TOTAL": None,
            },
            "Finance income (expenses) from reinsurance contracts held": {
                "LRC": {
                    "calculate": "-(INTRST_EXPNS_RESET_BEL_RNC_RWU + INTRST_EXPNS_RESET_CRDT_RISK_RNC_RWU + INTRST_EXPNS_RESET_RA_RNC_RWU + CSM_UNWND)",
                },
                "LC": None,
                "LIC": {
                    "calculate": "( INTRST_EXPNS_RE_BEA_IBNR_CY + INTRST_EXPNS_RE_BEA_IBNR_PY ) + ( INTRST_EXPNS_RE_BEA_CASE_CY + INTRST_EXPNS_RE_BEA_CASE_PY ) + ( INTRST_EXPNS_RE_BEA_LAE_CY + INTRST_EXPNS_RE_BEA_LAE_PY ) + - ( INTRST_EXPNS_RE_CRDT_RISK_IBNR_CY + INTRST_EXPNS_RE_CRDT_RISK_IBNR_PY ) + - ( INTRST_EXPNS_RE_CRDT_RISK_CASE_CY + INTRST_EXPNS_RE_CRDT_RISK_CASE_PY ) + - ( INTRST_EXPNS_RE_CRDT_RISK_LAE_CY + INTRST_EXPNS_RE_CRDT_RISK_LAE_PY) + ( INTRST_EXPNS_RE_RA_IBNR_CY + INTRST_EXPNS_RE_RA_IBNR_PY ) + ( INTRST_EXPNS_RE_RA_CASE_CY + INTRST_EXPNS_RE_RA_CASE_PY ) + ( INTRST_EXPNS_RE_RA_LAE_CY + INTRST_EXPNS_RE_RA_LAE_PY )",
                },
                "TOTAL": None,
            },
            "Other changes": {
                "LRC": {
                    "calculate": "-(CLOS_AOCI_EXPNS_BEL_OTH - CLOS_AOCI_RVNU_BEL_OTH) - (CLOS_AOCI_EXPNS_CRDT_RISK_OTH - CLOS_AOCI_RVNU_CRDT_RISK_OTH) - (CLOS_AOCI_EXPNS_RA_OTH - CLOS_AOCI_RVNU_RA_OTH) + (OPEN_AOCI_EXPNS_BEL_OTH - OPEN_AOCI_RVNU_BEL_OTH) + (OPEN_AOCI_EXPNS_CRDT_RISK_OTH - OPEN_AOCI_RVNU_CRDT_RISK_OTH) + (OPEN_AOCI_EXPNS_RA_OTH - OPEN_AOCI_RVNU_RA_OTH)",
                },
                "LC": None,
                "LIC": {
                    "calculate": "-(OPEN_AOCI_RVNU_RE_BEA_IBNR_CY + OPEN_AOCI_RVNU_RE_BEA_IBNR_PY + OPEN_AOCI_EXPNS_RE_BEA_IBNR_CY + OPEN_AOCI_EXPNS_RE_BEA_IBNR_PY ) + - (OPEN_AOCI_RVNU_RE_BEA_CASE_CY + OPEN_AOCI_RVNU_RE_BEA_CASE_PY + OPEN_AOCI_EXPNS_RE_BEA_CASE_CY + OPEN_AOCI_EXPNS_RE_BEA_CASE_PY) + - (OPEN_AOCI_RVNU_RE_BEA_LAE_CY + OPEN_AOCI_RVNU_RE_BEA_LAE_PY + OPEN_AOCI_EXPNS_RE_BEA_LAE_CY + OPEN_AOCI_EXPNS_RE_BEA_LAE_PY) + (OPEN_AOCI_RVNU_RE_CRDT_RISK_IBNR_CY + OPEN_AOCI_RVNU_RE_CRDT_RISK_IBNR_PY + OPEN_AOCI_EXPNS_RE_CRDT_RISK_IBNR_CY + OPEN_AOCI_EXPNS_RE_CRDT_RISK_IBNR_PY ) + (OPEN_AOCI_RVNU_RE_CRDT_RISK_CASE_CY + OPEN_AOCI_RVNU_RE_CRDT_RISK_CASE_PY + OPEN_AOCI_EXPNS_RE_CRDT_RISK_CASE_CY + OPEN_AOCI_EXPNS_RE_CRDT_RISK_CASE_PY) + (OPEN_AOCI_RVNU_RE_CRDT_RISK_LAE_CY + OPEN_AOCI_RVNU_RE_CRDT_RISK_LAE_PY + OPEN_AOCI_EXPNS_RE_CRDT_RISK_LAE_CY + OPEN_AOCI_EXPNS_RE_CRDT_RISK_LAE_PY) + - (OPEN_AOCI_RVNU_RE_RA_IBNR_CY + OPEN_AOCI_RVNU_RE_RA_IBNR_PY + OPEN_AOCI_EXPNS_RE_RA_IBNR_CY + OPEN_AOCI_EXPNS_RE_RA_IBNR_PY ) + - (OPEN_AOCI_RVNU_RE_RA_CASE_CY + OPEN_AOCI_RVNU_RE_RA_CASE_PY + OPEN_AOCI_EXPNS_RE_RA_CASE_CY + OPEN_AOCI_EXPNS_RE_RA_CASE_PY) + - (OPEN_AOCI_RVNU_RE_RA_LAE_CY + OPEN_AOCI_RVNU_RE_RA_LAE_PY + OPEN_AOCI_EXPNS_RE_RA_LAE_CY + OPEN_AOCI_EXPNS_RE_RA_LAE_PY) + CLOS_AOCI_RVNU_RE_BEA_IBNR_PY + CLOS_AOCI_EXPNS_RE_BEA_IBNR_PY + CLOS_AOCI_RVNU_RE_BEA_CASE_PY + CLOS_AOCI_EXPNS_RE_BEA_CASE_PY + CLOS_AOCI_RVNU_RE_BEA_LAE_PY + CLOS_AOCI_EXPNS_RE_BEA_LAE_PY + -(CLOS_AOCI_RVNU_RE_CRDT_RISK_IBNR_PY + CLOS_AOCI_EXPNS_RE_CRDT_RISK_IBNR_PY) + -(CLOS_AOCI_RVNU_RE_CRDT_RISK_CASE_PY + CLOS_AOCI_EXPNS_RE_CRDT_RISK_CASE_PY) + -(CLOS_AOCI_RVNU_RE_CRDT_RISK_LAE_PY + CLOS_AOCI_EXPNS_RE_CRDT_RISK_LAE_PY) + CLOS_AOCI_RVNU_RE_RA_IBNR_PY + CLOS_AOCI_EXPNS_RE_RA_IBNR_PY + CLOS_AOCI_RVNU_RE_RA_CASE_PY + CLOS_AOCI_EXPNS_RE_RA_CASE_PY + CLOS_AOCI_RVNU_RE_RA_LAE_PY + CLOS_AOCI_EXPNS_RE_RA_LAE_PY + CLOS_AOCI_RVNU_RE_BEA_IBNR_CY + CLOS_AOCI_EXPNS_RE_BEA_IBNR_CY + CLOS_AOCI_RVNU_RE_BEA_CASE_CY + CLOS_AOCI_EXPNS_RE_BEA_CASE_CY + CLOS_AOCI_RVNU_RE_BEA_LAE_CY + CLOS_AOCI_EXPNS_RE_BEA_LAE_CY + -(CLOS_AOCI_RVNU_RE_CRDT_RISK_IBNR_CY + CLOS_AOCI_EXPNS_RE_CRDT_RISK_IBNR_CY) + -(CLOS_AOCI_RVNU_RE_CRDT_RISK_CASE_CY + CLOS_AOCI_EXPNS_RE_CRDT_RISK_CASE_CY) + -(CLOS_AOCI_RVNU_RE_CRDT_RISK_LAE_CY + CLOS_AOCI_EXPNS_RE_CRDT_RISK_LAE_CY) + CLOS_AOCI_RVNU_RE_RA_IBNR_CY + CLOS_AOCI_EXPNS_RE_RA_IBNR_CY + CLOS_AOCI_RVNU_RE_RA_CASE_CY + CLOS_AOCI_EXPNS_RE_RA_CASE_CY + CLOS_AOCI_RVNU_RE_RA_LAE_CY + CLOS_AOCI_EXPNS_RE_RA_LAE_CY",
                },
                "TOTAL": None,
            },
            "Total amounts recognised in comprehensive income": {
                "header": True,
                "index": 16,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[17]['Excluding_loss_recovery']",
                },
                "LC": None,
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[17]['AIC']",
                },
                "TOTAL": None,
            },
            "Investment components": None,
            "Other changes (2)": None,
            "Cash flows": {
                "header": True,
                "index": 19,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[19]['Excluding_loss_recovery'] + result_df.iloc[20]['Excluding_loss_recovery'] + result_df.iloc[21]['Excluding_loss_recovery']",
                },
                "LC": None,
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[19]['AIC'] + result_df.iloc[20]['AIC'] + result_df.iloc[21]['AIC']",
                },
                "TOTAL": None,
            },
            "Premiums paid net of ceding commissions and other directly attributable expenses paid": {
                "LRC": {
                    "calculate": "(ACTCF_PREM - ACTCF_RE_COMM)",
                },
                "LC": None,
                "LIC": None,
                "TOTAL": None,
            },
            "Recoveries from reinsurance": {
                "LRC": None,
                "LC": None,
                "LIC": {
                    "calculate": "-( ACTCF_CLM_INSRC_CY + ACTCF_CLM_INSRC_PY )",
                },
                "TOTAL": None,
            },
            "Total cash flows": None,
            "Net balance as at 31 December": {
                "index": 23,
            },
            "Closing reinsurance contract assets": {
                "LRC": {
                    "calculate": "-(CLOS_CURR_BEL_OTH + CLOS_CURR_CRDT_RISK_OTH + CLOS_CURR_RA_OTH + CLOS_CSM)",
                    "expression": {
                        "condition": "> 0",
                    },
                },
                "LC": None,
                "LIC": {
                    "calculate": "( CLOS_CURR_RE_BEA_CASE_CY + CLOS_CURR_RE_BEA_CASE_PY + CLOS_CURR_RE_BEA_IBNR_CY + CLOS_CURR_RE_BEA_IBNR_PY + CLOS_CURR_RE_BEA_LAE_CY + CLOS_CURR_RE_BEA_LAE_PY - (CLOS_CURR_RE_CRDT_RISK_CASE_CY + CLOS_CURR_RE_CRDT_RISK_CASE_PY + CLOS_CURR_RE_CRDT_RISK_IBNR_CY + CLOS_CURR_RE_CRDT_RISK_IBNR_PY + CLOS_CURR_RE_CRDT_RISK_LAE_CY + CLOS_CURR_RE_CRDT_RISK_LAE_PY) + CLOS_CURR_RE_RA_CASE_CY + CLOS_CURR_RE_RA_CASE_PY + CLOS_CURR_RE_RA_IBNR_CY + CLOS_CURR_RE_RA_IBNR_PY + CLOS_CURR_RE_RA_LAE_CY + CLOS_CURR_RE_RA_LAE_PY )",
                    "expression": {
                        "condition": "> 0",
                    },
                },
                "TOTAL": None,
            },
            "Closing reinsurance contract liabilities": {
                "LRC": {
                    "calculate": "(CLOS_CURR_BEL_OTH + CLOS_CURR_CRDT_RISK_OTH + CLOS_CURR_RA_OTH + CLOS_CSM)",
                    "expression": {
                        "condition": "> 0",
                    },
                },
                "LC": None,
                "LIC": {
                    "calculate": "-( CLOS_CURR_RE_BEA_CASE_CY + CLOS_CURR_RE_BEA_CASE_PY + CLOS_CURR_RE_BEA_IBNR_CY + CLOS_CURR_RE_BEA_IBNR_PY + CLOS_CURR_RE_BEA_LAE_CY + CLOS_CURR_RE_BEA_LAE_PY - (CLOS_CURR_RE_CRDT_RISK_CASE_CY + CLOS_CURR_RE_CRDT_RISK_CASE_PY + CLOS_CURR_RE_CRDT_RISK_IBNR_CY + CLOS_CURR_RE_CRDT_RISK_IBNR_PY + CLOS_CURR_RE_CRDT_RISK_LAE_CY + CLOS_CURR_RE_CRDT_RISK_LAE_PY) + CLOS_CURR_RE_RA_CASE_CY + CLOS_CURR_RE_RA_CASE_PY + CLOS_CURR_RE_RA_IBNR_CY + CLOS_CURR_RE_RA_IBNR_PY + CLOS_CURR_RE_RA_LAE_CY + CLOS_CURR_RE_RA_LAE_PY )",
                    "expression": {
                        "condition": "> 0",
                    },
                },
                "TOTAL": None,
            },
            "Net balance as at 31 December (2)": {
                "index": 26,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[24]['Excluding_loss_recovery'] - result_df.iloc[25]['Excluding_loss_recovery']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[24]['Loss_recovery'] - result_df.iloc[25]['Loss_recovery']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[24]['AIC'] - result_df.iloc[25]['AIC']",
                },
                "TOTAL": None,
            },
        },
        "101_primary": {
            "Opening reinsurance contract assets": {
                "LRC": {
                    "calculate": "-(OPEN_CURR_BEL_OTH + OPEN_CURR_CRDT_RISK_OTH)",
                    "expression": {
                        "condition": "> 0",
                        "add_max": " (OPEN_CURR_RE_BEA_CASE_CY + OPEN_CURR_RE_BEA_CASE_PY + OPEN_CURR_RE_BEA_IBNR_CY + OPEN_INIT_RE_BEA_IBNR_PY + OPEN_CURR_RE_BEA_LAE_CY + OPEN_INIT_RE_BEA_LAE_PY - (OPEN_CURR_RE_CRDT_RISK_CASE_CY + OPEN_CURR_RE_CRDT_RISK_CASE_PY + OPEN_CURR_RE_CRDT_RISK_IBNR_CY + OPEN_INIT_RE_CRDT_RISK_IBNR_PY + OPEN_CURR_RE_CRDT_RISK_LAE_CY + OPEN_INIT_RE_CRDT_RISK_LAE_PY) + OPEN_AOCI_RVNU_RE_BEA_IBNR_PY + OPEN_AOCI_RVNU_RE_BEA_LAE_PY - OPEN_AOCI_RVNU_RE_CRDT_RISK_IBNR_PY - OPEN_AOCI_RVNU_RE_CRDT_RISK_LAE_PY + OPEN_AOCI_EXPNS_RE_BEA_IBNR_PY + OPEN_AOCI_EXPNS_RE_BEA_LAE_PY - OPEN_AOCI_EXPNS_RE_CRDT_RISK_IBNR_PY - OPEN_AOCI_EXPNS_RE_CRDT_RISK_LAE_PY)",
                    },
                },
                "LC": {
                    "calculate": "-(OPEN_INIT_RA_OTH - OPEN_AOCI_RVNU_RA_OTH + OPEN_AOCI_EXPNS_RA_OTH )",
                    "expression": {
                        "condition": "> 0",
                        "add_max": "(OPEN_CURR_RE_RA_CASE_CY + OPEN_CURR_RE_RA_CASE_PY + OPEN_CURR_RE_RA_IBNR_CY + OPEN_INIT_RE_RA_IBNR_PY + OPEN_CURR_RE_RA_LAE_CY + OPEN_INIT_RE_RA_LAE_PY + OPEN_AOCI_RVNU_RE_RA_IBNR_PY + OPEN_AOCI_RVNU_RE_RA_LAE_PY + OPEN_AOCI_EXPNS_RE_RA_IBNR_PY + OPEN_AOCI_EXPNS_RE_RA_LAE_PY)",
                    },
                },
                "LIC": {
                    "calculate": "-(OPEN_CSM)",
                    "expression": {
                        "condition": "> 0",
                    },
                },
                "TOTAL": None,
            },
            "Opening reinsurance contract liabilities": {
                "LRC": {
                    "calculate": "(OPEN_CURR_BEL_OTH + OPEN_CURR_CRDT_RISK_OTH)",
                    "expression": {
                        "condition": "> 0",
                        "add_max": " -( OPEN_CURR_RE_BEA_CASE_CY + OPEN_CURR_RE_BEA_CASE_PY + OPEN_CURR_RE_BEA_IBNR_CY + OPEN_INIT_RE_BEA_IBNR_PY + OPEN_CURR_RE_BEA_LAE_CY + OPEN_INIT_RE_BEA_LAE_PY - (OPEN_CURR_RE_CRDT_RISK_CASE_CY + OPEN_CURR_RE_CRDT_RISK_CASE_PY + OPEN_CURR_RE_CRDT_RISK_IBNR_CY + OPEN_INIT_RE_CRDT_RISK_IBNR_PY + OPEN_CURR_RE_CRDT_RISK_LAE_CY + OPEN_INIT_RE_CRDT_RISK_LAE_PY) + OPEN_AOCI_RVNU_RE_BEA_IBNR_PY + OPEN_AOCI_RVNU_RE_BEA_LAE_PY - OPEN_AOCI_RVNU_RE_CRDT_RISK_IBNR_PY - OPEN_AOCI_RVNU_RE_CRDT_RISK_LAE_PY + OPEN_AOCI_EXPNS_RE_BEA_IBNR_PY + OPEN_AOCI_EXPNS_RE_BEA_LAE_PY - OPEN_AOCI_EXPNS_RE_CRDT_RISK_IBNR_PY - OPEN_AOCI_EXPNS_RE_CRDT_RISK_LAE_PY)",
                    },
                },
                "LC": {
                    "calculate": "(OPEN_INIT_RA_OTH - OPEN_AOCI_RVNU_RA_OTH + OPEN_AOCI_EXPNS_RA_OTH)",
                    "expression": {
                        "condition": "> 0",
                        "add_max": "-(OPEN_CURR_RE_RA_CASE_CY + OPEN_CURR_RE_RA_CASE_PY + OPEN_CURR_RE_RA_IBNR_CY + OPEN_INIT_RE_RA_IBNR_PY + OPEN_CURR_RE_RA_LAE_CY + OPEN_INIT_RE_RA_LAE_PY + OPEN_AOCI_RVNU_RE_RA_IBNR_PY + OPEN_AOCI_RVNU_RE_RA_LAE_PY + OPEN_AOCI_EXPNS_RE_RA_IBNR_PY + OPEN_AOCI_EXPNS_RE_RA_LAE_PY)",
                    },
                },
                "LIC": {
                    "calculate": "(OPEN_CSM)",
                    "expression": {
                        "condition": "> 0",
                    },
                },
                "TOTAL": None,
            },
            "Opening net balance": {
                "index": 2,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[0]['Future_cash_flows'] - result_df.iloc[1]['Future_cash_flows']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[0]['Risk_adjustment'] - result_df.iloc[1]['Risk_adjustment']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[0]['CSM'] - result_df.iloc[1]['CSM']",
                },
                "TOTAL": None,
            },
            "Changes that relate to current service": {
                "header": True,
                "index": 3,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[4]['Future_cash_flows'] + result_df.iloc[5]['Future_cash_flows'] + result_df.iloc[6]['Future_cash_flows']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[4]['Risk_adjustment'] + result_df.iloc[5]['Risk_adjustment'] + result_df.iloc[6]['Risk_adjustment']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[4]['CSM'] + result_df.iloc[5]['CSM'] + result_df.iloc[6]['CSM']",
                },
                "TOTAL": None,
            },
            "CSM recognised in profit or loss for the services received": {
                "LRC": None,
                "LC": None,
                "LIC": {
                    "calculate": "CSM_AMORT",
                },
                "TOTAL": None,
            },
            "Change in the risk adjustment for non-financial risk for the risk expired": {
                "LRC": None,
                "LC": {
                    "calculate": "-EXP_RA_AMORT_OTH_RNC_RWU",
                },
                "LIC": None,
                "TOTAL": None,
            },
            "Experience adjustments - relating to incurred claims and other directly attributable expenses recovery": {
                "LRC": {
                    "calculate": "EXP_CLM_INSRC_RNC_RWU + EXP_CLM_INVST_RNC_RWU + EXP_LAE_OTH_RNC_RWU + EXP_INVST_COMP_RNC_RWU + EXP_CRDT_LOSS_RNC_RWU + ( CLOS_INIT_RE_BEA_CASE_CY + CLOS_INIT_RE_BEA_IBNR_CY + CLOS_INIT_RE_BEA_LAE_CY - CLOS_INIT_RE_CRDT_RISK_CASE_CY - CLOS_INIT_RE_CRDT_RISK_IBNR_CY - CLOS_INIT_RE_CRDT_RISK_LAE_CY ) + ACTCF_CLM_INSRC_CY",
                },
                "LC": {
                    "calculate": "CLOS_INIT_RE_RA_CASE_CY + CLOS_INIT_RE_RA_IBNR_CY + CLOS_INIT_RE_RA_LAE_CY",
                },
                "LIC": None,
                "TOTAL": None,
            },
            "Changes that relate to future service": {
                "header": True,
                "index": 7,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[8]['Future_cash_flows'] + result_df.iloc[9]['Future_cash_flows'] + result_df.iloc[10]['Future_cash_flows'] + result_df.iloc[11]['Future_cash_flows'] + result_df.iloc[12]['Future_cash_flows'] + result_df.iloc[13]['Future_cash_flows']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[8]['Risk_adjustment'] + result_df.iloc[9]['Risk_adjustment'] + result_df.iloc[10]['Risk_adjustment'] + result_df.iloc[11]['Risk_adjustment'] + result_df.iloc[12]['Risk_adjustment'] + result_df.iloc[13]['Risk_adjustment']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[8]['CSM'] + result_df.iloc[9]['CSM'] + result_df.iloc[10]['CSM'] + result_df.iloc[11]['CSM'] + result_df.iloc[12]['CSM'] + result_df.iloc[13]['CSM']",
                },
                "TOTAL": None,
            },
            "Changes in estimates that adjust the CSM": {
                "LRC": {
                    "calculate": "-(INIT_BEL_OTH_RPA - EXP_CLOS_INIT_BEL_OTH_RNC_RWU)",
                },
                "LC": {
                    "calculate": "-(INIT_RA_OTH_RPA - EXP_CLOS_INIT_RA_OTH_RNC_RWU)",
                },
                "LIC": {
                    "calculate": "(INIT_BEL_OTH_RPA - EXP_CLOS_INIT_BEL_OTH_RNC_RWU) + (INIT_RA_OTH_RPA - EXP_CLOS_INIT_RA_OTH_RNC_RWU)",
                },
                "TOTAL": None,
            },
            "Contracts initially recognised in the period": {
                "LRC": {
                    "calculate": "-(INCPT_INIT_BEL_OTH_RWU_NB + INCPT_INIT_CRDT_RISK_OTH_RWU_NB)",
                },
                "LC": {
                    "calculate": "-INCPT_INIT_RA_OTH_RWU_NB",
                },
                "LIC": {
                    "calculate": "INCPT_INIT_BEL_OTH_RWU_NB + INCPT_INIT_CRDT_RISK_OTH_RWU_NB + INCPT_INIT_RA_OTH_RWU_NB",
                },
                "TOTAL": None,
            },
            "CSM adjustment for income on initial recognition of onerous underlying contracts": None,
            "Reversals of a loss-recovery component other than changes in the FCF of reinsurance contracts held": None,
            "Changes in the FCF of reinsurance contracts held from onerous underlying contracts": None,
            "Experience adjustments - arising from ceded premiums paid in the period that relate to future service": {
                "LRC": {
                    "calculate": "EXP_RE_COMM_RNC_RWU + EXP_PREM_RNC_RWU",
                },
                "LC": None,
                "LIC": {
                    "calculate": "-(EXP_RE_COMM_RNC_RWU + EXP_PREM_RNC_RWU)",
                },
                "TOTAL": None,
            },
            "Changes that relate to past service": {
                "header": True,
                "index": 14,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[15]['Future_cash_flows'] + result_df.iloc[16]['Future_cash_flows'] + result_df.iloc[17]['Future_cash_flows'] + result_df.iloc[18]['Future_cash_flows'] + result_df.iloc[19]['Future_cash_flows']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[15]['Risk_adjustment'] + result_df.iloc[16]['Risk_adjustment'] + result_df.iloc[17]['Risk_adjustment'] + result_df.iloc[18]['Risk_adjustment'] + result_df.iloc[19]['Risk_adjustment']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[15]['CSM'] + result_df.iloc[16]['CSM'] + result_df.iloc[17]['CSM'] + result_df.iloc[18]['CSM'] + result_df.iloc[19]['CSM']",
                },
                "TOTAL": None,
            },
            "Changes that relate to past service - changes in the FCF relating to incurred claims recovery": {
                "LRC": {
                    "calculate": "-( EXPCF_CLM_IBNR_CY + EXPCF_CLM_IBNR_PY ) + -( EXPCF_CLM_CASE_CY + EXPCF_CLM_CASE_PY ) + -( EXPCF_LOSS_ADJ_EXPNS_CY + EXPCF_LOSS_ADJ_EXPNS_PY ) + ( EXPCF_CRDT_LOSS_IBNR_CY + EXPCF_CRDT_LOSS_IBNR_PY ) + ( EXPCF_CRDT_LOSS_CASE_CY + EXPCF_CRDT_LOSS_CASE_PY ) + ( EXPCF_CRDT_LOSS_LAE_CY + EXPCF_CRDT_LOSS_LAE_PY) + ADJ_RE_BEA_IBNR_PY + ADJ_RE_BEA_CASE_PY + ADJ_RE_BEA_LAE_PY + - ADJ_RE_CRDT_RISK_IBNR_PY + - ADJ_RE_CRDT_RISK_CASE_PY + - ADJ_RE_CRDT_RISK_LAE_PY + ACTCF_CLM_INSRC_PY",
                },
                "LC": {
                    "calculate": "-( EXP_RA_AMORT_IBNR_CY + EXP_RA_AMORT_IBNR_PY ) + -( EXP_RA_AMORT_CASE_CY + EXP_RA_AMORT_CASE_PY ) + -( EXP_RA_AMORT_LAE_CY + EXP_RA_AMORT_LAE_PY ) + ADJ_RE_RA_IBNR_PY + ADJ_RE_RA_CASE_PY + ADJ_RE_RA_LAE_PY",
                },
                "LIC": None,
                "TOTAL": None,
            },
            "Changes in estimates relate to losses on onerous contracts and reversal of those losses": None,
            "Experience adjustments - arising from ceded premiums paid in the period that relate to past service": None,
            "Effect of changes in the risk of reinsurers": {
                "LRC": {
                    "calculate": "-(RESET_CRDT_RISK_OTH_RPA - EXP_CLOS_RESET_CRDT_RISK_OTH_RNC_RWU)",
                },
                "LC": None,
                "LIC": None,
                "TOTAL": None,
            },
            "Cost of retroactive cover for reinsurance contracts held": None,
            "Net income (expenses) from reinsurance contracts held": {
                "header": True,
                "index": 20,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[21]['Future_cash_flows'] + result_df.iloc[22]['Future_cash_flows']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[21]['Risk_adjustment'] + result_df.iloc[22]['Risk_adjustment']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[21]['CSM'] + result_df.iloc[22]['CSM']",
                },
                "TOTAL": None,
            },
            "Finance income (expenses) from reinsurance contracts held": {
                "LRC": {
                    "calculate": "-(INTRST_EXPNS_RESET_BEL_RNC_RWU + INTRST_EXPNS_RESET_CRDT_RISK_RNC_RWU) -(RESET_BEL_OTH_RPA - EXP_CLOS_RESET_BEL_OTH_RNC_RWU) + (INIT_BEL_OTH_RPA - EXP_CLOS_INIT_BEL_OTH_RNC_RWU) + ( INTRST_EXPNS_RE_BEA_IBNR_CY + INTRST_EXPNS_RE_BEA_IBNR_PY ) + ( INTRST_EXPNS_RE_BEA_CASE_CY + INTRST_EXPNS_RE_BEA_CASE_PY ) + ( INTRST_EXPNS_RE_BEA_LAE_CY + INTRST_EXPNS_RE_BEA_LAE_PY ) + - ( INTRST_EXPNS_RE_CRDT_RISK_IBNR_CY + INTRST_EXPNS_RE_CRDT_RISK_IBNR_PY ) + - ( INTRST_EXPNS_RE_CRDT_RISK_CASE_CY + INTRST_EXPNS_RE_CRDT_RISK_CASE_PY ) + - ( INTRST_EXPNS_RE_CRDT_RISK_LAE_CY + INTRST_EXPNS_RE_CRDT_RISK_LAE_PY)",
                },
                "LC": {
                    "calculate": "-INTRST_EXPNS_RESET_RA_RNC_RWU - (RESET_RA_OTH_RPA - EXP_CLOS_RESET_RA_OTH_RNC_RWU) + (INIT_RA_OTH_RPA - EXP_CLOS_INIT_RA_OTH_RNC_RWU) + ( INTRST_EXPNS_RE_RA_IBNR_CY + INTRST_EXPNS_RE_RA_IBNR_PY ) + ( INTRST_EXPNS_RE_RA_CASE_CY + INTRST_EXPNS_RE_RA_CASE_PY ) + ( INTRST_EXPNS_RE_RA_LAE_CY + INTRST_EXPNS_RE_RA_LAE_PY )",
                },
                "LIC": {
                    "calculate": "-CSM_UNWND",
                },
                "TOTAL": None,
            },
            "Other changes": {
                "LRC": {
                    "calculate": "(OPEN_AOCI_EXPNS_BEL_OTH - OPEN_AOCI_RVNU_BEL_OTH) + (OPEN_AOCI_EXPNS_CRDT_RISK_OTH - OPEN_AOCI_RVNU_CRDT_RISK_OTH) - (CLOS_AOCI_EXPNS_BEL_OTH - CLOS_AOCI_RVNU_BEL_OTH) - (CLOS_AOCI_EXPNS_CRDT_RISK_OTH - CLOS_AOCI_RVNU_CRDT_RISK_OTH) - (OPEN_AOCI_RVNU_RE_BEA_IBNR_CY + OPEN_AOCI_RVNU_RE_BEA_IBNR_PY + OPEN_AOCI_EXPNS_RE_BEA_IBNR_CY + OPEN_AOCI_EXPNS_RE_BEA_IBNR_PY ) + - (OPEN_AOCI_RVNU_RE_BEA_CASE_CY + OPEN_AOCI_RVNU_RE_BEA_CASE_PY + OPEN_AOCI_EXPNS_RE_BEA_CASE_CY + OPEN_AOCI_EXPNS_RE_BEA_CASE_PY) + - (OPEN_AOCI_RVNU_RE_BEA_LAE_CY + OPEN_AOCI_RVNU_RE_BEA_LAE_PY + OPEN_AOCI_EXPNS_RE_BEA_LAE_CY + OPEN_AOCI_EXPNS_RE_BEA_LAE_PY) + (OPEN_AOCI_RVNU_RE_CRDT_RISK_IBNR_CY + OPEN_AOCI_RVNU_RE_CRDT_RISK_IBNR_PY + OPEN_AOCI_EXPNS_RE_CRDT_RISK_IBNR_CY + OPEN_AOCI_EXPNS_RE_CRDT_RISK_IBNR_PY ) + (OPEN_AOCI_RVNU_RE_CRDT_RISK_CASE_CY + OPEN_AOCI_RVNU_RE_CRDT_RISK_CASE_PY + OPEN_AOCI_EXPNS_RE_CRDT_RISK_CASE_CY + OPEN_AOCI_EXPNS_RE_CRDT_RISK_CASE_PY) + (OPEN_AOCI_RVNU_RE_CRDT_RISK_LAE_CY + OPEN_AOCI_RVNU_RE_CRDT_RISK_LAE_PY + OPEN_AOCI_EXPNS_RE_CRDT_RISK_LAE_CY + OPEN_AOCI_EXPNS_RE_CRDT_RISK_LAE_PY) + CLOS_AOCI_RVNU_RE_BEA_IBNR_PY + CLOS_AOCI_EXPNS_RE_BEA_IBNR_PY + CLOS_AOCI_RVNU_RE_BEA_CASE_PY + CLOS_AOCI_EXPNS_RE_BEA_CASE_PY + CLOS_AOCI_RVNU_RE_BEA_LAE_PY + CLOS_AOCI_EXPNS_RE_BEA_LAE_PY + -(CLOS_AOCI_RVNU_RE_CRDT_RISK_IBNR_PY + CLOS_AOCI_EXPNS_RE_CRDT_RISK_IBNR_PY) + -(CLOS_AOCI_RVNU_RE_CRDT_RISK_CASE_PY + CLOS_AOCI_EXPNS_RE_CRDT_RISK_CASE_PY) + -(CLOS_AOCI_RVNU_RE_CRDT_RISK_LAE_PY + CLOS_AOCI_EXPNS_RE_CRDT_RISK_LAE_PY) + CLOS_AOCI_RVNU_RE_BEA_IBNR_CY + CLOS_AOCI_EXPNS_RE_BEA_IBNR_CY + CLOS_AOCI_RVNU_RE_BEA_CASE_CY + CLOS_AOCI_EXPNS_RE_BEA_CASE_CY + CLOS_AOCI_RVNU_RE_BEA_LAE_CY + CLOS_AOCI_EXPNS_RE_BEA_LAE_CY + -(CLOS_AOCI_RVNU_RE_CRDT_RISK_IBNR_CY + CLOS_AOCI_EXPNS_RE_CRDT_RISK_IBNR_CY) + -(CLOS_AOCI_RVNU_RE_CRDT_RISK_CASE_CY + CLOS_AOCI_EXPNS_RE_CRDT_RISK_CASE_CY) + -(CLOS_AOCI_RVNU_RE_CRDT_RISK_LAE_CY + CLOS_AOCI_EXPNS_RE_CRDT_RISK_LAE_CY)",
                },
                "LC": {
                    "calculate": "-(CLOS_AOCI_EXPNS_RA_OTH - CLOS_AOCI_RVNU_RA_OTH) + (OPEN_AOCI_EXPNS_RA_OTH - OPEN_AOCI_RVNU_RA_OTH) - (OPEN_AOCI_RVNU_RE_RA_IBNR_CY + OPEN_AOCI_RVNU_RE_RA_IBNR_PY + OPEN_AOCI_EXPNS_RE_RA_IBNR_CY + OPEN_AOCI_EXPNS_RE_RA_IBNR_PY ) + - (OPEN_AOCI_RVNU_RE_RA_CASE_CY + OPEN_AOCI_RVNU_RE_RA_CASE_PY + OPEN_AOCI_EXPNS_RE_RA_CASE_CY + OPEN_AOCI_EXPNS_RE_RA_CASE_PY) + - (OPEN_AOCI_RVNU_RE_RA_LAE_CY + OPEN_AOCI_RVNU_RE_RA_LAE_PY + OPEN_AOCI_EXPNS_RE_RA_LAE_CY + OPEN_AOCI_EXPNS_RE_RA_LAE_PY) + CLOS_AOCI_RVNU_RE_RA_IBNR_PY + CLOS_AOCI_EXPNS_RE_RA_IBNR_PY + CLOS_AOCI_RVNU_RE_RA_CASE_PY + CLOS_AOCI_EXPNS_RE_RA_CASE_PY + CLOS_AOCI_RVNU_RE_RA_LAE_PY + CLOS_AOCI_EXPNS_RE_RA_LAE_PY + CLOS_AOCI_RVNU_RE_RA_IBNR_CY + CLOS_AOCI_EXPNS_RE_RA_IBNR_CY + CLOS_AOCI_RVNU_RE_RA_CASE_CY + CLOS_AOCI_EXPNS_RE_RA_CASE_CY + CLOS_AOCI_RVNU_RE_RA_LAE_CY + CLOS_AOCI_EXPNS_RE_RA_LAE_CY",
                },
                "LIC": None,
                "TOTAL": None,
            },
            "Total amounts recognised in comprehensive income": {
                "header": True,
                "index": 23,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[24]['Future_cash_flows']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[24]['Risk_adjustment']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[24]['CSM']",
                },
                "TOTAL": None,
            },
            "Other changes (2)": None,
            "Cash flows": {
                "header": True,
                "index": 25,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[26]['Future_cash_flows'] + result_df.iloc[27]['Future_cash_flows']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[26]['Risk_adjustment'] + result_df.iloc[27]['Risk_adjustment']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[26]['CSM'] + result_df.iloc[27]['CSM']",
                },
                "TOTAL": None,
            },
            "Premiums paid net of ceding commissions and other directly attributable expenses paid to reinsurer": {
                "LRC": None,
                "LC": None,
                "LIC": {
                    "calculate": "(ACTCF_PREM - ACTCF_RE_COMM)",
                },
                "TOTAL": None,
            },
            "Recoveries from reinsurance": {
                "LRC": {
                    "calculate": "-(ACTCF_CLM_INSRC_CY + ACTCF_CLM_INSRC_PY)",
                },
                "LC": None,
                "LIC": None,
                "TOTAL": None,
            },
            "Total cash flows": {
                "index": 28,
            },
            "Closing net balance": {
                "index": 29,
            },
            "Closing reinsurance contract assets": {
                "LRC": {
                    "calculate": "-(CLOS_CURR_BEL_OTH + CLOS_CURR_CRDT_RISK_OTH)",
                    "expression": {
                        "condition": "> 0",
                        "add_max": "( CLOS_CURR_RE_BEA_CASE_CY + CLOS_CURR_RE_BEA_CASE_PY + CLOS_CURR_RE_BEA_IBNR_CY + CLOS_CURR_RE_BEA_IBNR_PY + CLOS_CURR_RE_BEA_LAE_CY + CLOS_CURR_RE_BEA_LAE_PY - (CLOS_CURR_RE_CRDT_RISK_CASE_CY + CLOS_CURR_RE_CRDT_RISK_CASE_PY + CLOS_CURR_RE_CRDT_RISK_IBNR_CY + CLOS_CURR_RE_CRDT_RISK_IBNR_PY + CLOS_CURR_RE_CRDT_RISK_LAE_CY + CLOS_CURR_RE_CRDT_RISK_LAE_PY) )",
                    },
                },
                "LC": {
                    "calculate": "-(CLOS_CURR_RA_OTH)",
                    "expression": {
                        "condition": "> 0",
                        "add_max": "(CLOS_CURR_RE_RA_CASE_CY + CLOS_CURR_RE_RA_CASE_PY + CLOS_CURR_RE_RA_IBNR_CY + CLOS_CURR_RE_RA_IBNR_PY + CLOS_CURR_RE_RA_LAE_CY + CLOS_CURR_RE_RA_LAE_PY)",
                    },
                },
                "LIC": {
                    "calculate": "-(CLOS_CSM)",
                    "expression": {
                        "condition": "> 0",
                    },
                },
                "TOTAL": None,
            },
            "Closing reinsurance contract liabilities": {
                "LRC": {
                    "calculate": "(CLOS_CURR_BEL_OTH + CLOS_CURR_CRDT_RISK_OTH)",
                    "expression": {
                        "condition": "> 0",
                        "add_max": "-( CLOS_CURR_RE_BEA_CASE_CY + CLOS_CURR_RE_BEA_CASE_PY + CLOS_CURR_RE_BEA_IBNR_CY + CLOS_CURR_RE_BEA_IBNR_PY + CLOS_CURR_RE_BEA_LAE_CY + CLOS_CURR_RE_BEA_LAE_PY - (CLOS_CURR_RE_CRDT_RISK_CASE_CY + CLOS_CURR_RE_CRDT_RISK_CASE_PY + CLOS_CURR_RE_CRDT_RISK_IBNR_CY + CLOS_CURR_RE_CRDT_RISK_IBNR_PY + CLOS_CURR_RE_CRDT_RISK_LAE_CY + CLOS_CURR_RE_CRDT_RISK_LAE_PY) )",
                    },
                },
                "LC": {
                    "calculate": "( CLOS_CURR_RA_OTH )",
                    "expression": {
                        "condition": "> 0",
                        "add_max": "-(CLOS_CURR_RE_RA_CASE_CY + CLOS_CURR_RE_RA_CASE_PY + CLOS_CURR_RE_RA_IBNR_CY + CLOS_CURR_RE_RA_IBNR_PY + CLOS_CURR_RE_RA_LAE_CY + CLOS_CURR_RE_RA_LAE_PY)",
                    },
                },
                "LIC": {
                    "calculate": "( CLOS_CSM )",
                    "expression": {
                        "condition": "> 0",
                    },
                },
                "TOTAL": None,
            },
            "Closing net balance (2)": {
                "index": 32,
                "LRC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[30]['Future_cash_flows'] - result_df.iloc[31]['Future_cash_flows']",
                },
                "LC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[30]['Risk_adjustment'] - result_df.iloc[31]['Risk_adjustment']",
                },
                "LIC": {
                    "self-reference": True,
                    "calculate": "result_df.iloc[30]['CSM'] - result_df.iloc[31]['CSM']",
                },
                "TOTAL": None,
            },
        },
    },
}
