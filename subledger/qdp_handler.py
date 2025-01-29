from cm_dashboards.subledger import abstract_handler as gf


class QdpHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "qdp_template.csv"

    DB_QUERY = "select A00_GOC as COA, * from I_Reporting_Origin"

    def get_db_query(self):
        return self.DB_QUERY

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def add_calculated_columns(self, df):
        """
        Add calculated ledger entries
        """
        # Writing CSM/expense of the amount of BEL and RA after volume adjustment based on initial EIR
        df["Writing_Expense_BEL_Loss_INIT_EIR_QDP"] = df.Initial_BEL_Loss_QDP_Proc
        df["Writing_Expense_BEL_Other_INIT_EIR_QDP"] = df.Initial_BEL_Other_QDP_Proc
        df["Writing_Expense_RA_Loss_INIT_EIR_QDP"] = df.Initial_RA_Loss_QDP_Proc
        df["Writing_Expense_RA_Other_INIT_EIR_QDP"] = df.Initial_RA_Other_QDP_Proc
        # Redemption of CSM/expense for the same amount of BEL and RA after volume adjustment based on intial EIR
        df["Redemption_Expense_BEL_Loss_INIT_EIR_QDP"] = df.Initial_BEL_Loss_QDP_Proc
        df["Redemption_Expense_BEL_Other_INIT_EIR_QDP"] = df.Initial_BEL_Other_QDP_Proc
        df["Redemption_Expense_RA_Loss_INIT_EIR_QDP"] = df.Initial_RA_Loss_QDP_Proc
        df["Redemption_Expense_RA_Other_INIT_EIR_QDP"] = df.Initial_RA_Other_QDP_Proc
        # Writing interest expense and the amount of BEL and RA after volume adjustment based on reset EIR
        df["Writing_Expense_BEL_Loss_Reset_EIR_QDP"] = df.Reset_BEL_Loss_QDP_Proc
        df["Writing_Expense_BEL_Other_Reset_EIR_QDP"] = df.Reset_BEL_Other_QDP_Proc
        df["Writing_Expense_RA_Loss_Reset_EIR_QDP"] = df.Reset_RA_Loss_QDP_Proc
        df["Writing_Expense_RA_Other_Reset_EIR_QDP"] = df.Reset_RA_Other_QDP_Proc
        # Redemption of interest expense and the amount of BEL and RA after volume adjustment based on reset EIR
        df["Redemption_Expense_BEL_Loss_Reset_EIR_QDP"] = df.Reset_BEL_Loss_QDP_Proc
        df["Redemption_Expense_BEL_Other_Reset_EIR_QDP"] = df.Reset_BEL_Other_QDP_Proc
        df["Redemption_Expense_RA_Loss_Reset_EIR_QDP"] = df.Reset_RA_Loss_QDP_Proc
        df["Redemption_Expense_RA_Other_Reset_EIR_QDP"] = df.Reset_RA_Other_QDP_Proc
        return df
