import logging

logger = logging.getLogger(__name__)

import base64
import configparser
import copy
import datetime
import hashlib
import json
import os
import sys
import tempfile
import time
from collections import namedtuple
from functools import wraps
from pathlib import Path
from typing import Any, Dict
from urllib.parse import parse_qs, urlparse

from flask import redirect, session, url_for
from lxml import etree

import cm_dashboards.wvr_data.wvr_functions as wvr_functions


def extract_url_params(input_url):
    """
    Extract url parameters into dictionary
    """
    if not input_url.startswith("?"):
        input_url = "?" + input_url
    parsed_url = urlparse(input_url)
    params = parse_qs(parsed_url.query)
    return params


def get_jobrun_from_url(input_url):
    params = extract_url_params(input_url)
    jobrun = params.get("jobrun", [None])[0]
    return jobrun


def get_company_id_from_url(input_url):
    """
    Get company id from url
    """
    params = extract_url_params(input_url)
    company_id = params.get("company_id", [None])[0]
    return company_id


def get_journal_type_from_url(input_url):
    """
    Get journal type from url
    """
    params = extract_url_params(input_url)
    journal_type = params.get("journal_type", [None])[0]
    return journal_type


def get_jobrun_id_from_url(input_url):
    """
    Get journal type from url
    """
    params = extract_url_params(input_url)
    jobrun_id = params.get("jobrun", [None])[0]
    logger.info(f"Job Run ID: {jobrun_id}")
    return jobrun_id


def encode_and_decode_string(input, encoding=True):
    """
    Encoding and Decoding String with Base64
    """
    result = None
    if encoding:
        input_string_bytes = input.encode("ascii")
        base64_bytes = base64.b64encode(input_string_bytes)
        result = base64_bytes.decode("ascii")
    else:
        base64_bytes = input.encode("ascii")
        output_string_bytes = base64.b64decode(base64_bytes)
        result = output_string_bytes.decode("ascii")

    return result


def get_journal_title(journal_type):
    """
    Get journal title based on journal type
    """
    journals = {
        "primary": "Accounting Info Primary",
        "reinsurance": "Accounting Info Reinsurance",
        "primary_life": "Accounting Info Primary (Life)",
        "primary_general": "Accounting Info Primary (General)",
        "primary_general_paa": "Accounting Info Primary (General/PAA)",
        "reinsurance_life": "Accounting Info Reinsurance (Life)",
        "reinsurance_general": "Accounting Info Reinsurance (General)",
        "reinsurance_general_paa": "Accounting Info Reinsurance (General/PAA)",
        "IFRS17_BBA_Reinsurance_Movement": "IFRS17 BBA Reinsurance Movement",
        "IFRS17_BBA_Primary_Movement": "IFRS17 BBA Primary Movement",
    }
    try:
        result = journals[journal_type]
    except KeyError:
        return "Journal Type {0} not found".format(journal_type)
    return result


def get_journal_tabs(journal_type):
    """
    Create tabs for journal
    """
    tab_names = {
        "IFRS17_BBA_Primary_Movement": [
            "FN 100 (Primary)",
            "FN 101 (Primary)",
        ],
        "IFRS17_BBA_Reinsurance_Movement": [
            "FN 100 (Reinsurance)",
            "FN 101 (Reinsurance)",
        ],
    }

    try:
        result = tab_names[journal_type]
    except KeyError:
        raise KeyError("Journal type {0} not found".format(journal_type))
    return result


def create_link_to_back(project_name, input_url):
    """
    Create link to back to previous page
    """
    params = extract_url_params(input_url)
    jobrun = params.get("jobrun", [None])[0]
    wvr = params.get("wvr", [None])[0]
    back_url = f"/dash/{project_name}/?jobrun={jobrun}&wvr={wvr}"
    return back_url


def get_wvr_path_from_url(input_url, multiple=False, extrat_params=True):
    """
    This function returns WVR path(s) from given URL query string
    :param input_url: URL query string
    :param multiple: flag indicating if multiple paths should be returned
    :return wvr_path: full path of WVR file, or None if no path is found (list, if multiple paths)
    """
    if extrat_params:
        logger.info(f"URL query string: {input_url}")
        params = extract_url_params(input_url)
        wvrs = params.get("wvr", [None])
    else:
        wvrs = input_url.get("wvr", [None])
    logger.info(f"Mupltiple request: {multiple} / WVR path(s): {wvrs}")

    # Check if invalid wvr path exists in the request
    if multiple and any([wvr is None for wvr in wvrs]) or (not multiple and wvrs[0] is None):
        logger.error("Invalid WVR path found in request")
        return None

    # If only single path needed
    if not multiple:
        first_wvr = wvrs[0]
        wvr_path = get_jobrun_path(first_wvr)

        # Return None if file does not exist
        if not os.path.exists(wvr_path):
            logger.error(f"ERROR: File does not exist: {wvr_path}")
            wvr_path = None
        logger.info(f"WVR path: {wvr_path}")
        return wvr_path

    # If multiple paths are requested
    wvr_paths = []
    for wvr in wvrs:
        logger.info(f"WVR: {wvr}")
        wvr_path = get_jobrun_path(wvr)

        # Skip if the file does not exist
        if not os.path.exists(wvr_path):
            logger.error(f"ERROR: File does not exist: {wvr_path}")
            continue
        wvr_paths.append(wvr_path)

    # Remove duplicates
    wvr_paths = list(set(wvr_paths))
    logger.info(f"WVR paths: {wvr_paths}")
    return wvr_paths


def find_config_file(file_name):
    """
    Check locations in the current and parent directories
    for config.ini and return the first matching one
    """
    config_file_locations = [
        file_name,
        os.path.join("../", file_name),
        os.path.join("../../", file_name),
        os.path.join("../../../", file_name),
    ]
    for file in config_file_locations:
        if os.path.exists(file):
            return Path(file)
    return None


def get_config_file(file_path):
    """
    Return Config object from reading specified ini file
    """
    config = configparser.ConfigParser()
    config.read(file_path)
    return config


def get_entry_from_config_file(section, tag, default=None):
    """
    Get an entry from the config file
    """
    config_file_path = find_config_file("dashboard_config.ini")
    if config_file_path is None:
        logger.error("config.ini file not found!")
        return default
    config = get_config_file(config_file_path)
    if config.has_section(section):
        if tag in config[section]:
            entry = config[section][tag]
            return entry
        else:
            logger.debug("Section {0} has no tag {1}".format(section, tag))
            return default
    else:
        logger.debug("No such section {0}".format(section))
    return default


def get_modelrunner_db_url():
    url = get_entry_from_config_file("database", "url")
    return url


def get_jobrun_path(jobrun_name):
    jobrun_root = get_entry_from_config_file("folders", "jobruns")
    jobrun_wvr = jobrun_name
    if not jobrun_name.endswith(".wvr"):
        jobrun_wvr = jobrun_wvr + ".wvr"
    jobrun_wvr_path = os.path.join(jobrun_root, jobrun_wvr)
    jobrun_wvr_path = jobrun_wvr_path.replace("\\", "/")
    return jobrun_wvr_path


def parse_runinfo_xml(xml_data):
    """
    Format Runinfo XML into list
    """
    runinfo_list = list()
    root = etree.fromstring(xml_data.encode("UTF-16"))
    for model in root.findall(".//Model"):
        runinfo = {}
        runinfo["Number"] = get_element_text(model, "Number")
        runinfo["Name"] = get_element_text(model, "Name")
        runinfo["FullName"] = get_element_text(model, "FullName")
        runinfo["Is64Bit"] = get_element_text(model, "Is64Bit")
        runinfo["DelayPrepareData"] = get_element_text(model, "DelayPrepareData")
        runinfo["InitialiseOnGrid"] = get_element_text(model, "InitialiseOnGrid")
        runinfo["IsMPIEnabled"] = get_element_text(model, "IsMPIEnabled")
        runinfo_list.append(runinfo)
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


def set_wvr_path(params: dict[str:str]) -> dict[str:str]:
    """
    Set WVR path from URL query string
    :param params: dictionary of parameters
    :return params: dictionary of parameters with WVR path
    """
    # Loop through all parameters, and set WVR path per key
    for key, value in params.items():
        # Get WVR path from jobrun ID in URL
        wvr_path = get_jobrun_path(value[0])
        params[key] = wvr_path

    logger.info("WVR paths: {}".format(params))
    return params


def validate_wvr_paths(wvrs: list[str]) -> list[str]:
    """
    Validate WVR paths
    :param wvr_paths: list of WVR paths
    :return wvr_paths: list of WVR paths
    """
    result = list()
    # Check if invalid wvr path exists in the request
    if any([wvr is None or wvr == "" for wvr in wvrs]):
        logger.error("Invalid WVR path found in request, switching to manual WVR selection mode")
        return result

    # Check if file exists
    for wvr in wvrs:
        # Normalize path for Windows
        wvr = wvr.replace("\\", "/")
        wvr_path = get_jobrun_path(wvr)
        # Skip if the file does not exist
        if not os.path.exists(wvr_path):
            logger.error("ERROR: File does not exist: {0} - {1}".format(wvr, wvr_path))
            continue
        result.append(wvr)

    logger.info("WVR paths: {}".format(result))

    return result


def get_jobrun_folders() -> list[str]:
    """
    Helper function to get all jobrun folders from the root folder specified in config.ini file
    :return jobrun_folders: list of jobrun folders
    """
    # Get root folder containing jobrun folders.
    jobrun_root = get_entry_from_config_file("folders", "jobruns")
    jobrun_folders = list()

    # Get all subfolders and normalize path for Windows.
    # Also read the subfolder content and find .wvr file and get the full path of the .wvr file
    for f in os.scandir(jobrun_root):
        if not f.is_dir():
            continue

        for wvr in os.scandir(f.path):
            if wvr.name.endswith(".wvr"):
                file_path = wvr.path.replace(jobrun_root, "")
                file_path = file_path.replace("\\", "/")
                file_path = file_path[1:]
                jobrun_folders.append(file_path)

    # logger.info("Jobrun folders: {}".format(jobrun_folders))
    return jobrun_folders


def set_dash_config(server):
    """
    Read dash config from config file and save in app config for later use
    """

    # Define default cache configuration parameters
    default_debug_mode = False
    default_cache_dir = tempfile.mkdtemp()
    default_cache_timeout = 24  # 24 hours
    default_cache_threshold = 1000

    try:
        # Read dash config from config file or use default values
        debug_mode = get_entry_from_config_file("dashboard", "debug_mode", default_debug_mode)
        cache_timeout = get_entry_from_config_file("dashboard", "cache_timeout", default_cache_timeout)
        cache_threshold = get_entry_from_config_file("dashboard", "cache_threshold", default_cache_threshold)

        logger.info("Debug mode: {0}".format(debug_mode))
        logger.info("Cache dir: {0}".format(default_cache_dir))
        logger.info("Cache timeout: {0} hour".format(cache_timeout))
        logger.info("Cache threshold: {0}".format(cache_threshold))

        debug_mode = True if (isinstance(debug_mode, str) and debug_mode.lower() == "true") else False
        cache_timeout = int(cache_timeout) * 60 * 60  # Convert to seconds
        cache_threshold = int(cache_threshold)

        # Save dash config in app config for later use
        server.config["DEBUG_MODE"] = debug_mode
        server.config["CACHE_DIR"] = default_cache_dir
        server.config["CACHE_TIMEOUT"] = cache_timeout
        server.config["CACHE_THRESHOLD"] = cache_threshold

    except Exception as e:
        logger.error("Error setting dash config: {0}".format(e))
        logger.info("Using default dash config")
        server.config["DEBUG_MODE"] = default_debug_mode
        server.config["CACHE_DIR"] = default_cache_dir
        server.config["CACHE_TIMEOUT"] = default_cache_timeout
        server.config["CACHE_THRESHOLD"] = default_cache_threshold

    return server


def set_kics_name():
    """
    Set KICS user name
    """
    valid_names = ["HANA", "DGB"]
    try:
        kics_name = get_entry_from_config_file("account", "kics_name", "DGB")
        kics_name = kics_name.upper().strip()
        if kics_name not in valid_names:
            kics_name = "DGB"
    except Exception as e:
        logger.error("Error setting KICS name: {0}".format(e))
        kics_name = "DGB"

    logger.info("KICS name: {0}".format(kics_name))
    return kics_name


def generate_unique_id(input_dict):
    """
    Generate unique id based on dictionary object
    :param input_dict: dictionary object (dict)
    :return unique_id: unique id (string)
    """
    if not isinstance(input_dict, dict):
        error_message = f"Input is not a dictionary object - {input_dict}"
        logger.error(error_message)
        raise TypeError(error_message)

    # Skip "aggregation_std" key as it's irrelevant for unique id
    input_dict_copy = copy.deepcopy(input_dict)
    input_dict_copy.pop("aggregation_std", None)

    # Convert the dictionary to string
    my_dict_str = json.dumps(input_dict, sort_keys=True)

    # Hash the string using SHA-256
    unique_id = hashlib.sha256(my_dict_str.encode()).hexdigest()
    logger.info("Unique ID: {}".format(unique_id))

    return unique_id


def create_dict_with_unique_id(unique_id, data_dict):
    """
    Create dictionary object with unique id as key
    """
    return {unique_id: data_dict}


def change_to_working_dir():
    application_path = r"c:\dashboard"
    if getattr(sys, "frozen", False):
        # Pyinstaller executable, log to same directory
        application_path = os.path.dirname(sys.executable)
    else:
        # Python script, log to same directory
        application_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(application_path)


def set_orsa_wvr_paths(wvr_paths):
    """
    Set ORSA WVR paths automatically and return mapped WVR paths
    :param input_url: URL query string
    :return wvr_path: full path of WVR file, or None if no path is found (list, if multiple paths)
    """
    # List of needed mapper names
    mappers = [
        "Aggregation_std",
        "Base",
        "Catastrophe",
        "Expense",
        "Lapse_Down",
        "Lapse_Mass",
        "Lapse_Up",
        "Longevity",
        "Morbidity",
        "Mortality",
        "Equity_Type_1_General",
        "Equity_Type_2_General",
        "Interest_Down",
        "Interest_Up",
        "Property",
        "Spread_Bond_Infra_Corp",
        "Spread_Bond_Infra_Invest",
        "Spread_Bond_No_Infra",
        "Fx_Down",
        "Fx_Up",
    ]

    try:
        mapped_results = dict()
        common_mappers = list()
        for mapper in mappers[1:]:
            # Find WVR path based on mapper name pattern
            patter_name = f"{mapper}.wvr"
            filtered_wvr_paths = list(filter(lambda x: x.endswith(patter_name), wvr_paths))

            # Store the relevant WVR path if found
            if len(filtered_wvr_paths) == 0:
                logger.info(f"No path found for {mapper}, skipping ...")
                continue
                # raise Exception(f"No path found for {mapper}, aborting ...")

            # Log warning if multiple paths are found
            if len(filtered_wvr_paths) > 1:
                logger.info(f"Multiple paths found for {mapper}, selecting first one: {filtered_wvr_paths[0]}")
            else:
                logger.info(f"Path found for {mapper}: {filtered_wvr_paths[0]}")

            mapped_results[mapper.lower()] = filtered_wvr_paths[0]
            common_mappers.append(filtered_wvr_paths[0])

        # Raise exception if not all WVR paths are set
        logger.info("Same model-named ORSA WVR paths: {}".format(mapped_results))

        # Set unique WVR path for "Aggregation_std" mapper as it's the only one that not found in common_mappers
        common_mappers = set(common_mappers)
        wvr_paths = set(wvr_paths)
        unique_wvr_paths = list(wvr_paths - common_mappers)
        logger.info("Unique ORSA WVR paths: {}".format(unique_wvr_paths))
        found_models = wvr_functions.identify_models(unique_wvr_paths, ["SII_Aggregation_Std_Formula_Group"])
        mapped_results["aggregation_std"] = found_models.get("SII_Aggregation_Std_Formula_Group")

        logger.info("Final ORSA WVR paths: {}".format(mapped_results))
        return mapped_results

    except Exception as e:
        raise e


def set_jics_model_name(model_names):
    """
    Automatically set JICS model name
    """
    model_name = None
    for name in model_names:
        if "solo" in name.lower():
            model_name = name
            break
        if "group" in name.lower():
            model_name = name
            break
    if model_name is None:
        logger.error("Cannot find valid JICS model name")
        raise Exception("Cannot find valid JICS model name, please check WVR file")
    logger.info(f"Selected model name: {model_name}")
    return model_name


def set_version(server):
    """
    Set version from version.txt file
    """
    try:
        current_path = os.path.dirname(os.path.realpath(__file__))
        version_file = os.path.join(current_path, "version.txt")
        with open(version_file, "r") as f:
            version = f.read().strip()
    except Exception as e:
        logger.error(f"Error setting version: {e}")
        version = "Unknown"
    logger.info(f"Current version: {version}")
    server.jinja_env.globals["VERSION"] = version
    return server


def set_server_key(server):
    """
    Set server key from dashboard_config.ini file
    """
    key = None
    try:
        key = get_entry_from_config_file("server", "key")
        key = bytes.fromhex(key)
        server.secret_key = key
    except Exception as e:
        logger.error(f"Error setting server key: {e}")
    return server


def set_compress_content(server):
    """
    Set compress content flag
    """
    compress_content = False
    try:
        compress_content = get_entry_from_config_file("server", "compress_content", "")
        compress_content = compress_content.lower() == "true"
    except Exception as e:
        logger.error(f"Error setting server key: {e}")
    logger.info(f"Compress content enabled: {compress_content}")
    server.config["COMPRESS_CONTENT"] = compress_content
    return server


def is_session_expired(enabled=False):
    """
    Function to check session validity
    :param is_enabled: Enable/Disable session check
    :return boolean: True if session is expired, False otherwise
    """
    if not enabled:
        logger.info("Session check disabled, skipping")
        return False
    if not session.get("logged_in"):
        return True
    logger.info(f"Session active for user: {session.get('username')}")
    return False


def check_session(is_enabled=True):
    """
    Custom decorator to check session validity before accessing the dashboards
    :param is_enabled: Enable/Disable session check
    :return: Wrapper function
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not is_enabled:
                logger.info("Session check disabled, skipping")
                return func(*args, **kwargs)
            if is_session_expired(is_enabled):
                logger.info("Session expired, blocking access")
                return redirect(url_for("is_session_valid"))
            return func(*args, **kwargs)

        return wrapper

    return decorator


def enable_session_validity_check(server):
    """
    Enable session validity check
    """
    is_enabled = False
    try:
        is_enabled = get_entry_from_config_file("server", "require_wm_session", False)
        is_enabled = True if (isinstance(is_enabled, str) and is_enabled.lower() == "true") else False
    except Exception as e:
        logger.error(f"Error setting session validity check: {e}")

    logger.info(f"Session validity check enabled: {is_enabled}")
    server.config["ENABLE_SESSION_VALIDITY_CHECK"] = is_enabled
    return server


def add_exception_info(exception: BaseException, additional_info: str) -> BaseException:
    """
    Add additional information to an exception
    :param exception: Exception to modify
    :param additional_info: Additional information to add to the exception
    :return: Modified exception
    """
    # Get the type of the original exception
    exception_type: type = type(exception)

    # Create a new exception with the modified message
    new_exception: BaseException = exception_type(f"{additional_info} - {exception}")

    # Copy the traceback information from the original exception to the new exception
    new_exception.__traceback__: BaseException = exception.__traceback__

    return new_exception


def get_range_destination(book, range_name):
    """
    Get coordinates and sheet of this range
    :param book: Excel workbook object
    :param range_name: Range name (str)
    :return: Coordinates (str), sheet (str)
    """
    # logger.info(f"Getting range destination for {range_name}")
    # Get location information of this range
    try:
        dest = list(book.defined_names[range_name].destinations)
    except KeyError as error:
        message = f"Range name {range_name} doesn't exist"
        logger.info(f"Error while getting range destination: {error}")
        logger.info(message)
        raise add_exception_info(error, message)

    # Excel cell coordinates of the range
    try:
        coords = dest[0][1].replace("$", "")
    except IndexError as error:
        message = f"Range name {range_name} doesn't refer to a range"
        logger.info(f"Error while getting coordinates: {error}")
        logger.info(message)
        raise add_exception_info(error, message)

    # Get the sheet object
    illegal_chars = ["\\", "[", "]", ":"]
    if any(c in dest[0][0] for c in illegal_chars):
        message = f"Range name {range_name} refers to illegal worksheet path: {dest[0][0]}"
        logger.error(message)
        raise add_exception_info(error, "Error while getting sheet")

    try:
        sheet = book[dest[0][0]]
    except KeyError as error:
        message = f"Range name {range_name} refers to illegal worksheet path: {dest[0][0]}"
        logger.error(f"Error while getting sheet: {error}")
        logger.error(message)
        raise add_exception_info(error, "Error while getting sheet")

    # logger.info(f"Range destination: {coords}, Sheet: {sheet}")
    return coords, sheet


def get_db_connection(wvr_path, model_name):
    """
    Get database connection (initalize connection for boost further processing)
    :param wvr_path: WVR path (str)
    :param model_name: Model name (str)
    :return: Database connection (pyodbc connection object)
    """
    connection = None
    try:
        connect_string = wvr_functions.get_wvr_connection_url(wvr_path, model_name)
        logger.info("Connect string: {}".format(connect_string))
        connection = wvr_functions.get_connection(connect_string)
    except Exception as e:
        logger.error(f"Error while establishing connection: {e}")
    return connection


def generate_filename(extention, prefix="JICS", add_timestamp=True):
    """
    Generate filename based on the given format
    :param extention: File extention (e.g. xlsx, xls, csv)
    :return: Generated filename (e.g. JICS_20210101_000000.xlsx)
    """
    prefix = prefix.replace(" ", "_")
    if add_timestamp:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"{prefix}_{timestamp}.{extention}"
    else:
        filename = f"{prefix}.{extention}"
    return filename


def remove_substring(string):
    """
    Remove substring from string
    :param string: string
    :return: string
    """
    if "." in string:
        string = string.split(".")[0]
    if "Unnamed" in string:
        string = ""
    return string


def convert_dict_to_namedtuple(dict_data: Dict[str, Any], name: str = "NamedTuple") -> namedtuple:
    """
    Convert dictionary to namedtuple
    :param dict_data: dictionary data
    :param name: name of namedtuple (str) - default: NamedTuple
    :return: namedtuple
    """
    try:
        namedtuple_type = namedtuple(name, dict_data.keys())
        namedtuple_data = namedtuple_type(**dict_data)
    except Exception as e:
        logger.error(f"Error while converting dictionary to namedtuple: {e}")
        raise e
    return namedtuple_data


def timeit(is_callback=False):
    """
    Custom decorator to mesure function execution time
    :param is_callbacl: flag to determine whether it's callback or regular function
    """

    def decorator(func):
        @wraps(func)
        def timeit_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            func_type = "Callback" if is_callback else "Function"
            logger.info(f"{func_type} '{func.__name__}' took {total_time:.4f} seconds")
            return result

        return timeit_wrapper

    return decorator
