from flask import make_response


class ResponseBody:
    def __init__(self, message, code, data):
        self.message = message
        self.code = code
        self.data = data

    def to_dict(self):
        return make_response(
            {
                "message": self.message,
                "code": self.code,
                "data": self.data
            }
        )