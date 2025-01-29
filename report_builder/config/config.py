import dash
import plotly.io as plt_io

from cm_dashboards.custom_template import custom_template
from cm_dashboards.server import cache, server

# Define application name and title
PROJECT_NAME = "report_builder"
PROJECT_TITLE = "Self report builder"
plt_io.templates["cloud_manager"] = custom_template

# External scripts and CSS stylesheets
external_scripts = [
    "../static/utils/tabs.js",
]
external_stylesheets = [
    "../static/css/bootstrap.css",
    "../static/css/ifrs17.css",
    "../static/css/custom_tab.css",
    "../static/css/orsa.css",
]

# App configuration and initialization
app = dash.Dash(
    name=PROJECT_NAME,
    title=PROJECT_TITLE,
    update_title=f"(Updating) {PROJECT_TITLE}",
    server=server,
    eager_loading=True,
    url_base_pathname=f"/dash/{PROJECT_NAME}/",
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    compress=server.config["COMPRESS_CONTENT"],
)
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# Suppress callback exceptions in production mode
debug_mode = server.config["DEBUG_MODE"]
app.config.suppress_callback_exceptions = not debug_mode
app.enable_dev_tools(
    debug=debug_mode,
    dev_tools_ui=debug_mode,
    dev_tools_props_check=debug_mode,
)

cache = cache
timeout = server.config["CACHE_TIMEOUT"]
