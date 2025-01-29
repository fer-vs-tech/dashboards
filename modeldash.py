import logging
import os
import sys

sys.path.append("..")

logger = logging.getLogger(__name__)

import argparse

import cm_dashboards.utilities as utilities

# Make executable location current dir
utilities.change_to_working_dir()


def get_host():
    """
    Read server hoste from config
    """
    host = utilities.get_entry_from_config_file("server", "host", "*")
    logger.info("Launching on host {0}".format(host))
    return host


def get_port():
    """
    Read port from config
    """
    port = utilities.get_entry_from_config_file("dashboard", "port")

    if port is None:
        port = "5051"
    if not port.isdecimal():
        logger.error("Invalid port number: {0}".format(port))
        sys.exit(1)
    if int(port) > 65535:
        logger.error("Invalid port number: {0}".format(port))
        sys.exit(1)
    logger.info("Launching on port {0}".format(port))
    return port


def get_ipv6():
    """
    Enable/Disable IPv6 from config
    """
    ipv6 = utilities.get_entry_from_config_file("server", "ipv6")
    if ipv6 is None or ipv6 != "True":
        ipv6 = False
    else:
        ipv6 = True
    logger.info("IPv6 enabled: {0}".format(ipv6))
    return ipv6


def get_protocol():
    """
    Get http/https protocol from config
    """
    protocol = utilities.get_entry_from_config_file("server", "protocol")
    if protocol is None or protocol != "https":
        protocol = "http"
    logger.info("Protocol is {0}".format(protocol))
    return protocol


def setup_logging(args=[]):
    """
    Set up loggers
    """
    import logging
    import logging.handlers

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--noconsole",
        help="Disable logging to console",
        action="store_true",
    )
    parser.add_argument(
        "--nologs",
        help="Disable logging",
        action="store_true",
    )
    args = parser.parse_args(args)
    if args.nologs:
        # Used if we already set up logging e.g. in service module
        return

    # Get root logger
    mlogger = logging.getLogger("")

    # If path does not exist, create it
    path = utilities.get_entry_from_config_file("logging", "logs", r"C:\dashboard")
    if not os.path.exists(path):
        os.makedirs(path)
    loglevel = utilities.get_entry_from_config_file("logging", "loglevel", "INFO")
    maxfilesize = int(
        utilities.get_entry_from_config_file("logging", "maxfilesize", 5000000)
    )
    backups = int(utilities.get_entry_from_config_file("logging", "backups", 10))
    logpath = os.path.join(path, "dashboards.log")
    mlogger.setLevel(logging.getLevelName(loglevel))

    # Create file logger
    fh = logging.handlers.RotatingFileHandler(
        logpath, maxBytes=maxfilesize, backupCount=backups, encoding="utf-8"
    )
    fh.setLevel(logging.getLevelName(loglevel))

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s.%(funcName)s:%(lineno)d:%(threadName)s - %(message)s"
    )
    fh.setFormatter(formatter)
    mlogger.addHandler(fh)

    if args.noconsole:
        pass
    else:
        import cm_dashboards.ansistrm

        # Create console logger if appropriate
        ch = cm_dashboards.ansistrm.ColorizingStreamHandler()
        ch.setLevel(logging.getLevelName(loglevel))
        ch.setFormatter(formatter)
        mlogger.addHandler(ch)


def main(args=[]):
    from waitress import serve

    setup_logging(args)

    if getattr(sys, "frozen", False):
        logger.info("Starting in FROZEN Mode")
    else:
        logger.info("Starting in DEVELOPMENT Mode")

    logger.info("FV: here")

    import cm_dashboards.report_builder.main
    import cm_dashboards.demo_nl.main
    import cm_dashboards.demo_ifrs17.main
    import cm_dashboards.nonlife.nonlife_pivot_sample
    import cm_dashboards.nonlife.nonlife_sample
    import cm_dashboards.nonlife_standalone.nonlife_solo
    import cm_dashboards.nonlife_standalone.nonlife_solo_development

    # import cm_dashboards.bs_pl.bs_pl_dash
    # import cm_dashboards.china_paa.main
    # import cm_dashboards.china_subledger.main
    # import cm_dashboards.custom_error_handlers
    #
    # # import cm_dashboards.model_info.model_info_dash
    # import cm_dashboards.dash_routes
    # import cm_dashboards.esg.main
    # import cm_dashboards.flaor.main
    # import cm_dashboards.ifrs17_accounting.home_page
    # import cm_dashboards.ifrs17_accounting.journal_view
    # import cm_dashboards.ifrs17_accounting_selic.home_page
    # import cm_dashboards.ifrs17_accounting_selic.journal_view_paa_page
    # import cm_dashboards.ifrs17_accounting_selic.journal_view_page
    # import cm_dashboards.ifrs17_disclosure.main
    # import cm_dashboards.ifrs17_paa.ifrs17_paa
    # import cm_dashboards.jics.main
    # import cm_dashboards.kics.main
    # import cm_dashboards.kics_cloud.main
    # import cm_dashboards.nippon.ESR_chart
    # import cm_dashboards.nonlife.nonlife_pivot_sample
    # import cm_dashboards.nonlife.nonlife_sample
    # import cm_dashboards.nonlife_standalone.nonlife_solo
    # import cm_dashboards.nonlife_standalone.nonlife_solo_development
    # #import cm_dashboards.orsa.main
    # import cm_dashboards.other_accounting.paa_dash
    # import cm_dashboards.other_accounting.vfa_dash
    # import cm_dashboards.reinsurance.re_genledger_dash
    # import cm_dashboards.reinsurance.re_reconciliation_dash
    # import cm_dashboards.reinsurance.re_subledger_dash
    # import cm_dashboards.reinsurance.re_trial_balance_dash
    #
    # # import graph.FMP
    # import cm_dashboards.solvency_capital.sc_dash
    # import cm_dashboards.subledger.genledger_dash
    # import cm_dashboards.subledger.reconciliation_dash
    #
    # # Korea Standard Code dashboards
    # import cm_dashboards.subledger.subledger_dash
    # import cm_dashboards.subledger.trial_balance_dash
    # import cm_dashboards.wvr_data.wvr_data_dash
    # import cm_dashboards.wvr_data.wvr_data_dash_solo
    from cm_dashboards.server import server as application

    # Set waitress logging level to ERROR
    waitress_logger = logging.getLogger("waitress")
    waitress_logger.setLevel(logging.ERROR)

    # Get server settings
    use_ipv6 = get_ipv6()
    host = get_host()
    port = get_port()
    protocol = get_protocol()

    # Run server
    serve(
        application,
        url_scheme=protocol,
        listen="{0}:{1}".format(host, port),
        ipv6=use_ipv6,
    )


# Command line entry point
if __name__ == "__main__":
    main(sys.argv[1:])
