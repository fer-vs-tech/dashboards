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
                        className="logo-text", children="Non Life Standard Code Dashboard"
                    ),
                ],
            ),
            html.Div(
                className="body-container",
                children=[
                    html.Div(
                        children=[
                            dbc.Toast(
                                "Failed to load data, please make sure provided the WVR files are valid",
                                id="error-toast2",
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
                                        id="programs",
                                        storage_type="session",
                                    ),
                                    dcc.Store(
                                        id="portfolios",
                                        storage_type="session",
                                    ),
                                    dcc.Store(
                                        id="methods",
                                        storage_type="session",
                                    ),
                                    dcc.Store(
                                        id="dates",
                                        storage_type="session",
                                    ),
                                    dcc.Store(
                                        id="dev-periods",
                                        storage_type="session",
                                    ),
                                    dcc.Store(
                                        id="origin-periods",
                                        storage_type="session",
                                    ),
                                    ],
                            ),
                                    dcc.Store(
                                        id="calculated-results",
                                        storage_type="memory",
                                    ),
                                    dcc.Store(
                                        id="calculated-results-df",
                                        storage_type="memory",
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
                                        id="lic-tab",
                                        label="LIC Model",
                                        tab_class_name="unactive-tab",
                                        label_class_name="unactive-tab-label",
                                        active_tab_class_name="active-tab",
                                        active_label_class_name="active-tab-label",
                                        disabled=True,
                                        children=[
                                                dbc.Accordion(
                                                    id="controllers",
                                                    start_collapsed=False,
                                                    always_open=True,
                                                    active_item="lic-filters",
                                                    children=[
                                                        dbc.AccordionItem(
                                                            item_id="lic-filters",
                                                            title="Filters",
                                                            children=[
                                                                dcc.Loading(
                                                                    type="dot",
                                                                    color="#2741BC",
                                                                    children=[
                                                                html.Div(
                                                                    children=[
                                                                        dbc.Row(
                                                                            children=[
                                                                                dbc.Col(
                                                                                    children=[
                                                                                        html.B(
                                                                                            "Program"
                                                                                        ),
                                                                                                dcc.Dropdown(
                                                                                                    id="lic-program-dropdown",
                                                                                                    placeholder="Select program ...",
                                                                                                    persistence=True,
                                                                                                    clearable=False,
                                                                                                    # disabled=True,
                                                                                                ),
                                                                                    ],
                                                                                ),
                                                                                dbc.Col(
                                                                                    children=[
                                                                                        html.B(
                                                                                            "Portfolio"
                                                                                        ),
                                                                                                dcc.Dropdown(
                                                                                                    id="lic-portfolio-dropdown",
                                                                                                    placeholder="Select portfolio ...",
                                                                                                    persistence=True,
                                                                                                    clearable=False,
                                                                                                    # disabled=True,
                                                                                                ),
                                                                                    ],
                                                                                ),
                                                                                dbc.Col(
                                                                                    children=[
                                                                                        html.B(
                                                                                            "Method"
                                                                                        ),
                                                                                                dcc.Dropdown(
                                                                                                    id="lic-method-dropdown",
                                                                                                    placeholder="Select method ...",
                                                                                                    persistence=True,
                                                                                                    clearable=False,
                                                                                                    # disabled=True,
                                                                                                ),
                                                                                    ],
                                                                                ),
                                                                                dbc.Col([
                                                                                    html.B("Dev Period Position"),
                                                                                    dcc.RangeSlider(id='lic-slider-dev', min=1, max=2, step=1)
                                                                                ]
                                                                                ),
                                                                                dbc.Col([
                                                                                    html.B("Origin Period Position"),
                                                                                    dcc.RangeSlider(id='lic-slider-origin', min=1, max=2, step=1)
                                                                                ]
                                                                                ),
                                                                            ],
                                                                        ),
                                                                        dbc.Row(
                                                                            [
                                                                                dbc.Col(
                                                                                    children=[
                                                                                        html.B(
                                                                                            "Section"
                                                                                        ),
                                                                                                dcc.Dropdown(
                                                                                                    id="lic-section-dropdown",
                                                                                                    placeholder="Select option ...",
                                                                                                    persistence=True,
                                                                                                    clearable=False,
                                                                                                ),
                                                                                    ],
                                                                                ),
                                                                                dbc.Col(
                                                                                    children=[
                                                                                        html.B("Type"),
                                                                                                dcc.Dropdown(
                                                                                                    id="lic-type-dropdown",
                                                                                                    placeholder="Select option ...",
                                                                                                    persistence=True,
                                                                                                    clearable=False,
                                                                                                    options=[]
                                                                                                ),
                                                                                    ],
                                                                                ),
                                                                                dbc.Col(
                                                                                    children=[
                                                                                        html.B("Output"),
                                                                                                dcc.Dropdown(
                                                                                                    id="lic-component-dropdown",
                                                                                                    placeholder="Select output ...",
                                                                                                    persistence=True,
                                                                                                    clearable=False,
                                                                                                    options=[]
                                                                                                ),
                                                                                    ],
                                                                                ),
                                                                                dbc.Col(
                                                                                    children=[
                                                                                        html.B("Date"),
                                                                                                dcc.Dropdown(
                                                                                                    id="lic-date-dropdown",
                                                                                                    placeholder="Select output type ...",
                                                                                                    persistence=True,
                                                                                                    clearable=False,
                                                                                                ),
                                                                                    ],
                                                                                ),
                                                                                dbc.Col(
                                                                                    children=[
                                                                                        dbc.Button(
                                                                                            "Show Results",
                                                                                            id="lic-apply-button",
                                                                                            className="me-2",
                                                                                            n_clicks=0,
                                                                                            style={
                                                                                                "height": "57%",
                                                                                                "width": "100%",
                                                                                                "margin-top": "24px",
                                                                                            },
                                                                                        ),
                                                                                    ],
                                                                                )
                                                                            ]
                                                                        )
                                                                    ],
                                                                ),
                                                                        ],
                                                                ),
                                                            ],
                                                        ),
                                                        dcc.Loading(
                                                            type="dot",
                                                            color="#2741BC",
                                                            debug=False,
                                                            children=[
                                                        dbc.AccordionItem(
                                                            item_id="acc-chart",
                                                            title="Chart",
                                                            children=[
                                                                    dcc.Graph(
                                                                        config={
                                                                            "displaylogo": False
                                                                        },
                                                                        id="ult-development-factors-chart",
                                                                    ),
                                                                    html.Div(
                                                                        id="data-chart",
                                                                        children=[
                                                                            html.Div(
                                                                                className="text-center",
                                                                                style={
                                                                                    "display": "flex",
                                                                                    "justify-content": "center",
                                                                                    "align-items": "center",
                                                                                    # "height": "50vh",
                                                                                },
                                                                                #children="No chart to display. Please populate filters and click Show Results.",
                                                                                children="",
                                                                            ),
                                                                        ],
                                                                    ),
                                                            ],
                                                        ),
                                                            ],
                                                        ),
                                                        dcc.Loading(
                                                            type="dot",
                                                            color="#2741BC",
                                                            debug=False,
                                                            children=[
                                                        dbc.AccordionItem(
                                                            item_id="acc-data",
                                                            title="Data",
                                                            children=[
                                                                dash_table.DataTable(
                                                                    id="ult-development-factors-table",
                                                                    export_format="xlsx",
                                                                    style_table=
                                                                        {
                                                                            "overflowX": "auto",
                                                                            "minWidth": "100%",
                                                                            "maxWidth": "100%",
                                                                            "width": "100%",
                                                                            "maxHeight": "700px",
                                                                            "height": "300px",
                                                                        },
                                                                    style_data_conditional=[
                                                                        {'if': {'column_id': 'Origin'},
                                                                         'backgroundColor': '#d4dcfb',
                                                                         'color': '#3759cd',
                                                                         'fontWeight': 'bold',
                                                                         'textAlign': 'center',
                                                                         },
                                                                        {'if': {'column_id': 'Stats (Post-Outlier)'},
                                                                         'backgroundColor': '#d4dcfb',
                                                                         'color': '#3759cd',
                                                                         'fontWeight': 'bold',
                                                                         'textAlign': 'center',
                                                                         },
                                                                        {'if': {'column_id': 'Stats (Pre-Outlier)'},
                                                                         'backgroundColor': '#d4dcfb',
                                                                         'color': '#3759cd',
                                                                         'fontWeight': 'bold',
                                                                         'textAlign': 'center',
                                                                         },
                                                                    ],
                                                                    merge_duplicate_headers=True,
                                                                    cell_selectable=False,
                                                                ),
                                                                html.Div(
                                                                id="raw-data",
                                                                children=[
                                                                    html.Div(
                                                                        className="text-center",
                                                                        style={
                                                                            "display": "flex",
                                                                            "justify-content": "center",
                                                                            "align-items": "center",
                                                                            # "height": "50vh",
                                                                        },
                                                                        children="No data to display. Please populate filters and click Show Results.",
                                                                    ),
                                                                ],
                                                            ),
                                                            ],
                                                        ),
                                                                ],
                                                        ),
                                                    ],
                                                ), #end of accordion
                                            ], #tab childrens
                                    ), #tab close
                                    dbc.Tab(
                                        id="lrc-fit-tab",
                                        label="LRC Fit Model",
                                        tab_class_name="unactive-tab",
                                        label_class_name="unactive-tab-label",
                                        active_tab_class_name="active-tab",
                                        active_label_class_name="active-tab-label",
                                        disabled=True,
                                        children=[
                                            dbc.Accordion(
                                                id="controllers-lrc-fit",
                                                start_collapsed=False,
                                                always_open=True,
                                                active_item="acc-lrc-fit-filters",
                                                children=[
                                                    dbc.AccordionItem(
                                                        item_id="acc-lrc-fit-filters",
                                                        title="Filters",
                                                        children=[
                                                            dcc.Loading(
                                                                type="dot",
                                                                color="#2741BC",
                                                                children=[
                                                                    html.Div(
                                                                        children=[
                                                                            dbc.Row(
                                                                                children=[
                                                                                    dbc.Col(
                                                                                        children=[
                                                                                            html.B(
                                                                                                "Program"
                                                                                            ),
                                                                                            dcc.Dropdown(
                                                                                                id="lrc-fit-program-dropdown",
                                                                                                placeholder="Select program ...",
                                                                                                persistence=True,
                                                                                                clearable=False,
                                                                                                # disabled=True,
                                                                                            ),
                                                                                        ],
                                                                                    ),
                                                                                    dbc.Col(
                                                                                        children=[
                                                                                            html.B(
                                                                                                "Portfolio"
                                                                                            ),
                                                                                            dcc.Dropdown(
                                                                                                id="lrc-fit-portfolio-dropdown",
                                                                                                placeholder="Select portfolio ...",
                                                                                                persistence=True,
                                                                                                clearable=False,
                                                                                                # disabled=True,
                                                                                            ),
                                                                                        ],
                                                                                    ),
                                                                                    dbc.Col(
                                                                                        children=[
                                                                                            html.B(
                                                                                                "Method"
                                                                                            ),
                                                                                            dcc.Dropdown(
                                                                                                id="lrc-fit-method-dropdown",
                                                                                                placeholder="Select method ...",
                                                                                                persistence=True,
                                                                                                clearable=False,
                                                                                                # disabled=True,
                                                                                            ),
                                                                                        ],
                                                                                    ),
                                                                                    dbc.Col([
                                                                                        html.B("Dev Period Position"),
                                                                                        dcc.RangeSlider(id='lrc-fit-slider-dev', min=1, max=2, step=1)
                                                                                    ]
                                                                                    ),
                                                                                    dbc.Col([
                                                                                        html.B("Origin Period Position"),
                                                                                        dcc.RangeSlider(id='lrc-fit-slider-origin', min=1, max=2, step=1)
                                                                                    ]
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                            dbc.Row(
                                                                                [
                                                                                    dbc.Col(
                                                                                        children=[
                                                                                            html.B(
                                                                                                "Model"
                                                                                            ),
                                                                                            dcc.Dropdown(
                                                                                                id="lrc-fit-model-dropdown",
                                                                                                placeholder="Select model ...",
                                                                                                persistence=True,
                                                                                                clearable=False,
                                                                                            ),
                                                                                        ],
                                                                                    ),
                                                                                    dbc.Col(
                                                                                        children=[
                                                                                            html.B("Distribution"),
                                                                                            dcc.Dropdown(
                                                                                                id="lrc-fit-distribution-dropdown",
                                                                                                placeholder="Select distribution ...",
                                                                                                persistence=True,
                                                                                                clearable=False,
                                                                                                options=[]
                                                                                            ),
                                                                                        ],
                                                                                    ),
                                                                                    dbc.Col(
                                                                                        children=[
                                                                                            html.B("Variable"),
                                                                                            dcc.Dropdown(
                                                                                                id="lrc-fit-variable-dropdown",
                                                                                                placeholder="Select variable ...",
                                                                                                persistence=True,
                                                                                                clearable=False,
                                                                                                options=[]
                                                                                            ),
                                                                                        ],
                                                                                    ),
                                                                                    dbc.Col(
                                                                                        children=[
                                                                                            html.B("Date"),
                                                                                            dcc.Dropdown(
                                                                                                id="lrc-fit-date-dropdown",
                                                                                                placeholder="Select output type ...",
                                                                                                persistence=True,
                                                                                                clearable=False,
                                                                                            ),
                                                                                        ],
                                                                                    ),
                                                                                    dbc.Col(
                                                                                        children=[
                                                                                            dbc.Button(
                                                                                                "Show Results",
                                                                                                id="lrc-fit-apply-button",
                                                                                                className="me-2",
                                                                                                n_clicks=0,
                                                                                                style={
                                                                                                    "height": "57%",
                                                                                                    "width": "100%",
                                                                                                    "margin-top": "24px",
                                                                                                },
                                                                                            ),
                                                                                        ],
                                                                                    )
                                                                                ]
                                                                            )
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    dcc.Loading(
                                                        type="dot",
                                                        color="#2741BC",
                                                        debug=False,
                                                        children=[
                                                            dbc.AccordionItem(
                                                                item_id="lrc-fit-acc-chart",
                                                                title="Chart",
                                                                children=[
                                                                    html.Div(
                                                                        id="lrc-fit-data-chart",
                                                                        children=[
                                                                            html.Div(
                                                                                className="text-center",
                                                                                style={
                                                                                    "display": "flex",
                                                                                    "justify-content": "center",
                                                                                    "align-items": "center",
                                                                                    # "height": "50vh",
                                                                                },
                                                                                children="No chart to display. Please populate filters and click Show Results.",
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    dcc.Loading(
                                                        type="dot",
                                                        color="#2741BC",
                                                        debug=False,
                                                        children=[
                                                            dbc.AccordionItem(
                                                                item_id="lrc-fit-acc-data",
                                                                title="Data",
                                                                children=html.Div(
                                                                    id="lrc-fit-raw-data",
                                                                    children=[
                                                                        html.Div(
                                                                            className="text-center",
                                                                            style={
                                                                                "display": "flex",
                                                                                "justify-content": "center",
                                                                                "align-items": "center",
                                                                                # "height": "50vh",
                                                                            },
                                                                            children="No data to display. Please populate filters and click Show Results.",
                                                                        ),
                                                                    ],
                                                                ),
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),  # end of accordion
                                        ],  # tab childrens
                                    ),
                                    dbc.Tab(
                                        id="lrc-eval-tab",
                                        label="LRC Eval Model",
                                        tab_class_name="unactive-tab",
                                        label_class_name="unactive-tab-label",
                                        active_tab_class_name="active-tab",
                                        active_label_class_name="active-tab-label",
                                        disabled=True,
                                        children=[
                                            dbc.Accordion(
                                                id="controllers-lrc-eval",
                                                start_collapsed=False,
                                                always_open=True,
                                                active_item="acc-lrc-eval-filters",
                                                children=[
                                                    dbc.AccordionItem(
                                                        item_id="acc-lrc-eval-filters",
                                                        title="Filters",
                                                        children=[
                                                            dcc.Loading(
                                                                type="dot",
                                                                color="#2741BC",
                                                                children=[
                                                                    html.Div(
                                                                        children=[
                                                                            dbc.Row(
                                                                                children=[
                                                                                    dbc.Col(
                                                                                        children=[
                                                                                            html.B(
                                                                                                "Program"
                                                                                            ),
                                                                                            dcc.Dropdown(
                                                                                                id="lrc-eval-program-dropdown",
                                                                                                placeholder="Select program ...",
                                                                                                persistence=True,
                                                                                                clearable=False,
                                                                                                # disabled=True,
                                                                                            ),
                                                                                        ],
                                                                                    ),
                                                                                    dbc.Col(
                                                                                        children=[
                                                                                            html.B(
                                                                                                "Portfolio"
                                                                                            ),
                                                                                            dcc.Dropdown(
                                                                                                id="lrc-eval-portfolio-dropdown",
                                                                                                placeholder="Select portfolio ...",
                                                                                                persistence=True,
                                                                                                clearable=False,
                                                                                                # disabled=True,
                                                                                            ),
                                                                                        ],
                                                                                    ),
                                                                                    dbc.Col(
                                                                                        children=[
                                                                                            html.B(
                                                                                                "Method"
                                                                                            ),
                                                                                            dcc.Dropdown(
                                                                                                id="lrc-eval-method-dropdown",
                                                                                                placeholder="Select method ...",
                                                                                                persistence=True,
                                                                                                clearable=False,
                                                                                                # disabled=True,
                                                                                            ),
                                                                                        ],
                                                                                    ),
                                                                                    dbc.Col([
                                                                                        html.B("Dev Period Position"),
                                                                                        dcc.RangeSlider(id='lrc-eval-slider-dev', min=1, max=2, step=1)
                                                                                    ]
                                                                                    ),
                                                                                    dbc.Col([
                                                                                        html.B("Origin Period Position"),
                                                                                        dcc.RangeSlider(id='lrc-eval-slider-origin', min=1, max=2, step=1)
                                                                                    ]
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                            dbc.Row(
                                                                                [
                                                                                    dbc.Col(
                                                                                        children=[
                                                                                            html.B(
                                                                                                "Model"
                                                                                            ),
                                                                                            dcc.Dropdown(
                                                                                                id="lrc-eval-model-dropdown",
                                                                                                placeholder="Select model ...",
                                                                                                persistence=True,
                                                                                                clearable=False,
                                                                                            ),
                                                                                        ],
                                                                                    ),
                                                                                    dbc.Col(
                                                                                        children=[
                                                                                            html.B("Section"),
                                                                                            dcc.Dropdown(
                                                                                                id="lrc-eval-section-dropdown",
                                                                                                placeholder="Select section ...",
                                                                                                persistence=True,
                                                                                                clearable=False,
                                                                                                options=[]
                                                                                            ),
                                                                                        ],
                                                                                    ),
                                                                                    dbc.Col(
                                                                                        children=[
                                                                                            html.B("Output"),
                                                                                            dcc.Dropdown(
                                                                                                id="lrc-eval-component-dropdown",
                                                                                                placeholder="Select output ...",
                                                                                                persistence=True,
                                                                                                clearable=False,
                                                                                                options=[]
                                                                                            ),
                                                                                        ],
                                                                                    ),
                                                                                    dbc.Col(
                                                                                        children=[
                                                                                            html.B("Date"),
                                                                                            dcc.Dropdown(
                                                                                                id="lrc-eval-date-dropdown",
                                                                                                placeholder="Select output type ...",
                                                                                                persistence=True,
                                                                                                clearable=False,
                                                                                            ),
                                                                                        ],
                                                                                    ),
                                                                                    dbc.Col(
                                                                                        children=[
                                                                                            dbc.Button(
                                                                                                "Show Results",
                                                                                                id="lrc-eval-apply-button",
                                                                                                className="me-2",
                                                                                                n_clicks=0,
                                                                                                style={
                                                                                                    "height": "57%",
                                                                                                    "width": "100%",
                                                                                                    "margin-top": "24px",
                                                                                                },
                                                                                            ),
                                                                                        ],
                                                                                    )
                                                                                ]
                                                                            )
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    dcc.Loading(
                                                        type="dot",
                                                        color="#2741BC",
                                                        debug=False,
                                                        children=[
                                                            dbc.AccordionItem(
                                                                item_id="lrc-eval-acc-chart",
                                                                title="Chart",
                                                                children=[
                                                                    html.Div(
                                                                        id="lrc-eval-data-chart",
                                                                        children=[
                                                                            html.Div(
                                                                                className="text-center",
                                                                                style={
                                                                                    "display": "flex",
                                                                                    "justify-content": "center",
                                                                                    "align-items": "center",
                                                                                    # "height": "50vh",
                                                                                },
                                                                                children="No chart to display. Please populate filters and click Show Results.",
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                    dcc.Loading(
                                                        type="dot",
                                                        color="#2741BC",
                                                        debug=False,
                                                        children=[
                                                            dbc.AccordionItem(
                                                                item_id="lrc-eval-acc-data",
                                                                title="Data",
                                                                children=html.Div(
                                                                    id="lrc-eval-raw-data",
                                                                    children=[
                                                                        html.Div(
                                                                            className="text-center",
                                                                            style={
                                                                                "display": "flex",
                                                                                "justify-content": "center",
                                                                                "align-items": "center",
                                                                                # "height": "50vh",
                                                                            },
                                                                            children="No data to display. Please populate filters and click Show Results.",
                                                                        ),
                                                                    ],
                                                                ),
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),  # end of accordion
                                        ],  # tab childrens
                                    ),
                                    ],
                            ),
                        ],
                    ),
                ],
            ),
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
