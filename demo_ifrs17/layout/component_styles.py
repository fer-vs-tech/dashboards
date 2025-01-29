
import dash_bootstrap_components as dbc

subledger_cond_style = [
                            {
                                'if': {
                                    'filter_query': '{Balance} = "TRUE"',
                                    'column_id': 'Balance'
                                },
                                'backgroundColor': '#f5f9ed',
                                'color': '#478778',
                                'fontWeight': 'bold'
                            },
                            {
                                'if': {
                                    'filter_query': '{Change in LIC} != ""',
                                    'column_id': 'Change in LIC'
                                },
                                'backgroundColor': '#f5f9ed',
                                'color': '#478778',
                                'fontWeight': 'bold'
                            },
                            {
                                'if': {
                                    'filter_query': '{Change in PVCF} != ""',
                                    'column_id': 'Change in PVCF'
                                },
                                'backgroundColor': '#f5f9ed',
                                'color': '#478778',
                                'fontWeight': 'bold'
                            },
                            {
                                'if': {
                                    'filter_query': '{Change in RA} != ""',
                                    'column_id': 'Change in RA'
                                },
                                'backgroundColor': '#f5f9ed',
                                'color': '#478778',
                                'fontWeight': 'bold'
                            },
                            {
                                'if': {
                                    'filter_query': '{Change in CSM} != ""',
                                    'column_id': 'Change in CSM'
                                },
                                'backgroundColor': '#f5f9ed',
                                'color': '#478778',
                                'fontWeight': 'bold'
                            },
                            {
                                'if': {
                                    'filter_query': '{Cash This Year (inc Inv Income)} != ""',
                                    'column_id': 'Cash This Year (inc Inv Income)'
                                },
                                'backgroundColor': '#f5f9ed',
                                'color': '#478778',
                                'fontWeight': 'bold'
                            },
                            {
                                'if': {
                                    'filter_query': '{Ins Revenue} != ""',
                                    'column_id': 'Ins Revenue'
                                },
                                'backgroundColor': '#f5f9ed',
                                'color': '#478778',
                                'fontWeight': 'bold'
                            },
                            {
                                'if': {
                                    'filter_query': '{Ins Serv Exp} != ""',
                                    'column_id': 'Ins Serv Exp'
                                },
                                'backgroundColor': '#f5f9ed',
                                'color': '#478778',
                                'fontWeight': 'bold'
                            },
                            {
                                'if': {
                                    'filter_query': '{IFIE, less Inv Income, less other exp} != ""',
                                    'column_id': 'IFIE, less Inv Income, less other exp'
                                },
                                'backgroundColor': '#f5f9ed',
                                'color': '#478778',
                                'fontWeight': 'bold'
                            },
                            {
                                'if': {
                                    'filter_query': '{Change in OCI} != ""',
                                    'column_id': 'Change in OCI'
                                },
                                'backgroundColor': '#f5f9ed',
                                'color': '#478778',
                                'fontWeight': 'bold'
                            },
                        ]


disclosure_cond_style = [
    {
        'if': {
            'filter_query': "{Record_Type}  = 'Item'",
            'column_id': 'Item',
        },
        'textAlign': 'left',
        'textIndent': '30px',
    },
    {
        'if': {
            'filter_query': "{Record_Type}  = 'Item'",
            'column_id': 'Item',
        },
        'textAlign': 'left',
        'textIndent': '30px',
    },
    {
        'if': {
            'filter_query': "{Record_Type}  = 'Sub_Header'",
            'column_id': 'Item'
        },
        'fontWeight': 'bold',
        'fontStyle': 'italic',
        'color': '#00008B',
        'textAlign': 'left',
        'textIndent': '1px',
    },
    {
        'if': {
            'filter_query': "{Record_Type}  = 'Header_Bold'",
            'column_id': 'Item',
        },
        'fontWeight': 'bold',
        'textAlign': 'left',
        'textIndent': '1px',
    },
    {
        'if': {
            'filter_query': "{Record_Type}  = 'Header_Bold'",
        },
        'fontWeight': 'bold',
    },
    {
        'if': {
            'filter_query': "{Record_Type}  = 'Header_Bold_Greyed'",
        },
        'fontWeight': 'bold',
        'textAlign': 'left',
        'backgroundColor': '#f6f4f2',
        'textIndent': '1px',
        #'value': 'x',
    },
    {
        'if': {
            'filter_query': "{Record_Type}  = 'Greyed'",
        },
        'textAlign': 'left',
        'backgroundColor': '#f6f4f2',
        'textIndent': '30px',
        # 'value': 'x',
    },
    # {
    #     'if': {
    #         'column_id': 'Record_Type',
    #     },
    #     'display': 'none'
    # },
    # {
    #     'if': {
    #         'column_id': 'RNA Disc Code',
    #     },
    #     'display': 'none'
    # },
]

report_label = {
                'font-size': 20,
                'color': '#2741BC',
                #'fontWeight': 'bold',
                'maxWidth': 500,
                'width': 500,
}

key_summary_label_style = {
                'font-size': 18,
                'color': '#2741BC',
                'fontWeight': 'bold',
                'maxWidth': 300,
                'width': 300,
}

no_data_yet = {
                'font-size': 14,
                'color': 'grey',
                'fontWeight': 'bold',
                'maxWidth': 300,
                'width': 300,
}

label_style = {
                'font-size': 15,
                'color': '#2741BC',
                'fontWeight': 'bold',
                'maxWidth': 300,
                'width': 300,
}

net_label_style = {
                'font-size': 15,
                'color': '#2741BC',
                'fontWeight': 'bold',
                'maxWidth': 180,
                'width': 180,
}

label_style_disc = {
                'font-size': 13,
                'color': '#2741BC',
                'fontWeight': 'bold',
                'maxWidth': 500,
                'width': 500,
}

label_style_disc2 = {
                'font-size': 13,
                'color': '#2741BC',
                'fontWeight': 'bold',
                'maxWidth': 500,
                'width': 500,
                'textIndent':'30px',
}

label_style_title = {
                'font-size': 20,
                'color': '#2741BC',
                'fontWeight': 'bold',
                'maxWidth': 300,
                'width': 300
}

cond_style_header_disc_table = [
    {
        'if': {
            'column_id': 'Record_Type',
        },
        'display': 'none'
    },
    {
        'if': {
            'column_id': 'RNA Disc Code',
        },
        'display': 'none'
    },
]


label_no_data = dbc.Label("No data produced yet", style=no_data_yet)