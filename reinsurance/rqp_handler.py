from cm_dashboards.reinsurance import abstract_handler as gf


class RqpHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "rqp_template.csv"

    DB_QUERY = (
        "select A00_Treaty as COA, * from FMP_WAP.I_Reins_RQT f "
        + "inner join FMP_WAP.T_Runs r on f.ExecutionID = r.ExecutionID "
        + "where r.Job_Run = {0}"
    )

    def get_db_query(self):
        return self.DB_QUERY

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def add_calculated_columns(self, df):
        """
        Add calculated ledger entries
        """
        # Writing CSM/expense of the amount of BEL and RA after volume adjustment based on initial EIR
        df["Writing_CSM_Initial_EIR_REINS"] = (
            df.Initial_BEL_REINS_RQT_Proc
            + df.Initial_RA_REINS_RQT_Proc
            - df.Initial_Credit_Loss_BEL_REINS_RQT_Proc
        )
        # Redemption of CSM/expense for the same amount of BEL and RA after volume adjustment based on intial EIR
        df["Redemption_CSM_Initial_EIR_REINS"] = (
            df.Initial_BEL_REINS_RQT_Proc
            + df.Initial_RA_REINS_RQT_Proc
            - df.Initial_Credit_Loss_BEL_REINS_RQT_Proc
        )
        # Writing interest expense and the amount of BEL and RA after volume adjustment based on current EIR
        df[
            "Writing_BEL_Interest_Expense_Current_EIR_REINS"
        ] = df.Current_BEL_REINS_RQT_Proc
        df[
            "Writing_RA_Interest_Expense_Current_EIR_REINS"
        ] = df.Current_RA_REINS_RQT_Proc
        df[
            "Writing_Credit_Loss_Interest_Expense_Current_EIR_REINS"
        ] = df.Current_Credit_Loss_BEL_REINS_RQT_Proc
        # Redemption of interest expense and the amount of BEL and RA after volume adjustment based on current EIR
        df[
            "Redemption_BEL_Interest_Expense_Current_EIR_REINS"
        ] = df.Current_BEL_REINS_RQT_Proc
        df[
            "Redemption_RA_Interest_Expense_Current_EIR_REINS"
        ] = df.Current_RA_REINS_RQT_Proc
        df[
            "Redemption_Credit_Loss_Interest_Expense_Current_EIR_REINS"
        ] = df.Current_Credit_Loss_BEL_REINS_RQT_Proc
        return df
