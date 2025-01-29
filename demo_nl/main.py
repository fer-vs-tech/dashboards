"""
@author: Fernando Valentin
@project: Non Life Std Code
@description: Non Life Std Code Dashboards
@date: 2024-10-12
"""
import logging

logger = logging.getLogger(__name__)
import sys

sys.path.append("..")

import cm_dashboards.custom_html_template as custom_html_template
import cm_dashboards.demo_nl.config.callbacks
import cm_dashboards.demo_nl.config.controllers
from cm_dashboards.demo_nl.config.config import PROJECT_TITLE, app
from cm_dashboards.demo_nl.layout.layout_loader import generate_main_layout

# Apply custom HTML template to the app, set the layout and title
app.index_string = custom_html_template.WM_TEMPLATE
app.layout = generate_main_layout(PROJECT_TITLE)
