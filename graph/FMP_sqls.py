gocs = (
    "SELECT DISTINCT "
    '"A00_GOC" as "GOC" '
    "FROM FMP_WAP.I_FMP "
    # 'WHERE ExecutionID = (select max(ExecutionID) from I_FMP)'
)

closing_dates = (
    "SELECT DISTINCT "
    '"Projection_layer_CallDate" as "closingDates" '
    "FROM FMP_WAP.I_FMP "
    # 'WHERE ExecutionID = (select max(ExecutionID) from I_FMP)'
)


############################################ BEL ########################################################
def BEL_beg_bal(job, goc, date):
    beg_bal = (
        'SELECT Initial_Other_BEL_FMP_Proc  as "Initial Balance" '
        # "Sto BEL as \"End Balance\" "
        "FROM FMP_WAP.I_FMP f "
        # 'WHERE ExecutionID = (select max(ExecutionID) from I_FMP) '
        "inner join FMP_WAP.T_Runs r on f.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return beg_bal


def BEL_Exp_Init_WAP(job, goc, date):
    exp = (
        "SELECT "
        'Exp_Initial_BEL_Other_RSP_WAP_Proc as "cal" '
        "FROM FMP_WAP.I_RSP_WAP rw "
        # 'where ExecutionID = (select max(ExecutionID) from I_RSP_WAP) '
        "inner join FMP_WAP.T_Runs r on rw.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return exp


def BEL_WAP(job, goc, date):
    wap = (
        # "SELECT Projection_layer_CallDate, A00_GOC, "
        "SELECT "
        # 'New_Biz_Weighted_Avg_Loss_BEL_Diff_RSP_WAP_Proc as "NB WA Diff (Loss)", '
        'Exp_Initial_BEL_Other_RSP_WAP_Proc as "cal", '
        'New_Biz_Weighted_Avg_Other_BEL_Diff_RSP_WAP_Proc as "NB WA Diff (Other)", '
        'Expected_Premium_Total_RSP_WAP_Proc as "Exp prem", '
        'Exp_Claim_Insurance_Component_Other_RSP_WAP_Proc as "Exp claim (Ins)", '
        'Exp_Claim_Investment_Component_Other_RSP_WAP_Proc as "Exp claim (Inv)", '
        'Exp_Direct_Acq_Cost_Prem_Other_RSP_WAP_Proc as "Exp AC (prem)", '
        'Exp_Direct_Acq_Cost_Non_Prem_Other_RSP_WAP_Proc as "Exp AC (non-prem)", '
        'Exp_Direct_Maintenance_Cost_Other_RSP_WAP_Proc as "Exp maint cost", '
        'Expected_Direct_Inspection_Cost_Other_RSP_WAP_Proc as "Exp insp cost", '
        'Exp_Direct_Invest_Manage_Cost_Other_RSP_WAP_Proc as "Exp Invest manage Cost", '
        'Expected_Policy_Loan_Cash_Flows_Other_RSP_WAP_Proc as "Exp PL CF", '
        'Reset_BEL_Interest_Expense_Other_RSP_WAP_Proc as "Unwinding (Beg to End)" '
        "FROM FMP_WAP.I_RSP_WAP rw "
        # 'where ExecutionID = (select max(ExecutionID) from I_RSP_WAP) '
        "inner join FMP_WAP.T_Runs r on rw.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return wap


def BEL_RDP(job, goc, date):
    rdp = (
        # "SELECT Projection_layer_CallDate, A00_GOC, "
        "SELECT "
        # 'Exp_BEL_Loss_component_Diff_Actual_Rate_RDP_Proc as "Act rate (Loss)", '
        'Exp_BEL_Other_component_Diff_Actual_Rate_RDP_Proc as "Act rate" '
        "FROM FMP_WAP.I_RDP rd "
        # 'where ExecutionID = (select max(ExecutionID) from I_RSP_WAP) '
        "inner join FMP_WAP.T_Runs r on rd.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return rdp


def BEL_QDP(job, goc, date):
    qdp = (
        # "SELECT Projection_layer_CallDate, A00_GOC, "
        'SELECT Initial_BEL_Other_QDP_Proc as "Vol adj" '
        "FROM FMP_WAP.I_QDP q "
        # 'where ExecutionID = (select max(ExecutionID) from I_RSP_WAP) '
        "inner join FMP_WAP.T_Runs r on q.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return qdp


def BEL_PAP(job, goc, date):
    pap = (
        # "SELECT Projection_layer_CallDate, A00_GOC, "
        'SELECT Initial_BEL_Other_PAP_Proc as "Act assumpt" '
        "FROM FMP_WAP.I_PAP p "
        # 'where ExecutionID = (select max(ExecutionID) from I_RSP_WAP) '
        "inner join FMP_WAP.T_Runs r on p.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return pap


def BEL_EBP(job, goc, date):
    ebp = (
        # "SELECT Projection_layer_CallDate, A00_GOC, "
        'SELECT Initial_BEL_Other_EBP_Proc as "Eco assumpt" '
        "FROM FMP_WAP.I_EBP e "
        # 'where ExecutionID = (select max(ExecutionID) from I_RSP_WAP) '
        "inner join FMP_WAP.T_Runs r on e.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return ebp


def BEL_LossComp(job, goc, date):
    LossComp = (
        # "SELECT Projection_layer_CallDate, A00_GOC, "
        'SELECT Ending_AOCI_BEL_Other_LossComp_Proc as "Disc rate", '
        'Ending_AOCI_BEL_Loss_LossComp_Proc as "Loss comp (AOCI)" '
        "FROM FMP_WAP.I_LossComp a "
        # 'where ExecutionID = (select max(ExecutionID) from I_RSP_WAP) '
        "inner join FMP_WAP.T_Runs r on a.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return LossComp


############################################ RA ########################################################
def RA_beg_bal(job, goc, date):
    beg_bal = (
        "SELECT Initial_Other_RA_FMP_Proc as beg "
        "FROM FMP_WAP.I_FMP f "
        # "WHERE ExecutionID = (select max(ExecutionID) from I_FMP) "
        "inner join FMP_WAP.T_Runs r on f.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return beg_bal


def RA_Exp_Init_WAP(job, goc, date):
    exp = (
        "SELECT "
        'Exp_Initial_RA_Other_RSP_WAP_Proc as "cal" '
        "FROM FMP_WAP.I_RSP_WAP rw "
        # 'where ExecutionID = (select max(ExecutionID) from I_RSP_WAP) '
        "inner join FMP_WAP.T_Runs r on rw.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return exp


def RA_WAP(job, goc, date):
    ra = (
        # "SELECT Projection_layer_CallDate, A00_GOC, "
        "SELECT "
        'Exp_Initial_RA_Other_RSP_WAP_Proc as "cal", '
        'New_Biz_Weighted_Avg_Other_RA_Diff_RSP_WAP_Proc as "NB WA Diff", '
        # "New_Biz_Wwighted_Avg_Loss_RA_Diff_RSP_WAP_Proc as \"New Biz Weighted Avg Difference\", "
        # "RA_amortization_Loss_RSP_WAP_Proc as \"RA Amortization Loss\", "
        'RA_amortization_Other_RSP_WAP_Proc as "Exp. RA amort", '
        # "Reset_RA_Interest_Expense_Loss_RSP_WAP_Proc as \"Unwinding Loss (Beg to End)\", "
        'Reset_RA_Interest_Expense_Other_RSP_WAP_Proc as "Unwinding (Beg to End)" '
        "FROM FMP_WAP.I_RSP_WAP rw "
        # "WHERE ExecutionID = (select max(ExecutionID) from I_RSP_WAP) "
        "inner join FMP_WAP.T_Runs r on rw.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return ra


def RA_RDP(job, goc, date):
    rdp = (
        # "SELECT Projection_layer_CallDate, A00_GOC, "
        'SELECT Exp_RA_Other_component_Diff_Actual_Rate_RDP_Proc as "Act rate" '
        "FROM FMP_WAP.I_RDP rd "
        # 'where ExecutionID = (select max(ExecutionID) from I_RSP_WAP) '
        "inner join FMP_WAP.T_Runs r on rd.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return rdp


def RA_QDP(job, goc, date):
    qdp = (
        # "SELECT Projection_layer_CallDate, A00_GOC, "
        'SELECT Initial_RA_Other_QDP_Proc as "Vol adj" '
        "FROM FMP_WAP.I_QDP q "
        # 'where ExecutionID = (select max(ExecutionID) from I_RSP_WAP) '
        "inner join FMP_WAP.T_Runs r on q.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return qdp


def RA_PAP(job, goc, date):
    pap = (
        # "SELECT Projection_layer_CallDate, A00_GOC, "
        'SELECT Initial_RA_Other_PAP_Proc as "Act assumpt" '
        "FROM FMP_WAP.I_PAP p "
        # 'where ExecutionID = (select max(ExecutionID) from I_RSP_WAP) '
        "inner join FMP_WAP.T_Runs r on p.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return pap


def RA_EBP(job, goc, date):
    ebp = (
        # "SELECT Projection_layer_CallDate, A00_GOC, "
        'SELECT Initial_RA_Other_EBP_Proc as "Eco assumpt" '
        "FROM FMP_WAP.I_EBP e "
        # 'where ExecutionID = (select max(ExecutionID) from I_RSP_WAP) '
        "inner join FMP_WAP.T_Runs r on e.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return ebp


def RA_LossComp(job, goc, date):
    LossComp = (
        # "SELECT Projection_layer_CallDate, A00_GOC, "
        'SELECT Ending_AOCI_RA_Other_LossComp_Proc as "Disc rate", '
        'Ending_AOCI_RA_Loss_LossComp_Proc as "Loss comp (AOCI)" '
        "FROM FMP_WAP.I_LossComp a "
        # 'where ExecutionID = (select max(ExecutionID) from I_RSP_WAP) '
        "inner join FMP_WAP.T_Runs r on a.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return LossComp


############################################ CSM ########################################################
def CSM_beg_bal(job, goc, date):
    beg_bal = (
        "SELECT Initial_CSM_FMP_Proc as beg "
        "FROM FMP_WAP.I_FMP f "
        # "WHERE ExecutionID = (select max(ExecutionID) from I_FMP) "
        "inner join FMP_WAP.T_Runs r on f.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return beg_bal


def CSM_WAP(job, goc, date):
    csm = (
        # "SELECT Projection_layer_CallDate, A00_GOC, "
        'SELECT -(New_Biz_Weighted_Avg_Other_BEL_Diff_RSP_WAP_Proc + New_Biz_Wwighted_Avg_Loss_RA_Diff_RSP_WAP_Proc) as "NB WA Diff", '
        '(Expected_Premium_Total_RSP_WAP_Proc + Exp_Claim_Investment_Component_Other_RSP_WAP_Proc + \
        Exp_Direct_Acq_Cost_Prem_Other_RSP_WAP_Proc + Expected_Policy_Loan_Cash_Flows_Other_RSP_WAP_Proc) \
            - \
        (Expected_Premium_Total_RSP_WAP_Proc + Exp_Claim_Investment_Component_Other_RSP_WAP_Proc  +\
        Exp_Direct_Acq_Cost_Prem_Other_RSP_WAP_Proc + Expected_Policy_Loan_Cash_Flows_Other_RSP_WAP_Proc) as "Difference (Act - Exp)" '
        "FROM FMP_WAP.I_RSP_WAP rw "
        # "where ExecutionID = (select max(ExecutionID) from I_RSP_WAP) "
        "inner join FMP_WAP.T_Runs r on rw.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return csm


def CSM_AMOR(job, goc, date):
    amor = (
        # "SELECT Projection_layer_CallDate, A00_GOC, "
        "SELECT "
        'Interest_Expense_CSM_CSM_AMOR_Proc as "Interest Expense", '
        'Amortization_Amount_CSM_CSM_AMOR_Proc as "Amortization", '
        'Subsequent_Measurement_Loss_CSM_AMOR_Proc as "SM Loss" '
        "FROM FMP_WAP.I_CSM_AMOR a "
        # 'where ExecutionID = (select max(ExecutionID) from I_RSP_WAP) '
        "inner join FMP_WAP.T_Runs r on a.ExecutionID = r.ExecutionID "
        "where r.Job_Run = {0} "
        "AND A00_GOC = '{1}' "
        "AND Projection_layer_CallDate = '{2}' "
    ).format(job, goc, date)
    return amor
