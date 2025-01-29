import pandas as pd

import cm_dashboards.alchemy_db as db
import cm_dashboards.wvr_data.wvr_functions as wvr_functions


class ScPaaHandler:
    IR_TEMPLATE = "./solvency_capital/ir_paa_template.csv"
    SUBLEDGER_TEMPLATE = "./solvency_capital/sc_paa_template.csv"

    DB_QUERY = "select A00_GOC as COA, * from I_Reporting_PAA"

    def get_db_query(self):
        return self.DB_QUERY

    def get_subledger_template(self):
        return self.SUBLEDGER_TEMPLATE

    def execute(self, wvr_path):
        df = self.get_data_wvr(wvr_path)
        pop_template = pd.DataFrame()
        i = 0
        for step_date, df_by_date in df.groupby("StepDate"):
            df_by_date_calc = self.add_calculated_columns(df_by_date)
            rotated_date_df = self.rotate_data(df_by_date_calc)
            if i == 0:
                template = self.IR_TEMPLATE
            else:
                template = self.SUBLEDGER_TEMPLATE
            i += 1
            sub_pop_template = self.subledger_apply_template(rotated_date_df, template)
            print(sub_pop_template)
            if pop_template.empty:
                pop_template = sub_pop_template
            else:
                pop_template = pop_template.append(sub_pop_template)
            if i == 2:
                # TODO: only show the first 2 for demo
                break
        print(pop_template)
        return pop_template

    def get_data(self, jobrun_id):
        query = self.get_db_query().format(jobrun_id)
        df = db.query_to_dataframe(db.get_db_connection(), query)
        return df

    def get_data_wvr(self, wvr_path):
        """
        Get R3S data from wvr
        """
        query = self.get_db_query()
        connect_string = wvr_functions.get_wvr_connection_url(
            wvr_path, "IFRS17_PAA_SM_Proc"
        )
        con = wvr_functions.get_connection(connect_string)
        df = pd.read_sql(query, con)
        con.close()
        return df

    def add_calculated_columns(self, df):
        """
        Add calculated ledger entries
        """
        # print(df[df.StepDate <= date.fromisoformat("2019-03-31")])
        df["CF_Premium_Opening_cr"] = df.CF_Premium_Opening
        df["DAC_Initial_New_Opening_cr"] = df.DAC_Initial_New_Opening
        df["Insurance_Contract_Revenue_cr"] = df.Insurance_Contract_Revenue
        df["Insurance_Service_Expenses_LIC_cr"] = df.Insurance_Service_Expenses_LIC
        df["Loss_On_Onerous_Group_LossComp_cr"] = df.Loss_On_Onerous_Group_LossComp
        df["Outgo_Total_Paid_cr"] = df.Outgo_Total_Paid
        df["Liability_Incurred_Claims_derecog_cr"] = (
            df.Liability_Incurred_Claims_derecog
        )
        df["DAC_amort_Curr_cr"] = df.DAC_amort_Curr
        return df

    def rotate_data(self, df):
        """
        Get R3S data from database and transform it
        """
        # Add extra calculated columns
        df = self.add_calculated_columns(df)
        # Pivot table
        trans = df.transpose().reset_index()
        # Set column headers
        trans.columns = trans.iloc[0]
        # Set beginning row
        prepared_data = trans[1:]
        return prepared_data

    def subledger_apply_template(self, df, template):
        """
        Apply data to subledger template
        """
        # Get template for ledger table
        self.template = pd.read_csv(template)
        # Merge R3S data into template
        sub_template = pd.merge(
            self.template,
            df,
            left_on="COA_hidden",
            right_on="COA",
            how="left",
            suffixes=("", "_y"),
        )

        # Drop duplicate COA column
        sub_template.drop(
            sub_template.filter(regex="_y$").columns.tolist(), axis=1, inplace=True
        )
        return sub_template
