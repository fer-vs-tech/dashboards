from cm_dashboards.subledger import abstract_handler as gf


class CsmHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "csm_template.csv"

    DB_QUERY = "select A00_GOC as COA, * from I_Reporting_Origin"

    def get_db_query(self):
        return self.DB_QUERY

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def add_calculated_columns(self, df):
        """
        Add calculated ledger entries
        """
        df[
            "Recognition_interest_expense_for_CSM"
        ] = df.Interest_Expense_CSM_CSM_AMOR_Proc
        df["Writing_off_CSM_suspense_account"] = (
            df.Ending_CSM_after_PRP_CSM_AMOR_Proc
            + df.Subsequent_Measurement_Loss_CSM_AMOR_Proc
            - df.Reversal_of_previous_loss_CSM_AMOR_Proc
        )
        df["Recognition_amortized_CSM"] = df.Amortization_Amount_CSM_CSM_AMOR_Proc

        return df
