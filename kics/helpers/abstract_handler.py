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

    @property
    def table_name(self):
        return self._DB_TABLE

    @property
    def db_query(self):
        return self._DB_QUERY

    def set_table_name(self, table_name):
        self._table_name = table_name
        return self

    def set_db_query(self, db_query):
        self._DB_QUERY = db_query
        return self

    def set_df(self, df):
        self._df = df
        return self

    def set_limit(self, limit):
        self._DB_QUERY += f" LIMIT {limit}"
        return self

    def select_only(self, columns):
        """
        Select only the columns specified
        """
        self._DB_QUERY = f"SELECT {', '.join(columns)} FROM {self.table_name} LIMIT 1"
        return self

    def add_where_clause(self, query):
        self._DB_QUERY = f"SELECT * FROM {self.table_name} {query}"
        return self

    def get_wvr_data(self, wvr_path, model):
        """
        Get R3S data from wvr
        """
        query = self.db_query
        connect_string = wvr_functions.get_wvr_connection_url(wvr_path, model)
        con = wvr_functions.get_connection(connect_string)

        if self.table_name is not None:
            wvr_functions.get_wvr_table_rowcount(self.table_name, con)

        # logger.info(f"table_list - {wvr_functions.get_wvr_table_list(con)}\n")
        # logger.info(wvr_functions.get_wvr_table_data(table_name, con, limit=20))

        start_query = timer()
        df = pd.read_sql(query, con)
        end_query = timer()
        logger.info(
            "Query for {0} execution took {1}s".format(model, end_query - start_query)
        )
        con.close()

        return df
