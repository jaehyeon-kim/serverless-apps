import os
import base64
import urllib.parse
import typing
from dataclasses import dataclass
from mangum import Mangum
from mangum.types import ASGIApp
from mangum.protocols.http import ASGIHTTPCycle
from mangum.adapter import get_server_and_client


@dataclass
class MangumExt(Mangum):

    api_gateway_base_path: typing.Optional[str] = None

    def strip_base_path(self, event: dict) -> str:
        path_info = event["path"]
        if self.api_gateway_base_path:
            script_name = "/" + self.api_gateway_base_path
            if path_info.startswith(script_name):
                path_info = path_info[len(script_name) :]
        return urllib.parse.unquote(path_info or "/")

    def handle_http(self, event: dict, context: dict) -> dict:
        server, client = get_server_and_client(event)
        headers = event.get("headers", {})
        headers_key_value_pairs = [[k.lower().encode(), v.encode()] for k, v in headers.items()]
        query_string_params = event["queryStringParameters"]
        query_string = (
            urllib.parse.urlencode(query_string_params).encode() if query_string_params else b""
        )
        scope = {
            "type": "http",
            "http_version": "1.1",
            "method": event["httpMethod"],
            "headers": headers_key_value_pairs,
            "path": self.strip_base_path(event),
            "raw_path": None,
            "root_path": "",
            "scheme": headers.get("X-Forwarded-Proto", "https"),
            "query_string": query_string,
            "server": server,
            "client": client,
            "asgi": {"version": "3.0"},
            "aws": {"event": event, "context": context},
        }

        is_binary = event.get("isBase64Encoded", False)
        body = event["body"] or b""
        if is_binary:
            body = base64.b64decode(body)
        elif not isinstance(body, bytes):
            body = body.encode()

        asgi_cycle = ASGIHTTPCycle(scope, is_binary=is_binary, logger=self.logger)
        asgi_cycle.put_message({"type": "http.request", "body": body, "more_body": False})
        response = asgi_cycle(self.app)
        return response
