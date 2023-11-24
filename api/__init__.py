
import logging, json, os

########### SETUP LOGGING #############
logFormatter = logging.Formatter("%(asctime)s -- [%(threadName)-12.12s] -- [%(levelname)-5.5s] in %(module)s -- %(message)s")
log_path = os.path.join("logs",os.getenv("env_name"))

fileHandler = logging.FileHandler(log_path)   # SET LOGGING HANDLER TO WRITE TO A FILE
consoleHandler = logging.StreamHandler()      # SET LOGGING HANDLER TO WRITE TO A FILE

fileHandler.setFormatter(logFormatter)            # FORMAT SETTER
consoleHandler.setFormatter(logFormatter)         # FORMAT SETTER
logging.getLogger().addHandler(consoleHandler)    # ADD THE INDIVIDUAL HANDLERS TO ROOT LOGGER
logging.getLogger().addHandler(fileHandler)       # ADD THE INDIVIDUAL HANDLERS TO ROOT LOGGER
#######################################

from flask import Flask, request, jsonify
from .qna import api as QNAApi

api = Flask(__name__)      # < -------- APP ROOT
api.register_blueprint(QNAApi, url_prefix = "/api/v1") # < -------- Extraction API Registration

"""
# Root Level `before` and `after` request functionality.
# This should be used at higher levels only.
# For any new before/after request Items, create a new method with the decorator.
"""

@api.before_request
def request_logging():
    log_message = ["\n======== Request Interceptor ========",
        " ~~~~ [{}] -- `{}` ~~~~".format(request.method, request.url),
        " ~ Params : {}".format(json.dumps(request.json, indent=3)),
        " ~ Headers : {}".format(json.dumps(dict(request.headers), indent=3)),
        "======== END ========\n"
    ]
    logging.warning("\n".join(log_message))
    ##########################################################################################
    return None

@api.after_request
def response_logging(response):
    log_message = ["\n======== Response Interceptor ========",
    " ~ Data : {}".format(response.get_data().decode(), indent=3),
    " ~ Status : {}".format(response.status, indent=3),
    " ~ Headers : {}".format(json.dumps(dict(response.headers), indent=3)),
    "======== END ========\n"]
    logging.warning("\n".join(log_message))
    return response

###############REGISTER ALL EXCEPTIONS HERE##########################
from lib.exceptions import InvalidFile

@api.errorhandler(InvalidFile)
def api_invalid_token_exception(e):
    return jsonify(e.to_dict()), e.status_code
