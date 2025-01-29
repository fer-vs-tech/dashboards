import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html


def generate_main_layout(title):
    """
    Generates the main layout for the dashboard.
    :param title: The title of the dashboard
    :param dashboard_data: The dashboard data
    :return: The main layout
    """
    FIGURE_CONFIG = {
        "displaylogo": False,
        "displayModeBar": False,
    }

    FIGURE_STYLE = {
        "height": "500px",
    }

    PIE_CHART_STYLE = {
        "height": "200px",
        "width": "100%",
    }

    BAR_CHART_STYLE = {
        "height": "304px",
        "width": "90%",
    }

    LONGER_BAR_CHART_STYLE = {
        "height": "383px",
        "width": "90%",
    }

    # Table styles
    style_table = dict(overflowX="auto", minWidth="100", maxHeight="380px")
    style_cell = dict(minWidth="130px", width="180px", textAlign="left")

    main_layout = dbc.Container(
        className="dbc",
        children=[
            html.Div(
                className="logo",
                children=[
                    html.Img(src="/dash/static/assets/wm_logo.svg"),
                    html.Div(
                        className="logo-text", children="Demo_IFRS17 reporting dashboards"
                    ),
                ],
            ),
            html.Div(
                className="main-container",
                children=[
                    html.Div(
                        children=[
                            dbc.Toast(
                                "Failed to load data, please make sure provided the WVR files are valid",
                                id="error-toast",
                                header="Error occurred",
                                is_open=False,
                                dismissable=True,
                                icon="danger",
                                style={
                                    "position": "fixed",
                                    "top": 84,
                                    "right": 10,
                                    "width": 290,
                                },
                            ),
                            dcc.Loading(
                                type="cube",
                                color="#2741BC",
                                debug=False,
                                children=[
                                    dcc.Location(id="url", refresh=True),
                                    dcc.Store(
                                        id="wvr_files",
                                        storage_type="session",
                                    ),
                                    dcc.Store(
                                        id="prepared_data",
                                        storage_type="session",
                                    ),
                                    dcc.Store(
                                        id="chart_data",
                                        storage_type="session",
                                    ),
                                    dbc.Tabs(
                                        id="tabs",
                                        active_tab="tab-0",
                                        children=[
                                            dbc.Tab(
                                                label="Overview NL",
                                                tab_class_name="unactive-tab",
                                                label_class_name="unactive-tab-label",
                                                active_tab_class_name="active-tab",
                                                active_label_class_name="active-tab-label",
                                                children=[
                                                    html.Div(
                                                        className="body-content overview",
                                                        children=[
                                                            dbc.Row(
                                                                style={
                                                                    "margin-bottom": "-4px",
                                                                },
                                                                children=[
                                                                    dbc.Col(
                                                                        width=3,
                                                                        className="box-container box-radius",
                                                                        style={
                                                                            "borderRadius": "0px 10px 10px 10px",
                                                                            "margin-right": "12px",
                                                                            "width": "586px",
                                                                        },
                                                                        children=[
                                                                            html.Label(
                                                                                "Balance Sheet"
                                                                            ),
                                                                            html.Div(
                                                                                className="gap-medium"
                                                                            ),
                                                                            html.Div(
                                                                                style=dict(
                                                                                    display="flex",
                                                                                    justifyContent="center",
                                                                                    alignItems="center",
                                                                                ),
                                                                                children=[
                                                                                    dcc.Graph(
                                                                                        id="balance-sheet-graph",
                                                                                        config=FIGURE_CONFIG,
                                                                                        style=BAR_CHART_STYLE,
                                                                                        responsive=True,
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        width=3,
                                                                        className="box-container box-radius",
                                                                        style={
                                                                            "width": "455px",
                                                                            "margin-right": "12px",
                                                                        },
                                                                        children=[
                                                                            html.Label(
                                                                                "Risk Distribution"
                                                                            ),
                                                                            html.Div(
                                                                                className="gap-medium"
                                                                            ),
                                                                            html.Div(
                                                                                className="gap-medium"
                                                                            ),
                                                                            dcc.Graph(
                                                                                id="risk-distribution-graph",
                                                                                config=FIGURE_CONFIG,
                                                                                style=PIE_CHART_STYLE,
                                                                                responsive=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        width=3,
                                                                        className="box-container box-radius",
                                                                        style={
                                                                            "width": "375px",
                                                                            "margin-right": "12px",
                                                                        },
                                                                        children=[
                                                                            html.Label(
                                                                                "Market Risk Distribution"
                                                                            ),
                                                                            html.Div(
                                                                                className="gap-medium"
                                                                            ),
                                                                            html.Div(
                                                                                className="gap-medium"
                                                                            ),
                                                                            dcc.Graph(
                                                                                id="market-risk-distribution-graph",
                                                                                config=FIGURE_CONFIG,
                                                                                style=PIE_CHART_STYLE,
                                                                                responsive=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        width=3,
                                                                        className="box-container box-radius",
                                                                        style={
                                                                            "borderRadius": "10px 0px 10px 10px",
                                                                            "margin-right": "0px",
                                                                            "width": "390px",
                                                                        },
                                                                        children=[
                                                                            html.Label(
                                                                                "Life Insurance Risk Distribution"
                                                                            ),
                                                                            html.Div(
                                                                                className="gap-medium"
                                                                            ),
                                                                            html.Div(
                                                                                className="gap-medium"
                                                                            ),
                                                                            dcc.Graph(
                                                                                id="life-insurance-risk-distribution-graph",
                                                                                config=FIGURE_CONFIG,
                                                                                style=PIE_CHART_STYLE,
                                                                                responsive=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                            dbc.Row(
                                                                children=[
                                                                    dbc.Col(
                                                                        width=4,
                                                                        className="box-container box-radius",
                                                                        style={
                                                                            "width": "658px",
                                                                            "height": "491px",
                                                                            "margin-right": "12px",
                                                                            "margin-bottom": "0px",
                                                                        },
                                                                        children=[
                                                                            html.Label(
                                                                                "Asset Portfolio Projected"
                                                                            ),
                                                                            html.Div(
                                                                                className="gap-medium"
                                                                            ),
                                                                            html.Div(
                                                                                style=dict(
                                                                                    display="flex",
                                                                                    justifyContent="center",
                                                                                    alignItems="center",
                                                                                ),
                                                                                children=[
                                                                                    dcc.Graph(
                                                                                        id="asset-mv-graph",
                                                                                        config=FIGURE_CONFIG,
                                                                                        style=LONGER_BAR_CHART_STYLE,
                                                                                        responsive=True,
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        width=4,
                                                                        className="box-container box-radius",
                                                                        style={
                                                                            "width": "580px",
                                                                            "height": "491px",
                                                                            "margin-right": "12px",
                                                                            "margin-bottom": "0px",
                                                                        },
                                                                        children=[
                                                                            html.Label(
                                                                                "Market Risk (Projected)"
                                                                            ),
                                                                            html.Div(
                                                                                className="gap-medium"
                                                                            ),
                                                                            html.Div(
                                                                                style=dict(
                                                                                    display="flex",
                                                                                    justifyContent="center",
                                                                                    alignItems="center",
                                                                                ),
                                                                                children=[
                                                                                    dcc.Graph(
                                                                                        id="market-risk-projected-graph",
                                                                                        config=FIGURE_CONFIG,
                                                                                        style=LONGER_BAR_CHART_STYLE,
                                                                                        responsive=True,
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        width=4,
                                                                        className="box-container box-radius",
                                                                        style={
                                                                            "width": "580px",
                                                                            "height": "491px",
                                                                            "margin-bottom": "0px",
                                                                        },
                                                                        children=[
                                                                            html.Label(
                                                                                "Life Insurance Risk (Projected)"
                                                                            ),
                                                                            html.Div(
                                                                                className="gap-medium"
                                                                            ),
                                                                            html.Div(
                                                                                style=dict(
                                                                                    display="flex",
                                                                                    justifyContent="center",
                                                                                    alignItems="center",
                                                                                ),
                                                                                children=[
                                                                                    dcc.Graph(
                                                                                        id="life-insurance-risk-projected-graph",
                                                                                        config=FIGURE_CONFIG,
                                                                                        style=LONGER_BAR_CHART_STYLE,
                                                                                        responsive=True,
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
                                            dbc.Tab(
                                                label="Solvency Summary",
                                                tab_class_name="unactive-tab",
                                                label_class_name="unactive-tab-label",
                                                active_tab_class_name="active-tab",
                                                active_label_class_name="active-tab-label",
                                                children=[
                                                    html.Div(
                                                        className="body-content figure-containe",
                                                        children=[
                                                            html.Label(
                                                                "Break down of aggregation solvency results"
                                                            ),
                                                            html.Div(
                                                                className="gap-medium"
                                                            ),
                                                            html.Div(
                                                                className="tabular-data-container",
                                                                children=[
                                                                    html.Span(
                                                                        className="note",
                                                                        children="(2018-12-31 기준, 단위 : 10만원)",
                                                                    ),
                                                                    dash_table.DataTable(
                                                                        id="solvency-results-table",
                                                                        page_size=300,
                                                                        cell_selectable=False,
                                                                        style_table=dict(
                                                                            overflowX="auto",
                                                                            minWidth="100",
                                                                            maxHeight="57vh",
                                                                        ),
                                                                        fixed_rows={
                                                                            "headers": True,
                                                                            "data": 0,
                                                                        },
                                                                        style_cell=style_cell,
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            dbc.Tab(
                                                label="Balance Sheet",
                                                tab_class_name="unactive-tab",
                                                label_class_name="unactive-tab-label",
                                                active_tab_class_name="active-tab",
                                                active_label_class_name="active-tab-label",
                                                children=[
                                                    html.Div(
                                                        className="body-content",
                                                        children=[
                                                            html.Label("Balance Sheet"),
                                                            html.Div(
                                                                style=dict(
                                                                    width="900px",
                                                                    marginLeft="17px",
                                                                ),
                                                                children=[
                                                                    dcc.Graph(
                                                                        id="balance-sheet-figure",
                                                                        responsive=True,
                                                                        config=FIGURE_CONFIG,
                                                                        style=dict(
                                                                            height="386px"
                                                                        ),
                                                                    ),
                                                                    html.Div(
                                                                        className="gap-medium"
                                                                    ),
                                                                    html.Div(
                                                                        className="gap-small"
                                                                    ),
                                                                    html.Span(
                                                                        className="note",
                                                                        children="(2018-12-31 기준, 단위 : 10만원)",
                                                                    ),
                                                                    dash_table.DataTable(
                                                                        id="balance-sheet-table",
                                                                        page_size=300,
                                                                        cell_selectable=False,
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            dbc.Tab(
                                                label="Risk Distribution",
                                                tab_class_name="unactive-tab",
                                                label_class_name="unactive-tab-label",
                                                active_tab_class_name="active-tab",
                                                active_label_class_name="active-tab-label",
                                                children=[
                                                    html.Div(
                                                        className="body-content",
                                                        children=[
                                                            html.Label(
                                                                "Risk Distribution"
                                                            ),
                                                            html.Div(
                                                                style=dict(
                                                                    width="980px",
                                                                    marginLeft="17px",
                                                                ),
                                                                children=[
                                                                    html.Div(
                                                                        style=dict(
                                                                            height="400px",
                                                                            display="flex",
                                                                            justifyContent="center",
                                                                            alignItems="center",
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="risk-distribution-figure",
                                                                                responsive=True,
                                                                                config=FIGURE_CONFIG,
                                                                                style=dict(
                                                                                    height="100%",
                                                                                    width="630px",
                                                                                ),
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    html.Div(
                                                                        style=dict(
                                                                            height="30px",
                                                                        ),
                                                                    ),
                                                                    html.Span(
                                                                        className="note",
                                                                        children="(2018-12-31 기준, 단위 : 10만원)",
                                                                    ),
                                                                    dash_table.DataTable(
                                                                        id="risk-distribution-table",
                                                                        page_size=300,
                                                                        cell_selectable=False,
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            dbc.Tab(
                                                label="Market Risk Distribution",
                                                tab_class_name="unactive-tab",
                                                label_class_name="unactive-tab-label",
                                                active_tab_class_name="active-tab",
                                                active_label_class_name="active-tab-label",
                                                children=[
                                                    html.Div(
                                                        className="body-content",
                                                        children=[
                                                            html.Label(
                                                                "Market Risk Distribution"
                                                            ),
                                                            html.Div(
                                                                style=dict(
                                                                    width="980px",
                                                                    marginLeft="17px",
                                                                ),
                                                                children=[
                                                                    html.Div(
                                                                        style=dict(
                                                                            height="400px",
                                                                            display="flex",
                                                                            justifyContent="center",
                                                                            alignItems="center",
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="market-risk-distribution-figure",
                                                                                responsive=True,
                                                                                config=FIGURE_CONFIG,
                                                                                style=dict(
                                                                                    height="100%",
                                                                                    width="630px",
                                                                                ),
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    html.Div(
                                                                        style=dict(
                                                                            height="30px",
                                                                        ),
                                                                    ),
                                                                    html.Span(
                                                                        className="note",
                                                                        children="(2018-12-31 기준, 단위 : 10만원)",
                                                                    ),
                                                                    dash_table.DataTable(
                                                                        id="market-risk-distribution-table",
                                                                        page_size=300,
                                                                        cell_selectable=False,
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            dbc.Tab(
                                                label="Life Insurance Risk Distribution",
                                                tab_class_name="unactive-tab",
                                                label_class_name="unactive-tab-label",
                                                active_tab_class_name="active-tab",
                                                active_label_class_name="active-tab-label",
                                                children=[
                                                    html.Div(
                                                        className="body-content",
                                                        children=[
                                                            html.Label(
                                                                "Life Insurance Risk Distribution"
                                                            ),
                                                            html.Div(
                                                                style=dict(
                                                                    width="980px",
                                                                    marginLeft="17px",
                                                                ),
                                                                children=[
                                                                    html.Div(
                                                                        style=dict(
                                                                            height="400px",
                                                                            display="flex",
                                                                            justifyContent="center",
                                                                            alignItems="center",
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="life-insurance-risk-distribution-figure",
                                                                                responsive=True,
                                                                                config=FIGURE_CONFIG,
                                                                                style=dict(
                                                                                    height="100%",
                                                                                    width="630px",
                                                                                ),
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    html.Div(
                                                                        style=dict(
                                                                            height="30px",
                                                                        ),
                                                                    ),
                                                                    html.Span(
                                                                        className="note",
                                                                        children="(2018-12-31 기준, 단위 : 10만원)",
                                                                    ),
                                                                    dash_table.DataTable(
                                                                        id="life-insurance-risk-distribution-table",
                                                                        page_size=300,
                                                                        cell_selectable=False,
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            dbc.Tab(
                                                label="Projected Risk (Agg)",
                                                tab_class_name="unactive-tab",
                                                label_class_name="unactive-tab-label",
                                                active_tab_class_name="active-tab",
                                                active_label_class_name="active-tab-label",
                                                children=[
                                                    html.Div(
                                                        className="body-content",
                                                        children=[
                                                            html.Label(
                                                                "Projected Risk (Agg)"
                                                            ),
                                                            html.Div(
                                                                className="gap-medium"
                                                            ),
                                                            dbc.Row(
                                                                style=dict(
                                                                    height="453px"
                                                                ),
                                                                children=[
                                                                    dbc.Col(
                                                                        className="rb-2 figure-container",
                                                                        width=dict(
                                                                            projected - market - risk - table                 size=5,
                                                                            offset=16,
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="projected-market-risk-graph",
                                                                                config=FIGURE_CONFIG,
                                                                                responsive=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        className="rb-2 figure-container",
                                                                        width=dict(
                                                                            size=7,
                                                                            offset=16,
                                                                        ),
                                                                        style=dict(
                                                                            marginTop="80px"
                                                                        ),
                                                                        children=[
                                                                            html.Span(
                                                                                className="note",
                                                                                children="(2018-12-31 기준, 단위 : 10만원)",
                                                                            ),
                                                                            dash_table.DataTable(
                                                                                id="projected-market-risk-table",
                                                                                page_size=300,
                                                                                cell_selectable=False,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                            html.Div(
                                                                className="gap-medium"
                                                            ),
                                                            html.Div(
                                                                className="gap-medium"
                                                            ),
                                                            dbc.Row(
                                                                style=dict(
                                                                    height="453px"
                                                                ),
                                                                children=[
                                                                    dbc.Col(
                                                                        className="rb-2 figure-container",
                                                                        width=dict(
                                                                            size=5,
                                                                            offset=16,
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="projected-life-insurance-risk-graph",
                                                                                config=FIGURE_CONFIG,
                                                                                responsive=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        className="rb-2 figure-container",
                                                                        style=dict(
                                                                            marginTop="80px"
                                                                        ),
                                                                        width=dict(
                                                                            size=7,
                                                                            offset=16,
                                                                        ),
                                                                        children=[
                                                                            html.Span(
                                                                                className="note",
                                                                                children="(2018-12-31 기준, 단위 : 10만원)",
                                                                            ),
                                                                            dash_table.DataTable(
                                                                                id="projected-life-insurance-risk-table",
                                                                                page_size=300,
                                                                                cell_selectable=False,
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
                                                label="Projected Market Risk",
                                                tab_class_name="unactive-tab",
                                                label_class_name="unactive-tab-label",
                                                active_tab_class_name="active-tab",
                                                active_label_class_name="active-tab-label",
                                                children=[
                                                    html.Div(
                                                        className="body-content",
                                                        children=[
                                                            html.Label(
                                                                "Projected Market Risk"
                                                            ),
                                                            html.Div(
                                                                className="gap-medium"
                                                            ),
                                                            dbc.Row(
                                                                style=dict(
                                                                    height="453px"
                                                                ),
                                                                children=[
                                                                    dbc.Col(
                                                                        className="rb-2 figure-container",
                                                                        width=dict(
                                                                            size=6,
                                                                            offset=16,
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="equity-graph",
                                                                                config=FIGURE_CONFIG,
                                                                                responsive=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        className="rb-2 figure-container",
                                                                        width=dict(
                                                                            size=6,
                                                                            offset=16,
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="interest-graph",
                                                                                config=FIGURE_CONFIG,
                                                                                responsive=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                            html.Div(
                                                                className="gap-medium"
                                                            ),
                                                            html.Div(
                                                                className="gap-small"
                                                            ),
                                                            dbc.Row(
                                                                style=dict(
                                                                    height="453px"
                                                                ),
                                                                children=[
                                                                    dbc.Col(
                                                                        className="rb-2 figure-container",
                                                                        width=dict(
                                                                            size=6,
                                                                            offset=16,
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="property-graph",
                                                                                config=FIGURE_CONFIG,
                                                                                style=dict(
                                                                                    width="87%",
                                                                                    height="100%",
                                                                                ),
                                                                                responsive=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        className="rb-2 figure-container",
                                                                        width=dict(
                                                                            size=6,
                                                                            offset=16,
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="currency-graph",
                                                                                config=FIGURE_CONFIG,
                                                                                responsive=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                            html.Div(
                                                                className="gap-medium"
                                                            ),
                                                            html.Div(
                                                                className="gap-small"
                                                            ),
                                                            dbc.Row(
                                                                style=dict(
                                                                    height="453px"
                                                                ),
                                                                children=[
                                                                    dbc.Col(
                                                                        className="rb-2 figure-container",
                                                                        width=dict(
                                                                            size=6,
                                                                            offset=16,
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="spread-graph",
                                                                                config=FIGURE_CONFIG,
                                                                                responsive=True,
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
                                                label="Projected Life Insurance Risk",
                                                tab_class_name="unactive-tab",
                                                label_class_name="unactive-tab-label",
                                                active_tab_class_name="active-tab",
                                                active_label_class_name="active-tab-label",
                                                children=[
                                                    html.Div(
                                                        className="body-content",
                                                        children=[
                                                            html.Label(
                                                                "Projected Life Insurance Risk"
                                                            ),
                                                            html.Div(
                                                                className="gap-medium"
                                                            ),
                                                            dbc.Row(
                                                                style=dict(
                                                                    height="453px"
                                                                ),
                                                                children=[
                                                                    dbc.Col(
                                                                        className="rb-2 figure-container",
                                                                        width=dict(
                                                                            size=6,
                                                                            offset=16,
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="mortality-graph",
                                                                                config=FIGURE_CONFIG,
                                                                                responsive=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        className="rb-2 figure-container",
                                                                        width=dict(
                                                                            size=6,
                                                                            offset=16,
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="morbidity-graph",
                                                                                config=FIGURE_CONFIG,
                                                                                responsive=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                            dbc.Row(
                                                                style=dict(
                                                                    height="453px"
                                                                ),
                                                                children=[
                                                                    dbc.Col(
                                                                        className="rb-2 figure-container",
                                                                        width=dict(
                                                                            size=6,
                                                                            offset=16,
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="longevity-graph",
                                                                                config=FIGURE_CONFIG,
                                                                                responsive=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        className="rb-2 figure-container",
                                                                        width=dict(
                                                                            size=6,
                                                                            offset=16,
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="lapse-graph",
                                                                                config=FIGURE_CONFIG,
                                                                                responsive=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                            html.Div(
                                                                className="gap-medium"
                                                            ),
                                                            dbc.Row(
                                                                style=dict(
                                                                    height="453px"
                                                                ),
                                                                children=[
                                                                    dbc.Col(
                                                                        className="rb-2 figure-container",
                                                                        width=dict(
                                                                            size=6,
                                                                            offset=16,
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="expense-graph",
                                                                                config=FIGURE_CONFIG,
                                                                                responsive=True,
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        className="rb-2 figure-container",
                                                                        width=dict(
                                                                            size=6,
                                                                            offset=16,
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="catastrophe-graph",
                                                                                config=FIGURE_CONFIG,
                                                                                responsive=True,
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
                                                label="ORSA Summary",
                                                tab_class_name="unactive-tab",
                                                label_class_name="unactive-tab-label",
                                                active_tab_class_name="active-tab",
                                                active_label_class_name="active-tab-label",
                                                children=[
                                                    html.Div(
                                                        className="body-content merged-header",
                                                        children=[
                                                            html.Label(
                                                                "ORSA Future B/S Projection"
                                                            ),
                                                            html.Div(
                                                                className="gap-medium"
                                                            ),
                                                            html.Div(
                                                                style={
                                                                    "padding": "0px 36px"
                                                                },
                                                                children=[
                                                                    html.Span(
                                                                        className="note",
                                                                        children="(2018-12-31 기준, 단위 : 10만원)",
                                                                    ),
                                                                    dash_table.DataTable(
                                                                        id="future-bs-projection-table",
                                                                        page_size=300,
                                                                        merge_duplicate_headers=True,
                                                                        style_table=dict(
                                                                            overflowX="auto",
                                                                            minWidth="100%",
                                                                            maxHeight="57vh",
                                                                        ),
                                                                        fixed_rows={
                                                                            "headers": True,
                                                                            "data": 0,
                                                                        },
                                                                        style_cell=style_cell,
                                                                        cell_selectable=False,
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            dbc.Tab(
                                                label="Projected Asset Portfolio 1",
                                                tab_class_name="unactive-tab",
                                                label_class_name="unactive-tab-label",
                                                active_tab_class_name="active-tab",
                                                active_label_class_name="active-tab-label",
                                                children=[
                                                    html.Div(
                                                        className="body-content",
                                                        children=[
                                                            html.Label(
                                                                "Projected Asset Portfolio 1"
                                                            ),
                                                            html.Div(
                                                                className="gap-medium"
                                                            ),
                                                            html.Div(
                                                                style=dict(
                                                                    width="980px",
                                                                    marginLeft="17px",
                                                                ),
                                                                children=[
                                                                    html.Div(
                                                                        style=dict(
                                                                            height="400px",
                                                                            display="flex",
                                                                            justifyContent="center",
                                                                            alignItems="center",
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="asset-portfolio-figure",
                                                                                responsive=True,
                                                                                config=FIGURE_CONFIG,
                                                                                style=dict(
                                                                                    height="100%",
                                                                                    width="700px",
                                                                                ),
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    html.Div(
                                                                        className="gap-medium"
                                                                    ),
                                                                    html.Div(
                                                                        className="gap-small"
                                                                    ),
                                                                    html.Span(
                                                                        className="note",
                                                                        children="(2018-12-31 기준, 단위 : 10만원)",
                                                                    ),
                                                                    dash_table.DataTable(
                                                                        id="asset-portfolio-table",
                                                                        page_size=300,
                                                                        cell_selectable=False,
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            dbc.Tab(
                                                label="Projected Asset Portfolio 2",
                                                tab_class_name="unactive-tab",
                                                label_class_name="unactive-tab-label",
                                                active_tab_class_name="active-tab",
                                                active_label_class_name="active-tab-label",
                                                children=[
                                                    html.Div(
                                                        className="body-content",
                                                        children=[
                                                            html.Label(
                                                                "Projected Asset Portfolio 2",
                                                            ),
                                                            html.Div(
                                                                className="gap-medium"
                                                            ),
                                                            html.Div(
                                                                style=dict(
                                                                    width="980px",
                                                                    marginLeft="17px",
                                                                ),
                                                                children=[
                                                                    html.Div(
                                                                        style=dict(
                                                                            height="400px",
                                                                            display="flex",
                                                                            justifyContent="center",
                                                                            alignItems="center",
                                                                        ),
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id="asset-mv-figure",
                                                                                responsive=True,
                                                                                config=FIGURE_CONFIG,
                                                                                style=dict(
                                                                                    height="100%",
                                                                                    width="620px",
                                                                                ),
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    html.Div(
                                                                        className="gap-small"
                                                                    ),
                                                                    html.Span(
                                                                        className="note",
                                                                        children="(2018-12-31 기준, 단위 : 10만원)",
                                                                    ),
                                                                    dash_table.DataTable(
                                                                        id="asset-mv-table",
                                                                        page_size=300,
                                                                        cell_selectable=False,
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
            ),
        ],
    )

    return main_layout


def generate_toast_message(
    messages: list[str], icon: str = "danger"
) -> list[dbc.Toast]:
    """
    Generate toast messages for error messages

    :param message: Message to display
    :param icon:  Class name (default: danger)
    :return: List of toast messages (dbc.Toast)
    """
    toast_messages: list[dbc.Toast] = list()

    # Check if messages is a list
    if not isinstance(messages, list):
        messages = [messages]

    # Generate toast messages for each message with different duration
    for i, (header, message) in enumerate(messages, start=1):
        duration = 8000
        toast_messages.append(
            dbc.Toast(
                message,
                header=header,
                is_open=True,
                dismissable=True,
                duration=duration * i,
                icon=icon,
                style={
                    "position": "fixed",
                    "bottom": 120,
                    "right": 5,
                    "width": 300,
                    "zIndex": 10000,
                },
            )
        )

    return toast_messages
