import json
import base64
from typing import Dict, List, Union, TypeVar

from werkzeug import Request, Response
from werkzeug.datastructures import MultiDict

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


def flattern(d: "MultiDict[K, V]") -> Dict[K, Union[V, List[V]]]:
    return {k: v[0] if len(v) == 1 else v for k, v in d.to_dict(flat=False).items()}


@Request.application
def request_handler(request: Request) -> Response:
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
