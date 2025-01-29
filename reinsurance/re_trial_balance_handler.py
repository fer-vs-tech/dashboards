import importlib.resources as pkg_resources

import pandas as pd

from cm_dashboards.reinsurance import abstract_handler as gf
from cm_dashboards.reinsurance import re_reconciliation_handler as rl


class ReTrialBalanceHandler(gf.GenericHandler):
    SUBLEDGER_TEMPLATE = "re_trial_balance_template.csv"

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def prepare_data(self, jobrun_id):
        handler = rl.ReReconciliationHandler()
        # Get reconciliation data
        handler.prepare_data(jobrun_id)
        recon = handler.prepared_data

        # Get Insurance, Interest Fields
        insurance = recon[
            recon.index.isin(
                [
                    "BEL",
                    "RA",
                    "Credit Loss BEL",
                    "CSM",
                    "Deferred Tax Liabilities",
                    "AOCI",
                ]
            )
        ]
        insurance = insurance.append(
            recon[recon.index.str.startswith("Reinsurance Revenue New")]
        )
        insurance = insurance.append(
            recon[recon.index.str.startswith("Reinsurance Expense New")]
        )
        insurance = insurance.append(
            recon[recon.index.str.startswith("Reinsurance Interest Expense New")]
        )
        # Re-use the Account_Name index column only
        trial = insurance.drop(insurance.columns, axis=1)
        # Populate Debit/Credit column values
        trial["Debit"] = insurance.sum(axis=1)
        trial["Credit"] = insurance.sum(axis=1)
        trial["Debit"] = [x if x > 0 else 0 for x in trial["Debit"]]
        trial["Credit"] = [-x if x < 0 else 0 for x in trial["Credit"]]
        # Sum everything to get the total
        trial.loc["Total"] = trial.sum()
        # print(trial)
        self.prepared_data = trial

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
