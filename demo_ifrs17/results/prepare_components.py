#demo_ifrs/results/prepare_components.py

import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html
import plotly.express as px
import math

from cm_dashboards.demo_ifrs17.config.config import cache, timeout
import cm_dashboards.demo_ifrs17.layout.component_styles as styles
import cm_dashboards.demo_ifrs17.layout.component_styles as styles

import logging

logger = logging.getLogger(__name__)


@cache.memoize(timeout=timeout)
def return_filter_indicators(filtered_gocs):
    style = {"height":"25px",'font-size': 12,'display':'inline-block','padding-top':'1px'}
    color = "primary"
    cn = "g-1"
    components = []

    for item in filtered_gocs:
        if item.get('value') not in ["Off",None]:
            components.append(dbc.Alert(f"{item.get('model')} {item.get('group')}: {item.get('value')}", color=color, className=cn, style=style))

    return components

# PREVIOUS VERSION BASED ON SESSION DATA ELEMENTS
# @cache.memoize(timeout=timeout)
# def return_filter_indicators(filtered_gocs):
#     style = {"height":"25px",'font-size': 12,'display':'inline-block','padding-top':'1px'}
#     color = "primary"
#     cn = "g-1"
#     components = []
#
#     for item in filtered_gocs:
#         if item.get('Value') != "Off":
#             components.append(dbc.Alert(f"{item.get('Model')} {item.get('GoC')}: {item.get('Value')}", color=color, className=cn, style=style))
#
#     return components

def generate_disclosure_accordions (dictionary, master_groups):
    ret_components = []
    data_items = []
    title = ""
    data_template = {}
    for record in dictionary:
        if record.get('Record_Type') == 'HEADER_01':
            title = record.get('Description')
        else:
            data = {"Record_Type": record['Record_Type'], "RNA Disc Code": record['RNA_Disc_Code'], "Item": record['Description']}
            values = record['Value']
            if values and values != '0':
                for key in values.keys():
                    data[key] = values[key]
            else:
                for group in master_groups:
                    data[group] = "-"
            data_template = data
            data_items.append(data)

    columns = [{'name': 'Record_Type', 'id': 'Record_Type'},
               {'name': 'RNA Disc Code', 'id': 'RNA Disc Code'},
               {'name': 'Item', 'id': 'Item'},
               ]

    for grp_filtered in master_groups:
        columns.append({'name': str(grp_filtered), 'id': str(grp_filtered)})

    ret_components.append(dbc.AccordionItem([
        dash_table.DataTable(data=data_items,
                          columns = columns,
                          style_table={'overflowX': 'scroll'},
                          style_header_conditional=styles.cond_style_header_disc_table,
                          style_data_conditional=styles.disclosure_cond_style)],
        title=title, className="ms-auto"))

    return ret_components


def breakdown_gen_presentation(data, master_groups):
    presentation = []
    components_list = []
    title = ""
    columns = [{'name': 'Item', 'id': 'Item'}, ]

    for grp_filtered in master_groups:
        grp = "AGG. ALL" if grp_filtered == "Value" else grp_filtered
        columns.append({'name': str(grp), 'id': str(grp_filtered)})

    for record in data:
        if record.get('record_type') == "01_HEADER":
            if title != "" and len(presentation) > 0:
                components_list = create_summary_reverse(title, presentation, columns, components_list)
                presentation = []
            title = record.get('description')
        else:
            line = {"BS Code": record['RNA BS Code'], "Item": record['description']}
            dict = record['value']
            if dict:
                for key in dict.keys():
                    # new_key = "AGG. ALL" if key == "Value" else key
                    if dict[key] != "":
                        line[key] = math.trunc(dict[key])
                    else:
                        line[key] = ""
                    # multiplier = 10 ** 2
                    # line[key] = int(dict[key] * multiplier) / multiplier
                    # line[key] = math.trunc(dict[key])
                    # GOOD line[key] = dict[key]
            else:
                for group in master_groups:
                    line[group] = "-"
            presentation.append(line)

    components_list = create_summary_reverse(title, presentation, columns, components_list)

    return components_list


def netall_gen_presentation(data, master_groups):
    presentation = []
    components_list = []
    title = ""
    columns = [{'name': 'Item', 'id': 'Item'}, ]

    for grp_filtered in master_groups:
        grp = "AGG. ALL" if grp_filtered == "Value" else grp_filtered
        columns.append({'name': str(grp), 'id': str(grp_filtered)})

    for record in data:
        if record.get('Record_Type') == "01_HEADER":
            if title != "" and len(presentation) > 0:
                components_list = create_summary_reverse(title, presentation, columns, components_list)
                presentation = []
            title = record.get('Description')
        else:
            line = {"RNA_Disc_Code": record['RNA_Disc_Code'], "Item": record['Description']}
            dict = record['Value']
            if dict:
                for key in dict.keys():
                    # new_key = "AGG. ALL" if key == "Value" else key
                    if dict[key] != "":
                        line[key] = math.trunc(dict[key])
                    else:
                        line[key] = ""
                    # multiplier = 10 ** 2
                    # line[key] = int(dict[key] * multiplier) / multiplier
                    # line[key] = math.trunc(dict[key])
                    # GOOD line[key] = dict[key]
            else:
                for group in master_groups:
                    line[group] = "-"
            presentation.append(line)

    components_list = create_summary_reverse(title, presentation, columns, components_list)

    return components_list


def generate_disclosures_sums (dictionary, master_groups, components_list):
    ret_components = []
    data_items = []
    title = ""

    columns = [{'name': 'Item', 'id': 'Item'},]

    for grp_filtered in master_groups:
        grp = "AGG. ALL" if grp_filtered == "Value" else grp_filtered
        columns.append({'name': str(grp), 'id': str(grp_filtered)})

    for record in dictionary:
        if record.get('Record_Type') == 'HEADER_01':
            title = record.get('Description')
        else:
            data = {"Record_Type": record['Record_Type'], "RNA Disc Code": record['RNA_Disc_Code'], "Item": record['Description']}
            values = record['Value']
            if values and values != '0':
                for key in values.keys():
                    data[key] = round(values[key],14)
            else:
                for group in master_groups:
                    data[group] = "-"
            data_template = data
            data_items.append(data)

    ret_components = create_summary(title, data_items, columns, components_list)

    return ret_components

def create_summary_reverse (title, data, columns, components_list):
    new_summary  = []
    childs = []
    childs.append(html.Summary(title, style=styles.label_style_disc))
    childs.append(dash_table.DataTable(data=data,
                  columns=columns,
                  style_table={'overflowX': 'auto','overflowY': 'auto'}, #, 'display': 'block'},
                  # style_header_conditional=cond_style_header_disc_table,
                  style_data={'textAlign': 'center'},
                  style_data_conditional=styles.disclosure_cond_style,
                  export_format="xlsx",
                  export_headers='display',
                  export_columns='visible',
                  cell_selectable=True,
                  #fixed_rows={'headers': True, 'data': 0},
                  include_headers_on_copy_paste=True
                  # hidden_columns=['Record_Type']
                  ))
    new_summary.append(html.Hr())
    new_summary.append(html.Details(children=childs))

    returned = components_list
    returned.extend(new_summary)

    return returned


def create_summary (title, data, columns, components_list):
    new_summary  = []
    childs = []
    childs.append(html.Summary(title, style=styles.label_style_disc))
    childs.append(dash_table.DataTable(data=data,
                  columns=columns,
                  style_table={'overflowX': 'auto','overflowY': 'auto'}, #, 'display': 'block'},
                  # style_header_conditional=cond_style_header_disc_table,
                  style_data={'textAlign': 'center'},
                  style_data_conditional=styles.disclosure_cond_style,
                  export_format="xlsx",
                  export_headers='display',
                  export_columns='visible',
                  cell_selectable=True,
                  #fixed_rows={'headers': True, 'data': 0},
                  include_headers_on_copy_paste=True
                  # hidden_columns=['Record_Type']
                  ))
    new_summary.append(html.Hr())
    new_summary.append(html.Details(children=childs))

    new_summary.extend(components_list)

    return new_summary


def generate_disclosure_summaries2 (dictionary, master_groups):
    ret_components = []
    data_items = []
    title = ""
    data_template = {}
    for record in dictionary:
        if record.get('Record_Type') == 'HEADER_01':
            title = record.get('Description')
        else:
            data = {"Record_Type": record['Record_Type'], "RNA Disc Code": record['RNA_Disc_Code'], "Item": record['Description']}
            values = record['Value']
            if values and values != '0':
                for key in values.keys():
                    data[key] = round(values[key],14)
            else:
                for group in master_groups:
                    data[group] = "-"
            data_template = data
            data_items.append(data)

    # columns = [{'name': 'Record_Type', 'id': 'Record_Type', 'hidden': True},
    #            {'name': 'RNA Disc Code', 'id': 'RNA Disc Code', 'hidden': True},
    #            {'name': 'Item', 'id': 'Item'},
    #            ]

    columns = [
               {'name': 'Item', 'id': 'Item'},
               ]

    for grp_filtered in master_groups:
        columns.append({'name': str(grp_filtered), 'id': str(grp_filtered)})


    # first_key = {}
    # first_key = next(iter(data_items[0]))
    #
    # for k in first_key.keys():
    #     logger.debug(k)

    ret_components.append(html.Hr())
    ret_components.append(html.Details(children=[html.Summary(title, style=styles.label_style_disc),
                                                             dash_table.DataTable(data=data_items,
                                                                                  columns = columns,
                                                                                  style_table={'overflowX': 'auto'},
                                                                                  #style_header_conditional=cond_style_header_disc_table,
                                                                                  style_data={'textAlign':'center'},
                                                                                  style_data_conditional=styles.disclosure_cond_style,
                                                                                  export_format="xlsx",
                                                                                  export_headers='display',
                                                                                  export_columns='visible',
                                                                                  cell_selectable=True,
                                                                                  fixed_rows={'headers':True, 'data':0},
                                                                                  include_headers_on_copy_paste=True
                                                                                  #hidden_columns=['Record_Type']
                                                                                  )
                                                             ]))
    return ret_components

def generate_disclosure_summaries (dictionary, master_groups):
    ret_components = []
    sub_components = []
    data_items = []
    title = ""
    subtitle = ""
    tempo_data = None

    columns = [
               {'name': 'Item', 'id': 'Item'},
               ]
    for grp_filtered in master_groups:
        columns.append({'name': str(grp_filtered), 'id': str(grp_filtered)})


    for record in dictionary:
        if record.get('Record_Type') == 'HEADER_01':
            title = record.get('Description')
        elif record.get('Record_Type') == 'Sub_Header2':
            subtitle = record.get('Description')
            if data_items:
                logger.debug("compose subsection")
                sub_components.append(html.Details(children=[html.Summary(subtitle, style=styles.label_style_disc2),
                                                             dash_table.DataTable(data=data_items,
                                                                                  columns=columns,
                                                                                  style_table={'overflowX': 'auto'},
                                                                                  # style_header_conditional=cond_style_header_disc_table,
                                                                                  style_data={'textAlign': 'center'},
                                                                                  style_data_conditional=styles.disclosure_cond_style,
                                                                                  export_format="xlsx",
                                                                                  export_headers='display',
                                                                                  export_columns='visible',
                                                                                  cell_selectable=True,
                                                                                  fixed_rows={'headers': True, 'data': 0},
                                                                                  include_headers_on_copy_paste=True
                                                                                  # hidden_columns=['Record_Type']
                                                                                  )
                                                             ]))
                data_items = []
        else:
            tempo_data = {"Record_Type": record['Record_Type'], "RNA Disc Code": record['RNA_Disc_Code'], "Item": record['Description']}
            values = record['Value']
            if values and values != '0':
                for key in values.keys():
                    tempo_data[key] = round(values[key],14)
            else:
                for group in master_groups:
                    tempo_data[group] = "-"
            data_items.append(tempo_data)

    ret_components.append(html.Hr())

    if data_items and title != "":
        sub_child = []
        sub_child.append(html.Summary(title, style=styles.label_style_disc))
        sub_child.append(dash_table.DataTable(data=data_items,
                          columns=columns,
                          style_table={'overflowX': 'auto'},
                          # style_header_conditional=cond_style_header_disc_table,
                          style_data={'textAlign': 'center'},
                          style_data_conditional=styles.disclosure_cond_style,
                          export_format="xlsx",
                          export_headers='display',
                          export_columns='visible',
                          cell_selectable=True,
                          fixed_rows={'headers': True, 'data': 0},
                          include_headers_on_copy_paste=True
                          # hidden_columns=['Record_Type']
                          ))
        for s in sub_components:
            sub_child.append(s)
        ret_components.append(html.Details(children=sub_child))

    logger.debug(ret_components)
    return ret_components


def generate_bs_summary (dictionary, title):
    cols = []
    # data_items = []
    # first_key = next(iter(dictionary))
    # for k in first_key:
    #     cols.append(k)

    ret_components = []
    ret_components.append(html.Hr())
    ret_components.append(html.Details(children=[html.Summary(str(title), style=styles.label_style_disc),
                                                             dash_table.DataTable(data=dictionary,
                                                                                  style_table={'overflowX': 'auto'},
                                                                                  style_header_conditional=styles.cond_style_header_disc_table,
                                                                                  style_data_conditional=styles.disclosure_cond_style,)
                                                             ]))
    return ret_components


def create_pie_chart(
    df, names: str, values: str, size_width, size_height, color_schema: dict, margin=None, text_size=15
):
    """
    Create pie chart object
    :param df: data to be used for chart creation
    :param names: Data names to be used for chart creation
    :param values: Data values to be used for chart creation
    :param title: Title of the chart
    :param color_schema: List of color values
    :param margin: Margin to be used to update the chart (optional)
    :param text_size: Text size for chart (optional)
    :return chart: chart object
    """
    # Default margin
    if margin is None:
        margin = dict(l=1, r=1, t=1, b=1)
        #margin = dict(l=0, r=0, t=0, b=0)


    chart = px.pie(
        data_frame=df,
        names=names,
        values=values,
        #color_discrete_sequence=px.colors.sequential.Blues_r,
        color_discrete_sequence=color_schema,
        width=size_width,
        height=size_height
    )
    chart.update_traces(
        textposition="inside",
        textinfo="percent+label",
        textfont=dict(
            family="sans serif 'Nunito Sans'", size=text_size, color="#FFFFFF"
        ),
        hovertemplate="<br>Percentage: %{percent}<extra></extra>",
    )
    # Apply white border to pie chart
    chart.update_traces(marker=dict(line=dict(color="#FFFFFF", width=1)), sort=False)

    # Update legend position
    chart.update_layout(
        margin=margin,
        legend=dict(orientation="v", x=1.2, y=0.5),
    )
    return chart


def generate_key_summary (disc_key_value):
    if not disc_key_value:
        return None

    columns = [{'name': 'Statement of Profit & Loss', 'id': 'Item'},{'name': 'AGG. ALL', 'id': 'aggall'}]

    data = []

    key_results = ["Net_D.PL.1", "Net_D.PL.1.1", "Net_D.PL.1.2", "Net_D.PL.1.3", "Net_D.PL.2", "Net_D.PL.2.1",
                   "Net_D.PL.2.2", "Net_D.PL.2.3", "Net_D.PL.3", "Net_D.PL.4", "Net_D.PL.5", "Net_D.PL.6"]

    key_descriptions = ["Insurance service result",
    "Insurance revenue",
    "Insurance service expense",
    "Net income or expense from reinsurance contracts held",
    "Financial insurance result",
    "Investment income",
    "Insurance finance expenses",
    "Reinsurance finance income",
    "Other income and expense",
    "Income tax",
    "PROFIT BEFORE TAX",
    "PROFIT AFTER TAX"]

    for key, description in zip(key_results, key_descriptions):
        tempo = disc_key_value.get(key)
        if tempo:
            data.append({"Item": description, "aggall": tempo.get('AGG. ALL')})

    return_table = dash_table.DataTable(data=data,
                         columns=columns,
                         style_table={'overflowX': 'auto'},
                         # style_header_conditional=cond_style_header_disc_table,
                         style_data={'textAlign': 'center'},
                         style_data_conditional=styles.disclosure_cond_style,
                         export_format="xlsx",
                         export_headers='display',
                         export_columns='visible',
                         cell_selectable=True,
                         include_headers_on_copy_paste=True
                         # hidden_columns=['Record_Type']
                         )

    return return_table


def generate_key_openings (disc_key_value):
    if not disc_key_value:
        return None


    columns = [{'name': 'Item', 'id': 'Item'},{'name': 'OPENING (current rates)', 'id': 'opening'},{'name': 'CLOSING (current rates)', 'id': 'closing'}]

    data = []

    key_descriptions = ["Insurance Contract Liability",
                        "LRC  (Excl. LC/LR or CSM)",
                        "LRC CSM",
                        "LRC  (Loss Component)",
                        "LRC  (Loss Recovery Component)",
                        "Liability for Incurred Claim"]

    #key_openings = ["Net_D.ICL_A.1", "Net_D.LRC_A.1", "Net_D.CSM_B.1", "Net_D.LC_A.1", "Net_D.LR_A.1", "Net_D.LIC_A.1"]
    key_openings = ["Net_D.ICL_A.1", "Net_D.LRC_A.1-Net_D.CSM_B.1", "Net_D.CSM_B.1", "Net_D.LC_A.1", "Net_D.LR_A.1", "Net_D.LIC_A.1"]
    #key_closings = ["Net_D.ICL_A.6", "Net_D.LRC_A.6", "Net_D.CSM_B.6", "Net_D.LC_A.6", "Net_D.LR_A.6", "Net_D.LIC_A.6"]
    key_closings = ["Net_D.ICL_A.6", "Net_D.LRC_A.6-Net_D.CSM_B.6", "Net_D.CSM_B.6", "Net_D.LC_A.6", "Net_D.LR_A.6", "Net_D.LIC_A.6"]

    for desc, opening, closing in zip (key_descriptions, key_openings, key_closings):
        opening_val = ""
        closing_val = ""
        if "-" in opening:
            openings = opening.split("-")
            if len(openings) == 2:
                opening_val = disc_key_value.get(openings[0]).get('AGG. ALL') - disc_key_value.get(openings[1]).get('AGG. ALL')
        else:
            tempo_opening = disc_key_value.get(opening)
            if tempo_opening:
                opening_val = tempo_opening.get('AGG. ALL')

        if "-" in closing:
            closings = closing.split("-")
            closing_val = disc_key_value.get(closings[0]).get('AGG. ALL') - disc_key_value.get(closings[1]).get('AGG. ALL')
        else:
            tempo_closing = disc_key_value.get(closing)
            if tempo_closing:
                closing_val = tempo_closing.get('AGG. ALL')

        data.append({"Item": desc, "opening": opening_val, "closing": closing_val})

    return_table = dash_table.DataTable(data=data,
                         columns=columns,
                         style_table={'overflowX': 'auto'},
                         # style_header_conditional=cond_style_header_disc_table,
                         style_data={'textAlign': 'center'},
                         style_data_conditional=styles.disclosure_cond_style,
                         export_format="xlsx",
                         export_headers='display',
                         export_columns='visible',
                         cell_selectable=True,
                         include_headers_on_copy_paste=True
                         # hidden_columns=['Record_Type']
                         )

    return return_table