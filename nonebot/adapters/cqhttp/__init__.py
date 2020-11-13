"""
CQHTTP (OneBot) v11 协议适配
============================

协议详情请看: `CQHTTP`_ | `OneBot`_

.. _CQHTTP:
    http://cqhttp.cc/
.. _OneBot:
    https://github.com/howmanybots/onebot
"""

import re
import sys
import hmac
import json
import asyncio

import httpx

from nonebot.log import logger
from nonebot.config import Config
from nonebot.message import handle_event
from nonebot.typing import overrides, Driver, WebSocket, NoReturn
from nonebot.typing import Any, Dict, Union, Tuple, Iterable, Optional
from nonebot.adapters import BaseBot, BaseEvent, BaseMessage, BaseMessageSegment
from nonebot.exception import NetworkError, ActionFailed, RequestDenied, ApiNotAvailable


def log(level: str, message: str):
    """
    :说明:

      用于打印 CQHTTP 日志。

    :参数:

      * ``level: str``: 日志等级
      * ``message: str``: 日志信息
    """
    return logger.opt(colors=True).log(level, "<m>CQHTTP</m> | " + message)


def get_auth_bearer(
        access_token: Optional[str] = None) -> Union[Optional[str], NoReturn]:
    if not access_token:
        return None
    scheme, _, param = access_token.partition(" ")
    if scheme.lower() not in ["bearer", "token"]:
        raise RequestDenied(401, "Not authenticated")
    return param


def escape(s: str, *, escape_comma: bool = True) -> str:
    """
    :说明:

      对字符串进行 CQ 码转义。

    :参数:

      * ``s: str``: 需要转义的字符串
      * ``escape_comma: bool``: 是否转义逗号（``,``）。
    """
    s = s.replace("&", "&amp;") \
        .replace("[", "&#91;") \
        .replace("]", "&#93;")
    if escape_comma:
        s = s.replace(",", "&#44;")
    return s


def unescape(s: str) -> str:
    """
    :说明:

      对字符串进行 CQ 码去转义。

    :参数:

      * ``s: str``: 需要转义的字符串
    """
    return s.replace("&#44;", ",") \
        .replace("&#91;", "[") \
        .replace("&#93;", "]") \
        .replace("&amp;", "&")


def _b2s(b: Optional[bool]) -> Optional[str]:
    """转换布尔值为字符串。"""
    return b if b is None else str(b).lower()


async def _check_reply(bot: "Bot", event: "Event"):
    """
    :说明:

      检查消息中存在的回复，去除并赋值 ``event.reply``, ``event.to_me``

    :参数:

      * ``bot: Bot``: Bot 对象
      * ``event: Event``: Event 对象
    """
    if event.type != "message":
        return

    try:
        index = list(map(lambda x: x.type == "reply",
                         event.message)).index(True)
    except ValueError:
        return
    msg_seg = event.message[index]
    event.reply = await bot.get_msg(message_id=msg_seg.data["id"])
    if event.reply["sender"]["user_id"] == event.self_id:
        event.to_me = True
    del event.message[index]
    if not event.message:
        event.message.append(MessageSegment.text(""))


def _check_at_me(bot: "Bot", event: "Event"):
    """
    :说明:

      检查消息开头或结尾是否存在 @机器人，去除并赋值 ``event.to_me``

    :参数:

      * ``bot: Bot``: Bot 对象
      * ``event: Event``: Event 对象
    """
    if event.type != "message":
        return

    if event.detail_type == "private":
        event.to_me = True
    else:
        at_me_seg = MessageSegment.at(event.self_id)

        # check the first segment
        if event.message[0] == at_me_seg:
            event.to_me = True
            del event.message[0]
            if event.message[0].type == "text":
                event.message[0].data["text"] = event.message[0].data[
                    "text"].lstrip()
                if not event.message[0].data["text"]:
                    del event.message[0]
            if event.message[0] == at_me_seg:
                del event.message[0]
                if event.message[0].type == "text":
                    event.message[0].data["text"] = event.message[0].data[
                        "text"].lstrip()
                    if not event.message[0].data["text"]:
                        del event.message[0]

        if not event.to_me:
            # check the last segment
            i = -1
            last_msg_seg = event.message[i]
            if last_msg_seg.type == "text" and \
                    not last_msg_seg.data["text"].strip() and \
                    len(event.message) >= 2:
                i -= 1
                last_msg_seg = event.message[i]

            if last_msg_seg == at_me_seg:
                event.to_me = True
                del event.message[i:]

        if not event.message:
            event.message.append(MessageSegment.text(""))


def _check_nickname(bot: "Bot", event: "Event"):
    """
    :说明:

      检查消息开头是否存在，去除并赋值 ``event.to_me``

    :参数:

      * ``bot: Bot``: Bot 对象
      * ``event: Event``: Event 对象
    """
    if event.type != "message":
        return

    first_msg_seg = event.message[0]
    if first_msg_seg.type != "text":
        return

    first_text = first_msg_seg.data["text"]

    nicknames = set(filter(lambda n: n, bot.config.nickname))
    if nicknames:
        # check if the user is calling me with my nickname
        nickname_regex = "|".join(nicknames)
        m = re.search(rf"^({nickname_regex})([\s,，]*|$)", first_text,
                      re.IGNORECASE)
        if m:
            nickname = m.group(1)
            log("DEBUG", f"User is calling me {nickname}")
            event.to_me = True
            first_msg_seg.data["text"] = first_text[m.end():]


def _handle_api_result(
        result: Optional[Dict[str, Any]]) -> Union[Any, NoReturn]:
    """
    :说明:

      处理 API 请求返回值。

    :参数:

      * ``result: Optional[Dict[str, Any]]``: API 返回数据

    :返回:

        - ``Any``: API 调用返回数据

    :异常:

        - ``ActionFailed``: API 调用失败
    """
    if isinstance(result, dict):
        if result.get("status") == "failed":
            raise ActionFailed(retcode=result.get("retcode"))
        return result.get("data")


class ResultStore:
    _seq = 1
    _futures: Dict[int, asyncio.Future] = {}

    @classmethod
    def get_seq(cls) -> int:
        s = cls._seq
        cls._seq = (cls._seq + 1) % sys.maxsize
        return s

    @classmethod
    def add_result(cls, result: Dict[str, Any]):
        if isinstance(result.get("echo"), dict) and \
                isinstance(result["echo"].get("seq"), int):
            future = cls._futures.get(result["echo"]["seq"])
            if future:
                future.set_result(result)

    @classmethod
    async def fetch(cls, seq: int, timeout: Optional[float]) -> Dict[str, Any]:
        future = asyncio.get_event_loop().create_future()
        cls._futures[seq] = future
        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.TimeoutError:
            raise NetworkError("WebSocket API call timeout") from None
        finally:
            del cls._futures[seq]


class Bot(BaseBot):
    """
    CQHTTP 协议 Bot 适配。继承属性参考 `BaseBot <./#class-basebot>`_ 。
    """

    def __init__(self,
                 driver: Driver,
                 connection_type: str,
                 config: Config,
                 self_id: str,
                 *,
                 websocket: Optional[WebSocket] = None):

        super().__init__(driver,
                         connection_type,
                         config,
                         self_id,
                         websocket=websocket)

    @property
    @overrides(BaseBot)
    def type(self) -> str:
        """
        - 返回: ``"cqhttp"``
        """
        return "cqhttp"

    @classmethod
    @overrides(BaseBot)
    async def check_permission(cls, driver: Driver, connection_type: str,
                               headers: dict,
                               body: Optional[dict]) -> Union[str, NoReturn]:
        """
        :说明:
          CQHTTP (OneBot) 协议鉴权。参考 `鉴权 <https://github.com/howmanybots/onebot/blob/master/v11/specs/communication/authorization.md>`_
        """
        x_self_id = headers.get("x-self-id")
        x_signature = headers.get("x-signature")
        access_token = get_auth_bearer(headers.get("authorization"))

        # 检查连接方式
        if connection_type not in ["http", "websocket"]:
            log("WARNING", "Unsupported connection type")
            raise RequestDenied(405, "Unsupported connection type")

        # 检查self_id
        if not x_self_id:
            log("WARNING", "Missing X-Self-ID Header")
            raise RequestDenied(400, "Missing X-Self-ID Header")

        # 检查签名
        secret = driver.config.secret
        if secret and connection_type == "http":
            if not x_signature:
                log("WARNING", "Missing Signature Header")
                raise RequestDenied(401, "Missing Signature")
            sig = hmac.new(secret.encode("utf-8"),
                           json.dumps(body).encode(), "sha1").hexdigest()
            if x_signature != "sha1=" + sig:
                log("WARNING", "Signature Header is invalid")
                raise RequestDenied(403, "Signature is invalid")

        access_token = driver.config.access_token
        if access_token and access_token != access_token:
            log(
                "WARNING", "Authorization Header is invalid"
                if access_token else "Missing Authorization Header")
            raise RequestDenied(
                403, "Authorization Header is invalid"
                if access_token else "Missing Authorization Header")
        return str(x_self_id)

    @overrides(BaseBot)
    async def handle_message(self, message: dict):
        """
        :说明:

          调用 `_check_reply <#async-check-reply-bot-event>`_, `_check_at_me <#check-at-me-bot-event>`_, `_check_nickname <#check-nickname-bot-event>`_ 处理事件并转换为 `Event <#class-event>`_
        """
        if not message:
            return

        if "post_type" not in message:
            ResultStore.add_result(message)
            return

        try:
            event = Event(message)

            # Check whether user is calling me
            await _check_reply(self, event)
            _check_at_me(self, event)
            _check_nickname(self, event)

            await handle_event(self, event)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                f"<r><bg #f8bbd0>Failed to handle event. Raw: {message}</bg #f8bbd0></r>"
            )

    @overrides(BaseBot)
    async def call_api(self, api: str, **data) -> Union[Any, NoReturn]:
        """
        :说明:

          调用 CQHTTP 协议 API

        :参数:

          * ``api: str``: API 名称
          * ``**data: Any``: API 参数

        :返回:

          - ``Any``: API 调用返回数据

        :异常:

          - ``NetworkError``: 网络错误
          - ``ActionFailed``: API 调用失败
        """
        if "self_id" in data:
            self_id = data.pop("self_id")
            if self_id:
                bot = self.driver.bots[str(self_id)]
                return await bot.call_api(api, **data)

        log("DEBUG", f"Calling API <y>{api}</y>")
        if self.connection_type == "websocket":
            seq = ResultStore.get_seq()
            await self.websocket.send({
                "action": api,
                "params": data,
                "echo": {
                    "seq": seq
                }
            })
            return _handle_api_result(await ResultStore.fetch(
                seq, self.config.api_timeout))

        elif self.connection_type == "http":
            api_root = self.config.api_root.get(self.self_id)
            if not api_root:
                raise ApiNotAvailable
            elif not api_root.endswith("/"):
                api_root += "/"

            headers = {}
            if self.config.access_token is not None:
                headers["Authorization"] = "Bearer " + self.config.access_token

            try:
                async with httpx.AsyncClient(headers=headers) as client:
                    response = await client.post(
                        api_root + api,
                        json=data,
                        timeout=self.config.api_timeout)

                if 200 <= response.status_code < 300:
                    result = response.json()
                    return _handle_api_result(result)
                raise NetworkError(f"HTTP request received unexpected "
                                   f"status code: {response.status_code}")
            except httpx.InvalidURL:
                raise NetworkError("API root url invalid")
            except httpx.HTTPError:
                raise NetworkError("HTTP request failed")

    @overrides(BaseBot)
    async def send(self,
                   event: "Event",
                   message: Union[str, "Message", "MessageSegment"],
                   at_sender: bool = False,
                   **kwargs) -> Union[Any, NoReturn]:
        """
        :说明:

          根据 ``event``  向触发事件的主体发送消息。

        :参数:

          * ``event: Event``: Event 对象
          * ``message: Union[str, Message, MessageSegment]``: 要发送的消息
          * ``at_sender: bool``: 是否 @ 事件主体
          * ``**kwargs``: 覆盖默认参数

        :返回:

          - ``Any``: API 调用返回数据

        :异常:

          - ``ValueError``: 缺少 ``user_id``, ``group_id``
          - ``NetworkError``: 网络错误
          - ``ActionFailed``: API 调用失败
        """
        msg = message if isinstance(message, Message) else Message(message)

        at_sender = at_sender and bool(event.user_id)

        params = {}
        if event.user_id:
            params["user_id"] = event.user_id
        if event.group_id:
            params["group_id"] = event.group_id
        params.update(kwargs)

        if "message_type" not in params:
            if "group_id" in params:
                params["message_type"] = "group"
            elif "user_id" in params:
                params["message_type"] = "private"
            else:
                raise ValueError("Cannot guess message type to reply!")

        if at_sender and params["message_type"] != "private":
            params["message"] = MessageSegment.at(params["user_id"]) + \
                MessageSegment.text(" ") + msg
        else:
            params["message"] = msg
        return await self.send_msg(**params)


class Event(BaseEvent):
    """
    CQHTTP 协议 Event 适配。继承属性参考 `BaseEvent <./#class-baseevent>`_ 。
    """

    def __init__(self, raw_event: dict):
        if "message" in raw_event:
            raw_event["message"] = Message(raw_event["message"])

        super().__init__(raw_event)

    @property
    @overrides(BaseEvent)
    def id(self) -> Optional[int]:
        """
        - 类型: ``Optional[int]``
        - 说明: 事件/消息 ID
        """
        return self._raw_event.get("message_id") or self._raw_event.get("flag")

    @property
    @overrides(BaseEvent)
    def name(self) -> str:
        """
        - 类型: ``str``
        - 说明: 事件名称，由类型与 ``.`` 组合而成
        """
        n = self.type + "." + self.detail_type
        if self.sub_type:
            n += "." + self.sub_type
        return n

    @property
    @overrides(BaseEvent)
    def self_id(self) -> str:
        """
        - 类型: ``str``
        - 说明: 机器人自身 ID
        """
        return str(self._raw_event["self_id"])

    @property
    @overrides(BaseEvent)
    def time(self) -> int:
        """
        - 类型: ``int``
        - 说明: 事件发生时间
        """
        return self._raw_event["time"]

    @property
    @overrides(BaseEvent)
    def type(self) -> str:
        """
        - 类型: ``str``
        - 说明: 事件类型
        """
        return self._raw_event["post_type"]

    @type.setter
    @overrides(BaseEvent)
    def type(self, value) -> None:
        self._raw_event["post_type"] = value

    @property
    @overrides(BaseEvent)
    def detail_type(self) -> str:
        """
        - 类型: ``str``
        - 说明: 事件详细类型
        """
        return self._raw_event[f"{self.type}_type"]

    @detail_type.setter
    @overrides(BaseEvent)
    def detail_type(self, value) -> None:
        self._raw_event[f"{self.type}_type"] = value

    @property
    @overrides(BaseEvent)
    def sub_type(self) -> Optional[str]:
        """
        - 类型: ``Optional[str]``
        - 说明: 事件子类型
        """
        return self._raw_event.get("sub_type")

    @sub_type.setter
    @overrides(BaseEvent)
    def sub_type(self, value) -> None:
        self._raw_event["sub_type"] = value

    @property
    @overrides(BaseEvent)
    def user_id(self) -> Optional[int]:
        """
        - 类型: ``Optional[int]``
        - 说明: 事件主体 ID
        """
        return self._raw_event.get("user_id")

    @user_id.setter
    @overrides(BaseEvent)
    def user_id(self, value) -> None:
        self._raw_event["user_id"] = value

    @property
    @overrides(BaseEvent)
    def group_id(self) -> Optional[int]:
        """
        - 类型: ``Optional[int]``
        - 说明: 事件主体群 ID
        """
        return self._raw_event.get("group_id")

    @group_id.setter
    @overrides(BaseEvent)
    def group_id(self, value) -> None:
        self._raw_event["group_id"] = value

    @property
    @overrides(BaseEvent)
    def to_me(self) -> Optional[bool]:
        """
        - 类型: ``Optional[bool]``
        - 说明: 消息是否与机器人相关
        """
        return self._raw_event.get("to_me")

    @to_me.setter
    @overrides(BaseEvent)
    def to_me(self, value) -> None:
        self._raw_event["to_me"] = value

    @property
    @overrides(BaseEvent)
    def message(self) -> Optional["Message"]:
        """
        - 类型: ``Optional[Message]``
        - 说明: 消息内容
        """
        return self._raw_event.get("message")

    @message.setter
    @overrides(BaseEvent)
    def message(self, value) -> None:
        self._raw_event["message"] = value

    @property
    @overrides(BaseEvent)
    def reply(self) -> Optional[dict]:
        """
        - 类型: ``Optional[dict]``
        - 说明: 回复消息详情
        """
        return self._raw_event.get("reply")

    @reply.setter
    @overrides(BaseEvent)
    def reply(self, value) -> None:
        self._raw_event["reply"] = value

    @property
    @overrides(BaseEvent)
    def raw_message(self) -> Optional[str]:
        """
        - 类型: ``Optional[str]``
        - 说明: 原始消息
        """
        return self._raw_event.get("raw_message")

    @raw_message.setter
    @overrides(BaseEvent)
    def raw_message(self, value) -> None:
        self._raw_event["raw_message"] = value

    @property
    @overrides(BaseEvent)
    def plain_text(self) -> Optional[str]:
        """
        - 类型: ``Optional[str]``
        - 说明: 纯文本消息内容
        """
        return self.message and self.message.extract_plain_text()

    @property
    @overrides(BaseEvent)
    def sender(self) -> Optional[dict]:
        """
        - 类型: ``Optional[dict]``
        - 说明: 消息发送者信息
        """
        return self._raw_event.get("sender")

    @sender.setter
    @overrides(BaseEvent)
    def sender(self, value) -> None:
        self._raw_event["sender"] = value


class MessageSegment(BaseMessageSegment):
    """
    CQHTTP 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。
    """

    @overrides(BaseMessageSegment)
    def __init__(self, type: str, data: Dict[str, Any]) -> None:
        if type == "text":
            data["text"] = unescape(data["text"])
        super().__init__(type=type, data=data)

    @overrides(BaseMessageSegment)
    def __str__(self):
        type_ = self.type
        data = self.data.copy()

        # process special types
        if type_ == "text":
            return escape(
                data.get("text", ""),  # type: ignore
                escape_comma=False)

        params = ",".join(
            [f"{k}={escape(str(v))}" for k, v in data.items() if v is not None])
        return f"[CQ:{type_}{',' if params else ''}{params}]"

    @overrides(BaseMessageSegment)
    def __add__(self, other) -> "Message":
        return Message(self) + other

    @staticmethod
    def anonymous(ignore_failure: Optional[bool] = None) -> "MessageSegment":
        return MessageSegment("anonymous", {"ignore": _b2s(ignore_failure)})

    @staticmethod
    def at(user_id: Union[int, str]) -> "MessageSegment":
        return MessageSegment("at", {"qq": str(user_id)})

    @staticmethod
    def contact_group(group_id: int) -> "MessageSegment":
        return MessageSegment("contact", {"type": "group", "id": str(group_id)})

    @staticmethod
    def contact_user(user_id: int) -> "MessageSegment":
        return MessageSegment("contact", {"type": "qq", "id": str(user_id)})

    @staticmethod
    def dice() -> "MessageSegment":
        return MessageSegment("dice", {})

    @staticmethod
    def face(id_: int) -> "MessageSegment":
        return MessageSegment("face", {"id": str(id_)})

    @staticmethod
    def forward(id_: str) -> "MessageSegment":
        log("WARNING", "Forward Message only can be received!")
        return MessageSegment("forward", {"id": id_})

    @staticmethod
    def image(file: str,
              type_: Optional[str] = None,
              cache: bool = True,
              proxy: bool = True,
              timeout: Optional[int] = None) -> "MessageSegment":
        return MessageSegment(
            "image", {
                "file": file,
                "type": type_,
                "cache": cache,
                "proxy": proxy,
                "timeout": timeout
            })

    @staticmethod
    def json(data: str) -> "MessageSegment":
        return MessageSegment("json", {"data": data})

    @staticmethod
    def location(latitude: float,
                 longitude: float,
                 title: Optional[str] = None,
                 content: Optional[str] = None) -> "MessageSegment":
        return MessageSegment(
            "location", {
                "lat": str(latitude),
                "lon": str(longitude),
                "title": title,
                "content": content
            })

    @staticmethod
    def music(type_: str, id_: int) -> "MessageSegment":
        return MessageSegment("music", {"type": type_, "id": id_})

    @staticmethod
    def music_custom(url: str,
                     audio: str,
                     title: str,
                     content: Optional[str] = None,
                     img_url: Optional[str] = None) -> "MessageSegment":
        return MessageSegment(
            "music", {
                "type": "custom",
                "url": url,
                "audio": audio,
                "title": title,
                "content": content,
                "image": img_url
            })

    @staticmethod
    def node(id_: int) -> "MessageSegment":
        return MessageSegment("node", {"id": str(id_)})

    @staticmethod
    def node_custom(user_id: int, nickname: str,
                    content: Union[str, "Message"]) -> "MessageSegment":
        return MessageSegment("node", {
            "user_id": str(user_id),
            "nickname": nickname,
            "content": content
        })

    @staticmethod
    def poke(type_: str, id_: str) -> "MessageSegment":
        return MessageSegment("poke", {"type": type_, "id": id_})

    @staticmethod
    def record(file: str,
               magic: Optional[bool] = None,
               cache: Optional[bool] = None,
               proxy: Optional[bool] = None,
               timeout: Optional[int] = None) -> "MessageSegment":
        return MessageSegment("record", {"file": file, "magic": _b2s(magic)})

    @staticmethod
    def reply(id_: int) -> "MessageSegment":
        return MessageSegment("reply", {"id": str(id_)})

    @staticmethod
    def rps() -> "MessageSegment":
        return MessageSegment("rps", {})

    @staticmethod
    def shake() -> "MessageSegment":
        return MessageSegment("shake", {})

    @staticmethod
    def share(url: str = "",
              title: str = "",
              content: Optional[str] = None,
              img_url: Optional[str] = None) -> "MessageSegment":
        return MessageSegment("share", {
            "url": url,
            "title": title,
            "content": content,
            "img_url": img_url
        })

    @staticmethod
    def text(text: str) -> "MessageSegment":
        return MessageSegment("text", {"text": text})

    @staticmethod
    def video(file: str,
              cache: Optional[bool] = None,
              proxy: Optional[bool] = None,
              timeout: Optional[int] = None) -> "MessageSegment":
        return MessageSegment("video", {
            "file": file,
            "cache": cache,
            "proxy": proxy,
            "timeout": timeout
        })

    @staticmethod
    def xml(data: str) -> "MessageSegment":
        return MessageSegment("xml", {"data": data})


class Message(BaseMessage):
    """
    CQHTTP 协议 Message 适配。
    """

    @staticmethod
    @overrides(BaseMessage)
    def _construct(msg: Union[str, dict, list]) -> Iterable[MessageSegment]:
        if isinstance(msg, dict):
            yield MessageSegment(msg["type"], msg.get("data") or {})
            return
        elif isinstance(msg, list):
            for seg in msg:
                yield MessageSegment(seg["type"], seg.get("data") or {})
            return

        def _iter_message(msg: str) -> Iterable[Tuple[str, str]]:
            text_begin = 0
            for cqcode in re.finditer(
                    r"\[CQ:(?P<type>[a-zA-Z0-9-_.]+)"
                    r"(?P<params>"
                    r"(?:,[a-zA-Z0-9-_.]+=?[^,\]]*)*"
                    r"),?\]", msg):
                yield "text", unescape(msg[text_begin:cqcode.pos +
                                           cqcode.start()])
                text_begin = cqcode.pos + cqcode.end()
                yield cqcode.group("type"), cqcode.group("params").lstrip(",")
            yield "text", unescape(msg[text_begin:])

        for type_, data in _iter_message(msg):
            if type_ == "text":
                if data:
                    # only yield non-empty text segment
                    yield MessageSegment(type_, {"text": data})
            else:
                data = {
                    k: v for k, v in map(
                        lambda x: x.split("=", maxsplit=1),
                        filter(lambda x: x, (
                            x.lstrip() for x in data.split(","))))
                }
                yield MessageSegment(type_, data)
