"""
Create a base class with common functions
- Have different types of responses
    - Http
    - Template
    - Json
    - ?????
"""


class HttpResponse:
    def __init__(self, data):
        self.data = data

    # TODO:
    #   The following should be customizable
    #       1. Status code
    #       2. Headers
    #       3. Content

    def to_bytes(self):
        # "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, world!"
        return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{self.data}".encode('utf-8')
