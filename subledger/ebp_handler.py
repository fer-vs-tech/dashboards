from cm_dashboards.subledger import abstract_handler as gf


class EbpHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "ebp_template.csv"

    DB_QUERY = "select A00_GOC as COA, * from I_Reporting_Origin"

    def get_db_query(self):
        return self.DB_QUERY

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def add_calculated_columns(self, df):
        """
        Add calculated ledger entries
        """
        # Writing CSM/expense of the amount of BEL and RA after economic assumption based on initial EIR
        df["Writing_Expense_BEL_Loss_INIT_EIR_EBP"] = df.Initial_BEL_Loss_EBP_Proc
        df["Writing_Expense_BEL_Other_INIT_EIR_EBP"] = df.Initial_BEL_Other_EBP_Proc
        df["Writing_Expense_RA_Loss_INIT_EIR_EBP"] = df.Initial_RA_Loss_EBP_Proc
        df["Writing_Expense_RA_Other_INIT_EIR_EBP"] = df.Initial_RA_Other_EBP_Proc
        # Writing interest expense and the amount of BEL and RA after economic assumption based on reset EIR
        df["Writing_Expense_BEL_Loss_Reset_EIR_EBP"] = df.Reset_BEL_Loss_EBP_Proc
        df["Writing_Expense_BEL_Other_Reset_EIR_EBP"] = df.Reset_BEL_Other_EBP_Proc
        df["Writing_Expense_RA_Loss_Reset_EIR_EBP"] = df.Reset_RA_Loss_EBP_Proc
        df["Writing_Expense_RA_Other_Reset_EIR_EBP"] = df.Reset_RA_Other_EBP_Proc
        return df
