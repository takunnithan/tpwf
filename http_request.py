class HttpRequest:
    def __init__(self, http_method, route, http_headers, http_body):
        self.http_method = http_method
        self.route = route
        self.headers = http_headers
        self.body = http_body

    def __repr__(self):
        return f"HttpRequest({self.http_method}, {self.route})"

    def print_request(self):
        print("------------------------------------------------------------------")
        print(self.http_method, self.route)
        print(self.headers)
        print(self.body)
        print("------------------------------------------------------------------")