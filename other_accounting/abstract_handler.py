import importlib.resources as pkg_resources
from timeit import default_timer as timer

import pandas as pd

import cm_dashboards.alchemy_db as db
import cm_dashboards.cloudmanager_db as cloudmanager_db
import cm_dashboards.wvr_data.wvr_functions as wvr_functions


class GenericHandler:
    def add_calculated_columns(self, df):
        raise NotImplementedError

    def pos(self, source_list):
        return [x if x > 0 else 0 for x in source_list]

    def neg(self, source_list):
        return [x if x < 0 else 0 for x in source_list]

    def change_sign(self, source_list):
        return [-x for x in source_list]

    def prepare_data_wvr(self, wvr_path, model):
        """
        Get R3S data from wvr
        """
        query = self.get_db_query()
        connect_string = wvr_functions.get_wvr_connection_url(wvr_path, model)
        con = wvr_functions.get_connection(connect_string)
        start_query = timer()
        df = pd.read_sql(query, con)
        end_query = timer()
        print(
            "Query for {0} execution took {1}s".format(model, end_query - start_query)
        )
        con.close()
        self.transpose_data(df)

    def prepare_data_old(self, jobrun_id):
        """
        Get R3S data from database
        """
        # DB_URL = db.get_db_connection_url(jobrun_id)
        query = self.get_db_query().format(jobrun_id)
        df = db.query_to_dataframe(
            cloudmanager_db.get_db_engine(jobrun_id).get_engine(), query
        )
        self.transpose_data(df)

    def transpose_data(self, df):
        """
        Reorientate data to match output
        """
        # Add extra calculated columns
        df = self.add_calculated_columns(df)
        # Pivot table
        trans = df.transpose().reset_index()
        # Set column headers
        trans.columns = trans.iloc[0]
        # Set beginning row
        self.prepared_data = trans[1:]

    def subledger_apply_template(self):
        """
        Apply data to subledger template
        """
        # Get template for ledger table
        template_csv = pkg_resources.open_text(
            cm_dashboards.subledger, self.get_subledger_template()
        )
        self.template = pd.read_csv(template_csv)

        # Merge R3S data into template
        pop_template = pd.merge(
            self.template,
            self.prepared_data,
            left_on="COA_hidden",
            right_on="COA",
            how="left",
            suffixes=("", "_y"),
        )
        # Drop duplicate COA column
        pop_template.drop(
            pop_template.filter(regex="_y$").columns.tolist(), axis=1, inplace=True
        )
        return pop_template

    def get_db_query(self):
        raise NotImplementedError

    def get_subledger_template(self):
        raise NotImplementedError
