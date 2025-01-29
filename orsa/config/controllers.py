import logging

logger = logging.getLogger(__name__)

import urllib.parse

from flask import redirect, render_template, request

import cm_dashboards.utilities as utilities
from cm_dashboards.orsa.config.config import PROJECT_NAME, PROJECT_TITLE
from cm_dashboards.server import server as application


@application.route(f"/dash/{PROJECT_NAME}/controllers", methods=["GET", "POST"])
def orsa_controllers():
    """
    Controller screen for the dash app
    """
    # Map the label names to the param names
    if request.method == "POST":
        # Validate the form data
        params = request.form.to_dict(flat=False)
        logger.info(f"Params: {params}")
        encoded_params = params.get("next", [""])[0]
        factor = params.get("factor", ["100000"])[0]
        decode_encoded_params = utilities.encode_and_decode_string(
            encoded_params, encoding=False
        )
        # Add factor to the params
        decode_encoded_params += "&factor={}".format(factor)
        final_query_string = utilities.encode_and_decode_string(
            decode_encoded_params, encoding=True
        )
        redirect_url = f"/dash/{PROJECT_NAME}/?{final_query_string}"

        return redirect(redirect_url)

    # Parse the URL query string
    downsale_factors = [10000, 100000, 1000000, 10000000, 100000000]
    query_string = "?" + request.query_string.decode("utf-8")
    logger.info("Query string: {}".format(query_string))

    # Encode the query string to be passed to the next page
    encode_query_string = utilities.encode_and_decode_string(
        query_string, encoding=True
    )
    return render_template(
        "orsa_controllers_screen.html",
        title=PROJECT_TITLE,
        query_string=encode_query_string,
        downsale_factors=downsale_factors,
    )
