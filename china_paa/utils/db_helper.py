from cm_dashboards.china_paa.utils import abstract_handler as gf
from cm_dashboards.china_paa.utils import helpers as helpers

"""
['A_Portfolio', 'G_Portfolio', 'R_Info_RuntimeParameters', 'Rc_RuntimeParameters',
'Rd_RuntimeParameters', 'Rn_RuntimeParameters', 'T_Table_Mapping', 'Z_Info_LRC_Premium',
'Z_Info_Portfolio', 'Zi_LRC_Premium', 'Zi_Portfolio', 'Zn_LRC_Premium', 'Zn_Portfolio']
"""


class TableInfos(gf.GenericHandler):
    """
    Table mapping is a special case, as it is used to get the list of tables
    """

    _DB_TABLE = "G_Portfolio"
    _DB_QUERY = f"SELECT * FROM [{_DB_TABLE}]"


class GroupData(gf.GenericHandler):
    """
    Retrieve data for a specific group based on the input parameters
    """

    _DB_TABLE = "G_Portfolio"
    _DB_QUERY = None

    def __init__(
        self,
        reporting_date,
        grp_type,
        inception_year,
        risk_type,
        portfolio,
        model_value,
    ):
        self._DB_QUERY = (
            f"SELECT * FROM [{self._DB_TABLE}] WHERE [Step Date] = '{reporting_date}'"
        )
        self._DB_QUERY += f" AND [Model Value] = '{model_value}'"
        # Eliminate optional search parameters if they are empty
        if grp_type != "":
            self._DB_QUERY += f" AND [Grp_Onerous_Type Value] = '{grp_type}'"
        if inception_year != "":
            self._DB_QUERY += f" AND [Inception_Year Value] = '{inception_year}'"
        if risk_type != "":
            self._DB_QUERY += f" AND [Risk_Type Value] = '{risk_type}'"
        if portfolio != "":
            self._DB_QUERY += f" AND [Product_Name Value] = '{portfolio}'"


class ControllersData(gf.GenericHandler):
    """
    Retrieve data for the controllers
    These are: reporting date, group id, inception year, portfolio, risk type
    """

    _DB_TABLE = "G_Portfolio"
    _DB_QUERY = None

    def __init__(self):
        self._DB_QUERY = f"""
            SELECT
                [Step Date] as Report_Date,
                [Group_Identifier] as Group_ID,
                [Grp_Onerous_Type Value] as Grp_Type,
                [Model Value] as Model,
                [Inception_Year Value] as Inception_Year,
                [Product_Name Value] as Portfolio,
                [Risk_Type Value] as Risk_Type
            FROM [{self._DB_TABLE}]
            ORDER BY [Step Date]
            """
