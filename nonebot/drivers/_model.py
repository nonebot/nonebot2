import abc
from enum import Enum
from http.cookiejar import Cookie, CookieJar
from typing import (
    IO,
    Any,
    Dict,
    List,
    Tuple,
    Union,
    Mapping,
    Iterator,
    Optional,
    MutableMapping,
)

from yarl import URL as URL
from multidict import CIMultiDict

RawURL = Tuple[bytes, bytes, Optional[int], bytes]

SimpleQuery = Union[str, int, float]
QueryVariable = Union[SimpleQuery, List[SimpleQuery]]
QueryTypes = Union[
    None, str, Mapping[str, QueryVariable], List[Tuple[str, QueryVariable]]
]

HeaderTypes = Union[
    None,
    CIMultiDict[str],
    Dict[str, str],
    List[Tuple[str, str]],
]

CookieTypes = Union[None, "Cookies", CookieJar, Dict[str, str], List[Tuple[str, str]]]

ContentTypes = Union[str, bytes, None]
DataTypes = Union[dict, None]
FileContent = Union[IO[bytes], bytes]
FileType = Tuple[Optional[str], FileContent, Optional[str]]
FileTypes = Union[
    # file (or bytes)
    FileContent,
    # (filename, file (or bytes))
    Tuple[Optional[str], FileContent],
    # (filename, file (or bytes), content_type)
    FileType,
]
FilesTypes = Union[Dict[str, FileTypes], List[Tuple[str, FileTypes]], None]


class HTTPVersion(Enum):
    H10 = "1.0"
    H11 = "1.1"
    H2 = "2"


class Request:
    def __init__(
        self,
        method: Union[str, bytes],
        url: Union["URL", str, RawURL],
        *,
        params: QueryTypes = None,
        headers: HeaderTypes = None,
        cookies: CookieTypes = None,
        content: ContentTypes = None,
        data: DataTypes = None,
        json: Any = None,
        files: FilesTypes = None,
        version: Union[str, HTTPVersion] = HTTPVersion.H11,
        timeout: Optional[float] = None,
        proxy: Optional[str] = None,
    ):
        # method
        self.method: str = (
            method.decode("ascii").upper()
            if isinstance(method, bytes)
            else method.upper()
        )
        # http version
        self.version: HTTPVersion = HTTPVersion(version)
        # timeout
        self.timeout: Optional[float] = timeout
        # proxy
        self.proxy: Optional[str] = proxy

        # url
        if isinstance(url, tuple):
            scheme, host, port, path = url
            url = URL.build(
                scheme=scheme.decode("ascii"),
                host=host.decode("ascii"),
                port=port,
                path=path.decode("ascii"),
            )
        else:
            url = URL(url)

        if params is not None:
            url = url.update_query(params)
        self.url: URL = url

        # headers
        self.headers: CIMultiDict[str]
        if headers is not None:
            self.headers = CIMultiDict(headers)
        else:
            self.headers = CIMultiDict()

        # cookies
        self.cookies = Cookies(cookies)

        # body
        self.content: ContentTypes = content
        self.data: DataTypes = data
        self.json: Any = json
        self.files: Optional[List[Tuple[str, FileType]]] = None
        if files:
            self.files = []
            files_ = files.items() if isinstance(files, dict) else files
            for name, file_info in files_:
                if not isinstance(file_info, tuple):
                    self.files.append((name, (None, file_info, None)))
                elif len(file_info) == 2:
                    self.files.append((name, (file_info[0], file_info[1], None)))
                else:
                    self.files.append((name, file_info))  # type: ignore

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        url = str(self.url)
        return f"<{class_name}({self.method!r}, {url!r})>"


class Response:
    def __init__(
        self,
        status_code: int,
        *,
        headers: HeaderTypes = None,
        content: ContentTypes = None,
        request: Optional[Request] = None,
    ):
        # status code
        self.status_code: int = status_code

        # headers
        self.headers: CIMultiDict[str]
        if headers is not None:
            self.headers = CIMultiDict(headers)
        else:
            self.headers = CIMultiDict()

        # body
        self.content: ContentTypes = content

        # request
        self.request: Optional[Request] = request


class WebSocket(abc.ABC):
    def __init__(self, *, request: Request):
        # request
        self.request: Request = request

    @property
    @abc.abstractmethod
    def closed(self) -> bool:
        """
        :类型: ``bool``
        :说明: 连接是否已经关闭
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def accept(self) -> None:
        """接受 WebSocket 连接请求"""
        raise NotImplementedError

    @abc.abstractmethod
    async def close(self, code: int = 1000, reason: str = "") -> None:
        """关闭 WebSocket 连接请求"""
        raise NotImplementedError

    @abc.abstractmethod
    async def receive(self) -> str:
        """接收一条 WebSocket text 信息"""
        raise NotImplementedError

    @abc.abstractmethod
    async def receive_bytes(self) -> bytes:
        """接收一条 WebSocket binary 信息"""
        raise NotImplementedError

    @abc.abstractmethod
    async def send(self, data: str) -> None:
        """发送一条 WebSocket text 信息"""
        raise NotImplementedError

    @abc.abstractmethod
    async def send_bytes(self, data: bytes) -> None:
        """发送一条 WebSocket binary 信息"""
        raise NotImplementedError


class Cookies(MutableMapping):
    def __init__(self, cookies: CookieTypes = None) -> None:
        self.jar: CookieJar = cookies if isinstance(cookies, CookieJar) else CookieJar()
        if cookies is not None and not isinstance(cookies, CookieJar):
            if isinstance(cookies, dict):
                for key, value in cookies.items():
                    self.set(key, value)
            elif isinstance(cookies, list):
                for key, value in cookies:
                    self.set(key, value)
            elif isinstance(cookies, Cookies):
                for cookie in cookies.jar:
                    self.jar.set_cookie(cookie)
            else:
                raise TypeError(f"Cookies must be dict or list, not {type(cookies)}")

    def set(self, name: str, value: str, domain: str = "", path: str = "/") -> None:
        cookie = Cookie(
            version=0,
            name=name,
            value=value,
            port=None,
            port_specified=False,
            domain=domain,
            domain_specified=bool(domain),
            domain_initial_dot=domain.startswith("."),
            path=path,
            path_specified=bool(path),
            secure=False,
            expires=None,
            discard=True,
            comment=None,
            comment_url=None,
            rest={},
            rfc2109=False,
        )
        self.jar.set_cookie(cookie)

    def get(
        self,
        name: str,
        default: Optional[str] = None,
        domain: str = None,
        path: str = None,
    ) -> Optional[str]:
        value: Optional[str] = None
        for cookie in self.jar:
            if (
                cookie.name == name
                and (domain is None or cookie.domain == domain)
                and (path is None or cookie.path == path)
            ):
                if value is not None:
                    message = f"Multiple cookies exist with name={name}"
                    raise ValueError(message)
                value = cookie.value

        return default if value is None else value

    def delete(
        self, name: str, domain: Optional[str] = None, path: Optional[str] = None
    ) -> None:
        if domain is not None and path is not None:
            return self.jar.clear(domain, path, name)

        remove = [
            cookie
            for cookie in self.jar
            if cookie.name == name
            and (domain is None or cookie.domain == domain)
            and (path is None or cookie.path == path)
        ]

        for cookie in remove:
            self.jar.clear(cookie.domain, cookie.path, cookie.name)

    def clear(self, domain: Optional[str] = None, path: Optional[str] = None) -> None:
        self.jar.clear(domain, path)

    def update(self, cookies: CookieTypes = None) -> None:
        cookies = Cookies(cookies)
        for cookie in cookies.jar:
            self.jar.set_cookie(cookie)

    def __setitem__(self, name: str, value: str) -> None:
        return self.set(name, value)

    def __getitem__(self, name: str) -> str:
        value = self.get(name)
        if value is None:
            raise KeyError(name)
        return value

    def __delitem__(self, name: str) -> None:
        return self.delete(name)

    def __len__(self) -> int:
        return len(self.jar)

    def __iter__(self) -> Iterator[Cookie]:
        return (cookie for cookie in self.jar)

    def __repr__(self) -> str:
        cookies_repr = ", ".join(
            [
                f"<Cookie {cookie.name}={cookie.value} for {cookie.domain} />"
                for cookie in self.jar
            ]
        )

        return f"<Cookies [{cookies_repr}]>"
