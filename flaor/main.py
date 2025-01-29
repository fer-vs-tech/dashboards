"""
author: Kamoliddin Usmonov
project: FLOAR Dashboards
description: FLOAR Reporting Dashboards that contains different type of charts and tables
date: 2023-12-15
"""
import logging

logger = logging.getLogger(__name__)
import sys

sys.path.append("..")

import cm_dashboards.custom_html_template as custom_html_template
import cm_dashboards.flaor.config.callbacks
from cm_dashboards.flaor.config.config import PROJECT_TITLE, app
from cm_dashboards.flaor.layout.layout_loader import generate_main_layout

# Apply custom HTML template to the app, set the layout and title
app.index_string = custom_html_template.WM_TEMPLATE
app.layout = generate_main_layout(PROJECT_TITLE)
