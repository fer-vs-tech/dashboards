import warnings

# Suppress warnings from pandas
warnings.simplefilter(action="ignore", category=Warning)

import logging
from timeit import default_timer as timer

import pandas as pd

import cm_dashboards.wvr_data.wvr_functions as wvr_functions

logger = logging.getLogger(__name__)


class GenericHandler:
    _DB_TABLE = None
    _DB_QUERY = None
    _DF = None

    @property
    def get_table_name(self):
        return self._DB_TABLE

    @property
    def get_df(self):
        return self._DF

    def get_db_query(self):
        return self._DB_QUERY

    def set_table_name(self, table_name):
        self._DB_TABLE = table_name
        return self

    def set_db_query(self, query):
        self._DB_QUERY = query
        return self

    def set_df(self, df):
        self._DF = df
        return self._DF

    def set_limit(self, limit):
        query = self.get_db_query() + f" LIMIT {limit}"
        return self.set_db_query(query)

    def select_only(self, columns):
        """
        Select only the columns specified
        """
        return self.set_db_query(
            f"SELECT {', '.join(columns)} FROM {self.get_table_name} LIMIT 1"
        )

    def add_where_clause(self, query):
        return self.set_db_query(f"SELECT * FROM {self._DB_TABLE} {query}")

    def add_calculated_columns(self, df):
        raise NotImplementedError

    def get_wvr_data(self, wvr_path, model):
        """
        Get R3S data from wvr
        """
        query = self.get_db_query()
        connect_string = wvr_functions.get_wvr_connection_url(wvr_path, model)
        # logger.info("Connect string: {}".format(connect_string))
        con = wvr_functions.get_connection(connect_string)

        # logger.info(f"table_list - {wvr_functions.get_wvr_table_list(con)}\n")
        # wvr_functions.get_wvr_table_rowcount(self.get_table_name, con)
        # logger.info(wvr_functions.get_wvr_table_data(table_name, con, limit=20))

        start_query = timer()
        df = pd.read_sql(query, con)
        end_query = timer()
        logger.info(
            "Query for {0} execution took {1}s".format(model, end_query - start_query)
        )
        con.close()
        df = self.add_calculated_columns(df)
        df = self.set_df(df)
        return df
