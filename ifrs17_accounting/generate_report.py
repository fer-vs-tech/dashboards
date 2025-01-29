"""
Stand alone script to Deves SAP report file
:author: Usmonov Kamoliddin
:date: 2023-09-22
"""

import logging

logger = logging.getLogger(__name__)

import argparse
import os
import sys
import time

from flask import send_file

sys.path.append("../..")


import cm_dashboards.ifrs17_accounting.helpers as helpers
import cm_dashboards.ifrs17_accounting.journal_table as journal_table


def main(wvr_path, journal_type, reverse, save_file_to=None):
    """
    Generate report file
    :param wvr_path: absolute path to WVR folder (str)
    :param journal_type: Journal type (primary or reinsurance)
    :param reverse: Reverse the records (bool)
    :param save_file_to: Save the file to this path (str)
    :return: File as download or save to path
    """
    # Clean DF
    journals_df = journal_table.get_data(
        wvr_path, None, journal_type, add_headnote=True, reversed=reverse
    )

    # Update DocDate and PostDate to be the next months last day
    if reverse:
        journals_df = helpers.reverse_journal_dates(journals_df)

    try:
        # Create connection strings
        db_start_time = time.perf_counter()
        journal_connection = helpers.get_connection_string(wvr_path, "journal")
        mapping_connection = helpers.get_connection_string(wvr_path, "mapping")

        # Get results from DB
        db_results = helpers.get_results_from_db(
            journal_type, journal_connection, mapping_connection
        )
        db_end_time = time.perf_counter()

        # Generate journal data
        start_time = time.perf_counter()
        result = helpers.generate_report_date(journals_df, db_results, reverse=reverse)

        # Close connections
        journal_connection.close()
        mapping_connection.close()
        end_time = time.perf_counter()

    except Exception as e:
        logger.error(f"Failed to get data from DB with error: {e}")
        raise

    # Prepare the df for exporting formats
    data_start_time = time.perf_counter()
    export_result = helpers.prepere_df_for_download(
        result, journals_df=journals_df, calculate_as_block=True
    )
    if export_result is None:
        raise Exception("Failed to prepare data for export")

    # Generate export file
    try:
        export_result = helpers.clear_some_field_values_by_checking(export_result)
        export_file = helpers.generate_export_file(export_result)
    except Exception as e:
        logger.error(f"Failed to generate export file with error: {e}")
        raise

    # Send the file
    doc_type = journals_df["Record_Type_Text"].iloc[0]
    report_date = journals_df["Document_Date"].iloc[0]
    filename = helpers.generate_filename(doc_type, journal_type, report_date, reverse)
    data_end_time = time.perf_counter()
    logger.info(
        "Time took {:6.3f} seconds for getting data from DB".format(
            db_end_time - db_start_time
        )
    )
    logger.info(
        "Time took {:6.3f} seconds for generation {:d} rows".format(
            end_time - start_time, result.shape[0]
        )
    )
    logger.info(
        "Time took {:6.3f} seconds for prepering {}".format(
            data_end_time - data_start_time, filename
        )
    )
    logger.info(f"Total time took: {data_end_time - db_start_time} seconds")

    # Send the file as download
    if save_file_to is None:
        return send_file(
            export_file,
            mimetype="text/csv",
            download_name=filename,
            as_attachment=True,
        )

    # Check if path exists, if not create it
    if not os.path.exists(save_file_to):
        logger.info(f"Creating path: {save_file_to}")
        os.makedirs(save_file_to)

    # Save the in-memory file to path
    file_path = os.path.join(save_file_to, filename)
    logger.info(f"Saving file to: {file_path}")
    with open(file_path, "wb") as f:
        f.write(export_file.getvalue())
        f.close()
    logger.info("File saved!")
    return file_path


def create_arg_parser():
    """
    Parse command line arguments for report generation
    """
    parser = argparse.ArgumentParser(
        prog="generate_report.py",
        description="Generate report file for DEVES SAP system",
    )
    parser.add_argument(
        "-w",
        "--wvr",
        help="Absolute path to WVR",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--type",
        help="Report type",
        choices=["primary", "reinsurance"],
        required=True,
    )
    parser.add_argument(
        "-r",
        "--reversed",
        help="Reversed",
        default=False,
        action=argparse.BooleanOptionalAction,
    )
    parser.add_argument(
        "-o",
        "--output-path",
        help="Output path",
        required=True,
    )

    return parser


if __name__ == "__main__":
    parser = create_arg_parser()
    args = parser.parse_args(sys.argv[1:])
    main(args.wvr, args.type, args.reversed, args.output_path)
