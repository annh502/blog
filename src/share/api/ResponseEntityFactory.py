from werkzeug.exceptions import Unauthorized, BadRequest, InternalServerError
from . import ResponseBody


def unauthorized(message):
    response_body = ResponseBody.ResponseBody(message, "UNAUTHORIZED", None)
    return response_body.to_dict(), Unauthorized.code


def bad_request(message, data=None):

    response_body = ResponseBody.ResponseBody(message, "BAD REQUEST", data)
    return response_body.to_dict(), BadRequest.code


def ok(data):
    response_body = ResponseBody.ResponseBody("Success", "SUCCESS", data)
    return response_body.to_dict(), 200


def internal_server_error(message):
    response_body = ResponseBody.ResponseBody(message, "INTERNAL SERVER ERROR", None)
    return response_body.to_dict(), InternalServerError.code
