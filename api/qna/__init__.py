import flask, logging
from flask import Blueprint, request, Response
#from lib.file_processor.remote_file_processor import RemoteFileProcessor
from lib.lanchain_utils.lanchain_simple_pipeline import LangchainSimplePipeline

"""
    GUIDE - 
    The API is being served with /api/v1 prefix. The API by default will consume parameters
    from URL for routing the request to correct extraction logic.
    
    By default all extraction triggers will be post requests, and the response object will
    contain only generic information such as dataset id and job id
    /jdpower/document_title/23/1
"""

api = Blueprint("Question&AnswerAPI",__name__)
@api.route('/ask', methods = ["POST"])
def ask():
    file_type = request.json['file_path'].split(".")[-1].lower()
    lcp = LangchainSimplePipeline(request.json['file_path'], file_type)
    response = []
    for question in request.json['questions']:
        answer = lcp.ask(question)
        logging.warning("Q: {}".format(question))
        logging.warning("A: {}".format(answer))
        response.append({question : answer})
    resp = flask.make_response(response)
    return resp