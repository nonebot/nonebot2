import base64
import json
import socket
from typing import TypeVar, Union

from werkzeug import Request, Response
from werkzeug.datastructures import MultiDict
from wsproto import ConnectionType, WSConnection
from wsproto.events import (
    AcceptConnection,
    BytesMessage,
    CloseConnection,
    Ping,
    TextMessage,
)
from wsproto.events import Request as WSRequest
from wsproto.frame_protocol import CloseReason

K = TypeVar("K")
V = TypeVar("V")


def json_safe(string, content_type="application/octet-stream") -> str:
    try:
        string = string.decode("utf-8")
        json.dumps(string)
        return string
    except (ValueError, TypeError):
        return b"".join(
            [
                b"data:",
                content_type.encode("utf-8"),
                b";base64,",
                base64.b64encode(string),
            ]
        ).decode("utf-8")


def flattern(d: "MultiDict[K, V]") -> dict[K, Union[V, list[V]]]:
    return {k: v[0] if len(v) == 1 else v for k, v in d.to_dict(flat=False).items()}


def http_echo(request: Request) -> Response:
    try:
        _json = json.loads(request.data.decode("utf-8"))
    except (ValueError, TypeError):
        _json = None

    return Response(
        json.dumps(
            {
                "url": request.url,
                "method": request.method,
                "origin": request.headers.get("X-Forwarded-For", request.remote_addr),
                "headers": flattern(
                    MultiDict((k, v) for k, v in request.headers.items())
                ),
                "args": flattern(request.args),
                "form": flattern(request.form),
                "data": json_safe(request.data),
                "json": _json,
                "files": flattern(
                    MultiDict(
                        (
                            k,
                            json_safe(
                                v.read(),
                                request.files[k].content_type
                                or "application/octet-stream",
                            ),
                        )
                        for k, v in request.files.items()
                    )
                ),
            }
        ),
        status=200,
        content_type="application/json",
    )


def websocket_echo(request: Request) -> Response:
    stream = request.environ["werkzeug.socket"]

    ws = WSConnection(ConnectionType.SERVER)

    in_data = b"GET %s HTTP/1.1\r\n" % request.path.encode("utf-8")
    for header, value in request.headers.items():
        in_data += f"{header}: {value}\r\n".encode()
    in_data += b"\r\n"

    ws.receive_data(in_data)

    running: bool = True
    while True:
        out_data = b""

        for event in ws.events():
            if isinstance(event, WSRequest):
                out_data += ws.send(AcceptConnection())
            elif isinstance(event, CloseConnection):
                out_data += ws.send(event.response())
                running = False
            elif isinstance(event, Ping):
                out_data += ws.send(event.response())
            elif isinstance(event, TextMessage):
                if event.data == "quit":
                    out_data += ws.send(
                        CloseConnection(CloseReason.NORMAL_CLOSURE, "bye")
                    )
                    running = False
                else:
                    out_data += ws.send(TextMessage(data=event.data))
            elif isinstance(event, BytesMessage):
                if event.data == b"quit":
                    out_data += ws.send(
                        CloseConnection(CloseReason.NORMAL_CLOSURE, "bye")
                    )
                    running = False
                else:
                    out_data += ws.send(BytesMessage(data=event.data))

        if out_data:
            stream.send(out_data)

        if not running:
            break

        in_data = stream.recv(4096)
        ws.receive_data(in_data)

    stream.shutdown(socket.SHUT_RDWR)
    return Response("", status=204)


@Request.application
def request_handler(request: Request) -> Response:
    if request.headers.get("Connection") == "Upgrade":
        return websocket_echo(request)
    else:
        return http_echo(request)
