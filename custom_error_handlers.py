import logging

logger = logging.getLogger(__name__)

import traceback

from flask import render_template, request
from werkzeug.exceptions import HTTPException

from cm_dashboards.server import server


@server.errorhandler(Exception)
def custom_error_handler(error):
    """
    This function is used to override the default error handler and return a custom error message
    Can handle any exception (HTTPException, Exception)
    :param error: error message
    :return: rendered template with error message
    """
    # Catch and handle Internal Server Error (500)
    if not isinstance(error, HTTPException):
        error_code = 500
        formatted_lines = traceback.format_exc().splitlines()
        error_title = "Internal Server Error"
        error_description = "Something went wrong. Please try again later. If the problem persists, please contact the administrator."
        internal_error = formatted_lines[-1]
        if "no such table" not in traceback.format_exc():
            logger.error(f"{traceback.format_exc()}")

        return (
            render_template(
                "error_page.html",
                error_code=error_code,
                error_title=error_title,
                error_description=error_description,
                internal_error=internal_error,
            ),
            error_code,
        )

    error_code = error.code
    error_title = error.name
    error_description = error.description
    logger.error(f"{error_code} - {error_title}, {error_description}")
    logger.error(f"URL was: {request.path}")

    return (
        render_template(
            "error_page.html",
            error_code=error_code,
            error_title=error_title,
            error_description=error_description,
        ),
        error_code,
    )
