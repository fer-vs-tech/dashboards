"""
@author: Fernando Valentin
@project: Report Builder
@description: Prototype for end-user report builder
@date: 2024-10-12
"""
import logging

logger = logging.getLogger(__name__)
import sys

sys.path.append("..")

import cm_dashboards.custom_html_template as custom_html_template
import cm_dashboards.report_builder.config.callbacks
from cm_dashboards.report_builder.config.config import PROJECT_TITLE, app
from cm_dashboards.report_builder.layout.layout_loader import generate_layout

# Apply custom HTML template to the app, set the layout and title
app.index_string = custom_html_template.WM_TEMPLATE
app.layout = generate_layout(PROJECT_TITLE)
