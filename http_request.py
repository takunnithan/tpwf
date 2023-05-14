class HttpRequest:
    def __init__(self, http_method, route):
        self.http_method = http_method
        self.route = route

    def __repr__(self):
        return f"HttpRequest({self.http_method}, {self.route})"
