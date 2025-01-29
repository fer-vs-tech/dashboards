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
    table_style = {
        "overflowX": "auto",
        "minWidth": "100%",
        "maxWidth": "100%",
        "width": "100%",
        "maxHeight": "500px",
        # "height": "300px",
    }
    toast_style = {
        "position": "fixed",
        "bottom": 120,
        "right": 5,
        "width": 300,
        "zIndex": 10000,
    }

    return dbc.Container(
        fluid="md",
        className="dbc",
        children=[
            html.Div(
                className="logo-container",
                children=[
                    html.Img(src="/dash/static/assets/wm_logo.svg"),
                ],
            ),
            html.Div(
                style={"display": "none"},
                children=[
                    dcc.Location(id="url", refresh=True),
                    dcc.Input(id="wvr_paths"),
                ],
            ),
            html.Div(
                className="body-container",
                children=[
                    html.Div(
                        className="title-container",
                        children=[
                            html.Div(
                                id="journal-title",
                                children=title,
                            ),
                        ],
                    ),
                    dbc.Toast(
                        id="error-toast",
                        header="Error occurred",
                        is_open=False,
                        dismissable=True,
                        icon="danger",
                        style=toast_style,
                    ),
                    html.Div(
                        children=[
                            dbc.Tabs(
                                id="tabs",
                                active_tab="tab-0",
                                children=[
                                    dbc.Tab(
                                        label="Solvency Overall",
                                        tab_class_name="unactive-tab",
                                        label_class_name="unactive-tab-label",
                                        active_tab_class_name="active-tab",
                                        active_label_class_name="active-tab-label",
                                        children=[
                                            dcc.Loading(
                                                id="loading-solvency-overall",
                                                type="circle",
                                                children=[
                                                    html.Div(
                                                        className="body-content",
                                                        style={"height": "57vh"},
                                                        children=[
                                                            html.Div(
                                                                className="merged-header",
                                                                children=[
                                                                    html.Br(),
                                                                    dcc.Graph(
                                                                        id="solvency-overall-chart",
                                                                        config=FIGURE_CONFIG,
                                                                    ),
                                                                    html.Br(),
                                                                    dcc.Graph(
                                                                        id="available-capital-chart",
                                                                        config=FIGURE_CONFIG,
                                                                    ),
                                                                    html.Br(),
                                                                    html.Label(
                                                                        "Required Capital"
                                                                    ),
                                                                    dash_table.DataTable(
                                                                        id="solvency-overall-table",
                                                                        style_table=table_style,
                                                                        merge_duplicate_headers=True,
                                                                        cell_selectable=False,
                                                                    ),
                                                                    html.Br(),
                                                                    html.Br(),
                                                                    dcc.Graph(
                                                                        id="required-capital-chart",
                                                                        config=FIGURE_CONFIG,
                                                                    ),
                                                                    html.Br(),
                                                                    html.Label(
                                                                        "Solvency Overall"
                                                                    ),
                                                                    dash_table.DataTable(
                                                                        id="required-capital-table",
                                                                        style_table=table_style,
                                                                        merge_duplicate_headers=True,
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
                                        label="ALM Results",
                                        tab_class_name="unactive-tab",
                                        label_class_name="unactive-tab-label",
                                        active_tab_class_name="active-tab",
                                        active_label_class_name="active-tab-label",
                                        children=[
                                            html.Div(
                                                className="body-content",
                                                style={"height": "57vh"},
                                                children=[
                                                    html.Div(
                                                        className="merged-header",
                                                        children=[
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="asset-portfolio-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            html.Label("ALM Results"),
                                                            dash_table.DataTable(
                                                                id="asset-portfolio-table",
                                                                style_table=table_style,
                                                                merge_duplicate_headers=True,
                                                                cell_selectable=False,
                                                                # export_format="xlsx",
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    dbc.Tab(
                                        label="Projected PAP BS",
                                        tab_class_name="unactive-tab",
                                        label_class_name="unactive-tab-label",
                                        active_tab_class_name="active-tab",
                                        active_label_class_name="active-tab-label",
                                        children=[
                                            html.Div(
                                                className="body-content",
                                                style={"height": "57vh"},
                                                children=[
                                                    html.Div(
                                                        className="merged-header",
                                                        children=[
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="projected-pap-rr-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="projected-pap-liability-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            html.Label(
                                                                "Projected MV B/S under Risk Regulation"
                                                            ),
                                                            dash_table.DataTable(
                                                                id="projected-pap-table",
                                                                style_table=table_style,
                                                                merge_duplicate_headers=True,
                                                                cell_selectable=False,
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    dbc.Tab(
                                        label="Life & Health Risk",
                                        tab_class_name="unactive-tab",
                                        label_class_name="unactive-tab-label",
                                        active_tab_class_name="active-tab",
                                        active_label_class_name="active-tab-label",
                                        children=[
                                            html.Div(
                                                className="body-content",
                                                style={"height": "57vh"},
                                                children=[
                                                    html.Div(
                                                        className="merged-header",
                                                        children=[
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="life-health-risk-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="life-health-risk-overall-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="mortality-risk-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="longevity-risk-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="morbitity-risk-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="lapse-risk-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="expense-risk-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="catastrophe-risk-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            html.Label(
                                                                "Life & Health Risk"
                                                            ),
                                                            html.Br(),
                                                            dash_table.DataTable(
                                                                id="life-health-risk-table",
                                                                style_table=table_style,
                                                                merge_duplicate_headers=True,
                                                                cell_selectable=False,
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    dbc.Tab(
                                        label="Market Risk",
                                        tab_class_name="unactive-tab",
                                        label_class_name="unactive-tab-label",
                                        active_tab_class_name="active-tab",
                                        active_label_class_name="active-tab-label",
                                        children=[
                                            html.Div(
                                                className="body-content",
                                                style={"height": "57vh"},
                                                children=[
                                                    html.Div(
                                                        className="merged-header",
                                                        children=[
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="market-risk-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="market-risk-overall-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="interest-risk-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="equity-risk-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="forex-risk-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="property-risk-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="concentration-risk-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Label("Market Risk"),
                                                            html.Br(),
                                                            dash_table.DataTable(
                                                                id="market-risk-table",
                                                                style_table=table_style,
                                                                merge_duplicate_headers=True,
                                                                cell_selectable=False,
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                    dbc.Tab(
                                        label="Credit Risk",
                                        tab_class_name="unactive-tab",
                                        label_class_name="unactive-tab-label",
                                        active_tab_class_name="active-tab",
                                        active_label_class_name="active-tab-label",
                                        children=[
                                            html.Div(
                                                className="body-content",
                                                style={"height": "57vh"},
                                                children=[
                                                    html.Div(
                                                        className="merged-header",
                                                        children=[
                                                            html.Br(),
                                                            dcc.Graph(
                                                                id="credit-risk-chart",
                                                                config=FIGURE_CONFIG,
                                                            ),
                                                            html.Br(),
                                                            html.Label("Credit Risk"),
                                                            html.Br(),
                                                            dash_table.DataTable(
                                                                id="credit-risk-table",
                                                                style_table=table_style,
                                                                merge_duplicate_headers=True,
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
    )


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
