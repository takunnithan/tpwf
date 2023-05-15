from http_parser import HttpRequest


class TPWF:
    # TODO: Create a class with a singleton object ???
    #   This is bad - shouldn't be a class level variable.
    function_to_url = {}

    def __init__(self):
        pass

    def add_url_rule(self, rule, f):
        self.function_to_url[rule] = f

    def get(self, rule):
        def decorator(f):
            self.add_url_rule(rule, f)
            return f
        return decorator

    @staticmethod
    def route_request(request: HttpRequest) -> str:
        route = request.route
        handler_func = TPWF.function_to_url.get(route)
        if not handler_func:  # Handle this properly with HTTP 404
            return ""
        return handler_func()
