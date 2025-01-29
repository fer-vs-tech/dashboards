from cm_dashboards.nonlife_standalone import abstract_handler as gf

# DB handler for IncPaidClaimsHandler
class IncPaidClaimsHandler(gf.GenericHandler):

    DB_QUERY = """
    Select Dev_Period_Position, Origin_Period_Position, Tri_Claim_Costs_By_Year,
    Tri_Case_Reserves_By_Year from [I_Data_Chain_Ladder] where Grouping_ID = 'Grp1_BCL'"""

    def get_db_query(self):
        return self.DB_QUERY

    def add_calculated_columns(self, df):
        """
        Add calculated entries
        """
        # Subtract these columns to get the desired number
        df["Incremental_Paid_Claims"] = (
            df.Tri_Claim_Costs_By_Year - df.Tri_Case_Reserves_By_Year
        )
        # Drop original columns, not needed for display
        df.drop(
            ["Tri_Claim_Costs_By_Year", "Tri_Case_Reserves_By_Year"],
            axis=1,
            inplace=True,
        )
        # Drop zeros for correct chart display
        df = df[df != 0].dropna()

        return df

# DB handler for Link Ratios Pre Outlier
class LinkRatiosPreOutlier(gf.GenericHandler):

    DB_QUERY = "Select Age_To_Age_Factors_Pre_Outliers, Dev_Period_Position, Origin_Period_Position from [I_Data_Chain_Ladder] where Grouping_ID = 'Grp1_BCL'"

    def get_db_query(self):
        return self.DB_QUERY

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        # Drop zeros for correct chart display
        df = df[df != 0].dropna()
        return df

# DB handler for Box Plot Outliers
class BoxPlotOutliers(gf.GenericHandler):

    DB_QUERY = """
    Select Age_To_Age_Factors_Pre_Outliers, Age_To_Age_Factors_Outliers_Bottom, Age_To_Age_Factors_Outliers_Top,
    Age_To_Age_Factors_Outliers_Percentile_25,
    Age_To_Age_Factors_Outliers_Percentile_50, Age_To_Age_Factors_Outliers_Percentile_75,
    Dev_Period_Position from [I_Data_Chain_Ladder] where Grouping_ID = 'Grp1_BCL'
    """

    def get_db_query(self):
        return self.DB_QUERY

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

class OutlierAnalysisMeanRatios(gf.GenericHandler):

    DB_QUERY = """
    Select Age_To_Age_Factors_Mean_Ratio,
    Dev_Period_Position, Origin_Period_Position from [I_Data_Chain_Ladder] where Grouping_ID = 'Grp1_BCL'
    """

    def get_db_query(self):
        return self.DB_QUERY

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        # df["Age_To_Age_Factors_Mean_Ratio_Max"] = df.groupby("Dev_Period_Position")["Age_To_Age_Factors_Mean_Ratio"].transform('max')
        # df["Age_To_Age_Factors_Mean_Ratio_Min"] = df.groupby("Dev_Period_Position")["Age_To_Age_Factors_Mean_Ratio"].transform('min')
        # Drop zeros for correct chart display
        df = df[df != 0].dropna()
        return df

# DB handler for Outlier Analysis p-Value
class OutlierAnalysisPValue(gf.GenericHandler):

    DB_QUERY = """
    Select Age_To_Age_Factors_Pval_Pre_Outliers,
    Dev_Period_Position, Origin_Period_Position from [I_Data_Chain_Ladder] where Grouping_ID = 'Grp1_BCL'
    """

    def get_db_query(self):
        return self.DB_QUERY

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        df["Origin_Period_Position"] = df["Origin_Period_Position"].astype(str)
        # Drop zeros for correct chart display
        df = df[df != 0].dropna()
        return df

# DB handler for Link Ratios Post Outlier
class LinkRatiosPostOutlier(gf.GenericHandler):

    DB_QUERY = "Select Age_To_Age_Factors_Post_Outliers, Dev_Period_Position, Origin_Period_Position from [I_Data_Chain_Ladder] where Grouping_ID = 'Grp1_BCL'"

    def get_db_query(self):
        return self.DB_QUERY

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        # Drop zeros for correct chart display
        df = df[df != 0].dropna()
        return df

# DB handler for Link Ratios Post Data Analysis Outlier
class LinkRatiosPostDataAnalysisOutlier(gf.GenericHandler):

    DB_QUERY = "Select Age_To_Age_Factors, Dev_Period_Position, Origin_Period_Position from [I_Data_Chain_Ladder] where Grouping_ID = 'Grp1_BCL'"

    def get_db_query(self):
        return self.DB_QUERY

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        # Drop zeros for correct chart display
        df = df[df != 0].dropna()
        return df

# DB handler for Development Factors Post Data
class DevelopmentFactorsPostData(gf.GenericHandler):

    DB_QUERY = "Select Dev_Factors, Dev_Period_Position, Origin_Period_Position from [I_Data_Chain_Ladder] where Grouping_ID = 'Grp1_BCL'"

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

# DB handler for Cumulative Incured Claims (Projected Post-Future Inflation Adj)
class CumulativeIncuredClaimsProjectedPostFutureInflationAdj(gf.GenericHandler):

    DB_QUERY = "Select Tri_Claim_Costs_Proj, Dev_Period_Position, Origin_Period_Position from [I_Data_Chain_Ladder] where Grouping_ID = 'Grp1_BCL'"

    def get_db_query(self):
        return self.DB_QUERY

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        # Drop zeros for correct chart display
        df = df[df != 0].dropna()
        return df

# DB handler for Incremental Incurred Claims Projected   
class IncrementalIncurredClaimsProjected(gf.GenericHandler):

    DB_QUERY = "Select Tri_Claim_Costs_Proj_By_Year, Dev_Period_Position, Origin_Period_Position from [I_Data_Chain_Ladder] where Grouping_ID = 'Grp1_BCL'"

    def get_db_query(self):
        return self.DB_QUERY

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        # Drop zeros for correct chart display
        df = df[df != 0].dropna()
        return df

# DB handler for Value at Risk (VAR) 
class ValueAtRisk(gf.GenericHandler):

    DB_QUERY = """
    Select BF_Ultimate_Estimate, BF_Future_Estimate, Distribution_LIC_RA,
    Dev_Period_Position, Bootstrap_Method, CC_Future_Estimate,
    Origin_Period_Position from [I_Data_Chain_Ladder] where Grouping_ID = 'Grp1_BCL'
    """

    def get_db_query(self):
        return self.DB_QUERY

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        # Drop zeros for correct chart display
        df = df[df != 0].dropna()
        return df

# DB handler for Claim Cost Results  
class ClaimCostsResults(gf.GenericHandler):

    DB_QUERY = """
    Select Origin_Period_Position, Claim_Paid_By_Origin, Case_Reserves_By_Origin,
    Claim_Costs_Incurred_By_Origin, Claim_Costs_Ult_By_Origin,
    Total_IBNR_BY_Origin, Claim_Costs_OS_By_Origin
    from [I_Data_Chain_Ladder] where Grouping_ID = 'Grp1_BCL'
    """

    def get_db_query(self):
        return self.DB_QUERY

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        # Drop zeros for correct chart display
        df = df[df != 0].dropna()
        return df

# DB handler for Claim Cost Payment Status
class ClaimCostsPaidStatus(ClaimCostsResults):

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        df["Claim_Costs_Summary"] = (df.Case_Reserves_By_Origin + df.Total_IBNR_BY_Origin)
        # Drop original columns, not needed for display
        # df.drop(
        #     ["Case_Reserves_By_Origin", "Total_IBNR_BY_Origin"],
        #     axis=1,
        #     inplace=True,
        # )
        # Drop zeros for correct chart display
        df = df[df != 0].dropna()
        return df

# DB handler for Claim Cost Results  
class ClaimsDataLossRatio(gf.GenericHandler):
    _DB_TABLE = "G_LRC_MLE"
    _DB_QUERY = """
    SELECT * FROM [{0}] WHERE Group_Identifier = '{1}'
    """.format(_DB_TABLE, 'Dist=LogNormal|Method=MLE|Var=Loss_Ratio|Product_Name=Grp1', 'AD_Test_Stat', 'Grp1')

    def get_db_query(self):
        return self._DB_QUERY

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        df = df[df.columns.drop(list(df.filter(regex=r'(Array|Function)')))]
        print(df)
        # Drop zeros for correct chart display
        # df = df[df != 0].dropna()
        return df

# Loss Ratio
class LossRatio(gf.GenericHandler):
    # ['G_LRC_Fitted', 'G_LRC_MLE', 'G_LRC_MME', 'R_Info_RuntimeParameters', 'Rc_RuntimeParameters',
    # 'Rd_RuntimeParameters', 'T_Table_Mapping', 'Z_Info_Model', 'Zc_Model', 'Zi_Model', 'Zn_Model'] 
    # Dist=LogNormal|Method=MLE|Var=Loss_Ratio|Product_Name=Grp1
    _DB_TABLE = "G_LRC_MLE"
    _DB_QUERY = """
    SELECT Source_Data_St FROM [{0}] WHERE Product_Name = '{3}' AND Group_Identifier = '{1}'
    """.format(_DB_TABLE, 'Var=Loss_Ratio|Product_Name=Grp1', 'AD_Test_Stat', 'Grp1')

    def get_db_query(self):
        return self._DB_QUERY

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        # df.drop(df.filter(regex='Array').columns, axis=1, inplace=True)
        # Drop zeros for correct chart display
        df = df[df != 0].dropna()
        return df

# LRC Evaluate
class LRCEvaluate(gf.GenericHandler):
    # ['G_Distributions', 'G_Selected', 'R_Info_RuntimeParameters', 'Rc_RuntimeParameters',
    # 'Rd_RuntimeParameters', 'Ri_RuntimeParameters', 'Rn_RuntimeParameters',
    # 'T_Table_Mapping', 'Z_Info_Model', 'Zi_Model', 'Zn_Model']
    _DB_TABLE = "G_Selected"
    # _DB_QUERY = """
    # SELECT Product_Name, Input_Variable, [Method Value], [Dist Value],
    # Fitted_Param_1, Fitted_Param_2, Input_Mean, Risk_Adjustment,
    # Risk_Adjustment_Ratio FROM [{0}] ORDER BY Product_Name, Input_Variable
    # """.format(_DB_TABLE)
    _DB_QUERY = "SELECT * FROM [{0}]".format(_DB_TABLE)

    def get_db_query(self):
        return self._DB_QUERY

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        # df.drop(df.filter(regex='Array').columns, axis=1, inplace=True)
        # Drop zeros for correct chart display
        df = df[df != 0].dropna()
        return df

# DB handler for Claim Cost Results  
class Parameterization(gf.GenericHandler):
    _DB_TABLE = "G_LRC_MLE"
    _DB_JOIN_TABLE = "G_LRC_MME"
    _DB_QUERY = """
    SELECT MLE.[Dist Value], MLE.Distribution_LR, MLE.Fitted_Param_1,
    MLE.Fitted_Param_2, MLE.Fitting_Method FROM [{0}] MLE
    WHERE MLE.Input_Variable = 'Loss_Ratio' AND MLE.Product_Name = 'Grp1'
    UNION
    SELECT MME.[Dist Value], MME.Distribution_LR, MME.Fitted_Param_1,
    MME.Fitted_Param_2, MME.Fitting_Method FROM [{1}] MME
    WHERE MME.Input_Variable = 'Loss_Ratio' AND MME.Product_Name = 'Grp1'
    ORDER BY [Distribution_LR] ASC
    """.format(_DB_TABLE, _DB_JOIN_TABLE)

    def get_db_query(self):
        return self._DB_QUERY

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        df = df[df.columns.drop(list(df.filter(regex=r'(Array|Function)')))]
        print(df)
        # Drop zeros for correct chart display
        # df = df[df != 0].dropna()
        return df