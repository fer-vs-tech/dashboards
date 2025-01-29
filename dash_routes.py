import logging

logger = logging.getLogger(__name__)

from flask import jsonify, make_response, redirect, render_template, request, session

from cm_dashboards.server import server as application
from cm_dashboards.utilities import encode_and_decode_string, is_session_expired

# Define route path prefix
PREFIX = "/dash"


@application.route("/")
@application.route(PREFIX)
@application.route(PREFIX + "/")
def dash_list():
    jobrun = request.args.get("id", type=int, default=0)
    return render_template("dashboards.html", jobrun=jobrun)


@application.route(f"{PREFIX}/alive")
def alive():
    """
    Health check
    """
    return make_response("OK", 200)


@application.route(f"{PREFIX}/is_session_valid")
def is_session_valid():
    """
    Check if WM session is active
    """
    # Decode referrer URL if provided
    encoded_referrer = None
    try:
        decoded_referrer = request.args.get("referrer", type=str)
        encoded_referrer = encode_and_decode_string(decoded_referrer, False)
    except Exception as e:
        logger.error(f"Error decoding referrer URL: {e}")

    # If session is expired, render error page with details
    if encoded_referrer is not None and is_session_expired(enabled=True):
        return render_template(
            "error_page.html",
            error_title="SESSION EXPIRED",
            error_code="401",
            error_description="Your session expired. Log back into Workload Manager for a new session and try to reload this page.",
            back_link=encoded_referrer,
        )

    # If referrer is provided, and session is renewed, redirect to referrer
    if encoded_referrer is not None:
        return redirect(encoded_referrer)

    # Otherwise, return session status
    return jsonify(
        {
            "status": "Active" if session.get("logged_in") else "Expired",
            "user": session.get("username"),
            "login_time": session.get("login_time"),
            "timezone": session.get("timezone"),
        }
    )
