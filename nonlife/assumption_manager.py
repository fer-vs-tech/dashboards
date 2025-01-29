"""
Created on 22 May 2020

@author: graham.howarth
"""
import pandas as pd
from sqlalchemy import create_engine

import cm_dashboards.nonlife.excel_tools as excel_tools


def pivot_data(df, dimension_names):
    """
    Convert list of range data to dataframe
    """

    if dimension_names is None:
        print("dimension names empty!")
        return None
    num_dimensions = len(dimension_names)

    prepare_headers_for_pivot(df, dimension_names)
    # Set column names to be the dimension names
    if num_dimensions > 1:
        df.columns.name = dimension_names[0]
    else:
        df.columns.name = "Step"
    try:
        stacked = df.stack()
        # Transposed column values go under 'Val'
        stacked.name = "Val"
        # Convert Series into dataframe
        stacked = stacked.reset_index()
        if num_dimensions > 1:
            # Drop dummy index
            stacked = stacked.drop("level_0", axis=1)
    except Exception as e:
        print(e)
        print("Data table not stackable")
        stacked = df
    return stacked


def unpivot_data(stacked_df, dimension_names):
    """
    For the purpose of re-orienting DB data in original Excel layout
    """
    print(dimension_names)
    if dimension_names is None:
        print("Dimension names is empty!")
        return None
    num_dimensions = len(dimension_names)
    first_dimension = dimension_names[0]
    # First dimension name comes last in excel format
    if len(dimension_names) > 1:
        dimension_names.append(dimension_names.pop(0))

    if first_dimension is None:
        print("No dimension names found")
        first_dimension = "Val"
    try:
        if num_dimensions > 1:
            # Set new indexes for unstack
            reindex_df = stacked_df.set_index(dimension_names)
            # unstack first dimension into columns
            unstacked = reindex_df.unstack(first_dimension)
        else:
            # Set new indexes for unstack
            reindex_df = stacked_df.set_index([dimension_names[0], "Step"])
            # unstack first dimension into columns
            unstacked = reindex_df.unstack("Step")
        # Remove ID index
        unstacked = unstacked.reset_index()
        unstacked = unstacked.rename(columns={"Val": "", "Category": ""})
        unstacked.columns = [f"{i}{j}" for i, j in unstacked.columns]
    except Exception as e:
        print(e)
        print("Data table not unstackable")
        unstacked = stacked_df
    return unstacked


def read_assumptions_file(excel_filepath):
    """
    Read Excel file
    """
    # Open Excel file
    book = excel_tools.load_workbook(excel_filepath, read_only=True, data_only=True)
    named_ranges = excel_tools.get_named_ranges(book)

    data_names_list = get_data_from_named_range_list(book, named_ranges)
    for initial_data, dimension_names in data_names_list:
        print("--Initial Data--")
        print(initial_data)
        stacked_data = pivot_data(initial_data, dimension_names)
        if stacked_data is not None:
            print("---Pivot Data---")
            print(stacked_data)
            unstacked_data = unpivot_data(stacked_data, dimension_names)
            print("---Unpivot Data---")
            print(unstacked_data)
    book.close()


def get_data_from_named_range_list(book, range_name_list):
    """
    Get the data from all named ranges in list
    """
    df_names_list = []
    for named_range in range_name_list:
        df, dimension_names = get_data_from_named_range(book, named_range)
        df_names_list.append((df, dimension_names))
    return df_names_list


def get_data_from_named_range(book, range_name):
    """
    Get the data from this range name
    """
    print("----------" + range_name + "----------")
    # Get the coordinates and sheet of this range
    coords, sheet = excel_tools.get_range_destination(book, range_name)

    # Get the data in this range
    data_list = excel_tools.load_workbook_range(coords, sheet)
    dimension_names = excel_tools.find_assumption_dimensions(data_list, coords, sheet)

    if len(data_list[0]) < 1:
        print("Table too small to pivot")
        return None
    if not data_list[0][0]:
        data_list[0][0] = "Category"
    # Convert to dataframe, using column headers
    df = pd.DataFrame(data_list, columns=data_list[0])

    # Drop duplicate header row
    df = df.drop(df.index[0])
    return df, dimension_names


def prepare_headers_for_pivot(df, dimension_names):
    num_dimensions = len(dimension_names)
    if num_dimensions > 1:
        header_names = dimension_names[1:]
        df.set_index(header_names, append=True, inplace=True)
    else:
        df.set_index(dimension_names[0], inplace=True)


if __name__ == "__main__":
    read_assumptions_file(
        # r"C:\r3s_workspaces\VN_3.1_200626\Assumptions\HLV_CF_Assumptions_2019.xlsx"
        # r"C:\Users\graham.howarth\OneDrive - RNA Analytics\r3s_workspaces\StandardCode\Example Model Workspaces\French\Assumptions\France_External_Assumptions.xlsx"
        r".\nonlife\Nonlife_Output Report_Sample2.xlsx"
    )
