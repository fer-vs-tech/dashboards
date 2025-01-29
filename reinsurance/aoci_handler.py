from cm_dashboards.reinsurance import abstract_handler as gf


class AociHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "aoci_template.csv"

    DB_QUERY = (
        "select A00_Treaty as COA, * from FMP_WAP.I_Reins_AOCI f "
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
        # Writing the difference between the balance after economic assumption and the balance updated current EIR on OCI account
        df["Loss_BEL_Diff_from_Economic_Change_Current_EIR_REINS"] = self.change_sign(
            self.neg(df.End_AOCI_BEL_REINS_AOCI_Reins_Proc)
        )
        df["Gain_BEL_Diff_from_Economic_Change_Current_EIR_REINS"] = self.pos(
            df.End_AOCI_BEL_REINS_AOCI_Reins_Proc
        )
        df["Loss_RA_Diff_from_Economic_Change_Current_EIR_REINS"] = self.change_sign(
            self.neg(df.End_AOCI_RA_REINS_AOCI_Reins_Proc)
        )
        df["Gain_RA_Diff_from_Economic_Change_Current_EIR_REINS"] = self.pos(
            df.End_AOCI_RA_REINS_AOCI_Reins_Proc
        )
        df["End_AOCI_CL_BEL_REINS_AOCI_Reins_Proc"] = self.change_sign(
            df.End_AOCI_CL_BEL_REINS_AOCI_Reins_Proc
        )
        df[
            "Loss_CL_BEL_Diff_from_Economic_Change_Current_EIR_REINS"
        ] = self.change_sign(self.neg(df.End_AOCI_CL_BEL_REINS_AOCI_Reins_Proc))
        df["Gain_CL_BEL_Diff_from_Economic_Change_Current_EIR_REINS"] = self.pos(
            df.End_AOCI_CL_BEL_REINS_AOCI_Reins_Proc
        )
        # Writing deferred corporate tax amount derived from the OCI amount for the current term
        df["End_corp_tax_AOCI_BEL_REINS_AOCI_Reins_Proc"] = self.change_sign(
            df.End_corp_tax_AOCI_BEL_REINS_AOCI_Reins_Proc
        )
        df["Loss_BEL_Def_Tax_REINS"] = self.pos(
            df.End_corp_tax_AOCI_BEL_REINS_AOCI_Reins_Proc
        )
        df["Gain_BEL_Def_Tax_REINS"] = self.change_sign(
            self.neg(df.End_corp_tax_AOCI_BEL_REINS_AOCI_Reins_Proc)
        )
        df["End_corp_tax_AOCI_RA_REINS_AOCI_Reins_Proc"] = self.change_sign(
            df.End_corp_tax_AOCI_RA_REINS_AOCI_Reins_Proc
        )
        df["Loss_RA_Def_Tax_REINS"] = self.pos(
            df.End_corp_tax_AOCI_RA_REINS_AOCI_Reins_Proc
        )
        df["Gain_RA_Def_Tax_REINS"] = self.change_sign(
            self.neg(df.End_corp_tax_AOCI_RA_REINS_AOCI_Reins_Proc)
        )
        df["Loss_CL_BEL_Def_Tax_REINS"] = self.pos(
            df.End_corp_tax_AOCI_CL_BEL_REINS_AOCI_Reins_Proc
        )
        df["Gain_CL_BEL_Def_Tax_REINS"] = self.change_sign(
            self.neg(df.End_corp_tax_AOCI_CL_BEL_REINS_AOCI_Reins_Proc)
        )

        return df
