from cm_dashboards.kics.helpers import abstract_handler as gf
from cm_dashboards.kics.helpers import helpers as helpers

"""
['A_AC', 'A_COMPANY_KICS_DATA', 'A_CREDIT_RISK_TOT', 'A_EQUITY_RISK', 'A_INT_RISK_TOT',
'A_KICS_PAP_BS', 'A_LIFE_CAT_RISK', 'A_LIFE_RISK_TOT', 'A_MARKET_RISK', 'A_OPERATION_RISK',
'A_PROPERTY_RISK', 'A_RC', 'G_INT_RISK_LIAB', 'I_CONCEN_G_RISK_GROUP', 'I_INT_RISK_ASSET',
'O_CAPITAL_SECURITIES', 'O_CONCEN_G_RISK_GROUP', 'O_CONCEN_P_RISK_GROUP', 'O_CREDIT_RISK',
'O_CREDIT_RISK_OTHER', 'O_CREDIT_RISK_REINS', 'O_FOREX_RISK_GROUP', 'O_INT_RISK_CUR_GROUP',
'O_LIFE_RISK', 'R_Info_RuntimeParameters', 'Rc_RuntimeParameters', 'Rd_RuntimeParameters',
'Rn_RuntimeParameters', 'T_Table_Mapping', 'Z_Info_DataLayer_Available_Capital_Data',
'Z_Info_DataLayer_Concentration_G_Risk_Data', 'Z_Info_DataLayer_Concentration_P_Risk_Sub_Data',
'Z_Info_DataLayer_Forex_Risk_Liab_Input', 'Z_Info_DataLayer_Reinsurance_Input', 'Z_Info_Layer',
'Z_Info_Model', 'Zc_DataLayer_Concentration_G_Risk_Data', 'Zc_DataLayer_Concentration_P_Risk_Sub_Data',
'Zc_DataLayer_Forex_Risk_Liab_Input', 'Zc_Model', 'Zn_DataLayer_Available_Capital_Data',
'Zn_DataLayer_Concentration_G_Risk_Data', 'Zn_DataLayer_Forex_Risk_Liab_Input', 'Zn_DataLayer_Reinsurance_Input',
'Zn_Layer', 'Zn_Model']
"""


class TableInfos(gf.GenericHandler):
    """
    Table mapping is a special case, as it is used to get the list of tables
    """

    _DB_TABLE = "T_Table_Mapping"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"

    def __init__(self, table_name=None):
        if table_name is not None:
            self._DB_TABLE = table_name
            self._DB_QUERY = f"SELECT * FROM [{self._DB_TABLE}]"


class JournalReportDates(gf.GenericHandler):
    """
    Get the list of report dates for a given journal
    """

    _DB_TABLE = "A_RC"
    _DB_QUERY = f"SELECT DISTINCT [Step Date] as Report_Date FROM [{_DB_TABLE}] WHERE [KICS Scenario] = '1'"

    def __init__(self, table_name=None, scenario=1):
        if table_name is not None:
            self._DB_TABLE = table_name
            self._DB_QUERY = f"SELECT [Step Date] as Report_Date, ISS_CP_NM as Company_Name FROM [{self._DB_TABLE}] WHERE [KICS Scenario] = '{scenario}'"


class Journal(gf.GenericHandler):
    """
    Individual Journal Data by Report Date
    """

    _DB_TABLE = "A_AC"
    _DB_QUERY = f"SELECT FROM [{_DB_TABLE}]"

    def __init__(
        self,
        table_name=None,
        select="*, [Step Date] as Step_Date",
        report_date=None,
        scenario=1,
    ):
        if table_name is not None:
            self._DB_TABLE = table_name
            self._DB_QUERY = f"SELECT {select} FROM [{self._DB_TABLE}] WHERE [Step Date] = '{report_date}'"
        if scenario is not None:
            self._DB_QUERY = f"SELECT {select} FROM [{self._DB_TABLE}] WHERE [Step Date] = '{report_date}' AND [KICS Scenario] = '{scenario}'"


class TransitionMeasure(gf.GenericHandler):
    """
    Transition Measure data by Report Date
    """

    _DB_TABLE = "A_AC"
    _DB_QUERY = None

    def __init__(self, report_date="2022-12-31", switch_query=True):
        if switch_query:
            self._DB_QUERY = f"""
                SELECT
                    (A_AC.[Step Date]) as Report_Date,
                    (A_AC.SMRT) as SMRT,
                    (A_AC.AVCPT_TTL_AMT) as AVCPT_TTL_AMT,
                    (A_AC.ALA_AF_COCPT_TTL_AMT) as ALA_AF_COCPT_TTL_AMT,
                    (A_AC.SPCPT_TTL_AMT) as SPCPT_TTL_AMT,
                    (A_AC.SPCPT_RCLITM_CRAM_EXCPT_INLAT) as SPCPT_RCLITM_CRAM_EXCPT_INLAT,
                    (A_AC.CRDF_IN_CCRSK_RQUAT_EXCS_AMT) as CRDF_IN_CCRSK_RQUAT_EXCS_AMT,
                    (A_AC.CSSC_STFC_NTCSRT_AMT) as CSSC_STFC_NTCSRT_AMT,
                    (A_AC.CSSC_STFCA_ODBAMT_AMT) as CSSC_STFCA_ODBAMT_AMT,
                    (A_RC.RQUAT_DCTAA_AMT) as RQUAT_DCTAA_AMT,
                    (A_RC.RQUAT_RRAAF_DCTAB_AMT) as RQUAT_RRAAF_DCTAB_AMT,
                    (A_RC.LFLT_INSU_RSKA) as LFLT_INSU_RSKA,
                    (A_RC.MKRSK_TOT_AMT) as MKRSK_TOT_AMT,
                    (A_RC.CRRK_DIRTY_DDAF_AMT) as CRRK_DIRTY_DDAF_AMT,
                    (A_RC.ORSK_TOT_AMT) as ORSK_TOT_AMT,
                    (A_RC.CTE_ACAM_AMT) as CTE_ACAM_AMT,
                    (A_MARKET_RISK.IRRSK_TTAM_AMT) as IRRSK_TTAM_AMT,
                    (A_MARKET_RISK.STK_RSKA) as STK_RSKA,
                    (A_MARKET_RISK.PPRSKA_AMT) as PPRSKA_AMT,
                    (A_MARKET_RISK.FRSAM_TOT_AMT) as FRSAM_TOT_AMT,
                    (A_MARKET_RISK.ASFC_RSKA_TOT_AMT) as ASFC_RSKA_TOT_AMT,
                    (A_LIFE_RISK_TOT.DTH_RSK_CLRITC_AMT) as DTH_RSK_CLRITC_AMT,
                    (A_LIFE_RISK_TOT.LGV_RSK_CLRITC_AMT) as LGV_RSK_CLRITC_AMT,
                    (A_LIFE_RISK_TOT.DSDS_RSK_CLRITC_AMT) as DSDS_RSK_CLRITC_AMT,
                    (A_LIFE_RISK_TOT.CNC_RSK_CLRITC_AMT) as CNC_RSK_CLRITC_AMT,
                    (A_LIFE_RISK_TOT.BZCF_RSK_CLRITC_AMT) as BZCF_RSK_CLRITC_AMT,
                    (A_LIFE_RISK_TOT.CTDS_RSK_VLU) as CTDS_RSK_VLU,
                    (A_RC.RQUAT_DCTAA_AMT / 2) as RQUAT_DCTAA_AMT_DIV_2,
                    (A_AC.SPCPT_RCLITM_CRAM_EXCPT_INLAT - A_AC.CSSC_STFC_NTCSRT_AMT) as DIFF_SPCPT_RCLITM_CRAM_EXCPT_INLAT_CSSC_STFC_NTCSRT_AMT,
                    (
                        CASE
                            WHEN (A_AC.SPCPT_RCLITM_CRAM_EXCPT_INLAT - A_AC.CSSC_STFC_NTCSRT_AMT) < (A_RC.RQUAT_DCTAA_AMT * 0.5) THEN
                                (A_AC.SPCPT_RCLITM_CRAM_EXCPT_INLAT - A_AC.CSSC_STFC_NTCSRT_AMT)
                            ELSE
                                (A_RC.RQUAT_DCTAA_AMT * 0.5)
                        END
                        + CASE
                            WHEN (A_AC.CSSC_STFC_NTCSRT_AMT - A_RC.RQUAT_DCTAA_AMT * 0.15) > 0 THEN
                                (A_AC.CSSC_STFC_NTCSRT_AMT - A_RC.RQUAT_DCTAA_AMT * 0.15)
                            ELSE
                                0
                        END
                        + A_AC.CRDF_IN_CCRSK_RQUAT_EXCS_AMT
                    ) as CALC_SPCPT_RCLITM_CRAM_EXCPT_INLAT_CSSC_STFC_NTCSRT_AMT,
                    (
                        A_AC.ALA_AF_COCPT_TTL_AMT
                        + CASE
                            WHEN A_AC.CSSC_STFC_NTCSRT_AMT < (A_RC.RQUAT_DCTAA_AMT * 0.15) THEN
                                A_AC.CSSC_STFC_NTCSRT_AMT
                            ELSE
                                A_RC.RQUAT_DCTAA_AMT * 0.15
                        END
                    ) as CALC_A_LA_AF_COCPT_TTL_AMT,
                    (
                        CASE
                            WHEN (A_AC.SPCPT_RCLITM_CRAM_EXCPT_INLAT - A_AC.CSSC_STFCA_ODBAMT_AMT) < (A_RC.RQUAT_DCTAA_AMT * 0.5) THEN
                                (A_AC.SPCPT_RCLITM_CRAM_EXCPT_INLAT - A_AC.CSSC_STFCA_ODBAMT_AMT)
                            ELSE
                                (A_RC.RQUAT_DCTAA_AMT * 0.5)
                        END
                        + A_AC.CSSC_STFCA_ODBAMT_AMT
                        + A_AC.CRDF_IN_CCRSK_RQUAT_EXCS_AMT
                    ) as CALC_A_LA_AF_COCPT_TTL_AMT_2

                FROM
                    A_AC
                LEFT JOIN
                    A_RC ON A_AC.[Step Date] = A_RC.[Step Date]
                LEFT JOIN
                    A_MARKET_RISK ON A_AC.[Step Date] = A_MARKET_RISK.[Step Date]
                LEFT JOIN
                    A_LIFE_RISK_TOT ON A_AC.[Step Date] = A_LIFE_RISK_TOT.[Step Date]
                WHERE
                    A_AC.[Step Date] = '{report_date}'
                LIMIT 1
                """
        else:
            self._DB_QUERY = f"""
                SELECT
                    (A_AC.[Step Date]) as Report_Date,
                    (A_AC.SMRT) as SMRT,
                    (A_AC.AVCPT_TTL_AMT) as AVCPT_TTL_AMT,
                    (A_AC.ALA_AF_COCPT_TTL_AMT) as ALA_AF_COCPT_TTL_AMT,
                    (A_AC.SPCPT_TTL_AMT) as SPCPT_TTL_AMT,
                    (A_AC.SPCPT_RCLITM_CRAM_EXCPT_INLAT) as SPCPT_RCLITM_CRAM_EXCPT_INLAT,
                    (A_AC.CRDF_IN_CCRSK_RQUAT_EXCS_AMT) as CRDF_IN_CCRSK_RQUAT_EXCS_AMT,
                    (A_AC.CSSC_STFC_NTCSRT_AMT) as CSSC_STFC_NTCSRT_AMT,
                    (A_AC.CSSC_STFCA_ODBAMT_AMT) as CSSC_STFCA_ODBAMT_AMT,
                    (A_RC.RQUAT_DCTAA_AMT) as RQUAT_DCTAA_AMT,
                    (A_RC.TM_RQUAT_RRAAF_DCTAB_AMT) as TM_RQUAT_RRAAF_DCTAB_AMT,
                    (A_RC.TM_LFLT_INSU_RSKA) as TM_LFLT_INSU_RSKA,
                    (A_RC.TM_MKRSK_TOT_AMT) as TM_MKRSK_TOT_AMT,
                    (A_RC.CRRK_DIRTY_DDAF_AMT) as CRRK_DIRTY_DDAF_AMT,
                    (A_RC.ORSK_TOT_AMT) as ORSK_TOT_AMT,
                    (A_RC.CTE_ACAM_AMT) as CTE_ACAM_AMT,
                    (A_MARKET_RISK.IRRSK_TTAM_AMT) as IRRSK_TTAM_AMT,
                    (A_MARKET_RISK.TER_STK_RSKA) as TER_STK_RSKA,
                    (A_MARKET_RISK.PPRSKA_AMT) as PPRSKA_AMT,
                    (A_MARKET_RISK.FRSAM_TOT_AMT) as FRSAM_TOT_AMT,
                    (A_MARKET_RISK.ASFC_RSKA_TOT_AMT) as ASFC_RSKA_TOT_AMT,
                    (A_LIFE_RISK_TOT.DTH_RSK_CLRITC_AMT) as DTH_RSK_CLRITC_AMT,
                    (A_LIFE_RISK_TOT.TIR_LGV_RSK_CLTC_AMT) as TIR_LGV_RSK_CLTC_AMT,
                    (A_LIFE_RISK_TOT.DSDS_RSK_CLRITC_AMT) as DSDS_RSK_CLRITC_AMT,
                    (A_LIFE_RISK_TOT.TIR_CNC_RSK_CLTC_AMT) as TIR_CNC_RSK_CLTC_AMT,
                    (A_LIFE_RISK_TOT.TIR_BZCF_RSK_CLTC_AMT) as TIR_BZCF_RSK_CLTC_AMT,
                    (A_LIFE_RISK_TOT.TIR_CTDS_RSK_VLU) as TIR_CTDS_RSK_VLU
                FROM
                    A_AC
                LEFT JOIN
                    A_RC ON A_AC.[Step Date] = A_RC.[Step Date]
                LEFT JOIN
                    A_MARKET_RISK ON A_AC.[Step Date] = A_MARKET_RISK.[Step Date]
                LEFT JOIN
                    A_LIFE_RISK_TOT ON A_AC.[Step Date] = A_LIFE_RISK_TOT.[Step Date]
                WHERE
                    A_AC.[Step Date] = '{report_date}'
                LIMIT 1
                """


class CreditRisk(gf.GenericHandler):
    """
    Credit Risk data handler
    """

    _DB_TABLE = "O_CREDIT_RISK"
    _DB_QUERY = None

    def __init__(self, journal_code, report_date=None, scenario=1, name="DGB"):
        match journal_code:
            case "6-1":
                self._DB_QUERY = f"""
                    SELECT
                        CRRK_MCLSF_NM,
                        RDYN_AVCLT_AMT,
                        CRDGT_DIRTY_AMT,
                        CRSAM_CLEANDB_AMT,
                        CRDCL_DIRTY_AMT,
                        CRDGT_CLN_AMT,
                        CRSTT_CLEANDB_AMT,
                        CASE 
                            WHEN
                                RDYN_AVCLT_AMT = 'Y'
                                OR (RDYN_AVCLT_AMT = 'N' AND CRRK_MCLSF_NM = 'C01')
                                OR (RDYN_AVCLT_AMT = 'N' AND CRRK_MCLSF_NM = 'M01') 
                            THEN CRSAM_CLEANDB_AMT - CRDCL_CLN_AMT 
                            ELSE 0 
                        END AS CREDIT_RISK_RWA
                    FROM
                        O_CREDIT_RISK
                    WHERE
                        [Step Date] = '{report_date}' AND [KICS Scenario] = {scenario}
                """

            case "6-2":
                if name == "HANA":
                    self._DB_QUERY = f"""
                        SELECT
                            (O_CREDIT_RISK_OTHER.CREP_CRDT_OAST_PCOAS_CLEANDB_AMT) as CREP_CRDT_OAST_PCOAS_CLEANDB_AMT,
                            (O_CREDIT_RISK.EXPS_CLN_AMT) as EXPS_CLN_AMT,
                            (O_CREDIT_RISK.CRRK_SCLSF_NM) as CRRK_SCLSF_NM,
                            (O_CREDIT_RISK.RDYN_AVCLT_AMT) as RDYN_AVCLT_AMT,
                            (O_CREDIT_RISK.KICS_EXPI_MNCT) as KICS_EXPI_MNCT,
                            (O_CREDIT_RISK.RDYN_AVGT_AMT) as RDYN_AVGT_AMT,
                            (O_CREDIT_RISK.EXPS_CLEANDB_AMT) as EXPS_CLEANDB_AMT
                        FROM
                            O_CREDIT_RISK
                        LEFT JOIN
                            O_CREDIT_RISK_OTHER ON
                                O_CREDIT_RISK.[Step Date] = O_CREDIT_RISK_OTHER.[Step Date]
                                AND
                                O_CREDIT_RISK.[KICS Scenario] = O_CREDIT_RISK_OTHER.[KICS Scenario]
                        WHERE O_CREDIT_RISK.[Step Date] = '{report_date}' AND O_CREDIT_RISK.[KICS Scenario] = {scenario}
                    """
                else:
                    self._DB_QUERY = f"""
                    SELECT
                        EXPS_CLN_AMT,
                        CRRK_SCLSF_NM,
                        RDYN_AVCLT_AMT,
                        KICS_EXPI_MNCT,
                        RDYN_AVGT_AMT,
                        CRRK_SDCLSF_NAM,
                        CASE 
                            WHEN NRSK_RTO = '' 
                            THEN EXPS_CLN_AMT 
                            ELSE EXPS_CLN_AMT * (1 - CAST(NRSK_RTO AS FLOAT)) 
                        END AS Credit_Exposure_Clean,
                        CASE 
                            WHEN NRSK_RTO = '' 
                            THEN 0 
                            ELSE EXPS_CLN_AMT * CAST(NRSK_RTO AS FLOAT)
                        END AS Credit_Exposure_Clean_2
                    FROM O_CREDIT_RISK
                    WHERE [Step Date] = '{report_date}'
                    AND [KICS Scenario] = {scenario}
                """

            case "6-3":
                if name == "HANA":
                    self._DB_QUERY = f"""
                        SELECT
                            (O_CREDIT_RISK.EXPS_CLN_AMT) as EXPS_CLN_AMT,
                            (O_CREDIT_RISK.CRRK_SCLSF_NM) as CRRK_SCLSF_NM,
                            (O_CREDIT_RISK.RDYN_AVCLT_AMT) as RDYN_AVCLT_AMT,
                            (O_CREDIT_RISK.KICS_EXPI_MNCT) as KICS_EXPI_MNCT,
                            (O_CREDIT_RISK.RDYN_AVGT_AMT) as RDYN_AVGT_AMT,
                            (O_CREDIT_RISK.CREP_AVCLT_CLN_AMT) as CREP_AVCLT_CLN_AMT,
                            (O_CREDIT_RISK.CRRK_MCLSF_NM) as CRRK_MCLSF_NM,
                            (O_CREDIT_RISK.CREP_AVGT_CLN_AMT) as CREP_AVGT_CLN_AMT,
                            (O_CREDIT_RISK.KICS_QG_Credit_Risk_Classification) as KICS_QG_Credit_Risk_Classification,
                            (O_CREDIT_RISK.AVGT_EXPS_DIRTY_AMT) as AVGT_EXPS_DIRTY_AMT,
                            (O_CREDIT_RISK.EXPS_CLEANDB_AMT) as EXPS_CLEANDB_AMT,
                            (A_CREDIT_RISK_TOT.CRDGTCR_OAST_RCRVN_AMT) as CRDGTCR_OAST_RCRVN_AMT
                        FROM
                            O_CREDIT_RISK
                        LEFT JOIN
                            A_CREDIT_RISK_TOT ON
                                O_CREDIT_RISK.[Step Date] = A_CREDIT_RISK_TOT.[Step Date]
                                AND
                                O_CREDIT_RISK.[KICS Scenario] = A_CREDIT_RISK_TOT.[KICS Scenario]
                        WHERE
                            O_CREDIT_RISK.[Step Date] = '{report_date}'
                            AND O_CREDIT_RISK.[KICS Scenario] = {scenario}
                    """
                else:
                    self._DB_QUERY = f"""
                        SELECT
                            EXPS_CLN_AMT,
                            CRRK_SCLSF_NM,
                            RDYN_AVCLT_AMT,
                            KICS_EXPI_MNCT,
                            RDYN_AVGT_AMT,
                            CREP_AVCLT_CLN_AMT,
                            AVGT_KICS_GRP,
                            CRRK_MCLSF_NM,
                            CREP_AVGT_CLN_AMT,
                            CASE 
                                WHEN NRSK_RTO = '' 
                                THEN EXPS_CLN_AMT 
                                ELSE EXPS_CLN_AMT * (1 - CAST(NRSK_RTO AS FLOAT)) 
                            END AS Credit_Exposure_Clean
                        FROM O_CREDIT_RISK
                        WHERE [Step Date] = '{report_date}'
                        AND [KICS Scenario] = {scenario}
                    """

            case "6-4":
                if name == "HANA":
                    self._DB_QUERY = f"""
                        SELECT
                            APPT_LTV_VLU,
                            EXPS_CLN_AMT,
                            CRRK_SCLSF_NM,
                            APPT_DSCR_,
                            AVGT_EXPS_DIRTY_AMT,
                            EXPS_CLEANDB_AMT
                        FROM O_CREDIT_RISK
                        WHERE [Step Date] = '{report_date}'
                        AND [KICS Scenario] = {scenario}
                    """
                else:
                    self._DB_QUERY = f"""
                        SELECT
                            APPT_LTV_VLU,
                            EXPS_CLN_AMT,
                            CRRK_SCLSF_NM,
                            APPT_DSCR_,
                            CASE 
                                WHEN NRSK_RTO = '' 
                                THEN EXPS_CLN_AMT 
                                ELSE EXPS_CLN_AMT * (1 - CAST(NRSK_RTO AS FLOAT)) 
                            END AS Credit_Exposure_Clean
                        FROM O_CREDIT_RISK
                        WHERE [Step Date] = '{report_date}'
                        AND [KICS Scenario] = {scenario}
                    """


class Sensitivity(gf.GenericHandler):
    """
    Sensitivity data by Report Date
    """

    _DB_TABLE = "A_AC"
    _DB_QUERY = None

    def __init__(
        self, journal_code, report_date="2022-12-31", scenario=1, switch_query=True
    ):
        match journal_code:
            case "10-1-1":
                if switch_query:
                    self._DB_QUERY = f"""
                        SELECT
                            (A_AC.AVCPT_TTL_AMT) as AVCPT_TTL_AMT,
                            (A_AC.NAST_VAL) as NAST_VAL,
                            (A_AC.RQUAT_AMT) as RQUAT_AMT,
                            (A_AC.CTE_RCGNT_AMT) as CTE_RCGNT_AMT,
                            (A_AC.SMRT) as SMRT,
                            (A_AC.AVCPT_TTL_AMT - A_AC.NAST_VAL) as AVCPT_TTL_AMT_NAST_VAL,
                            (A_RC.RQUAT_RRAAF_DCTAB_AMT) as RQUAT_RRAAF_DCTAB_AMT,
                            (A_RC.LFLT_INSU_RSKA) as LFLT_INSU_RSKA,
                            (A_RC.MKRSK_TOT_AMT) as MKRSK_TOT_AMT,
                            (A_RC.CRRK_DIRTY_DDAF_AMT) as CRRK_DIRTY_DDAF_AMT,
                            (A_RC.ORSK_TOT_AMT) as ORSK_TOT_AMT,
                            (A_MARKET_RISK.IRRSK_TTAM_AMT) as IRRSK_TTAM_AMT,
                            (A_INT_RISK_TOT.IRRSK_TTAM_AVRC_AMT) as IRRSK_TTAM_AVRC_AMT,
                            (A_INT_RISK_TOT.IRRSK_TTAM_IRU_AMT) as IRRSK_TTAM_IRU_AMT,
                            (A_INT_RISK_TOT.IRRSK_TTAM_IRDN_AMT) as IRRSK_TTAM_IRDN_AMT,
                            (A_INT_RISK_TOT.IRRSK_TTAM_IRPL_AMT) as IRRSK_TTAM_IRPL_AMT,
                            (A_INT_RISK_TOT.IRRSK_TTAM_IRDC_AMT) as IRRSK_TTAM_IRDC_AMT,
                            (A_LIFE_RISK_TOT.CNC_RSK_CLRITC_AMT) as CNC_RSK_CLRITC_AMT,
                            (A_LIFE_RISK_TOT.OPERT_ISHT_NAST_DEP_CLRITC_AMT) as OPERT_ISHT_NAST_DEP_CLRITC_AMT,
                            (A_LIFE_RISK_TOT.OPERT_DSHK_NAST_DEP_CLRITC_AMT) as OPERT_DSHK_NAST_DEP_CLRITC_AMT,
                            (A_LIFE_RISK_TOT.MCC_SHTM_NAST_DEP_CLRITC_AMT) as MCC_SHTM_NAST_DEP_CLRITC_AMT
                        FROM
                            A_AC
                        LEFT JOIN
                            A_RC ON A_AC.[Step Date] = A_RC.[Step Date]
                        LEFT JOIN
                            A_MARKET_RISK ON A_AC.[Step Date] = A_MARKET_RISK.[Step Date]
                        LEFT JOIN
                            A_LIFE_RISK_TOT ON A_AC.[Step Date] = A_LIFE_RISK_TOT.[Step Date]
                        LEFT JOIN
                            A_INT_RISK_TOT ON A_AC.[Step Date] = A_INT_RISK_TOT.[Step Date]
                        WHERE
                            A_AC.[Step Date] = '{report_date}'
                        LIMIT 1
                    """
                else:
                    self._DB_QUERY = f"""
                        SELECT
                            (A_AC.AVCPT_TTL_AMT) as AVCPT_TTL_AMT,
                            (A_AC.NAST_VAL) as NAST_VAL,
                            (A_AC.RQUAT_AMT) as RQUAT_AMT,
                            (A_AC.CTE_RCGNT_AMT) as CTE_RCGNT_AMT,
                            (A_AC.SMRT) as SMRT,
                            (A_RC.RQUAT_RRAAF_DCTAB_AMT) as RQUAT_RRAAF_DCTAB_AMT,
                            (A_RC.LFLT_INSU_RSKA) as LFLT_INSU_RSKA,
                            (A_RC.MKRSK_TOT_AMT) as MKRSK_TOT_AMT,
                            (A_RC.CRRK_DIRTY_DDAF_AMT) as CRRK_DIRTY_DDAF_AMT,
                            (A_RC.ORSK_TOT_AMT) as ORSK_TOT_AMT,
                            (A_MARKET_RISK.IRRSK_TTAM_AMT) as IRRSK_TTAM_AMT,
                            (A_INT_RISK_TOT.IRRSK_TTAM_AVRC_AMT) as IRRSK_TTAM_AVRC_AMT,
                            (A_INT_RISK_TOT.IRRSK_TTAM_IRU_AMT) as IRRSK_TTAM_IRU_AMT,
                            (A_INT_RISK_TOT.IRRSK_TTAM_IRDN_AMT) as IRRSK_TTAM_IRDN_AMT,
                            (A_INT_RISK_TOT.IRRSK_TTAM_IRPL_AMT) as IRRSK_TTAM_IRPL_AMT,
                            (A_INT_RISK_TOT.IRRSK_TTAM_IRDC_AMT) as IRRSK_TTAM_IRDC_AMT,
                            (A_LIFE_RISK_TOT.CNC_RSK_CLRITC_AMT) as CNC_RSK_CLRITC_AMT,
                            (A_LIFE_RISK_TOT.OPERT_ISHT_NAST_DEP_CLRITC_AMT) as OPERT_ISHT_NAST_DEP_CLRITC_AMT,
                            (A_LIFE_RISK_TOT.OPERT_DSHK_NAST_DEP_CLRITC_AMT) as OPERT_DSHK_NAST_DEP_CLRITC_AMT,
                            (A_LIFE_RISK_TOT.MCC_SHTM_NAST_DEP_CLRITC_AMT) as MCC_SHTM_NAST_DEP_CLRITC_AMT
                        FROM
                            A_AC
                        LEFT JOIN
                            A_RC ON A_AC.[Step Date] = A_RC.[Step Date]
                        LEFT JOIN
                            A_MARKET_RISK ON A_AC.[Step Date] = A_MARKET_RISK.[Step Date]
                        LEFT JOIN
                            A_LIFE_RISK_TOT ON A_AC.[Step Date] = A_LIFE_RISK_TOT.[Step Date]
                        LEFT JOIN
                            A_INT_RISK_TOT ON A_AC.[Step Date] = A_INT_RISK_TOT.[Step Date]
                        WHERE
                            A_AC.[Step Date] = '{report_date}'
                        LIMIT 1
                    """

            case "10-1-2":
                if switch_query:
                    self._DB_QUERY = f"""
                        SELECT
                            CRRK_DIRTY_DDAF_AMT,
                            ORSK_TOT_AMT
                        FROM
                            A_RC
                        WHERE
                            [Step Date] = '{report_date}'
                        LIMIT 1
                    """
                else:
                    self._DB_QUERY = f"""
                        SELECT
                            LFLT_INSU_RSKA
                        FROM
                            A_RC
                        WHERE
                            [Step Date] = '{report_date}'
                        LIMIT 1
                    """

            case "10-1-3":
                self._DB_QUERY = f"""
                    SELECT
                        DTH_RSK_CLRITC_AMT,
                        LGV_RSK_CLRITC_AMT,
                        DSDS_RSK_CLRITC_AMT,
                        CNC_RSK_CLRITC_AMT,
                        BZCF_RSK_CLRITC_AMT,
                        CTDS_RSK_VLU
                    FROM
                        A_LIFE_RISK_TOT
                    WHERE
                        [Step Date] = '{report_date}'
                    LIMIT 1
                """

            case "10-1-4":
                self._DB_QUERY = f"""
                    SELECT
                        STK_RSKA,
                        PPRSKA_AMT,
                        FRSAM_TOT_AMT,
                        ASFC_RSKA_TOT_AMT
                    FROM
                        A_MARKET_RISK
                    WHERE
                        [Step Date] = '{report_date}'
                    LIMIT 1
                """

            case "10-2-1":
                if switch_query:
                    self._DB_QUERY = f"""
                        SELECT
                            IRRKEX_ASTT_BAS_AMT,
                            IRRKEX_LBTT_BAS_AMT,
                            NASVAL_BAS_AMT
                        FROM
                            A_INT_RISK_TOT
                        WHERE
                            [Step Date] = '{report_date}'
                        LIMIT 1
                    """
                else:
                    self._DB_QUERY = f"""
                        SELECT
                            IRRKEX_ASTT_BAS_AMT,
                            IRRKEX_DHAS_TTAM_BAS_AMT,
                            IRRKEX_DHAS_CASH_BAS_AMT,
                            IRRKEX_DHAS_STK_BAS_AMT,
                            IRRKEX_DHAS_BOND_BAS_AMT,
                            IRRKEX_DHAS_LOAN_BAS_AMT,
                            IRRKEX_DHAS_CLLON_BAS_AMT,
                            IRRKEX_DHAS_PLOAN_BAS_AMT,
                            IRRKEX_DHAS_CLOAN_BAS_AMT,
                            IRRKEX_DHAS_PRPT_BAS_AMT,
                            IRRKEX_DHAS_NOAS_BAS_AMT,
                            IRRKEX_DHAS_RINSAT_RINSAT_UP_AMT,
                            IRRKEX_DHAS_PBRIA_BAS_AMT,
                            IRRKEX_DHAS_PBREIE_RINSAT_BAS_AMT,
                            IRRKEX_DHAS_DRVT_BAS_AMT,
                            IRRKEX_DHAS_IRHGDR_BAS_AMT,
                            IRRKEX_DHAS_IRIVDR_BAS_AMT,
                            IRRKEX_DHAS_IROTDR_BAS_AMT,
                            IRRKEX_DHAS_OTH_AMT,
                            IRRKEX_IDOW_TTAM_BAS_AMT,
                            IRRKEX_IDOW_CASH_BAS_AMT,
                            IRRKEX_IDOW_STK_BAS_AMT,
                            IRRKEX_IDOW_BOND_BAS_AMT,
                            IRRKEX_IDOW_LOAN_BAS_AMT,
                            IRRKEX_IDOW_PRPT_BAS_AMT,
                            IRRKEX_IDOW_NOAS_BAS_AMT,
                            IRRKEX_IDOW_DRVT_BAS_AMT,
                            IRRKEX_IDOW_IRHGDR_BAS_AMT,
                            IRRKEX_IDOW_IRIVDR_BAS_AMT,
                            IRRKEX_IDOW_IROTDR_BAS_AMT,
                            IRRKEX_IDOW_OTH_AMT,
                            IRRKEX_LBTT_BAS_AMT,
                            IRRKEX_DHLB_TTAM_BAS_AMT,
                            IRRKEX_DHLB_OCNT_PELBT_BAS_AMT,
                            IRRKEX_DHLB_NINLB_BAS_AMT,
                            IRRKEX_DHLB_BWAM_BAS_AMT,
                            IRRKEX_DHLB_AOBW_BAS_AMT,
                            IRRKEX_DHLB_CBND_BAS_AMT,
                            IRRKEX_DHLB_AOCB_BAS_AMT,
                            IRRKEX_DHLB_DRVT_BAS_AMT,
                            IRRKEX_DHLB_IRHGDR_BAS_AMT,
                            IRRKEX_DHLB_IRIVDR_BAS_AMT,
                            IRRKEX_DHLB_IROTDR_BAS_AMT,
                            IRRKEX_DHLB_OTH_AMT,
                            IRRKEX_IHAST_TTAM_BAS_AMT,
                            IRRKEX_IHAST_BWAM_BAS_AMT,
                            IRRKEX_IHAST_DRVT_BAS_AMT,
                            IRRKEX_IHAST_IRHGDR_BAS_AMT,
                            IRRKEX_IHAST_IRIVDR_BAS_AMT,
                            IRRKEX_IHAST_IROTDR_BAS_AMT,
                            IRRKEX_IHAST_OTH_AMT,
                            NASVAL_BAS_AMT,
                            NASVAL_IRIVDRE_TTAM_BAS_AMT,
                            NASVAL__BAS_AMT,
                            IRRSK_TTAM_AMT
                        FROM
                            A_INT_RISK_TOT
                        WHERE
                            [Step Date] = '{report_date}'
                        LIMIT 1
                    """

            case "10-2-2":
                self._DB_QUERY = f"""
                    SELECT * FROM A_INT_RISK_TOT
                    WHERE
                        [Step Date] = '{report_date}'
                    LIMIT 1
                """


class OperationRisk(gf.GenericHandler):
    """
    Operation Risk data handler
    """

    _DB_TABLE = "A_OPERATION_RISK"
    _DB_QUERY = None

    def __init__(self, report_date=None, scenario=1, name="DGB"):
        match name:
            case "HANA":
                self._DB_QUERY = f"""
                    SELECT
                        JB_Y1_PAD_PRM_GNLF_AMT,
                        JBB_Y1_PAD_PRM_GNLF_AMT,
                        PELBT_EXPS_CHGA_AMT,
                        ORSK_APPT_EXPS_CHGA_AMT,
                        PELBT_EXPS_RETI_AMT,
                        ORSK_APPT_EXPS_RETI_AMT,
                        PELBT_EXPS_GNLF_AMT,
                        ORSK_APPT_EXPS_GNLF_AMT,
                        ORSK_CHGA_AMT,
                        ORSK_RETI_AMT,
                        ORSK_GNLF_AMT,
                        Benefit_Claims_AE_Diff_Exposure_Var,
                        Benefit_Claims_AE_Diff_Exposure_Oth,
                        Benefit_Claims_AE_Diff_Risk_Var,
                        Benefit_Claims_AE_Diff_Risk_Oth,
                        Expense_AE_Diff_Exposure_Var,
                        Expense_AE_Diff_Exposure_Oth,
                        Expense_AE_Diff_Risk_Var,
                        Expense_AE_Diff_Risk_Oth,
                        Opening_Assumption_Risk_Var,
                        Opening_Assumption_Risk_Oth
                    FROM
                        {self._DB_TABLE}
                    WHERE
                        [Step Date] = '{report_date}' AND [KICS Scenario] = {scenario}
                """

            case "DGB":
                self._DB_QUERY = f"""
                    SELECT
                        JB_Y1_PAD_PRM_GNLF_AMT,
                        JBB_Y1_PAD_PRM_GNLF_AMT,
                        PELBT_EXPS_CHGA_AMT,
                        ORSK_APPT_EXPS_CHGA_AMT,
                        PELBT_EXPS_RETI_AMT,
                        ORSK_APPT_EXPS_RETI_AMT,
                        PELBT_EXPS_GNLF_AMT,
                        ORSK_APPT_EXPS_GNLF_AMT,
                        ORSK_CHGA_AMT,
                        ORSK_RETI_AMT,
                        ORSK_GNLF_AMT
                    FROM
                        {self._DB_TABLE}
                    WHERE
                        [Step Date] = '{report_date}' AND [KICS Scenario] = {scenario}
                """


class ConcenRiskGroupG(gf.GenericHandler):
    """
    Concentration Risk Group G data handler
    """

    _DB_TABLE = "O_CONCEN_G_RISK_GROUP"
    _DB_QUERY = None

    def __init__(self, report_date=None, scenario=1, name="DGB"):
        match name:
            case "HANA":
                self._DB_QUERY = f"""
                    SELECT
                        ASFRS_SPRT_NM,
                        KICS_CRRT_NM,
                        TPTN_CNRSK_EXPS_DPST_CLN_AMT,
                        TPTN_CNRSK_EXPS_STBD_CLN_AMT,
                        TPTN_CNRSK_EXPS_CRGT_CLN_AMT,
                        TPTN_CNRSK_EXPS_OUBND_AMT,
                        TPTN_CNRSK_EXPS_DRVT_CLN_AMT,
                        TPTN_CNRSK_EXPS_OITM_CLN_AMT,
                        ASFRS_SGRP_EXPS_AMT,
                        ASFRS_SGRP_LMT_CLNM_AMT,
                        ASFRS_SGRP_LIEXD_EXPS_AMT,
                        ASFRS_SGRP_RSKA,
                        (FV_AMT * ASFRS_SGRP_LMT_CLNM_AMT) AS G_RISK_LIMIT
                    FROM
                        {self._DB_TABLE}
                    WHERE
                        [Step Date] = '{report_date}' AND [KICS Scenario] = {scenario}
                """

            case "DGB":
                self._DB_QUERY = f"""
                    SELECT
                        ASFRS_SPRT_NM,
                        KICS_CRRT_NM,
                        TPTN_CNRSK_EXPS_DPST_CLN_AMT,
                        TPTN_CNRSK_EXPS_STBD_CLN_AMT,
                        TPTN_CNRSK_EXPS_CRGT_CLN_AMT,
                        TPTN_CNRSK_EXPS_OUBND_AMT,
                        TPTN_CNRSK_EXPS_DRVT_CLN_AMT,
                        TPTN_CNRSK_EXPS_OITM_CLN_AMT,
                        ASFRS_SGRP_EXPS_AMT,
                        ASFRS_SGRP_LMT_CLNM_AMT,
                        ASFRS_SGRP_LIEXD_EXPS_AMT,
                        ASFRS_SGRP_RSKA
                    FROM
                        {self._DB_TABLE}
                    WHERE
                        [Step Date] = '{report_date}' AND [KICS Scenario] = {scenario}
                """


class ConcenRiskGroupP(gf.GenericHandler):
    """
    Concentration Risk Group P data handler
    """

    _DB_TABLE = "O_CONCEN_P_RISK_GROUP"
    _DB_QUERY = None

    def __init__(self, report_date=None, scenario=1, name="DGB"):
        match name:
            case "HANA":
                self._DB_QUERY = f"""
                    SELECT
                        ASFRS_SPRT_NM,
                        PPPT_ASFC_RSKEP_AMT,
                        PPPT_LMT_CLNM,
                        PPPT_LIEXD_ASFREP_AMT,
                        PPPT_ASFC_RSKA,
                        PPPT_ASFC_RSKA,
                        (FV_AMT * PPPT_LMT_CLNM) AS P_RISK_LIMIT
                    FROM
                        {self._DB_TABLE}
                    WHERE
                        [Step Date] = '{report_date}' AND [KICS Scenario] = {scenario}
                """

            case "DGB":
                self._DB_QUERY = f"""
                    SELECT
                        ASFRS_SPRT_NM,
                        PPPT_ASFC_RSKEP_AMT,
                        PPPT_LMT_CLNM,
                        PPPT_LIEXD_ASFREP_AMT,
                        PPPT_ASFC_RSKA,
                        PPPT_ASFC_RSK
                    FROM
                        {self._DB_TABLE}
                    WHERE
                        [Step Date] = '{report_date}' AND [KICS Scenario] = {scenario}
                """


class CreditRiskTotal(gf.GenericHandler):
    """
    Credit Risk Total data handler
    """

    _DB_TABLE = "A_CREDIT_RISK_TOT"
    _DB_QUERY = None

    def __init__(self, report_date, scenario=1, name="DGB"):
        match name:
            case "HANA":
                self._DB_QUERY = f"""
                    SELECT
                        CRSCR_OAST_CLEANDB_AMT,
                        CRSCR_REINS_DDB_AMT,
                        CRDCLCR_OAST_CLN_AMT,
                        CRDGTCR_OAST_CLN_AMT,
                        (CRSCR_OAST_CLEANDB_AMT - CRSCR_OAST_RCRVN_MD_DDB_AMT) AS CRSCR_OAST_RCRVN_MD_DDB_AMT,
                        (CRDCLCR_OAST_CLN_AMT + CRDGTCR_OAST_CLN_AMT - CRDGTCR_OAST_RCRML_AMT) as CRDCLCR_OAST_CLN_AMT_S
                    FROM
                        {self._DB_TABLE}
                    WHERE
                        [Step Date] = '{report_date}' AND [KICS Scenario] = {scenario}
                """

            case "DGB":
                self._DB_QUERY = f"""
                    SELECT
                        ACRSCR_OAST_CLEANDB_AMT,
                        CRSCR_REINS_DDB_AMT,
                        CRDCLCR_OAST_CLN_AMT,
                        CRDGTCR_OAST_CLN_AMT
                    FROM
                        {self._DB_TABLE}
                    WHERE
                        [Step Date] = '{report_date}' AND [KICS Scenario] = {scenario}
                """
