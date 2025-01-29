import importlib.resources as pkg_resources

import pandas as pd

import cm_dashboards.subledger
from cm_dashboards.reinsurance import abstract_handler as gf
from cm_dashboards.reinsurance import re_genledger_handler as gl


class ReReconciliationHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "re_reconciliation_template.csv"

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def prepare_data(self, jobrun_id):
        handler = gl.ReGenLedgerHandler()
        # Get ledger data
        ledger = handler.get_combined_ledger(jobrun_id)
        # Drop non-required columns
        ledger = ledger.drop(
            [
                "COA_hidden",
                "Inforce_NB",
                "format_hidden",
                "bottom_border_hidden",
            ],
            axis=1,
        )

        # Collapse and sum up CR and DR account values
        cr_dr_totals = ledger.groupby(["Account_Name", "Dr_Cr"], as_index=False).sum()
        pd.set_option("display.max_columns", None)

        # Split CR and DR into separate data frames
        cr_totals = cr_dr_totals.loc[cr_dr_totals["Dr_Cr"] == "Cr"]
        dr_totals = cr_dr_totals.loc[cr_dr_totals["Dr_Cr"] == "Dr"]

        # Drop DR_CR column
        cr_totals = cr_totals.drop(
            ["Dr_Cr", "Description", "Group", "COA"],
            axis=1,
        )
        dr_totals = dr_totals.drop(
            ["Dr_Cr", "Description", "Group", "COA"],
            axis=1,
        )

        # Reconcile
        reconciled = dr_totals.set_index("Account_Name").subtract(
            cr_totals.set_index("Account_Name"), fill_value=0
        )
        ### Add Group Totals
        # BEL Total
        reconciled.loc["BEL"] = reconciled[reconciled.index.str.startswith("BEL")].sum()
        reconciled.loc["BEL"] += reconciled.loc["(Sus) CSM New Biz_REINS"]
        # RA Total
        reconciled.loc["RA"] = reconciled[reconciled.index.str.startswith("RA")].sum()
        # Credit Loss Total
        reconciled.loc["Credit Loss BEL"] = reconciled[
            reconciled.index.str.startswith("Credit Loss BEL")
        ].sum()
        # CSM Total
        reconciled.loc["CSM"] = reconciled[reconciled.index.str.startswith("CSM")].sum()
        # Reinsurance Revenue Total
        reconciled.loc["Reinsurance Revenue"] = reconciled[
            reconciled.index.str.startswith("Reinsurance Revenue")
        ].sum()
        # Reinsurance Expense Total
        reconciled.loc["Reinsurance Expense"] = reconciled[
            reconciled.index.str.startswith("Reinsurance Expense")
        ].sum()
        # Reinsurance Interest Expense Total
        reconciled.loc["Interest Expense-PL"] = reconciled[
            reconciled.index.str.startswith("Reinsurance Interest Expense")
        ].sum()
        # OCI Total
        reconciled.loc["AOCI"] = reconciled[
            reconciled.index.str.startswith("AOCI")
        ].sum()

        self.prepared_data = reconciled

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
            left_on="Account_Name",
            right_on="Account_Name",
            how="left",
            suffixes=("", "_y"),
        )
        # Drop duplicate COA column
        pop_template.drop(
            pop_template.filter(regex="_y$").columns.tolist(), axis=1, inplace=True
        )
        return pop_template.fillna(0)
