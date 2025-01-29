import sys

sys.path.append("..")

import logging

logger = logging.getLogger(__name__)

import datetime
import os
from timeit import default_timer as timer

import pandas as pd
import pyodbc
from lxml import etree

import cm_dashboards.alchemy_db as db
import cm_dashboards.utilities as utilities


def get_wvr_path_from_jobrun_id(jobrun_id):
    """
    Get the full path to the wvr given the jobrun id
    """
    jobrun_root = utilities.get_entry_from_config_file("folders", "jobruns")
    jobrun_name = db.get_jobrun_name_from_id(jobrun_id)
    jobrun_wvr = jobrun_name + ".wvr"
    jobrun_wvr_path = os.path.join(jobrun_root, jobrun_wvr)
    return jobrun_wvr_path


def get_model_name_from_url(url):
    """
    Get model name from URL
    """
    jobrun_root = utilities.get_entry_from_config_file("folders", "jobruns")
    params = utilities.extract_url_params(url)
    jobrun_name = params.get("wvr", [None])[0]
    model_list = model_names_in_jobrun(jobrun_root, jobrun_name)
    return model_list


def model_names_in_jobrun(jobrun_root, jobrun_name):
    wvr_path = os.path.join(jobrun_root, jobrun_name)
    return model_names_in_wvr(wvr_path)


def model_names_in_wvr(wvr_path):
    """
    Get a list of model names in a wvr file
    """
    model_list = []
    runinfo_data = read_output_file(wvr_path)
    try:
        if not runinfo_data:
            raise Exception("No run info data found")
        for runinfo in runinfo_data:
            name = runinfo.get("FullName", "")
            # Get the original Model name, ignoring alias information
            real_name = name.split("'")[1]
            model_list.append(real_name)
        logger.info(f"Model names in WVR: {model_list}")
    except Exception as error:
        logger.error(f"Error while getting model names: {error}")
    finally:
        return model_list


def read_output_file(wvr_path, output_file="RunInfo.xml"):
    """
    Read the output file of a wvr file
    :param wvr_path: path to the wvr file
    :param output_file: name of the output file to read (default: RunInfo.xml)
    :return: list of dictionaries containing the runinfo data
    """
    runinfo_data = None
    try:
        if wvr_path.endswith(".wvr"):
            wvr_path = wvr_path[:-4]
        runinfo_path = os.path.join(wvr_path, "Output", output_file)
        runinfo_xml = None
        with open(runinfo_path, "r", encoding="utf-16") as f:
            runinfo_xml = f.read()
        runinfo_data = parse_xml_to_list(runinfo_xml, output_file)
    except Exception as error:
        logger.error(f"Error while reading RunInfo.xml: {error}")
    finally:
        return runinfo_data


def get_wvr_connection_url(wvr_path, model):
    """
    Get ODBC connection string to a wvr file
    """
    r3s_driver = "DRIVER={R³S Results Driver (*.wvr)};"
    # afm_driver = "DRIVER={Algo Financial Modeler Driver (*.wvr)};"
    connect_string = str(
        r3s_driver + r"DBQ={0};".format(wvr_path) + "MODEL={0}".format(model)
    )
    return connect_string


def get_connection(connect_string):
    start = timer()
    con = pyodbc.connect(connect_string, autocommit=False, readonly=True)
    end = timer()
    logger.info(
        "Obtaining a connection to {0} took {1}s".format(connect_string, end - start)
    )
    return con


def get_wvr_table_list(con):
    """
    Get list of tables inside a wvr file
    """
    query = "Select [Table Name] from [T_Table_Mapping]"
    query_results = pd.read_sql(query, con)
    table_list = query_results["Table Name"].tolist()
    return table_list


def get_wvr_table_data(table, con, limit=1000):
    """
    Return data from the specified table
    """
    start = timer()
    table_data = pd.read_sql(
        "Select * from [{0}] limit {1}".format(table, limit),
        con,
    )
    logger.info("done")
    end = timer()
    logger.info(
        "Selected {0} rows from model table {1} in {2:.2f}s".format(
            table_data.shape[0], table, end - start
        )
    )
    return table_data


def get_wvr_table_rowcount(table, con):
    """
    Return data from the specified table
    """
    start = timer()
    rowcount = con.execute("Select count(*) from [{0}]".format(table)).fetchval()
    end = timer()
    logger.info(
        "Counted {0} rows in model table {1} in {2:.2f}s".format(
            rowcount, table, end - start
        )
    )
    return rowcount


def parse_xml_to_list(xml_data, output_file):
    """
    Parse XML data to a list of dictionaries
    :param xml_data: XML data to parse
    :param output_file: Name of the output file (RunInfo.xml or RuntimeParameter.xml)
    :return: list of dictionaries containing the data (key, value)
    """
    runinfo_list = []
    section_name = "Model" if output_file == "RunInfo.xml" else "RuntimeParameter"
    try:
        root = etree.fromstring(xml_data.encode("UTF-16"))
        for model in root.findall(f".//{section_name}"):
            match section_name:
                case "Model":
                    runinfo = {}
                    runinfo["Number"] = get_element_text(model, "Number")
                    runinfo["Name"] = get_element_text(model, "Name")
                    runinfo["FullName"] = get_element_text(model, "FullName")
                    runinfo["Is64Bit"] = get_element_text(model, "Is64Bit")
                    runinfo["DelayPrepareData"] = get_element_text(
                        model, "DelayPrepareData"
                    )
                    runinfo["InitialiseOnGrid"] = get_element_text(
                        model, "InitialiseOnGrid"
                    )
                    runinfo["IsMPIEnabled"] = get_element_text(model, "IsMPIEnabled")
                    runinfo_list.append(runinfo)
                case "RuntimeParameter":
                    runinfo = {}
                    runinfo["Name"] = get_element_text(model, "Name")
                    runinfo["Value"] = get_element_text(model, "Value")
                    runinfo_list.append(runinfo)
                case _:
                    raise Exception("Invalid output file")
    except Exception as error:
        logger.error(f"Error while parsing XML: {error}")
    finally:
        return runinfo_list


def get_element_text(parent, element_name):
    """
    Get Attribute value if node exists
    """
    text = ""
    if parent is not None:
        element = parent.find(element_name)
        if element is None:
            text = ""
        else:
            text = element.text
    return text


def identify_models(wvr_paths, model_names):
    """
    Helper function to detec needed WVR file when there are multiple WVR paths provided
    It reads each WVR file's output and returns wanted ones with its corresponding WVR path
    :param wvr_paths: list of WVR paths
    :param model_names: list of model names, used as pattern to identify
    :return result: dictionary, name and model path (key, value)
    """
    result = dict()
    if isinstance(wvr_paths, str):
        wvr_paths = [wvr_paths]
    if isinstance(model_names, str):
        model_names = [model_names]
    for model_name in model_names:
        if model_name in result.keys():
            logger.info(f"Model has already validated: {model_name}")
            continue
        for wvr_path in wvr_paths:
            model_exist = get_model_names(wvr_path, model_name)
            if bool(model_exist):
                result[model_name] = wvr_path
                break
    logger.info(f"Identified WVR paths: {result}")
    if not all(model in result.keys() for model in model_names):
        missing_models = list(set(result.keys()) ^ set(model_names))
        logger.error(f"Some required models are missing: {missing_models}")
        return dict()
    return result


def get_model_names(wvr_path, pattern):
    """
    This function returns existing model names
    :param wvr_path: path to the WVR file (str) (e.g. 'C:/temp/esg/model.wvr)
    :return filtered_model_names: list of existing model names
    """
    # Remove file extension .WVR
    wvr_path = wvr_path.replace(".wvr", "")
    model_names = model_names_in_wvr(wvr_path)
    logger.info(f"Existing model names: {model_names}")
    filtered_model_names = list(
        filter(
            lambda model_name: model_name.startswith(pattern),
            model_names,
        )
    )
    logger.info(f"Filtered model names: {filtered_model_names}")
    return filtered_model_names


def get_db_connection(wvr_path, model_name):
    """
    Get database connection (initalize connection for boost further processing)
    :param wvr_path: WVR path (str)
    :param model_name: Model name (str)
    :return: Database connection (pyodbc connection object)
    """
    connection = None
    try:
        connect_string = get_wvr_connection_url(wvr_path, model_name)
        logger.info("Connect string: {}".format(connect_string))
        connection = get_connection(connect_string)
    except Exception as e:
        logger.error(f"Error while establishing connection: {e}")
    return connection


def read_jobrun_params(wvr_path):
    """
    Read jobrun parameters from the WVR file (RuntimeParams.xml)
    :param wvr_path: path to the WVR file
    :return: dictionary of jobrun parameters
    """
    jobrun_params = dict()
    try:
        runinfo_data = read_output_file(wvr_path, "RuntimeParams.xml")
        if not runinfo_data:
            raise Exception("No run info data found")
        for runinfo in runinfo_data:
            name = runinfo.get("Name", "")
            value = runinfo.get("Value", "")
            jobrun_params[name] = value
    except Exception as error:
        logger.error(f"Error while reading jobrun parameters: {error}")
    finally:
        return jobrun_params


def from_r3s_date(r3s_date):
    """
    Take integer R3S date (days) and convert to string date yyyy-MM-dd
    """
    intval = 0
    try:
        intval = int(r3s_date)
    except ValueError:
        logger.error(f"Could not parse R3S date: {r3s_date}")
        return r3s_date
    r3s_start_date = datetime.datetime(1859, 12, 31)
    date_value = r3s_start_date + datetime.timedelta(days=intval)
    return date_value.strftime("%Y-%m-%d")
