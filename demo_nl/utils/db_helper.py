from cm_dashboards.demo_nl.utils import abstract_handler as gf
from cm_dashboards.demo_nl.utils import helpers as helpers


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


class FutureBSProjection(gf.GenericHandler):
    """
    Future BS Projection
    """

    _DB_TABLE = "A_Realistic_RN>Company"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"

    def __init__(self, report_dates):
        self._DB_QUERY = f"""
        SELECT
            [Step Date] AS Report_Date,
            [Realistic_RN Call Date] AS Call_Date,
            [Realistic_RN Scenario] as Scenario,
            Net_Asset_Value,
            Assets_Total,
            Liability_BE_Total,
            Value_New_Business,
            Liability_NP,
            Asset_Share_IF,
            Disc_CF_WP_Total
        FROM [{self._DB_TABLE}]
        WHERE [Realistic_RN Call Date] IN ({','.join([f"'{report_date}'" for report_date in report_dates])})
        AND [Step Date] IN ({','.join([f"'{report_date}'" for report_date in report_dates])})
        AND [Realistic_RN Scenario] = '1'
        AND [Realistic_RN Call Date] = [Step Date]
    """


class RCInformation(gf.GenericHandler):
    """
    RC Information table with all needed columns
    """

    _DB_TABLE = "A_SCR_Group"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"

    def __init__(self, report_date):
        self._DB_QUERY = f"""
        SELECT
            SCR,
            MCR,
            Risk_Margin,
            NAV_Base,
            Asset_Total,
            Liability_BE_Total,
            BSCR,
            SCR_Op,
            Adj,
            BSCR,
            SCR_Mkt,
            SCR_Life,
            SCR_NonLife,
            SCR_Health,
            SCR_Def,
            SCR_Life_Cat,
            SCR_Life_Exp,
            SCR_Life_Lapse,
            SCR_Life_LapseDown,
            SCR_Life_LapseMass,
            SCR_Life_LapseUp,
            SCR_Life_Long,
            SCR_Life_Morb,
            SCR_Life_Mort,
            SCR_Life_Rev,
            SCR_Mkt_Eq,
            SCR_Mkt_Eq_Type_1,
            SCR_Mkt_Eq_Type_2,
            SCR_Mkt_FX,
            SCR_Mkt_FX_Down_1,
            SCR_Mkt_FX_Up_1,
            SCR_Mkt_Int,
            SCR_Mkt_IntDown,
            SCR_Mkt_IntUp,
            SCR_Mkt_Prop,
            SCR_Mkt_Sp,
            SCR_Mkt_Sp_Bond_Infra_Corp,
            SCR_Mkt_Sp_Bond_Infra_Invest,
            SCR_Mkt_Sp_Bond_No_Infra,
            SCR_Mkt_Sp_Securitisation,
            SCR_Mkt_Sp_CD,
            SCR_Health_NonSLT,
            SCR_Health_SLT,
            SCR_Health_SLT_Exp,
            SCR_Health_SLT_Lapse,
            SCR_Health_SLT_LapseDown,
            SCR_Health_SLT_LapseMass,
            SCR_Health_SLT_LapseUp,
            SCR_Health_SLT_Long,
            SCR_Health_SLT_Morb,
            SCR_Health_SLT_MorbidityIncome,
            SCR_Health_SLT_MorbidityMedical,
            SCR_Health_SLT_MorbidityMedicalDown,
            SCR_Health_SLT_MorbidityMedicalUp,
            SCR_Health_SLT_Mort,
            SCR_Health_SLT_Rev,
            SCR_Op,
            BSCR,
            ExpUL,
            OP,
            OP_Premium,
            Earn_Life,
            Earn_LifeUL,
            Earn_NL,
            pEarn_Life,
            pEarn_LifeUL,
            pEarn_NL,
            OP_Provision,
            TP_Life_Gross_Reins,
            TP_LifeUL_Gross_Reins,
            TP_NL_Gross_Reins,
            Adj,
            Adj_TP,
            BSCR,
            nBSCR,
            FDB,
            Adj_DT,
            (SCR - MCR) as SCR_MCR,
            (Liability_BE_Total + Risk_Margin + MCR + SCR - MCR) as Total_Liab,
            (SCR_Mkt * BSCR / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def)) AS RiskDiversifed_1,
            (SCR_Life * BSCR / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def)) AS RiskDiversifed_2,
            (SCR_Health * BSCR / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def)) AS RiskDiversifed_3,
            (SCR_NonLife * BSCR / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def)) AS RiskDiversifed_4,
            (SCR_Def * BSCR / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def)) AS RiskDiversifed_5,
            (SCR_Mkt / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def + SCR_Op)) AS RiskPropotion_1,
            (SCR_Life / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def + SCR_Op)) AS RiskPropotion_2,
            (SCR_Health / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def + SCR_Op)) AS RiskPropotion_3,
            (SCR_NonLife / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def + SCR_Op)) AS RiskPropotion_4,
            (SCR_Def / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def + SCR_Op)) AS RiskPropotion_5,
            (SCR_Op / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def + SCR_Op)) AS RiskPropotion_6,
            (SCR_Mkt_Int * SCR_Mkt / (SCR_Mkt_Int + SCR_Mkt_Sp + SCR_Mkt_FX + SCR_Mkt_Eq + SCR_Mkt_Prop) * BSCR / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def)) AS MarketDiversifed_1,
            (SCR_Mkt_Sp * SCR_Mkt / (SCR_Mkt_Int + SCR_Mkt_Sp + SCR_Mkt_FX + SCR_Mkt_Eq + SCR_Mkt_Prop) * BSCR / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def)) AS MarketDiversifed_2,
            (SCR_Mkt_FX * SCR_Mkt / (SCR_Mkt_Int + SCR_Mkt_Sp + SCR_Mkt_FX + SCR_Mkt_Eq + SCR_Mkt_Prop) * BSCR / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def)) AS MarketDiversifed_3,
            (SCR_Mkt_Eq * SCR_Mkt / (SCR_Mkt_Int + SCR_Mkt_Sp + SCR_Mkt_FX + SCR_Mkt_Eq + SCR_Mkt_Prop) * BSCR / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def)) AS MarketDiversifed_4,
            (SCR_Mkt_Prop * SCR_Mkt / (SCR_Mkt_Int + SCR_Mkt_Sp + SCR_Mkt_FX + SCR_Mkt_Eq + SCR_Mkt_Prop) * BSCR / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def)) AS MarketDiversifed_5,
            (SCR_Mkt_Int / (SCR_Mkt_Int + SCR_Mkt_Sp + SCR_Mkt_FX + SCR_Mkt_Eq + SCR_Mkt_Prop)) AS MarketProportion_1,
            (SCR_Mkt_Sp / (SCR_Mkt_Int + SCR_Mkt_Sp + SCR_Mkt_FX + SCR_Mkt_Eq + SCR_Mkt_Prop)) AS MarketProportion_2,
            (SCR_Mkt_FX / (SCR_Mkt_Int + SCR_Mkt_Sp + SCR_Mkt_FX + SCR_Mkt_Eq + SCR_Mkt_Prop)) AS MarketProportion_3,
            (SCR_Mkt_Eq / (SCR_Mkt_Int + SCR_Mkt_Sp + SCR_Mkt_FX + SCR_Mkt_Eq + SCR_Mkt_Prop)) AS MarketProportion_4,
            (SCR_Mkt_Prop / (SCR_Mkt_Int + SCR_Mkt_Sp + SCR_Mkt_FX + SCR_Mkt_Eq + SCR_Mkt_Prop)) AS MarketProportion_5,
            (SCR_Life_Cat * SCR_Life / (SCR_Life_Cat + SCR_Life_Exp + SCR_Life_Lapse + SCR_Life_Long + SCR_Life_Morb + SCR_Life_Mort + SCR_Life_Rev) * BSCR / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def)) AS LifeInsDiversifed_1,
            (SCR_Life_Exp * SCR_Life / (SCR_Life_Cat + SCR_Life_Exp + SCR_Life_Lapse + SCR_Life_Long + SCR_Life_Morb + SCR_Life_Mort + SCR_Life_Rev) * BSCR / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def)) AS LifeInsDiversifed_2,
            (SCR_Life_Lapse * SCR_Life / (SCR_Life_Cat + SCR_Life_Exp + SCR_Life_Lapse + SCR_Life_Long + SCR_Life_Morb + SCR_Life_Mort + SCR_Life_Rev) * BSCR / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def)) AS LifeInsDiversifed_3,
            (SCR_Life_Long * SCR_Life / (SCR_Life_Cat + SCR_Life_Exp + SCR_Life_Lapse + SCR_Life_Long + SCR_Life_Morb + SCR_Life_Mort + SCR_Life_Rev) * BSCR / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def)) AS LifeInsDiversifed_4,
            (SCR_Life_Morb * SCR_Life / (SCR_Life_Cat + SCR_Life_Exp + SCR_Life_Lapse + SCR_Life_Long + SCR_Life_Morb + SCR_Life_Mort + SCR_Life_Rev) * BSCR / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def)) AS LifeInsDiversifed_5,
            (SCR_Life_Mort * SCR_Life / (SCR_Life_Cat + SCR_Life_Exp + SCR_Life_Lapse + SCR_Life_Long + SCR_Life_Morb + SCR_Life_Mort + SCR_Life_Rev) * BSCR / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def)) AS LifeInsDiversifed_6,
            (SCR_Life_Rev * SCR_Life / (SCR_Life_Cat + SCR_Life_Exp + SCR_Life_Lapse + SCR_Life_Long + SCR_Life_Morb + SCR_Life_Mort + SCR_Life_Rev) * BSCR / (SCR_Mkt + SCR_Life + SCR_Health + SCR_NonLife + SCR_Def)) AS LifeInsDiversifed_7,
            (SCR_Life_Cat / (SCR_Life_Cat + SCR_Life_Exp + SCR_Life_Lapse + SCR_Life_Long + SCR_Life_Morb + SCR_Life_Mort + SCR_Life_Rev)) AS LifeInsProportion_1,
            (SCR_Life_Exp / (SCR_Life_Cat + SCR_Life_Exp + SCR_Life_Lapse + SCR_Life_Long + SCR_Life_Morb + SCR_Life_Mort + SCR_Life_Rev)) AS LifeInsProportion_2,
            (SCR_Life_Lapse / (SCR_Life_Cat + SCR_Life_Exp + SCR_Life_Lapse + SCR_Life_Long + SCR_Life_Morb + SCR_Life_Mort + SCR_Life_Rev)) AS LifeInsProportion_3,
            (SCR_Life_Long / (SCR_Life_Cat + SCR_Life_Exp + SCR_Life_Lapse + SCR_Life_Long + SCR_Life_Morb + SCR_Life_Mort + SCR_Life_Rev)) AS LifeInsProportion_4,
            (SCR_Life_Morb / (SCR_Life_Cat + SCR_Life_Exp + SCR_Life_Lapse + SCR_Life_Long + SCR_Life_Morb + SCR_Life_Mort + SCR_Life_Rev)) AS LifeInsProportion_5,
            (SCR_Life_Mort / (SCR_Life_Cat + SCR_Life_Exp + SCR_Life_Lapse + SCR_Life_Long + SCR_Life_Morb + SCR_Life_Mort + SCR_Life_Rev)) AS LifeInsProportion_6,
            (SCR_Life_Rev / (SCR_Life_Cat + SCR_Life_Exp + SCR_Life_Lapse + SCR_Life_Long + SCR_Life_Morb + SCR_Life_Mort + SCR_Life_Rev)) AS LifeInsProportion_7
        FROM [{self._DB_TABLE}]
        WHERE [Step Date] = '{report_date}'
        """


class RebalanceInfoAtBase(gf.GenericHandler):
    """
    Rebalance class for SCR Group
    """

    _DB_TABLE = "A_Realistic_RN>Assets_Total"
    _REPORT_DATE = [
        "2018-12-31",
        "2019-12-31",
        "2020-12-31",
        "2021-12-31",
        "2022-12-31",
        "2023-12-31",
    ]

    def __init__(self):
        self._DB_QUERY = f"""
        SELECT
            [Step Date] as ReportDate,
            [Realistic_RN Call Date] as CallDate,
            [Realistic_RN Scenario] as Scenario,
            Value_Market_Pre_Rebalance_Bond as Bond_1,
            Value_Market_Pre_Rebalance_Cash as Cash_1,
            Value_Market_Pre_Rebalance_Equity as Equity_1,
            Value_Market_Pre_Rebalance_Property as Property_1,
            Value_Market_Rebalanced_Bond as Bond_2,
            Value_Market_Rebalanced_Cash as Cash_2,
            Value_Market_Rebalanced_Equity as Equity_2,
            Value_Market_Rebalanced_Property as Property_2
        FROM [{self._DB_TABLE}]
        WHERE [Realistic_RN Call Date] = '2018-12-31'
        AND [Step Date] IN ({','.join([f"'{d}'" for d in self._REPORT_DATE])})
        """


class RebalanceAtCompanyLevel(gf.GenericHandler):
    """
    Rebalance class for SCR Group
    """

    _DB_TABLE = "A_Realistic_RN>Company"
    _REPORT_DATE = [
        "2018-12-31",
        "2019-12-31",
        "2020-12-31",
        "2021-12-31",
        "2022-12-31",
        "2023-12-31",
    ]

    def __init__(self):
        self._DB_QUERY = f"""
        SELECT
            [Step Date] as ReportDate,
            [Realistic_RN Call Date] as CallDate,
            [Realistic_RN Scenario] as Scenario,
            Liability_BE_Total,
            Liability_Total_Proxy
        FROM [{self._DB_TABLE}]
        WHERE [Realistic_RN Call Date] = '2018-12-31'
        AND [Step Date] IN ({','.join([f"'{d}'" for d in self._REPORT_DATE])})
        """



class nl_Dates(gf.GenericHandler):
    """
    RC Information table with all needed columns
    """

    _DB_TABLE = "G_Data_Chain_Ladder"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"

    def __init__(self, program):
        self._DB_TABLE = f"G_Data_{program}"
        self._DB_QUERY = f"""
        SELECT
            DISTINCT([Step Date]) AS report_date
        FROM [{self._DB_TABLE}]
        """


class nl_Programs(gf.GenericHandler):
    """
    RC Information table with all needed columns
    """

    _DB_TABLE = "T_Table_Mapping"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"

    def __init__(self):
        self._DB_QUERY = f"""
        SELECT
            DISTINCT(REPLACE([Program Name],'Data_','')) AS program_name        
        FROM [{self._DB_TABLE}]
        WHERE [Output Type] = 'Individual'
        """

class nl_Portfolios(gf.GenericHandler):
    """
    RC Information table with all needed columns
    """

    _DB_TABLE = "G_Data_Chain_Ladder"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"

    def __init__(self, program):
        self._DB_TABLE = f"G_Data_{program}"
        self._DB_QUERY = f"""
        SELECT
            DISTINCT([Grp Value]) AS portfolio
        FROM [{self._DB_TABLE}]
        """

class nl_TriangleSize(gf.GenericHandler):
    """
    RC Information table with all needed columns
    """

    _DB_TABLE = "I_Data_Chain_Ladder"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"

    def __init__(self, program):
        self._DB_TABLE = f"I_Data_{program}"
        self._DB_QUERY = f"""
        SELECT
            CAST(max([Tri_Dimension_Size_Dev]) AS integer) as dev, CAST(max([Tri_Dimension_Size_Origin]) AS integer) as origin 
        FROM [{self._DB_TABLE}]
        """

class nl_ClaimData(gf.GenericHandler):
    """
    RC Information table with all needed columns
    """

    _DB_TABLE = "I_Data_Chain_Ladder"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"

    def __init__(self, program, portfolio, method, var, rep_date, dev_value, orig_value):
        # if var == 'Tri_Paid_Claims_By_Year':
        #     var = "([Tri_Claim_Costs_By_Year] - [Tri_Case_Reserves_By_Year])"
        # elif var == "Tri_Paid_Claims":
        #     var = "([Tri_Claim_Costs] - [Tri_Case_Reserves])"
        # else:
        #     var = "[" + var + "]"
        var = "[" + var + "]"
        grouping = portfolio + "_" + method
        self._DB_TABLE = "I_Data_" + program
        self._DB_QUERY = f"""
        SELECT
            [Dev_Period_Position], [Origin_Period_Position], 
            ROUND({var},4) as returnValue 
            FROM [{self._DB_TABLE}]
            WHERE [Grouping_ID] = '{grouping}' AND [RunOff_Triangle Call Date] = '{rep_date}' 
            AND ([Dev_Period_Position] BETWEEN {dev_value[0]} AND {dev_value[1]})
            AND ([Origin_Period_Position] BETWEEN {orig_value[0]} AND {orig_value[1]})
            ORDER BY [Origin_Period_Position], [Record Number]                         
            """


class nl_ATA_Post_Stats(gf.GenericHandler):

    _DB_TABLE = "I_Data_Chain_Ladder"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"

    def __init__(self, program, portfolio, method, rep_date, dev_value, orig_value):
        grouping = portfolio + "_" + method
        self._DB_TABLE = "I_Data_" + program
        self._DB_QUERY = f"""
        SELECT
            [Dev_Period_Position],
            [Origin_Period_Position],
            [Age_To_Age_Factors_Var_Post_Outliers] AS [VAR], [Age_To_Age_Factors_Mu_Post_Outliers] AS [MU], 
            [Age_To_Age_Factors_Sigma_Post_Outliers] AS [SIGMA], [Age_To_Age_Factors_Mean] AS [MEAN] 
            FROM [{self._DB_TABLE}]
            WHERE [Grouping_ID] = '{grouping}' AND [RunOff_Triangle Call Date] = '{rep_date}' 
            AND ([Dev_Period_Position] BETWEEN {dev_value[0]} AND {dev_value[1]})
            AND ([Origin_Period_Position] = 1) 
            ORDER BY [Origin_Period_Position], [Record Number]                         
            """


class nl_ATA_Pre_Stats(gf.GenericHandler):

    _DB_TABLE = "I_Data_Chain_Ladder"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"

    def __init__(self, program, portfolio, method, rep_date, dev_value, orig_value):
        grouping = portfolio + "_" + method
        self._DB_TABLE = "I_Data_" + program
        self._DB_QUERY = f"""
        SELECT
            [Dev_Period_Position],
            [Origin_Period_Position],
            [Age_To_Age_Factors_Var_Pre_Outliers] AS [VAR], [Age_To_Age_Factors_Mu_Pre_Outliers] AS [MU], 
            [Age_To_Age_Factors_Sigma_Pre_Outliers] AS [SIGMA], [Age_To_Age_Factors_Mean] AS [MEAN] 
            FROM [{self._DB_TABLE}]
            WHERE [Grouping_ID] = '{grouping}' AND [RunOff_Triangle Call Date] = '{rep_date}' 
            AND ([Dev_Period_Position] BETWEEN {dev_value[0]} AND {dev_value[1]})
            AND ([Origin_Period_Position] = 1) 
            ORDER BY [Origin_Period_Position], [Record Number]                         
            """


class nl_ATA_Pre_Link_Ratios(gf.GenericHandler):

    _DB_TABLE = "I_Data_Chain_Ladder"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"

    def __init__(self, program, portfolio, method, rep_date, dev_value, orig_value):
        grouping = portfolio + "_" + method
        self._DB_TABLE = "I_Data_" + program
        self._DB_QUERY = f"""
        SELECT
        [Dev_Period_Position], [Origin_Period_Position], 
        ROUND([Age_To_Age_Factors_Pre_Outliers],4) as returnValue 
        FROM [{self._DB_TABLE}]
        WHERE [Grouping_ID] = '{grouping}' AND [RunOff_Triangle Call Date] = '{rep_date}' 
        AND ([Dev_Period_Position] BETWEEN {dev_value[0]} AND {dev_value[1]})
        AND ([Origin_Period_Position] BETWEEN {orig_value[0]} AND {orig_value[1]})
        ORDER BY [Origin_Period_Position], [Record Number]                         
        """

class nl_ATA_Post_Link_Ratios(gf.GenericHandler):

    _DB_TABLE = "I_Data_Chain_Ladder"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"

    def __init__(self, program, portfolio, method, rep_date, dev_value, orig_value):
        grouping = portfolio + "_" + method
        self._DB_TABLE = "I_Data_" + program
        self._DB_QUERY = f"""
        SELECT
        [Dev_Period_Position], [Origin_Period_Position], 
        ROUND([Age_To_Age_Factors_Post_Outliers],4) as returnValue 
        FROM [{self._DB_TABLE}]
        WHERE [Grouping_ID] = '{grouping}' AND [RunOff_Triangle Call Date] = '{rep_date}' 
        AND ([Dev_Period_Position] BETWEEN {dev_value[0]} AND {dev_value[1]})
        AND ([Origin_Period_Position] BETWEEN {orig_value[0]} AND {orig_value[1]})
        ORDER BY [Origin_Period_Position], [Record Number]                         
        """


# DB handler for Ultimate Development Factors (Cumulative)
class UltimateDevelopmentFactorsCumulative(gf.GenericHandler):

    DB_QUERY = "Select Ult_Dev_Factors, Dev_Period_Position, Origin_Period_Position from [I_Data_Chain_Ladder] where Grouping_ID = 'Grp1_BCL'"

    def get_db_query(self):
        return self.DB_QUERY

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        # Drop zeros for correct chart display
        df = df[df != 0].dropna()
        return df

# DB handler for Ultimate Development Factors (Cumulative)
class CumulativeIncurred(gf.GenericHandler):

    _DB_TABLE = "I_Data_Chain_Ladder"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"

    #DB_QUERY = "Select Ult_Dev_Factors, Dev_Period_Position, Origin_Period_Position from [I_Data_Chain_Ladder] where Grouping_ID = 'Grp1_BCL'"

    def get_db_query(self):
        return self._DB_QUERY

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        # Drop zeros for correct chart display
        df = df[df != 0].dropna()
        return df

    def __init__(self, inputs):
        grouping = inputs.portfolio + "_" + inputs.method
        var = "[" + inputs.component + "]"
        self._DB_TABLE = "I_Data_" + inputs.program
        self._DB_QUERY = f"""
        SELECT
        [Dev_Period_Position], [Origin_Period_Position], 
        ROUND({var},4) as returnValue 
        FROM [{self._DB_TABLE}]
        WHERE [Grouping_ID] = '{grouping}' AND [RunOff_Triangle Call Date] = '{inputs.reporting}' 
        AND ([Dev_Period_Position] BETWEEN {inputs.dev[0]} AND {inputs.dev[1]})
        AND ([Origin_Period_Position] BETWEEN {inputs.orig[0]} AND {inputs.orig[1]})
        ORDER BY [Origin_Period_Position], [Record Number]                         
        """



# DB handler for Box Plot Outliers
class BoxPlotOutliers(gf.GenericHandler):

    _DB_TABLE = "I_Data_Chain_Ladder"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"

    def get_db_query(self):
        return self._DB_QUERY

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        df["Age_To_Age_Factors_Mean_Pre_Outliers"] = df.Age_To_Age_Factors_Pre_Outliers.mean()
        # df["Age_To_Age_Factors_Median_Pre_Outliers"] = df.Age_To_Age_Factors_Pre_Outliers.median()
        # Drop original columns, not needed for display
        # df.drop(
        #     ["Age_To_Age_Factors_Pre_Outliers"],
        #     axis=1,
        #     inplace=True,
        # )
        # Drop zeros for correct chart display
        df = df[df != 0].dropna()
        return df

    def __init__(self, inputs):
        grouping = inputs.portfolio + "_" + inputs.method
        var = "[" + inputs.component + "]"
        self._DB_TABLE = "I_Data_" + inputs.program
        self._DB_QUERY = f"""
        SELECT
        [Age_To_Age_Factors_Pre_Outliers], [Age_To_Age_Factors_Outliers_Bottom], [Age_To_Age_Factors_Outliers_Top],
        [Age_To_Age_Factors_Outliers_Percentile_25],
        [Age_To_Age_Factors_Outliers_Percentile_50], [Age_To_Age_Factors_Outliers_Percentile_75],
        [Dev_Period_Position] 
        FROM [{self._DB_TABLE}]
        WHERE [Grouping_ID] = '{grouping}' AND [RunOff_Triangle Call Date] = '{inputs.reporting}' 
        AND ([Dev_Period_Position] BETWEEN {inputs.dev[0]} AND {inputs.dev[1]})
        AND ([Origin_Period_Position] = 1)
        ORDER BY [Origin_Period_Position], [Record Number]                         
        """

        # BETWEEN {inputs.orig[0]} AND {inputs.orig[1]}