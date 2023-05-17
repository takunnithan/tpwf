"""
Create a base class with common functions
- Have different types of responses
    - Http
    - Template
    - Json
    - ?????
"""
import http_status
from http_constant import TEXT_HTML


class HttpResponse:
    HTTP_VERSION = "HTTP/1.1"

    def __init__(self, body: str, status_code: int | None = None, headers: dict | None = None):
        self.body = body
        self.status_code = status_code or http_status.HTTP_200_OK
        self.headers = headers or {}

    def _status_line(self) -> str:
        return f"{self.HTTP_VERSION} {self.status_code} {http_status.HTTP_STATUS_TEXT.get(self.status_code, '')}\r\n"

    def _header_lines(self) -> str:
        if "Content-Type" not in self.headers:
            self.headers["Content-Type"] = TEXT_HTML
        header_lines = ""
        for header, value in self.headers.items():
            header_line = f"{header}: {value}\r\n"
            header_lines += header_line
        header_lines += "\r\n"
        return header_lines

    def to_bytes(self):
        return f"{self._status_line()}{self._header_lines()}{self.body}".encode('utf-8')
