import logging

import dash
from flask import json, jsonify, render_template
import json
import time
import pandas as pd

from dash import no_update
from dash.dependencies import Input, Output, State
from cm_dashboards.report_builder.config.config import app

logger = logging.getLogger(__name__)

# @server.route('/dash/ifrs17')
# def index():
#     messages = [{'title': 'Message One',
#                  'content': 'Message One Content'},
#                 {'title': 'Message Two',
#                  'content': 'Message Two Content'}
#                 ]
#     return render_template('"../templates/ifrs17_templates/index.html', messages=messages)
#
@app.callback(
    #Output("body-container", "children", allow_duplicate=True),
    [
    Output("table_variables", "data", allow_duplicate=True),
    Output("table_variables", "columns", allow_duplicate=True),
    ],
    Input("url", "search"),
    prevent_initial_call = True
)
def render_json(url_query_string):
    try:
        #logger.error("query string {]".format(url_query_string))
        logger.debug("query string")
        with open('c:/temp/variables.json', 'r') as myfile:
            data = json.load(myfile)

        df = pd.json_normalize(data)
        df.drop("field_type", axis=1, inplace=True)

        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]

        ret = ""
        for item_list in data:
            logger.debug(item_list["name"])
            ret = ret + str(item_list["name"]) + " "
            # for key in item_list:
            #     logger.debug(key)
            #     logger.debug(item_list[key])
            #logger.debug("The key and value are ({}) = ({})".format(key, value))



        return ret
        #return render_template('templates/index.html', messages=messages)
    except Exception as e:
        logger.error("Error while loading json: {}".format(e))

    return no_update