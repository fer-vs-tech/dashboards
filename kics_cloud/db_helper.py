from cm_dashboards.kics_cloud import abstract_handler as gf
from cm_dashboards.kics_cloud import helpers as helpers

"""
 ['A_AC', 'A_BALANCE_SHEET', 'A_CREDIT_RISK_TOT', 'A_EQUITY_RISK', 'A_INT_RISK_TOT',
 'A_KICS_CUR_BS', 'A_KICS_MV_BS', 'A_KICS_PC_BS', 'A_LIFE_RISK_TOT', 'A_MARKET_RISK',
 'A_MARKET_RISK_Calc', 'A_OPERATION_RISK', 'A_PROPERTY_RISK', 'A_RC', 'G_ACC_LIAB',
 'G_CREDIT_RISK_TOT', 'G_INT_RISK_ASSET', 'G_LIFE_RISK_TOT', 'G_MARKET_RISK_Calc',
 'I_MARKET_RISK_Calc', 'O_CONCEN_G_RISK_GROUP', 'O_CONCEN_P_RISK_GROUP', 'O_CREDIT_RISK',
 'O_CREDIT_RISK_OTHER', 'O_FOREX_RISK_GROUP', 'O_LIFE_RISK', 'R_Info_RuntimeParameters',
 'Rc_RuntimeParameters', 'Rd_RuntimeParameters', 'Rn_RuntimeParameters', 'T_Table_Mapping',
 'Z_Info_DataLayer_Available_Capital_Data', 'Z_Info_DataLayer_Forex_Risk_Liab_Input', 'Z_Info_DataLayer_Reinsurance_Input',
 'Z_Info_Layer', 'Z_Info_Model', 'Zc_Layer', 'Zc_Model', 'Zn_DataLayer_Available_Capital_Data',
 'Zn_DataLayer_Forex_Risk_Liab_Input', 'Zn_DataLayer_Reinsurance_Input', 'Zn_Layer', 'Zn_Model']

  ['I_Company', 'R_Info_RuntimeParameters', 'Rc_RuntimeParameters', 'Rd_RuntimeParameters',
  'Rn_RuntimeParameters', 'T_Table_Mapping', 'Z_Info_DataLayer_Bond_KRW', 'Z_Info_DataLayer_Bond_USD',
  'Z_Info_Layer', 'Z_Info_Model', 'Zc_DataLayer_Bond_KRW', 'Zc_DataLayer_Bond_USD', 'Zc_Model',
  'Zn_DataLayer_Bond_KRW', 'Zn_DataLayer_Bond_USD', 'Zn_Layer', 'Zn_Model']
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
            self._DB_QUERY = f"SELECT * FROM [{self._DB_TABL}]"

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class CompanyLevelAssetRisk(gf.GenericHandler):
    """
    Company Level Asset Risk
    """

    _DB_QUERY = None

    def __init__(self, report_date="2022-12-31"):
        self._DB_QUERY = f"""
        SELECT
            SUM(A_MARKET_RISK.Int_Risk_Total) as Interest_Risk,
            SUM(A_MARKET_RISK.Equity_Risk_TOT) as Equity_Risk,
            SUM(A_MARKET_RISK.Asset_Concen_Risk_Total) as Concentration_Risk,
            SUM(A_MARKET_RISK.Property_Risk) as Property_Risk,
            SUM(A_MARKET_RISK.Forex_Risk_TOT) as Forex_Risk,
            SUM(A_MARKET_RISK.Market_Risk_Total) as Market_Risk,
            SUM(A_CREDIT_RISK_TOT.Credit_Risk_Total) as Credit_Risk
        FROM
            A_MARKET_RISK
        LEFT JOIN
            A_CREDIT_RISK_TOT ON A_MARKET_RISK.[Step Date] = A_CREDIT_RISK_TOT.[Step Date]
        WHERE
            A_CREDIT_RISK_TOT.[Step Date] = '{report_date}'
        """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class ProductLevelAssetRisk(gf.GenericHandler):
    """
    Product Level Asset Risk
    """

    _DB_QUERY = None

    def __init__(self, report_date="2022-12-31"):
        self._DB_QUERY = f"""
        SELECT
            G_MARKET_RISK_Calc.[KICS_IR_Group Value] as Product,
            G_MARKET_RISK_Calc.Int_Risk_Total as Interest_Risk,
            G_MARKET_RISK_Calc.Equity_Risk_TOT as Equity_Risk,
            G_MARKET_RISK_Calc.Asset_Concen_Risk_Total as Concentration_Risk,
            G_MARKET_RISK_Calc.Property_Risk as Property_Risk,
            G_MARKET_RISK_Calc.Forex_Risk_TOT as Forex_Risk,
            G_MARKET_RISK_Calc.Market_Risk_Total as Market_Risk,
            G_CREDIT_RISK_TOT.Credit_Risk_Total as Credit_Risk
        FROM
            G_MARKET_RISK_Calc
                LEFT JOIN G_CREDIT_RISK_TOT ON G_MARKET_RISK_Calc.[KICS_IR_Group Value] = G_CREDIT_RISK_TOT.[KICS_IR_Group Value]
                AND G_MARKET_RISK_Calc.[Step Date] = G_CREDIT_RISK_TOT.[Step Date]
        WHERE
            (G_MARKET_RISK_Calc.[KICS_IR_Group Value] = 'Trad' OR G_MARKET_RISK_Calc.[KICS_IR_Group Value] = 'UL')
            AND
            G_MARKET_RISK_Calc.[Step Date] = '{report_date}'
        ORDER BY
            G_MARKET_RISK_Calc.[KICS_IR_Group Value] ASC
        """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class AssetInfo(gf.GenericHandler):
    """
    Asset Info
    """

    _DB_QUERY = None

    def __init__(self, report_date):
        self._DB_QUERY = f"""
        SELECT
            Asset_Group,
            SUM(
                CASE
                    WHEN IAS39_BS_Account_Code IN ('23', '24', '25', '26') THEN Value_Market_PP_KRW - Accrued_Interest_KRW
                    ELSE Value_Market_PP_KRW
                END
            ) AS Market_Value
        FROM
            I_Company
        WHERE
            [CF Call Date] = '{report_date}'
        GROUP BY
            Asset_Group
        """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class ProductLevelLifeRisk(gf.GenericHandler):
    """
    Product Level Life Risk Total
    """

    _DB_QUERY = None

    def __init__(self, report_date="2022-12-31"):
        self._DB_QUERY = f"""
        SELECT
            [Record Number] as Record_Number,
            KICS_PDT_GROP_COD as Product,
            DSOER_NADA as Lapse_down,
            LAG_SCCN_NADA as Lapse_mass,
            USOER_NADA as Lapse_up,
            DISA_DSAS_RSK_AMT as Morbidity,
            DTH_RSK_AMT as Mortality,
            LGV_RSK_AMT as Longetivty,
            UE_RSK_AMT as Expense,
            CE_Base_Det as BEL,
            RSUR_AST_CVAL as BEL_Reins
        FROM
            O_LIFE_RISK
        WHERE
            [Step Date] = '{report_date}'
        """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class CompanyLevelLifeRiskTotal(gf.GenericHandler):
    """
    Company Level Life Risk Total
    """

    _DB_QUERY = None

    def __init__(self, report_date="2022-12-31"):
        self._DB_QUERY = f"""
        SELECT
            SUM(dNAV_Life_Expense) as Expense,
            SUM(dNAV_Life_Lapse) as Lapse,
            SUM(dNAV_Life_Longevity) as Longevity,
            SUM(dNAV_Life_Morb) as Morbidity,
            SUM(dNAV_Life_Mortality) as Mortality,
            SUM(Life_Insurance_Risk) as Insurance_Risk,
            SUM(Risk_Margin) as Risk_Margin
        FROM
            G_LIFE_RISK_TOT
        WHERE
            [Step Date] = '{report_date}'
        """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class ProductLevelLifeRiskTotal(gf.GenericHandler):
    """
    Product Level Life Risk Total
    """

    _DB_QUERY = None

    def __init__(self, report_date="2022-12-31"):
        self._DB_QUERY = f"""
        SELECT
            [KICS_IR_Group Value] as Product,
            dNAV_Life_Expense as Expense,
            dNAV_Life_Lapse as Lapse,
            dNAV_Life_Longevity as Longevity,
            dNAV_Life_Morb as Morbidity,
            dNAV_Life_Mortality as Mortality,
            Life_Insurance_Risk as Insurance_Risk,
            Risk_Margin
        FROM
            G_LIFE_RISK_TOT
        WHERE
            ([KICS_IR_Group Value] = 'Trad' OR [KICS_IR_Group Value] = 'UL') 
            AND
            [Step Date] = '{report_date}'
        """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class OperationRiskTotal(gf.GenericHandler):
    """
    Operation Risk Total
    """

    _DB_QUERY = None

    def __init__(self, report_date="2022-12-31"):
        self._DB_QUERY = f"""
        SELECT
            Operation_Risk_Total as Operation_Risk
        FROM
            A_AC
        WHERE
            [Step Date] = '{report_date}'
        """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class LiabilityMovement(gf.GenericHandler):
    """
    Liability Movement
    """

    _DB_QUERY = None

    def __init__(self, report_date="2022-12-31"):
        self._DB_QUERY = f"""
        SELECT
            (CE_Base_WO_Res_Liab/1000000) as Best_Estimate_Liability,
            (Risk_Margin/1000000) as Risk_Margin
        FROM
            A_AC
        WHERE
            [Step Date] = '{report_date}'
        """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class AssetMovement(gf.GenericHandler):
    """
    Asset Movement
    """

    _DB_QUERY = None

    def __init__(self, report_date="2022-12-31"):
        self._DB_QUERY = f"""
        SELECT
            (KICS_MV_BS_10000000/1000000) as Asset
        FROM
            A_BALANCE_SHEET
        WHERE
            [Step Date] = '{report_date}'
        """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class InsuranceAndMarketRisk(gf.GenericHandler):
    """
    Insurance and Market Risk
    """

    _DB_QUERY = None

    def __init__(self, report_date="2022-12-31"):
        self._DB_QUERY = f"""
        SELECT
            (Insurance_Risk_Total/1000000) as Insurance_Risk,
            (Market_Risk_Total/1000000) as Market_Risk
        FROM
            A_AC
        WHERE
            [Step Date] = '{report_date}'
        """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class RatioMovement(gf.GenericHandler):
    """
    K-ICS Ratio Movement
    """

    _DB_QUERY = None

    def __init__(self, report_date="2022-12-31"):
        self._DB_QUERY = f"""
        SELECT
            (AC_Total/1000000) as Available_Capital,
            (Required_Capital/1000000) as Required_Capital,
            (KICS_Rate*100) as KICS_Ratio
        FROM
            A_AC
        WHERE
            [Step Date] = '{report_date}'
        """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class CapitalAndIndividualRisksMovement(gf.GenericHandler):
    """
    Required Capital & individual risks Movement
    """

    _DB_QUERY = None

    def __init__(self, report_date="2022-12-31"):
        self._DB_QUERY = f"""
        SELECT
            (SUM(A_AC.Required_Capital)/1000000) as Required_Capital,
            (SUM(A_AC.Insurance_Risk_Total)/1000000) as Insurance_Risk,
            (SUM(A_AC.Market_Risk_Total)/1000000) as Market_Risk,
            (SUM(A_AC.Credit_Risk_Reduced_Total)/1000000) as Credit_Risk,
            (SUM(A_AC.Operation_Risk_Total)/1000000) as Operation_Risk,
            (SUM(A_MARKET_RISK.Int_Risk_Total)/1000000) as Interest_Risk,
            (SUM(A_MARKET_RISK.Equity_Risk_TOT)/1000000) as Equity_Risk,
            (SUM(A_MARKET_RISK.Asset_Concen_Risk_Total)/1000000) as Concentration_Risk,
            (SUM(A_MARKET_RISK.Property_Risk)/1000000) as Property_Risk,
            (SUM(A_MARKET_RISK.Forex_Risk_TOT)/1000000) as Forex_Risk,
            (SUM(A_LIFE_RISK_TOT.dNAV_Life_Expense)/1000000) as Expense,
            (SUM(A_LIFE_RISK_TOT.dNAV_Life_Lapse)/1000000) as Lapse,
            (SUM(A_LIFE_RISK_TOT.dNAV_Life_Longevity)/1000000) as Longevity,
            (SUM(A_LIFE_RISK_TOT.dNAV_Life_Morb)/1000000) as Morbidity,
            (SUM(A_LIFE_RISK_TOT.dNAV_Life_Mortality)/1000000) as Mortality
        FROM
            A_AC
        LEFT JOIN
            A_MARKET_RISK ON A_AC.[Step Date] = A_MARKET_RISK.[Step Date]
        LEFT JOIN
            A_LIFE_RISK_TOT ON A_AC.[Step Date] = A_LIFE_RISK_TOT.[Step Date]
        WHERE
            A_AC.[Step Date] = '{report_date}'
        """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class InterestRateSensitivity(gf.GenericHandler):
    """
    Interest Rate Sensitivity
    """

    _DB_QUERY = None

    def __init__(self, report_date="2022-12-31"):
        self._DB_QUERY = f"""
        SELECT
            Group_ID,
            (SUM(BEL_Base)/1000000) as BEL_Base
        FROM
            G_Company
        WHERE
            [Step Date] = '{report_date}'
        GROUP BY Group_ID
        """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class AvailableCapital(gf.GenericHandler):
    """
    Available Capital
    """

    _DB_QUERY = None

    def __init__(self, report_date="2022-12-31"):
        self._DB_QUERY = f"""
        SELECT
            (AC_Total/1000000) as Available_Capital,
            (C_Tier1_Total/1000000) as Tier_1,
            (C_Tier2_Total/1000000) as Tier_2,
            ((C_Tier1_Total - Adjustment_Reserve)/1000000) as Capital,
            (Adjustment_Reserve/1000000) as Adjustment_Reserve
        FROM
            A_AC
        WHERE
            [Step Date] = '{report_date}'
        """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class TierOne(gf.GenericHandler):
    """
    Tier 1
    """

    _DB_QUERY = None

    def __init__(self, report_date="2022-12-31"):
        self._DB_QUERY = f"""
        SELECT
            (C_Tier1_Total/1000000) as Tier_1
        FROM
            A_AC
        WHERE
            [Step Date] = '{report_date}'
        """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class TierTwo(gf.GenericHandler):
    """
    Tier 2
    """

    _DB_QUERY = None

    def __init__(self, report_date="2022-12-31"):
        self._DB_QUERY = f"""
        SELECT
            (C_Tier2_Total/1000000) as Tier_2
        FROM
            A_AC
        WHERE
            [Step Date] = '{report_date}'
        """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df
