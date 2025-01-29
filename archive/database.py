"""
@author: graham.howarth
"""
import configparser

import pandas as pd
import psycopg2


# Execute an SQL query and return results in a data frame
def doQueryToDf(query, schema):
    con = getConnection(section=schema)
    print("Executing query: " + query)
    df = pd.read_sql(query, con=con)
    # print(df)
    # Close DB connection
    con.close()
    return df


def doQueryToList(query, schema):
    con = getConnection(section=schema)
    print("Executing query: " + query)
    results = con.execute(query).fetchall()
    con.close()
    return results


# Get an database connection
def getConnection(filename="config.ini", section="postgresql"):
    # Read Database connection string from config file
    config = configparser.ConfigParser()
    config.read(filename)
    db = {}
    if config.has_section(section):
        params = config.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    try:
        con = psycopg2.connect(**db)
        return con
    except psycopg2.DatabaseError as e:
        print(e)
        return e
