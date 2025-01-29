import logging

logger = logging.getLogger(__name__)

import sys

sys.path.append("../../..")

import getpass
import json
from enum import Enum
from timeit import default_timer as timer

import keyring
import pandas as pd
import pyodbc
import sqlalchemy
from sqlalchemy import func, text
from sqlalchemy.engine import URL, make_url
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.automap import (
    automap_base,
    generate_relationship,
    name_for_collection_relationship,
)
from sqlalchemy.orm import joinedload, relationship, sessionmaker
from sqlalchemy.sql.schema import MetaData, Table

import cm_dashboards.utilities as utilities


class DatabaseType(Enum):
    """
    DatabaseType enum
    """

    UNKNOWN = -1
    MSSQL = 0
    POSTGRES = 1
    SQLITE = 2


def get_db_type(db_url=None):
    """
    Get database type
    :param db_url: Database URL (optional)
    :return: Database type
    """
    # Get database URL from config file if not provided
    if db_url is None:
        db_url = utilities.get_modelrunner_db_url()

    # Return database type by matching the database URL
    if db_url.startswith("mssql+pyodbc"):
        return DatabaseType.MSSQL
    elif db_url.startswith("sqlite"):
        return DatabaseType.SQLITE
    elif db_url.startswith("postgresql"):
        return DatabaseType.POSTGRES
    else:
        logger.error("Unknown database type in config.ini")
        return DatabaseType.UNKNOWN


def get_db_url_with_credentials(db_url, prompt_for_password=False):
    """
    Get database URL with credentials
    :param db_url: Database URL
    :param prompt_for_password: Prompt for password if not found in credential store
    :return: Database URL with credentials
    """
    # Check URI syntax and get database type
    url = make_url(db_url)
    db_type = get_db_type(db_url)

    # Raise exception if database type is unknown
    if db_type == DatabaseType.UNKNOWN:
        raise Exception("Unknown database type in config.ini")

    # Return the URL if it's a SQLite database
    if db_type == DatabaseType.SQLITE:
        return url

    # Get database URL with credentials only for non-SQLite databases
    url_dict = url._asdict()
    if db_type == DatabaseType.MSSQL and "trusted_connection=yes" in db_url.lower():
        logger.info("Using SQL Server trusted connection...")
    elif not url.password:
        logger.info("Looking up DB password from credential store...")
        password = keyring.get_password("workflowmanager", url.username)
        if password is None:
            logger.warning("No credentials found")
            if prompt_for_password:
                password = getpass.getpass("Enter password for database:")
                if password is None or len(password.strip()) == 0:
                    logger.error("Password cannot be empty!")
                else:
                    keyring.set_password("workflowmanager", url.username, password)
                url_dict["password"] = password
        else:
            # Escape special characters
            url_dict["password"] = password

    # Reconstruct SQL Alchemy URL from dict components
    url = URL(**url_dict)
    return url


def query_to_dataframe(con, query):
    """
    Execute an SQL query and return results in a data frame
    :param con: SQL Alchemy connection
    :param query: SQL query
    :return: Data frame
    """
    if con is None:
        df = pd.DataFrame()
    else:
        df = pd.read_sql(query, con=con)
    return df


def query_to_list(con, query):
    """
    Execute an SQL query and return results in a list
    :param con: SQL Alchemy connection
    :param query: SQL query
    :return: List of results
    """
    return con.execute(query).fetchall()


def get_db_connection_url(jobrun_id):
    """
    Get a dashboard DB connection
    """
    # Cloud Manager engine connection
    cm_engine = get_db_engine(utilities.get_modelrunner_db_url())
    cm_meta = get_db_metadata_subset(cm_engine, ["JobRuns", "JobTemplates", "ParameterSetValues"])
    # We don't care about saving this as we'll only use it once per job for lookup of dashboard URL etc
    Session = sessionmaker()
    Session.configure(bind=cm_engine)
    cm_con = Session()
    # Extract the DB URL of this dashboard
    return get_dashboard_db_url(cm_con, cm_meta, jobrun_id)


def create_session(engine):
    """
    Create a session to the database and load the tables
    """
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
    except Exception as error:
        logger.error(f"Error occured while creating session: {error}")
        session = None
    return session


def auto_map_tables(engine):
    """
    Automap tables from the database
    """
    try:
        Base = automap_base()
        Base.prepare(engine, reflect=True, generate_relationship=_gen_relationship)
        return Base.classes
    except Exception as error:
        logger.error(f"Error occured while automapping tables: {error}")
        raise error


def prepend_name(base, local_cls, referred_cls, constraint):
    """
    Prepend the table name to the relationship
    """
    return "tbl_" + referred_cls.__name__.lower()


def _name_for_collection_relationship(base, local_cls, referred_cls, constraint):
    """
    Name for collection relationship
    """
    if constraint.name:
        return constraint.name.lower() + "_" + referred_cls.__name__.lower()
    return name_for_collection_relationship(base, local_cls, referred_cls, constraint)


def _gen_relationship(base, direction, return_fn, attrname, local_cls, referred_cls, **kw):
    """
    Generate relationship between tables
    """
    return generate_relationship(base, direction, return_fn, attrname + "_ref", local_cls, referred_cls, **kw)


def get_db_connection(url):
    """
    Get database connection
    """
    return get_db_engine(url)


def get_db_engine(db_url):
    """
    Get database engine
    """
    if not db_url:
        logger.info("Got empty DB URL")
        return None
    start = timer()
    db_type = get_db_type(db_url)
    logger.info(f"Database type is: {db_type.name}")
    url = get_db_url_with_credentials(db_url, prompt_for_password=True)
    engine = sqlalchemy.create_engine(url, pool_recycle=3600)
    pyodbc.pooling = False
    end = timer()
    logger.info(f"DB engine creation execution took {1000 * (end - start):.2f}ms")
    return engine


def get_db_metadata(engine):
    """
    Load pre-existing database into metadata tables
    """
    if not engine:
        logger.info("Database engine not initialised")
        return None
    start = timer()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    end = timer()
    logger.info(f"DB metadata full creation execution took {end - start:.2f}s")
    # logger.info(f"Found tables: {metadata.tables.keys()}")
    return metadata


def get_db_metadata_subset(engine, table_list):
    """
    Load pre-existing database into metadata tables
    """
    if not engine:
        logger.error("Database engine not initialised")
        return None
    start = timer()
    metadata = MetaData()
    for table in table_list:
        Table(table, metadata, autoload_with=engine)
    end = timer()
    logger.info(f"DB metadata subset creation execution took {end - start:.2f}s")
    # logger.info(f"Found tables: {metadata.tables.keys()}")
    return metadata


def get_dashboard_db_url(db_session, metadata, jobrun_id):
    """
    Get the database URL for this jobrun
    """
    # Get tables from metadata
    jobruns = metadata.tables["JobRuns"]
    jobtemplates = metadata.tables["JobTemplates"]
    parameters = metadata.tables["ParameterSets"]
    parameter_values = metadata.tables["ParameterSetValues"]

    # Get db output connection string used for this model
    db_url = ""
    connection_url = ""
    if jobrun_id is not None:
        # Get the jobtemplate ID for this jobrun
        jobtemplate_id = db_session.query(jobruns.c.jobTemplate_id).filter(jobruns.c.id == jobrun_id).scalar()
        parameter_name = db_session.query(jobruns.c.parameter_set_name).filter(jobruns.c.id == jobrun_id).scalar()
        # Get the parameter set ID for this jobtemplate
        parameters_id = (
            db_session.query(parameters.c.id)
            .filter(parameters.c.jobTemplate_id == jobtemplate_id)
            .filter(parameters.c.name == parameter_name)
            .scalar()
        )
        # Get the db URL parameter value
        db_url = (
            db_session.query(parameter_values.c.value)
            .filter(parameter_values.c.parameterSet_id == parameters_id)
            .filter(parameter_values.c.name == "Model_Runner_Database_URL")
            .scalar()
        )
        if db_url == None:
            logger.error(f"No Database URL found for jobrun {jobrun_id}")
            return None
        # We need to convert this ODBC URL so it can be used by SQL Alchemy
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": db_url})

    return connection_url


def get_jobrun_name_from_id(jobrun_id):
    """
    Get a dashboard DB connection
    """
    # Cloud Manager engine connection
    cm_engine = get_db_engine(utilities.get_modelrunner_db_url())
    cm_meta = get_db_metadata_subset(cm_engine, ["AssumptionSets", "JobRuns", "Assumptions"])
    # We don't care about saving this as we'll only use it once per job for lookup of dashboard URL etc
    Session = sessionmaker()
    Session.configure(bind=cm_engine)
    cm_con = Session()
    # Extract the DB URL of this dashboard
    jobrun_name = get_jobrun_name(cm_con, cm_meta, jobrun_id)
    cm_con.close()
    return jobrun_name


def get_jobrun_name(db_session, metadata, jobrun_id):
    jobruns = metadata.tables["JobRuns"]
    jobrun_name = db_session.query(jobruns.c.name).filter(jobruns.c.id == jobrun_id).scalar()
    return jobrun_name


def get_assumption_set_data(assumption_name, jobrun_id):
    """
    Get the assumption set data for the given assumption name and jobrun id
    Retrive job run owner's user group id then get visible user groups
    Query the max version of the assumption set for the visible user groups
    Return assumptions from the found max verioned assumption set
    """
    try:
        db_url = utilities.get_modelrunner_db_url()
        if db_url is None:
            raise ValueError("DB connection string is missing")
        engine = get_db_engine(db_url)
        if engine is None:
            raise ValueError("Cannot create DB engine")
        auto_mapped_classes = auto_map_tables(engine)
        session = create_session(engine)
        if session is None:
            raise ValueError("Cannot create session")
    except Exception as e:
        raise e

    try:
        # Load the automapped classes (tables)
        # logger.info(f"Auto mapped classes: {auto_mapped_classes.items()}")
        AssumptionSet = auto_mapped_classes.get("AssumptionSets")
        Assumption = auto_mapped_classes.get("Assumptions")
        JobRun = auto_mapped_classes.get("JobRuns")
        User = auto_mapped_classes.get("Users")
        UserGroup = auto_mapped_classes.get("UserGroups")
        JobNodeRuns = auto_mapped_classes.get("JobNodeRuns")
        JobNodes = auto_mapped_classes.get("JobNodes")

        # Reflect the relationships to make them available and use in queries
        UserGroup.parent = relationship(
            "UserGroups",
            backref="children",
            remote_side=[UserGroup.id],
            foreign_keys=[UserGroup.parent_id],
        )
        JobRun.owner = relationship("Users", foreign_keys=[JobRun.owner_id])
        User.userGroup = relationship("UserGroups", backref="users")
        AssumptionSet.owner = relationship("Users", backref="assumption_sets")
        AssumptionSet.assumptions = relationship("Assumptions", backref="assumption_set")

        jobrun = session.query(JobRun).filter(JobRun.id == jobrun_id).options(joinedload(JobRun.owner)).first()
        if not jobrun:
            raise Exception(f"No job run found with ID '{jobrun_id}'")
        user_group_id = jobrun.owner.userGroup_id
        visible_groups = get_visible_groups(session, UserGroup, user_group_id)
        logger.info(f"Visible user groups: {visible_groups}")
        assumption_set_id = get_latest_version_id(session, AssumptionSet, User, assumption_name, visible_groups)
        if not assumption_set_id:
            raise Exception("No assumption set found")

        assumption_set = session.query(Assumption).filter_by(assumption_set_id=assumption_set_id).all()
        if not assumption_set:
            raise Exception("No assumptions found")
        assumption_sets = get_assumption_entries(assumption_set)
        session.close()
        return assumption_sets

    except Exception as e:
        raise e

    finally:
        session.close()


def get_visible_groups(db_session, user_group, user_group_id):
    """
    Get visible user groups for the given user group id
    """
    result = []
    try:

        def get_all_child(children):
            """
            Get all child groups recursively and add to list
            """
            if children is not None:
                for child in children:
                    result.append(child.id)
                    get_all_child(child.children)
            return result

        user_group = db_session.query(user_group).filter(user_group.id == user_group_id).first()
        result = get_all_child(user_group.children)
        result.append(user_group.id)
    except Exception as e:
        logger.error(f"Error occurred while fetching user group children: {str(e)}")
    return result


def get_latest_version_id(session, assumption, user, name, user_group_id):
    """
    Get the latest version of the assumption set for the given user group id
    :param session: Database session
    :param assumption: Assumption table
    :param user: User table
    :param name: Assumption name
    :param user_group_id: User group
    :return: Assumption set id
    """
    try:
        entry = (
            session.query(
                assumption.id,
                assumption.name,
                func.max(assumption.version).label("max_version"),
            )
            .filter(assumption.name == name)
            .filter(assumption.owner.has(user.userGroup_id.in_(user_group_id)))
            .group_by(assumption.id, assumption.name)
            .order_by(text("max_version DESC"))
            .first()
        )
        logger.info(f"Fetched assumption entry: {entry}")
        if not entry or any([details is None for details in entry]):
            raise Exception(f"No assumption found with the given name: {name}")

        # If there are multiple entries with the same name, get first one
        entry_id, entry_name, max_existing_version = entry
        logger.info(f"Max version of '{entry_name}' (id={entry_id}): {max_existing_version}")
        return entry_id
    except Exception:
        # logger.error(f"Error occured while fetching latest max version: {error}")
        raise


def get_assumption_entries(assumptions):
    """
    Get assumption entries from the assumption set
    :param assumptions: List of assumption
    :return: Dictionary of assumption entries
    """
    result = {}
    try:
        for assumption in assumptions:
            logger.info(f"Added assumption '{assumption.name}' (v{assumption.version}): {len(assumption.entries)} entries")
            entries = assumption.entries
            if isinstance(entries, str):
                entries = json.loads(entries)
            result[assumption.name] = entries
    except Exception as error:
        logger.error(f"Error occured while loading assumption entries: {error}")
    return result
