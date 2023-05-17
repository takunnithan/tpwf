from http_request import HttpRequest
from http_constant import HTTP_VERBS
from http_exception import HttpParserException


class HttpParser:

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
    def parse(connection_data: str) -> HttpRequest:
        """
            TODO: Write a HTTP parser for this - Preferably a Class with helper functions etc


            TODO:
                -------------------------------------------------------------------------------------------
                1. Parse all Headers -> There must be a way to know when the headers end - MSDN
                2. Support for POST, PATCH, PUT
                3. Parse request body ( handling encoding, content-type( Text, Image, File, Json, Form, ??? )
                -------------------------------------------------------------------------------------------

            GET / HTTP/1.1
            Host: localhost:8000
            Connection: keep-alive
            sec-ch-ua: "Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"
            sec-ch-ua-mobile: ?0
            sec-ch-ua-platform: "Windows"
            Upgrade-Insecure-Requests: 1
            User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36
            Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
            Sec-Fetch-Site: none
            Sec-Fetch-Mode: navigate
            Sec-Fetch-User: ?1
            Sec-Fetch-Dest: document
            Accept-Encoding: gzip, deflate, br
            Accept-Language: en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,ml;q=0.6
        """
        connection_first_line = connection_data.split("\\n")[0]
        http_method = HttpParser._parse_http_verb(connection_first_line)
        route = HttpParser._parse_route(connection_first_line)
        return HttpRequest(http_method, route)
