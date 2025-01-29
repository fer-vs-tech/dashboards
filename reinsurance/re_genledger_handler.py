from cm_dashboards.reinsurance import aoci_handler as aoci
from cm_dashboards.reinsurance import csm_handler as csm
from cm_dashboards.reinsurance import rqa_handler as rqa
from cm_dashboards.reinsurance import rqp_handler as rqp
from cm_dashboards.reinsurance import rwa_handler as rwa
from cm_dashboards.reinsurance import rwu_handler as rwu


class ReGenLedgerHandler:
    def get_combined_ledger(self, jobrun_id):
        rwa_handler = rwa.RwaHandler()
        # Get data from database, rotate and format
        rwa_handler.prepare_data(jobrun_id)
        # Apply data to subledger template file
        pop_template = rwa_handler.subledger_apply_template()

        rwu_handler = rwu.RwuHandler()
        # Get data from database, rotate and format
        rwu_handler.prepare_data(jobrun_id)
        # Apply data to subledger template file
        pop_template = pop_template.append(rwu_handler.subledger_apply_template())

        rqp_handler = rqp.RqpHandler()
        # Get data from database, rotate and format
        rqp_handler.prepare_data(jobrun_id)
        # Apply data to subledger template file
        pop_template = pop_template.append(rqp_handler.subledger_apply_template())

        rqa_handler = rqa.RqaHandler()
        # Get data from database, rotate and format
        rqa_handler.prepare_data(jobrun_id)
        # Apply data to subledger template file
        pop_template = pop_template.append(rqa_handler.subledger_apply_template())

        csm_handler = csm.CsmHandler()
        # Get data from database, rotate and format
        csm_handler.prepare_data(jobrun_id)
        # Apply data to subledger template file
        pop_template = pop_template.append(csm_handler.subledger_apply_template())

        aoci_handler = aoci.AociHandler()
        # Get data from database, rotate and format
        aoci_handler.prepare_data(jobrun_id)
        # Apply data to subledger template file
        pop_template = pop_template.append(aoci_handler.subledger_apply_template())

        return pop_template
