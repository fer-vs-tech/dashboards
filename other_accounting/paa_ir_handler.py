from cm_dashboards.other_accounting import abstract_handler as gf


class PaaIrHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "paa_ir_template.csv"

    DB_QUERY = "select A00_GOC as COA, * from I_Reporting_PAA"

    def get_db_query(self):
        return self.DB_QUERY

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def add_calculated_columns(self, df):
        """
        Add calculated ledger entries
        """
        df["BEL_Initial_Recognition_IR_Proc"] = -df.BEL_Initial_Recognition_IR_Proc

        df["BEL_Initial_Recognition_IR_Proc_PAA"] = df.BEL_Initial_Recognition_IR_Proc

        return df
