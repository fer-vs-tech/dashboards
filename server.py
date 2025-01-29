import logging

logger = logging.getLogger(__name__)


from flask import Flask, redirect, request, url_for
from flask_caching import Cache

from cm_dashboards.utilities import (
    enable_session_validity_check,
    encode_and_decode_string,
    is_session_expired,
    set_compress_content,
    set_dash_config,
    set_server_key,
    set_version,
)

server = Flask(__name__, static_url_path="/dash/static")

# Set server key, version and dash configs to server instance
server = set_server_key(server)
server = set_version(server)
server = set_dash_config(server)
server = enable_session_validity_check(server)
server = set_compress_content(server)

# Initialize cache object
cache = Cache(
    server,
    config={
        "CACHE_TYPE": "FileSystemCache",
        "CACHE_DIR": server.config["CACHE_DIR"],
        "CACHE_DEFAULT_TIMEOUT": server.config["CACHE_TIMEOUT"],
        "CACHE_THRESHOLD": server.config["CACHE_THRESHOLD"],
    },
)


@server.before_request
def before_request():
    """
    Check session validity before each request
    """
    # Skip session validity check if disabled
    if not server.config["ENABLE_SESSION_VALIDITY_CHECK"]:
        return

    # Skip dash inner requests
    if (
        "_reload-hash" in request.url
        or "_dash-update-component" in request.url
        or "_dash-dependencies" in request.url
        or "_dash-layout" in request.url
    ):
        return

    # Grab current endpoint and validate session if not in whitelist
    current_endpoint = request.endpoint
    if current_endpoint is not None and current_endpoint not in [
        "alive",
        "static",
        "dash_list",
        "check_session",
        "is_session_valid",
    ]:
        logger.info(f"Current endpoint: {current_endpoint} / URL: {request.url}")
        session_expired = is_session_expired(enabled=True)
        if session_expired:
            logger.info("Session expired, blocking access")
            encoded_url = encode_and_decode_string(request.url)
            return redirect(url_for("is_session_valid", referrer=encoded_url))
        logger.info("Session active, allowing access")
