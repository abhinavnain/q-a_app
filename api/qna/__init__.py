import flask
from flask import Blueprint, request, Response
from lib.file_processor.remote_file_processor import RemoteFileProcessor

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
    print(request.json)
    file_data = RemoteFileProcessor(request.json["file_path"])
    file_data.get_file()
    print(file_data._file_data)
    resp = flask.make_response({"FOUND":"IT"})
    return resp