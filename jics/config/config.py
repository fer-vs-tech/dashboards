import dash

from cm_dashboards.server import cache, server

PROJECT_NAME = "jics"
PROJECT_TITLE = "J-ICS QIS reporting dashboards"
EXPORT_LINK = f"/dash/{PROJECT_NAME}/export"

external_scripts = [
    "../static/utils/tabs.js",
    "../static/utils/merge_cells.js",
]
external_stylesheets = [
    "../static/css/bootstrap.css",
    "../static/css/ifrs17.css",
]
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
