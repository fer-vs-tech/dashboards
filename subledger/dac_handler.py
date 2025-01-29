from cm_dashboards.subledger import abstract_handler as gf


class DacHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "dac_template.csv"

    DB_QUERY = "select A00_GOC as COA, * from I_Reporting_Origin"

    def get_db_query(self):
        return self.DB_QUERY

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def add_calculated_columns(self, df):
        """
        Add calculated ledger entries
        """
        df["Recognition_Amortized_DAC"] = df.Amortization_Amount_DAC_AMOR_Proc
        return df
