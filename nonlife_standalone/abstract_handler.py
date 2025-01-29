from timeit import default_timer as timer

import pandas as pd

import cm_dashboards.wvr_data.wvr_functions as wvr_functions


class GenericHandler:
    # Define default table
    _DB_TABLE = "I_Data_Chain_Ladder"

    def get_table_name(self):
        return self._DB_TABLE

    def add_calculated_columns(self, df):
        raise NotImplementedError

    def get_wvr_data(self, wvr_path, model):
        """
        Get R3S data from wvr
        """
        query = self.get_db_query()
        table_name = self.get_table_name()
        connect_string = wvr_functions.get_wvr_connection_url(wvr_path, model)
        con = wvr_functions.get_connection(connect_string)

        # if model == "NL_LRC_Fit":
        #     print(f"table_list - {wvr_functions.get_wvr_table_list(con)}\n")
        #     print(f"{wvr_functions.get_wvr_table_rowcount(table_name, con)}" " rows in table\n")
        #     # print(wvr_functions.get_wvr_table_data(table_name, con, limit=20))

        start_query = timer()
        df = pd.read_sql(query, con)
        end_query = timer()
        print(
            "Query for {0} execution took {1}s".format(model, end_query - start_query)
        )
        con.close()
        # Add extra calculated columns
        df = self.add_calculated_columns(df)
        return df

    def get_db_query(self):
        raise NotImplementedError
