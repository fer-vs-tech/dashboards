from cm_dashboards.esg import abstract_handler as gf
from cm_dashboards.esg import helpers as helpers

"""
['A_Portfolio', 'A_Reinsurance', 'G_Portfolio', 'R_Info_RuntimeParameters', 'Rc_RuntimeParameters',
'Rd_RuntimeParameters', 'Ri_RuntimeParameters', 'Rn_RuntimeParameters', 'T_Table_Mapping',
'Z_Info_Discounting>Layer', 'Z_Info_Discounting>Portfolio', 'Z_Info_Model', 'Z_Info_Portfolio',
'Z_Info_Projected_CFs>Layer','Z_Info_Projected_CFs>Portfolio', 'Zc_Model', 'Zi_Discounting>Layer',
'Zi_Discounting>Portfolio', 'Zi_Model', 'Zi_Portfolio', 'Zi_Projected_CFs>Layer',
'Zi_Projected_CFs>Portfolio', 'Zn_Discounting>Portfolio', 'Zn_Model', 'Zn_Portfolio', 'Zn_Projected_CFs>Portfolio']

['A_CF_ISP', 'A_CF_WL', 'G_CF_ISP', 'G_CF_WL', 'G_RN_Layer>CF_ISP', 'G_RN_Layer>CF_WL', 'L_Layer',
'L_RN_Layer>Layer', 'R_Info_RuntimeParameters', 'Rc_RuntimeParameters', 'Rd_RuntimeParameters',
'Rn_RuntimeParameters', 'T_Table_Mapping', 'Z_Info_CF_ISP', 'Z_Info_CF_WL', 'Z_Info_Model',
'Z_Info_RN_Layer>CF_ISP', 'Z_Info_RN_Layer>CF_WL', 'Zc_Model', 'Zl_Model', 'Zn_CF_ISP',
'Zn_CF_WL', 'Zn_Model', 'Zn_RN_Layer>CF_ISP', 'Zn_RN_Layer>CF_WL']
"""


class TableInfos(gf.GenericHandler):
    """
    Table mapping is a special case, as it is used to get the list of tables
    """

    _DB_TABLE = "T_Table_Mapping"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class CF_ISP(gf.GenericHandler):
    """
    CF ISP data generator
    Perform AVERAGE operation on needed columns
    Get absolute values for Net_CF and Int_On_CF columns before calculating average
    GROUP BY [Step Date]
    """

    _DB_TABLE = "A_CF_ISP"
    _DB_QUERY = f"""
    SELECT [Step Date] as Report_Date,
    AVG(PV_Net_CF_RN) as PV_Net_CF_RN,
    AVG(PV_Net_CF_RN_Next) as PV_Net_CF_RN_Next,
    AVG(PV_RA_Total_RN) as PV_RA_Total_RN,
    AVG(RC_Calc_RN) as RC_Calc_RN,
    AVG(PV_RA_Total_RN_NExt) as PV_RA_Total_RN_NExt,
    AVG(RC_Calc_RN_Next) as RC_Calc_RN_Next,
    ABS(AVG(Net_CF_RN_Next)) as Net_CF_RN_Next,
    ABS(AVG(Int_On_CF_RN_Next)) as Int_On_CF_RN_Next,
    ABS(AVG(Net_CF)) as Net_CF,
    ABS(AVG(Int_On_CF)) as Int_On_CF
    FROM [{_DB_TABLE}] GROUP BY [Step Date]
    """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class CF_WL(gf.GenericHandler):
    """
    CF WL data generator
    Perform AVERAGE operation on needed columns
    GROUP BY [Step Date]
    """

    _DB_TABLE = "A_CF_WL"
    _DB_QUERY = f"""
    SELECT [Step Date] as Report_Date,
    AVG(PV_Net_CF_RN) as PV_Net_CF_RN,
    AVG(PV_Net_CF_RN_Next) as PV_Net_CF_RN_Next,
    AVG(PV_RA_Total_RN) as PV_RA_Total_RN,
    AVG(RC_Calc_RN) as RC_Calc_RN,
    AVG(PV_RA_Total_RN_NExt) as PV_RA_Total_RN_NExt,
    AVG(RC_Calc_RN_Next) as RC_Calc_RN_Next,
    AVG(Net_CF_RN_Next) as Net_CF_RN_Next,
    AVG(Int_On_CF_RN_Next) as Int_On_CF_RN_Next
    FROM [{_DB_TABLE}] GROUP BY [Step Date]
    """

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class GetChartData(gf.GenericHandler):
    """
    Get the data for a chart
    """

    _DB_TABLE = "G_Portfolio"
    _DB_QUERY = f"SELECT [Step Date] as Report_date FROM [{_DB_TABLE}]"

    def __init__(
        self,
        plot_variable="*",
        report_date=None,
        group=None,
        senario=None,
        max_date=None,
    ):
        # Adjust DB query parameters depending on the arguments
        self._DB_QUERY = f"SELECT [Step Date] as Report_date, {plot_variable} FROM [{self._DB_TABLE}]"

        # When reporting date is specified
        if report_date is not None and report_date != "All":
            self._DB_QUERY = f"{self._DB_QUERY} WHERE [Step Date] = '{report_date}'"

        # When grouping is specified
        if group is not None and group != "All":
            if "WHERE" in self._DB_QUERY:
                self._DB_QUERY = f"{self._DB_QUERY} AND [Group_ID] = '{group}'"
            else:
                self._DB_QUERY = f"{self._DB_QUERY} WHERE [Group_ID] = '{group}'"

        # When senario is specified
        if senario is not None and senario != "All":
            if "WHERE" in self._DB_QUERY:
                self._DB_QUERY = f"{self._DB_QUERY} AND [IFRS_17 Scenario] = {senario}"
            else:
                self._DB_QUERY = (
                    f"{self._DB_QUERY} WHERE [IFRS_17 Scenario] = {senario}"
                )

        # When max date is specified
        if max_date is not None and max_date != "AutoCalculate":
            if "WHERE" in self._DB_QUERY:
                self._DB_QUERY = f"{self._DB_QUERY} AND [Step Date] <= '{max_date}'"
            else:
                self._DB_QUERY = f"{self._DB_QUERY} WHERE [Step Date] <= '{max_date}'"

        # Add order by clause
        self._DB_QUERY = f"{self._DB_QUERY} ORDER BY [Step Date] ASC"

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class Senarios(gf.GenericHandler):
    """
    Get available senarios information
    """

    _DB_TABLE = "A_Portfolio"
    _DB_QUERY = f"SELECT [IFRS_17 Scenario] as Scenario FROM [{_DB_TABLE}] GROUP BY [IFRS_17 Scenario]"

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class ReportDate(gf.GenericHandler):
    """
    Get the list of report dates
    """

    _DB_TABLE = "A_Portfolio"
    _DB_QUERY = (
        f"SELECT [Step Date] as Report_Date FROM [{_DB_TABLE}] GROUP BY [Step Date]"
    )

    def __init__(self, max_date=None, table_name=None):
        if table_name is not None:
            self._DB_TABLE = table_name
            self._DB_QUERY = f"SELECT [Step Date] as Report_Date FROM [{self._DB_TABLE}] GROUP BY [Step Date]"
        if max_date is not None and max_date != "AutoCalculate":
            self._DB_QUERY = f"SELECT [Step Date] as Report_Date FROM [{self._DB_TABLE}] WHERE [Step Date] <= '{max_date}' GROUP BY [Step Date]"

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df


class Groups(gf.GenericHandler):
    """
    Get the list of groups
    """

    _DB_TABLE = "A_Portfolio"
    _DB_QUERY = f"SELECT Group_ID FROM [{_DB_TABLE}] GROUP BY Group_ID"

    def add_calculated_columns(self, df):
        """
        Add calculated entries or perform data cleansing
        """
        return df
