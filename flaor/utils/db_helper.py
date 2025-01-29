from cm_dashboards.flaor.utils import abstract_handler as gf
from cm_dashboards.flaor.utils import helpers as helpers

reporting_dates = [
    "2023-06-30",
    "2024-06-30",
    "2025-06-30",
    "2026-06-30",
    "2027-06-30",
    "2028-06-30",
]


class TableInfos(gf.GenericHandler):
    """
    Table mapping is a special case, as it is used to get the list of tables
    """

    _DB_TABLE = "T_Table_Mapping"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"

    def __init__(self, table_name=None):
        if table_name is not None:
            self._DB_TABLE = table_name
            self._DB_QUERY = f"SELECT * FROM [{self._DB_TABL}]"


class SolvencyOverall(gf.GenericHandler):
    """
    Solvency Overall data
    """

    global reporting_dates

    _DB_TABLE = "A_AC"
    _DB_QUERY = f"""
        SELECT
            [Step Date] AS Report_Date,
            ROUND(SMRT * 100, 1) AS KICS_Ratio,
            AVCPT_TTL_AMT AS Available_Capital,
            CSTK_RLTD_CPTL_AMT AS Common_Equity,
            CSCRT_CSTK_OTH_AMT AS Capital_Securities,
            RTEAM AS Retained_Earnings,
            CADJ_AMT AS Capital_Adjustments,
            OCI_ATA AS AOCI,
            ADJ_RSA AS Capital_Surplus,
            RQUAT_AMT AS Required_Capital
        FROM [{_DB_TABLE}]
        WHERE [Step Date] IN ({','.join([f"'{report_date}'" for report_date in reporting_dates])})
    """


class RequiredCapital(gf.GenericHandler):
    """
    Required Capital data
    """

    global reporting_dates

    _DB_TABLE = "A_RC"
    _DB_QUERY = f"""
        SELECT
            [Step Date] AS Report_Date,
            RQUAT_DCTAA_AMT AS Required_Capital,
            (
                LFLT_INSU_RSKA
                + MKRSK_TOT_AMT + CRRK_DIRTY_DDAF_AMT
                + GNDM_INSU_RSK_TOT_AMT + ORSK_TOT_AMT
            ) AS Required_Capital_Before_Diversification,
            LFLT_INSU_RSKA AS Life_and_Hearth_Risk,
            MKRSK_TOT_AMT AS Market_Risk,
            CRRK_DIRTY_DDAF_AMT AS Credit_Risk,
            GNDM_INSU_RSK_TOT_AMT AS Nonlife_Risk,
            ORSK_TOT_AMT AS Operational_Risk
        FROM [{_DB_TABLE}]
        WHERE [Step Date] IN ({','.join([f"'{report_date}'" for report_date in reporting_dates])})
    """


class AssetPortfolioIndividual(gf.GenericHandler):
    """
    Asset Portfolio individual data
    """

    global reporting_dates

    _DB_TABLE = "A_Company"
    _DB_QUERY = f"""
        SELECT
            (A_Company.[Step Date]) AS Report_Date,
            (A_Company.BE_NAV) AS Net_Asset_Value,
            (A_Assets_Total.Assets_Total) AS Assets,
            (A_Assets_Total.Value_Market_Rebalanced_Bond) AS Bond,
            (A_Assets_Total.Value_Market_Rebalanced_Bus_Loan) AS Loan,
            (A_Assets_Total.Value_Market_Rebalanced_Cash) AS Cash,
            (A_Assets_Total.Value_Market_Rebalanced_Equity) AS Equity,
            (A_Assets_Total.Value_Market_Rebalanced_Property) AS Property,
            ROUND((A_Assets_Total.Value_Market_Rebalanced_Bond / A_Assets_Total.Assets_Total) * 100, 2) AS Bond_Percent,
            ROUND((A_Assets_Total.Value_Market_Rebalanced_Bus_Loan / A_Assets_Total.Assets_Total) * 100, 2) AS Loan_Percent,
            ROUND((A_Assets_Total.Value_Market_Rebalanced_Cash / A_Assets_Total.Assets_Total) * 100, 2) AS Cash_Percent,
            ROUND((A_Assets_Total.Value_Market_Rebalanced_Equity / A_Assets_Total.Assets_Total) * 100, 2) AS Equity_Percent,
            ROUND((A_Assets_Total.Value_Market_Rebalanced_Property / A_Assets_Total.Assets_Total) * 100, 2) AS Property_Percent,
            (A_Company.BE_Liability) AS Liabs_WO_TVOG
        FROM
            A_Company
        LEFT JOIN
            A_Assets_Total ON A_Company.[Step Date] = A_Assets_Total.[Step Date]
        LEFT JOIN
            A_Liabs_Total ON A_Company.[Step Date] = A_Liabs_Total.[Step Date]
        WHERE A_Company.[Step Date] IN ({','.join([f"'{report_date}'" for report_date in reporting_dates])})
        GROUP BY
            A_Company.[Step Date],
            A_Company.BE_NAV,
            A_Assets_Total.Assets_Total,
            A_Assets_Total.Value_Market_Rebalanced_Bond,
            A_Assets_Total.Value_Market_Rebalanced_Bus_Loan,
            A_Assets_Total.Value_Market_Rebalanced_Cash,
            A_Assets_Total.Value_Market_Rebalanced_Equity,
            A_Assets_Total.Value_Market_Rebalanced_Property,
            A_Company.BE_Liability
    """


class AssetPortfolioGroup(gf.GenericHandler):
    """
    Asset Portfolio group data
    """

    global reporting_dates

    _DB_TABLE = "A_Company"
    _DB_QUERY = """
        SELECT
            (A_Company.[Step Date]) AS Report_Date,
            SUM(A_Company.Asset_CF_Total) AS Asset_CFs,
            SUM(A_Company.Liab_CF_Total) AS Liability_CFs,
            SUM(A_Company.Liquidity_Gap) AS Liquidity_Gap,
            SUM(A_Liabs_Total.BE_VNB) AS New_business,
            SUM(A_Company.RoAM_Rate) AS Avg_of_Return_on_Asset_Management,
            SUM(A_Company.i_CR_Dynamic) AS Avg_of_Crediting_Rate
        FROM
            A_Company
        LEFT JOIN
            A_Assets_Total ON A_Company.[Step Date] = A_Assets_Total.[Step Date]
        LEFT JOIN
            A_Liabs_Total ON A_Company.[Step Date] = A_Liabs_Total.[Step Date]
        GROUP BY
            A_Company.[Step Date]  
    """


class AssetPortfolioUniqueData(gf.GenericHandler):
    """
    Get Asset Portfolio by joining multiple tables
    """

    global reporting_dates

    _DB_TABLE = "A_Assets_Total"
    _DB_QUERY = f"""
        SELECT
            A_Bond.Value_Market_Pre_Rebalance AS Bond,
            A_Bus_Loan.Value_Market_Pre_Rebalance AS Loan,
            A_Cash.Value_Market_Pre_Rebalance AS Cash,
            A_Equity.Value_Market_Pre_Rebalance AS Equity,
            A_Property.Value_Market_Pre_Rebalance AS Property
        FROM
            A_Assets_Total
        LEFT JOIN
            A_Bond ON A_Assets_Total.[Step Date] = A_Bond.[Step Date]
        LEFT JOIN
            A_Bus_Loan ON A_Assets_Total.[Step Date] = A_Bus_Loan.[Step Date]
        LEFT JOIN
            A_Cash ON A_Assets_Total.[Step Date] = A_Cash.[Step Date]
        LEFT JOIN
            A_Equity ON A_Assets_Total.[Step Date] = A_Equity.[Step Date]
        LEFT JOIN
            A_Property ON A_Assets_Total.[Step Date] = A_Property.[Step Date]
        WHERE A_Assets_Total.[Step Date] = '{reporting_dates[0]}'
        """


class ProjectedRiskRegulatory(gf.GenericHandler):
    """
    Projected Risk Regulatory data
    """

    global reporting_dates

    _DB_TABLE = "A_KICS_PAP_BS"
    _DB_QUERY = f"""
        SELECT
            [Step Date] AS Report_Date,
            PAP_BS_110000000000 AS Assets_on_Management,
            PAP_BS_120000000000 AS Assets_NonOperating,
            (PAP_BS_200200101000 - PAP_BS_200200101022 + PAP_BS_200200201000) AS BE_Liabilities_WO_TVOG,
            PAP_BS_200200101022 AS TVOG,
            (PAP_BS_200200102000 + PAP_BS_200200202000) AS LIC,
            PAP_BS_200300000000 AS Risk_Margin,
            PAP_BS_210000000000 AS Other_Liabilities,
            (PAP_BS_110000000000 + PAP_BS_120000000000) AS Assets_Total,
            (
                PAP_BS_200200101000 - PAP_BS_200200101022 + PAP_BS_200200201000
                + PAP_BS_200200102000 + PAP_BS_200200202000
                + PAP_BS_200200101022 + PAP_BS_200300000000
                + PAP_BS_210000000000
            ) AS Liabilities_Total,
            (
                (
                    PAP_BS_110000000000 + PAP_BS_120000000000
                ) - (
                    PAP_BS_200200101000 - PAP_BS_200200101022 + PAP_BS_200200201000
                    + PAP_BS_200200102000 + PAP_BS_200200202000
                    + PAP_BS_200200101022 + PAP_BS_200300000000
                    + PAP_BS_210000000000
                )
            ) AS Capital_Total

        FROM
            [{_DB_TABLE}]
        WHERE
            [Step Date] IN ({','.join([f"'{report_date}'" for report_date in reporting_dates])})
    """


class LifeAndHealthRisk(gf.GenericHandler):
    """
    Life and Health Risk data
    """

    _DB_TABLE = "A_Life_Risk_ToT"
    _DB_QUERY = f"""
        SELECT
            [Step Date] AS Report_Date,
            CAST(LFLTIN_RSKA AS INTEGER) AS Life_Health_Risk,
            DTH_RSK_CLRITC_AMT AS Mortality,
            CAST(LGV_RSK_CLRITC_AMT AS INTEGER) AS Longevity,
            DSDS_RSK_CLRITC_AMT AS Morbidity,
            DSDSAM_SHTM_NAST_DEP_CLRITC_AMT AS Morbidity_Fixed,
            DSDSRM_SHTM_NAST_DEP_CLRITC_AMT AS Morbidity_Indemnity,
            CNC_RSK_CLRITC_AMT AS Lapse,
            OPERT_ISHT_NAST_DEP_CLRITC_AMT AS Lapse_Up,
            OPERT_DSHK_NAST_DEP_CLRITC_AMT AS Lapse_Down,
            MCC_SHTM_NAST_DEP_CLRITC_AMT AS Lapse_Mass,
            BZCF_RSK_CLRITC_AMT AS Expense,
            CTDS_RSK_VLU AS Catastrophe
        FROM
            [{_DB_TABLE}]
        WHERE
            [Step Date] IN ({','.join([f"'{report_date}'" for report_date in reporting_dates])})
    """


class MarketRisk(gf.GenericHandler):
    """
    Market Risk data
    """

    _DB_TABLE = "A_Market_Risk_ToT"
    _DB_QUERY = f"""
        SELECT
            [Step Date] AS Report_Date,
            MKRSK_TOT_AMT AS Market_Risk,
            IRRSK_TTAM_AMT AS Interest,
            IRRSK_TTAM_AVRC_AMT AS Interest_RM,
            IRRSK_TTAM_IRU_AMT AS Interest_LU,
            IRRSK_TTAM_IRDN_AMT AS Interest_LD,
            IRRSK_TTAM_IRPL_AMT AS Interest_Flat,
            IRRSK_TTAM_IRDC_AMT AS Interest_Slope,
            STK_RSKA AS Equity,
            STRSK_AVMK_LSST_CRNB_AMT AS Equity_Developed,
            STRSK_NCMKT_LSST_CRNB_AMT AS Equity_Emerging,
            STRSK_INFRA_STK_CRNB_AMT AS Equity_Infra,
            STRSK_PFSTK_CRNB_AMT AS Equity_Preferred,
            STRSK_LHST_CRNB_AMT AS Equity_Long_Term,
            STRSK_OSCT_CRNB_AMT AS Equity_Other,
            FRSAM_TOT_AMT AS Forex,
            FRSAM_ERTU_TOT_AMT AS Forex_Up,
            FRSAM_ERTD_TOT_AMT AS Forex_Down,
            FRSAM_RPCVA_AMT AS Volatility,
            CAST(PPRSKA_AMT AS INTEGER) AS Property,
            ASFC_RSKA_TOT_AMT AS Concentration,
            ASFRS_SGRP_RSKA AS Counterparty_Conc,
            PRPT_ASFRS_FNL_EXPS_AMT AS Property_Conc
        FROM
            [{_DB_TABLE}]
        WHERE
            [Step Date] IN ({','.join([f"'{report_date}'" for report_date in reporting_dates])})
    """


class CreditRisk(gf.GenericHandler):
    """
    Credit Risk data
    """

    _DB_TABLE = "A_Credit_Risk_ToT"
    _DB_QUERY = f"""
        SELECT
            [Step Date] AS Report_Date,
            CRSK_DIRTYDA_AMT AS Credit_Risk,
            CRSCR_CLEANDA_AMT AS Non_Collateralised_Total,
            CRSCR_NRSK_CLEANDA_AMT AS Risk_Free,
            CRSCR_PBPT_CLEANDA_AMT AS Public_Inst,
            CRSCR_GNCP_CLEANDA_AMT AS General_Corp,
            CRSCR_FLT_CLEANDA_AMT AS Securitisation,
            CRSCR_RFLZN_CLEANDA_AMT AS Re_Securitisation,
            CRSCR_REINS_DDAF_AMT AS Reinsurance_Assets,
            CRSCR_OAST_CLEANDA_AMT AS Other_Assets,
            CRSK_CLTR_CLEANDA_AMT AS Collateralised_Total,
            CRSK_CLTR_BPPT_CLEANDA_AMT AS Commercial,
            CRSK_CLAST_MGCLT_CLEANDA_AMT AS Mortgage
        FROM
            [{_DB_TABLE}]
        WHERE
            [Step Date] IN ({','.join([f"'{report_date}'" for report_date in reporting_dates])})
    """
