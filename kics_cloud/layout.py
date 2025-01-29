import dash_bootstrap_components as dbc
import plotly.io as plt_io
from dash import dash_table, dcc, html

from cm_dashboards.custom_template import custom_template

# Apply our custome template
plt_io.templates["cloud_manager"] = custom_template

# Main layout
STYLE_TABLE = {
    "overflowX": "auto",
    "minWidth": "100%",
    "maxHeight": "400px",
}
STYLE_CELL = {
    "minWidth": "120px",
    "width": "130px",
    "maxWidth": "180px",
    "overflow": "hidden",
    "textOverflow": "ellipsis",
}
STYLE_DATA = {
    "border": "none",
}
FIGURE_CONFIG = {
    "displaylogo": False,
    "displayModeBar": False,
}
PIE_CHART_STYLE = {
    "height": "290px",
    "width": "100%",
}
BAR_CHART_STYLE = {
    "height": "420px",
    "width": "85%",
}

BAR_CHART_STYLE_A = {
    "height": "360.94px",
    "width": "100%",
}

BAR_CHART_STYLE_H = {
    "height": "290px",
    "width": "100%",
}

WATERFALL_CHART_STYLE_H = {
    "height": "331px",
    "width": "100%",
}

MAIN_LAYOUT = dbc.Container(
    className="dbc",
    children=[
        dcc.Location(id="url", refresh=True),
        html.Div(
            className="logo",
            children=[
                html.Img(src="/dash/static/assets/kics_cloud_logo.svg"),
                html.Div(className="logo-text", children="K-ICS Result Charts"),
            ],
        ),
        html.Div(
            children=[
                dcc.Input(
                    id="kics-previous-wvr",
                    value="",
                    placeholder="C:\\temp\\results.wvr",
                    style={"display": "none"},
                ),
                dcc.Input(
                    id="kics-volume-wvr",
                    value="",
                    placeholder="C:\\temp\\results.wvr",
                    style={"display": "none"},
                ),
                dcc.Input(
                    id="kics-acturial-wvr",
                    value="",
                    placeholder="C:\\temp\\results.wvr",
                    style={"display": "none"},
                ),
                dcc.Input(
                    id="kics-economic-wvr",
                    value="",
                    placeholder="C:\\temp\\results.wvr",
                    style={"display": "none"},
                ),
                dcc.Input(
                    id="kics-current-wvr",
                    value="",
                    placeholder="C:\\temp\\results.wvr",
                    style={"display": "none"},
                ),
            ]
        ),
        html.Div(
            className="body-container",
            children=[
                dbc.Tabs(
                    id="tabs",
                    active_tab="tab-0",
                    children=[
                        dbc.Tab(
                            id="tab-0",
                            label="Chart",
                            tab_class_name="unactive-tab",
                            label_class_name="unactive-tab-label",
                            active_tab_class_name="active-tab",
                            active_label_class_name="active-tab-label",
                            children=[
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            width=3,
                                            className="box-container regular-table",
                                            style=dict(
                                                borderRadius="0px 10px 10px 10px"
                                            ),
                                            children=[
                                                dcc.Loading(
                                                    type="default",
                                                    color="#2741BC",
                                                    debug=False,
                                                    children=[
                                                        html.Label("Company"),
                                                        dcc.Graph(
                                                            id="company-risk-figure",
                                                            config=FIGURE_CONFIG,
                                                            style=PIE_CHART_STYLE,
                                                        ),
                                                        dash_table.DataTable(
                                                            id="company-risk",
                                                            page_size=300,
                                                            style_table=STYLE_TABLE,
                                                            style_cell=STYLE_CELL,
                                                            style_data=STYLE_DATA,
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        dbc.Col(
                                            width=dict(size=6, offset=16),
                                            className="box-container middle regular-table",
                                            children=[
                                                dcc.Loading(
                                                    type="default",
                                                    color="#2741BC",
                                                    debug=False,
                                                    children=[
                                                        dbc.Row(
                                                            children=[
                                                                dbc.Col(
                                                                    width=dict(
                                                                        size=6,
                                                                        offset=16,
                                                                    ),
                                                                    children=[
                                                                        html.Label(
                                                                            "Asset Info"
                                                                        ),
                                                                        dcc.Graph(
                                                                            id="asset-info-figure",
                                                                            config=FIGURE_CONFIG,
                                                                            style=PIE_CHART_STYLE,
                                                                        ),
                                                                        dash_table.DataTable(
                                                                            id="asset-info",
                                                                            page_size=300,
                                                                            style_table=STYLE_TABLE,
                                                                            style_cell=STYLE_CELL,
                                                                            style_data=STYLE_DATA,
                                                                        ),
                                                                    ],
                                                                ),
                                                                dbc.Col(
                                                                    width=dict(
                                                                        size=6,
                                                                        offset=16,
                                                                    ),
                                                                    children=[
                                                                        html.Label(),
                                                                        dcc.Graph(
                                                                            id="market-risk-figure",
                                                                            config=FIGURE_CONFIG,
                                                                            style=PIE_CHART_STYLE,
                                                                        ),
                                                                        dash_table.DataTable(
                                                                            id="market-risk",
                                                                            page_size=300,
                                                                            style_table=STYLE_TABLE,
                                                                            style_cell=STYLE_CELL,
                                                                            style_data=STYLE_DATA,
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        dbc.Col(
                                            className="box-container regular-table",
                                            width=3,
                                            children=[
                                                dcc.Loading(
                                                    type="default",
                                                    color="#2741BC",
                                                    debug=False,
                                                    children=[
                                                        html.Label("Liability Info"),
                                                        dcc.Graph(
                                                            id="liability-info-figure",
                                                            config=FIGURE_CONFIG,
                                                            style=BAR_CHART_STYLE_H,
                                                        ),
                                                        dash_table.DataTable(
                                                            id="liability-info",
                                                            page_size=300,
                                                            style_table=STYLE_TABLE,
                                                            style_cell=STYLE_CELL,
                                                            style_data=STYLE_DATA,
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                dbc.Row(
                                    className="box-container",
                                    justify="evenly",
                                    children=[
                                        html.Label("Product Info"),
                                        dbc.Col(
                                            width=3,
                                            children=[
                                                dcc.Loading(
                                                    type="default",
                                                    color="#2741BC",
                                                    debug=False,
                                                    children=[
                                                        dcc.Graph(
                                                            id="risk-figure",
                                                            config=FIGURE_CONFIG,
                                                            style=BAR_CHART_STYLE,
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        dbc.Col(
                                            width=3,
                                            className="special-table",
                                            children=[
                                                html.Label(),
                                                dash_table.DataTable(
                                                    id="product-info",
                                                    page_size=300,
                                                    style_table=STYLE_TABLE,
                                                    style_cell=STYLE_CELL,
                                                    style_data=STYLE_DATA,
                                                ),
                                            ],
                                        ),
                                        dbc.Col(
                                            width=3,
                                            children=[
                                                dcc.Loading(
                                                    type="default",
                                                    color="#2741BC",
                                                    debug=False,
                                                    children=[
                                                        dcc.Graph(
                                                            id="insurance-risk-figure",
                                                            config=FIGURE_CONFIG,
                                                            style=BAR_CHART_STYLE,
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        dbc.Col(
                                            width=3,
                                            children=[
                                                dcc.Loading(
                                                    type="default",
                                                    color="#2741BC",
                                                    debug=False,
                                                    children=[
                                                        dcc.Graph(
                                                            id="market-risk-2-figure",
                                                            config=FIGURE_CONFIG,
                                                            style=BAR_CHART_STYLE,
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        dbc.Tab(
                            id="tab-1",
                            label="Movement",
                            tab_class_name="unactive-tab",
                            label_class_name="unactive-tab-label",
                            active_tab_class_name="active-tab",
                            active_label_class_name="active-tab-label",
                            children=[
                                dbc.Row(
                                    style=dict(height="948px"),
                                    children=[
                                        dbc.Col(
                                            className="box-container custome-table rb-2",
                                            style=dict(
                                                height="948px",
                                                borderRadius="0px 10px 10px 10px",
                                                width="49.5%",
                                                marginRight="16px",
                                            ),
                                            width=dict(size=6, offset=16),
                                            children=[
                                                dcc.Loading(
                                                    type="default",
                                                    color="#2741BC",
                                                    debug=False,
                                                    children=[
                                                        html.Label(
                                                            "Liability Movement"
                                                        ),
                                                        dcc.Graph(
                                                            id="bel-movement",
                                                            config=FIGURE_CONFIG,
                                                            style=WATERFALL_CHART_STYLE_H,
                                                        ),
                                                        html.Br(),
                                                        dcc.Graph(
                                                            id="risk-margin-movement",
                                                            config=FIGURE_CONFIG,
                                                            style=WATERFALL_CHART_STYLE_H,
                                                        ),
                                                        dash_table.DataTable(
                                                            id="liability-movement",
                                                            page_size=300,
                                                            style_table=dict(
                                                                overflowX="auto",
                                                                minWidth="94%",
                                                                width="94%",
                                                                maxHeight="400px",
                                                                marginLeft="20px",
                                                            ),
                                                            style_cell=STYLE_CELL,
                                                            style_data=STYLE_DATA,
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        dbc.Col(
                                            className="box-container custome-table rb-1",
                                            style=dict(
                                                height="602px",
                                                width="49.5%",
                                            ),
                                            width=dict(size=6, offset=16),
                                            children=[
                                                dcc.Loading(
                                                    type="default",
                                                    color="#2741BC",
                                                    debug=False,
                                                    children=[
                                                        html.Label("Asset Movement"),
                                                        dcc.Graph(
                                                            id="asset-movement-figure",
                                                            config=FIGURE_CONFIG,
                                                            style=WATERFALL_CHART_STYLE_H,
                                                        ),
                                                        dash_table.DataTable(
                                                            id="asset-movement",
                                                            page_size=300,
                                                            style_table=dict(
                                                                overflowX="auto",
                                                                minWidth="53%",
                                                                width="53%",
                                                                maxHeight="400px",
                                                                marginLeft="90px",
                                                            ),
                                                            style_cell=STYLE_CELL,
                                                            style_data=STYLE_DATA,
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                dbc.Row(
                                    className="box-container",
                                    style=dict(height="631px", marginTop="16px"),
                                    children=[
                                        dbc.Col(
                                            width=dict(size=6, offset=16),
                                            className="custome-table with-border",
                                            style=dict(height="631px"),
                                            children=[
                                                dcc.Loading(
                                                    type="default",
                                                    color="#2741BC",
                                                    debug=False,
                                                    children=[
                                                        html.Label(
                                                            "Required Capital & individual risks Movement"
                                                        ),
                                                        html.Br(),
                                                        dcc.Graph(
                                                            id="required-capital-figure",
                                                            config=FIGURE_CONFIG,
                                                            style=dict(height="435px"),
                                                        ),
                                                        html.Br(),
                                                        html.Div(
                                                            children="Required Capital",
                                                            className="table-title required-capital",
                                                            style=dict(
                                                                minWidth="97%",
                                                                width="97%",
                                                            ),
                                                        ),
                                                        dash_table.DataTable(
                                                            id="required-capital",
                                                            page_size=300,
                                                            style_table=dict(
                                                                overflowX="auto",
                                                                minWidth="97%",
                                                                width="97%",
                                                                maxHeight="400px",
                                                            ),
                                                            style_cell=STYLE_CELL,
                                                            style_data=STYLE_DATA,
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        dbc.Col(
                                            width=dict(size=6, offset=16),
                                            className="custome-table with-border",
                                            style=dict(height="631px"),
                                            children=[
                                                dcc.Loading(
                                                    type="default",
                                                    color="#2741BC",
                                                    debug=False,
                                                    children=[
                                                        html.Label(""),
                                                        dbc.Row(
                                                            children=[
                                                                dbc.Col(
                                                                    width=dict(
                                                                        size=6,
                                                                    ),
                                                                    children=[
                                                                        dcc.Graph(
                                                                            id="market-risk-movement-figure",
                                                                            config=FIGURE_CONFIG,
                                                                            style=BAR_CHART_STYLE_A,
                                                                        ),
                                                                    ],
                                                                ),
                                                                dbc.Col(
                                                                    width=dict(
                                                                        size=6,
                                                                    ),
                                                                    children=[
                                                                        dcc.Graph(
                                                                            id="insurance-risk-movement-figure",
                                                                            config=FIGURE_CONFIG,
                                                                            style=BAR_CHART_STYLE_A,
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                        dbc.Row(
                                                            children=[
                                                                dbc.Col(
                                                                    children=[
                                                                        html.Div(
                                                                            children="Market Risk",
                                                                            className="table-title market-risk",
                                                                        ),
                                                                        dash_table.DataTable(
                                                                            id="market-risk-movement",
                                                                            page_size=300,
                                                                            style_table=STYLE_TABLE,
                                                                            style_cell=STYLE_CELL,
                                                                            style_data=STYLE_DATA,
                                                                        ),
                                                                        html.Div(
                                                                            children="Insurance Risk",
                                                                            className="table-title insurance-risk",
                                                                        ),
                                                                        dash_table.DataTable(
                                                                            id="insurance-risk-movement",
                                                                            page_size=300,
                                                                            style_table=STYLE_TABLE,
                                                                            style_cell=STYLE_CELL,
                                                                            style_data=STYLE_DATA,
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                dbc.Row(
                                    className="box-container",
                                    style=dict(height="765.6px", marginTop="16px"),
                                    children=[
                                        dbc.Col(
                                            width=dict(size=6, offset=16),
                                            style=dict(height="631px"),
                                            children=[
                                                dcc.Loading(
                                                    type="default",
                                                    color="#2741BC",
                                                    debug=False,
                                                    children=[
                                                        html.Label("Available Captal"),
                                                        dcc.Graph(
                                                            id="available-capital-figure",
                                                            config=FIGURE_CONFIG,
                                                            style=dict(
                                                                height="340px",
                                                                width="95.3%",
                                                            ),
                                                        ),
                                                        html.Br(),
                                                        html.Div(
                                                            children="Available Capital",
                                                            className="table-title insurance-risk",
                                                            style=dict(
                                                                width="98%",
                                                                marginTop="-1px",
                                                            ),
                                                        ),
                                                        html.Div(
                                                            className="custome-table with-border",
                                                            children=[
                                                                dash_table.DataTable(
                                                                    id="available-capital",
                                                                    page_size=300,
                                                                    style_table=dict(
                                                                        width="98%",
                                                                    ),
                                                                    style_cell=STYLE_CELL,
                                                                    style_data=STYLE_DATA,
                                                                ),
                                                            ],
                                                        ),
                                                        html.Div(
                                                            style=dict(height="41px")
                                                        ),
                                                        dbc.Row(
                                                            className="pad-row",
                                                            children=[
                                                                dbc.Col(
                                                                    className="custome-table",
                                                                    width=5,
                                                                    children=[
                                                                        dash_table.DataTable(
                                                                            id="tier-1",
                                                                            page_size=300,
                                                                            style_table=dict(
                                                                                width="328px",
                                                                                marginLeft="-11px",
                                                                            ),
                                                                            style_cell=STYLE_CELL,
                                                                            style_data=STYLE_DATA,
                                                                        ),
                                                                    ],
                                                                ),
                                                                dbc.Col(
                                                                    className="custome-table rb-1",
                                                                    width=7,
                                                                    children=[
                                                                        dash_table.DataTable(
                                                                            id="tier-2",
                                                                            page_size=300,
                                                                            style_table=dict(
                                                                                width="456px",
                                                                                marginLeft="20px",
                                                                            ),
                                                                            style_cell=STYLE_CELL,
                                                                            style_data=STYLE_DATA,
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        dbc.Col(
                                            width=dict(size=6),
                                            style=dict(height="765.6px"),
                                            children=[
                                                dcc.Loading(
                                                    type="default",
                                                    color="#2741BC",
                                                    debug=False,
                                                    children=[
                                                        html.Label(""),
                                                        dcc.Graph(
                                                            id="tier-1-figure",
                                                            config=FIGURE_CONFIG,
                                                            style=dict(
                                                                height="328px",
                                                                width="95.3%",
                                                            ),
                                                        ),
                                                        html.Br(),
                                                        dcc.Graph(
                                                            id="tier-2-figure",
                                                            config=FIGURE_CONFIG,
                                                            style=dict(
                                                                height="328px",
                                                                width="95.3%",
                                                            ),
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                dbc.Row(
                                    style=dict(height="951.4px"),
                                    children=[
                                        dbc.Col(
                                            width=dict(size=6, offset=16),
                                            className="box-container custome-table rb-2",
                                            style=dict(
                                                height="948px",
                                                width="49.5%",
                                                marginRight="16px",
                                            ),
                                            children=[
                                                dcc.Loading(
                                                    type="default",
                                                    color="#2741BC",
                                                    debug=False,
                                                    children=[
                                                        html.Label(
                                                            "Insurance & Market Risk"
                                                        ),
                                                        dcc.Graph(
                                                            id="insurance-risk-movement-2-figure",
                                                            config=FIGURE_CONFIG,
                                                            style=WATERFALL_CHART_STYLE_H,
                                                        ),
                                                        html.Br(),
                                                        dcc.Graph(
                                                            id="market-risk-movement-2-figure",
                                                            config=FIGURE_CONFIG,
                                                            style=WATERFALL_CHART_STYLE_H,
                                                        ),
                                                        dash_table.DataTable(
                                                            id="insurance-risk-movement-2",
                                                            page_size=300,
                                                            style_table=dict(
                                                                minWidth="94%",
                                                                width="94%",
                                                                maxHeight="400px",
                                                                marginLeft="20px",
                                                            ),
                                                            style_cell=STYLE_CELL,
                                                            style_data=STYLE_DATA,
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        dbc.Col(
                                            width=dict(size=6, offset=16),
                                            className="box-container custome-table",
                                            style=dict(height="583.8px", width="49.5%"),
                                            children=[
                                                dcc.Loading(
                                                    type="default",
                                                    color="#2741BC",
                                                    debug=False,
                                                    children=[
                                                        html.Label(
                                                            "K-ICS Ratio Movement"
                                                        ),
                                                        dcc.Graph(
                                                            id="ratio-movement-figure",
                                                            config=FIGURE_CONFIG,
                                                            style=WATERFALL_CHART_STYLE_H,
                                                        ),
                                                        html.Br(),
                                                        dash_table.DataTable(
                                                            id="ratio-movement",
                                                            page_size=300,
                                                            style_table=dict(
                                                                minWidth="94%",
                                                                width="94%",
                                                                maxHeight="400px",
                                                                marginLeft="20px",
                                                            ),
                                                            style_cell=STYLE_CELL,
                                                            style_data=STYLE_DATA,
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)
