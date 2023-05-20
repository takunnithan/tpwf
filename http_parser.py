from http_request import HttpRequest
from http_constant import HTTP_VERBS
from http_exception import HttpParserException


class HttpParser:

    @staticmethod
    def _parse_start_line(data_string: str):
        http_verb = HttpParser._parse_http_verb(data_string)
        route = HttpParser._parse_route(data_string)
        return http_verb, route

    @staticmethod
    def _parse_http_verb(data_string: str) -> str:
        """ Parsing `GET / HTTP/1.1` """
        values = data_string.split(" ")
        if values[0] not in HTTP_VERBS:
            raise HttpParserException(f"Invalid Http Verb : {values[0]}")
        return HTTP_VERBS[values[0]]

    @staticmethod
    def _parse_route(data_string: str) -> str:
        """ Parsing `GET / HTTP/1.1` """
        values = data_string.split(" ")
        return values[1]

    @staticmethod
    def _parse_http_request_body(data_string: str | list, content_type: str):
        """ Parse body from a Http request."""
        if content_type.startswith("text"):
            body = ""
            for line in data_string:
                body += line.strip() + "\n"
            return body
        elif content_type == "application/x-www-form-urlencoded":
            key_value_pairs = data_string[0].strip().split("&")
            key_value_dict = {}
            for key_value in key_value_pairs:
                items = key_value.split("=")
                key_value_dict[items[0]] = items[1]
            return key_value_dict
        elif content_type.startswith("multipart/form-data"):
            boundary = content_type.split("=")[1].strip()
            form_items = {}
            key, value = None, None
            for line in data_string[1:]:
                if boundary in line:
                    form_items[key] = value
                else:
                    if "name" in line:
                        key = line.split("=")[1].replace('"', '')
                    else:
                        value = line.strip()
            return form_items

        elif content_type.startswith("application"):
            body = ""
            for line in data_string:
                body += line.strip()
            return body

        # TODO: Raise a HTTP 400 error here
        raise HttpParserException(f"Unknown Content-Type {content_type}")

    @staticmethod
    def parse(connection_data: str) -> HttpRequest:
        """
            TODO:
                2. Handle - binary - files

        """
        http_request_lines = connection_data.split("\r\n")
        http_method, route = HttpParser._parse_start_line(http_request_lines[0])
        http_headers = {}
        body_start_index = 0
        for index, line in enumerate(http_request_lines[1:], 1):
            if not line:
                body_start_index = index + 1
                break
            key_value = line.split(":")
            http_headers[key_value[0]] = key_value[1].strip()
        http_body = None
        if "Content-Type" in http_headers:
            http_body = HttpParser._parse_http_request_body(
                http_request_lines[body_start_index:],
                http_headers["Content-Type"]
            )
        return HttpRequest(http_method, route, http_headers, http_body)
