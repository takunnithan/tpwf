from http_parser import HttpRequest
from http_response import HttpResponse
from http_status import HTTP_404_NOT_FOUND


class TPWF:
    # TODO: Create a class with a singleton object ???
    #   This is bad - shouldn't be a class level variable.
    function_to_url = {}

    def __init__(self):
        pass

    def add_url_rule(self, rule, request_method, f):
        self.function_to_url[(rule, request_method)] = f

    def route_decorator(self, rule, request_method):
        def decorator(f):
            self.add_url_rule(rule, request_method, f)
            return f
        return decorator

    def get(self, rule):
        return self.route_decorator(rule, 'GET')

    def post(self, rule):
        return self.route_decorator(rule, 'POST')

    def patch(self, rule):
        return self.route_decorator(rule, 'PATCH')

    def delete(self, rule):
        return self.route_decorator(rule, 'DELETE')

    def put(self, rule):
        return self.route_decorator(rule, 'PUT')

    @staticmethod
    def route_request(request: HttpRequest) -> str | HttpResponse:
        handler_func = TPWF.function_to_url.get((request.route, request.http_method))
        if not handler_func:
            return HttpResponse("", HTTP_404_NOT_FOUND)
        return handler_func(request)
