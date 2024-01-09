class ResponseOk:

    @classmethod
    def without_results(cls, code, message):
        response = {
            "code": code,
            "message": message
        }, 200
        return response

class ResponseErrorBadRequest:

    @classmethod
    def with_results(cls, error, message, details):
        response = {
            "error": error,
            "message": message,
            "details": details
        }, 422
        return response

class ResponseError:

    @classmethod
    def with_results(cls, error, message, details):
        response = {
            "error": error,
            "message": message,
            "details": details
        }, 500
        return response