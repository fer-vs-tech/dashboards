import sys

sys.path.append("..")

import pywintypes
import servicemanager
import win32service
import win32serviceutil

import cm_dashboards.ifrs17_accounting.generate_report as generate_report
import cm_dashboards.modeldash as modeldash


class DashboardgerSvc:
    def stop(self):
        """Stop the service"""
        self.running = False

    def run(self):
        """Main service loop"""
        self.running = True
        modeldash.main(["--noconsole"])


class DashboardFramework(win32serviceutil.ServiceFramework):
    _svc_name_ = "r3sdashboard"
    _svc_display_name_ = "R3S Dashboard Service"

    def SvcStop(self):
        """Stop the service"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.service_impl.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.service_impl = DashboardgerSvc()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        # Run the service
        self.service_impl.run()


def init():
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(DashboardFramework)
        try:
            servicemanager.StartServiceCtrlDispatcher()
        except pywintypes.error as e:
            # Failed to start as service, try to start as console
            print(e)
            # Run the service as console
            modeldash.main()

    elif sys.argv[1] == "--generate-report":
        try:
            # Parse arguments and run the script
            parser = generate_report.create_arg_parser()
            args = parser.parse_args(sys.argv[2:])
            print(f"Generating report with arguments: {args}")
            generate_report.main(args.wvr, args.type, args.reversed, args.output_path)
        except Exception as e:
            print(f"Failed to generate report with error: {e}")
            sys.exit(1)

    else:
        win32serviceutil.HandleCommandLine(DashboardFramework)


if __name__ == "__main__":
    init()
