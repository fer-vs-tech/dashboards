#demo_ifrs17/layouts/layout.py
import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html

import cm_dashboards.dash_utils as dash_utils

import cm_dashboards.demo_nl.utils.helpers as helpers

def render_content(contents):
    """
    Render dashboards based on the results
    """

    dashboard_details = helpers.dashboards_list()
    # Loop through the results and generate dashboard layout
    results = [dbc.Label(contents)]
    return results


def render_custom_triangle(dashboard_results):
    """
    Render dashboards based on the results
    """
    table_style = {
        "overflowX": "auto",
        "minWidth": "100%",
        "maxWidth": "100%",
        "width": "100%",
        "maxHeight": "500px",
        "height": "300px",
    }

    # Loop through the results and generate dashboard layout
    results = [dash_table.DataTable(
                            id=f"tri-table",
                            data=dashboard_results.to_dict(orient='records'),
                            #columns=dashboard_results[1],
                            #style_data_conditional=dashboard_results[2],
                            style_table=table_style,
                            merge_duplicate_headers=True,
                            cell_selectable=False,
    )]

    return results




def prepare_table_data(
    df,
    header_rows=[],
    hidden_columns=[],
    filter_column_style=None,
    additional_header=[],
    replace_zero=None,
    multi_index=False,
    show_negative_numbers=True,
):
    """
    Prepare table data
    :param df: DataFrame
    :param header_rows: list of header rows
    :param hidden_columns: list of hidden columns
    :return: tuple (data, columns, conditional_style) for dash_table.DataTable
    """
    # Check if replacement is needed
    if replace_zero is not None:
        df = df.replace({0: replace_zero})

    # Set multiindex table data, column if needed
    if multi_index:
        table_data, columns = dash_utils.set_multi_index_column_names(
            df, show_negative_numbers=show_negative_numbers
        )
    else:
        table_data = df.to_dict("records")
        table_columns = df.columns
        columns = dash_utils.set_column_names(
            table_columns,
            precision=0,
            hidden_columns=hidden_columns,
            show_negative_numbers=show_negative_numbers,
            additional_header=additional_header,
        )
    conditional_style = dash_utils.set_table_style_kics(
        columns, show_negative_numbers=show_negative_numbers
    )
    row_style = dash_utils.set_row_style(header_rows)
    style = conditional_style + row_style

    # Add conditional style for filter column
    if filter_column_style is not None:
        result = dash_utils.set_conditional_style_by_filtering(
            column=filter_column_style
        )
        style = style + result

    return table_data, columns, style


def render_error(error_message):
    """
    Render message if error occurred
    """
    return html.Div(
        className="one-half column mixed-table row",
        children=[
            html.Label(id="main-label"),
            html.Br(),
            html.Div(
                className="alert alert-danger",
                role="alert",
                children=[
                    html.P(
                        children=[
                            html.B("Failed to load the data"),
                            html.Br(),
                            html.Span(error_message),
                        ],
                    ),
                ],
            ),
        ],
    )


def render_datatable(results_data):
    """
    Render dashboards based on the results
    """
    table_style = {
        "overflowX": "auto",
        "minWidth": "100%",
        "maxWidth": "100%",
        "width": "100%",
        "maxHeight": "700px",
        "height": "300px",
    }

    results = []
    results.append(
                        dash_table.DataTable(
                            id=f"results-table",
                            data=results_data,
                            style_table=table_style,
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
                ),

    layout = [
        html.Div(
            children=results,
            id="tab-0",
        ),
    # layout = [
    #     dbc.Tabs(
    #         children=results,
    #         active_tab="tab-0",
    #     ),
    ]

    return layout


def render_chart(results_data):
    """
    Render dashboards based on the results
    """
    figurita = helpers.create_line_chart(df=results_data, x="Dev_Period_Position", y="returnValue", color="Origin_Period_Position", title="prueba")

    results = []
    results.append(
        dcc.Graph(id='chart-graph', figure=figurita)
                ),

    layout = [
        html.Div(
            children=results,
            id="tab-1",
        ),
    ]

    return layout


def render_chart_ata(results_data):
    """
    Render dashboards based on the results
    """
    figurita = helpers.create_line_chart_ATA(df=results_data, x="Dev_Period_Position", y=["SIGMA","MEAN", "MU", "VAR"], color="Origin_Period_Position", title="prueba")

    results = []
    results.append(
        dcc.Graph(id='chart-graph', figure=figurita)
                ),

    layout = [
        html.Div(
            children=results,
            id="tab-1",
        ),
    ]

    return layout