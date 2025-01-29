from cm_dashboards.subledger import csm_handler as csm
from cm_dashboards.subledger import dac_handler as dac
from cm_dashboards.subledger import ebp_handler as ebp
from cm_dashboards.subledger import fap_handler as fap
from cm_dashboards.subledger import losscomp_handler as losscomp
from cm_dashboards.subledger import pap_handler as pap
from cm_dashboards.subledger import qdp_handler as qdp
from cm_dashboards.subledger import rdp_handler as rdp
from cm_dashboards.subledger import wap_handler as wap

handlers = {
    "IFRS17_Origin_FMP_Proc": fap.FapHandler(),
    "IFRS17_Origin_RSP_WAP_Proc": wap.WapHandler(),
    "IFRS17_Origin_RDP_Proc": rdp.RdpHandler(),
    "IFRS17_Origin_QDP_Proc": qdp.QdpHandler(),
    "IFRS17_Origin_PAP_Proc": pap.PapHandler(),
    "IFRS17_Origin_EBP_Proc": ebp.EbpHandler(),
    "IFRS17_Origin_CSM_AMOR_Proc": csm.CsmHandler(),
    "IFRS17_Origin_DAC_AMOR_Proc": dac.DacHandler(),
    "IFRS17_Origin_LossComp_Proc": losscomp.LossCompHandler(),
}


class GenLedgerHandler:
    def get_combined_ledger(self, wvr_path):
        pop_template = None
        for model, handler in handlers.items():
            # Get data from database, rotate and format
            handler.prepare_data_wvr(wvr_path, model)
            # Apply data to subledger template file
            if pop_template is None:
                pop_template = handler.subledger_apply_template()
            else:
                pop_template = pop_template.append(handler.subledger_apply_template())

        return pop_template
