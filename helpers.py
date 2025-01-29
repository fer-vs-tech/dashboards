import re

import pandas as pd


def parse_string_series_as_dataframe(text):
    """
    This function parses a string series containing a list of strings
    and returns a dataframe.
    """
    # Remove the brackets and filter data
    result = re.findall(r"[\w\.-][\w\.-]+", text)[4:]

    # Map the list and convert a proper data type
    years = list(map(int, result[:11]))
    values = list(map(float, result[11:]))
    data_as_dict = {"Year": years, "Value": values}

    # Create a dataframe
    df = pd.DataFrame(data_as_dict)
    # Return the dataframe
    return df
