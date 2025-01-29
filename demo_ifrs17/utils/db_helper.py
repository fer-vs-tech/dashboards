#demo_ifrs17/helpers/db_helper.py

from cm_dashboards.demo_ifrs17.utils import abstract_handler as gf


class G_Portfolio_Distinct(gf.GenericHandler):
    """
    RC Information table with all needed columns
    """

    _DB_TABLE = "G_Portfolio"
    _DB_QUERY = f"SELECT TOP 0 * FROM [{_DB_TABLE}]"

    def __init__(self, column_name):
        self._DB_QUERY = f"""
        SELECT 
            DISTINCT([{column_name}]) grp
        FROM [{self._DB_TABLE}]                
        """

class G_Portfolio_Columns(gf.GenericHandler):
    """
    RC Information table with all needed columns
    """

    _DB_TABLE = "G_Portfolio"
    _DB_QUERY = f"SELECT TOP 0 * FROM [{_DB_TABLE}]"

    def __init__(self):
        self._DB_QUERY = f"""
        SELECT
            TOP 0 *
        FROM [{self._DB_TABLE}]                
        """

class G_Portfolio(gf.GenericHandler):
    """
    RC Information table with all needed columns
    """

    _DB_TABLE = "G_Portfolio"
    _DB_QUERY = f"SELECT TOP 0 * FROM [{_DB_TABLE}]"

    def __init__(self, field_list, step_date):
        self._DB_QUERY = f"""
        SELECT
            {field_list}
        FROM [{self._DB_TABLE}]
        WHERE [Step Date] = ('{step_date}')                
        """

class G_Portfolio_Sum(gf.GenericHandler):
    """
    RC Information table with all needed columns
    """

    _DB_TABLE = "G_Portfolio"
    _DB_QUERY = f"SELECT TOP 0 * FROM [{_DB_TABLE}]"

    def __init__(self, field_list, whr, grpby, model):
        self._DB_QUERY = f"""
        SELECT
            {field_list}
        FROM [{self._DB_TABLE}]
        WHERE {whr} """
        if model:
            self._DB_QUERY = self._DB_QUERY + f""" AND [Model Value] = '{model}' """
        self._DB_QUERY = self._DB_QUERY + f""" GROUP BY {grpby} """

# WHERE [Step Date] = ('{step_date}') """
# class A_Portfolio(gf.GenericHandler):
#     """
#     RC Information table with all needed columns
#     """
#
#     _DB_TABLE = "A_Portfolio"
#     _DB_QUERY = f"SELECT TOP 0 * FROM [{_DB_TABLE}]"
#
#     def __init__(self, field_list, step_date):
#         self._DB_QUERY = f"""
#         SELECT
#             {field_list}
#         FROM [{self._DB_TABLE}]
#         WHERE [Step Date] = ('{step_date}')
#         """

class G_Step_Dates(gf.GenericHandler):
    """
    RC Information table with all needed columns
    """

    _DB_TABLE = "G_Portfolio"
    _DB_QUERY = f"SELECT distinct([Step Date]) Step_Date FROM [{_DB_TABLE}]"

    def __init__(self):
        self._DB_QUERY = f"SELECT distinct([Step Date]) Step_Date FROM [{self._DB_TABLE}]"


# class A_Step_Dates(gf.GenericHandler):
#     """
#     RC Information table with all needed columns
#     """
#
#     _DB_TABLE = "A_Portfolio"
#     _DB_QUERY = f"SELECT distinct([Step Date]) Step_Date FROM [{_DB_TABLE}]"
#
#     def __init__(self):
#         self._DB_QUERY = f"SELECT distinct([Step Date]) Step_Date FROM [{self._DB_TABLE}]"


class G_ICL_Model_BBA(gf.GenericHandler):
    """
    RC Information table with all needed columns
    """

    _DB_TABLE = "G_Portfolio"
    _DB_QUERY = f"SELECT TOP 0 * FROM [{_DB_TABLE}]"

    def __init__(self, step_date):
        self._DB_QUERY = f"""
        SELECT [Model Value] as Model_Value, 
        SUM([Insurance_Contract_Liability_Final]) as Total_Ins,
        SUM([Insurance_Contract_Liability_Reins_Final]) as Total_Reins,
        SUM([Insurance_Contract_Liability_Final] + [Insurance_Contract_Liability_Reins_Final]) as Total_Net
        FROM [{self._DB_TABLE}]
        WHERE [Step Date] = '{step_date}'
        GROUP BY [Model Value]"""


class G_ICL_Model_PAA(gf.GenericHandler):
    """
    RC Information table with all needed columns
    """

    _DB_TABLE = "G_Portfolio"
    _DB_QUERY = f"SELECT TOP 0 * FROM [{_DB_TABLE}]"

    def __init__(self, step_date):
        self._DB_QUERY = f"""
        SELECT [Model Value] as Model_Value, 
        SUM([Insurance_Contract_Liability_Final]) as Totals
        FROM [{self._DB_TABLE}]
        WHERE [Step Date] = '{step_date}'
        GROUP BY [Model Value]"""
