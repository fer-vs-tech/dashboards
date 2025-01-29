from cm_dashboards.other_accounting import abstract_handler as gf


class VfaIrHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "vfa_ir_template.csv"

    DB_QUERY = "select A00_GOC as COA, * from I_Reporting_VFA"

    def get_db_query(self):
        return self.DB_QUERY

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def add_calculated_columns(self, df):
        """
        Add calculated ledger entries
        """
        df["CSM_Suspense_account_value"] = -df.CSM_Initial_Recognition_IR_Proc

        return df
