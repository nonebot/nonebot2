import asyncio

from nonebot.config import Config
from nonebot.adapters import BaseBot
from nonebot.typing import Any, Dict, List, Union, Driver, Optional, NoReturn, WebSocket, Iterable


def log(level: str, message: str):
    ...


def escape(s: str, *, escape_comma: bool = ...) -> str:
    ...


def unescape(s: str) -> str:
    ...


def _b2s(b: Optional[bool]) -> Optional[str]:
    ...


async def _check_reply(bot: "Bot", event: "Event"):
    ...


def _check_at_me(bot: "Bot", event: "Event"):
    ...


def _check_nickname(bot: "Bot", event: "Event"):
    ...


def _handle_api_result(
        result: Optional[Dict[str, Any]]) -> Union[Any, NoReturn]:
    ...


class ResultStore:
    _seq: int = ...
    _futures: Dict[int, asyncio.Future] = ...

    @classmethod
    def get_seq(cls) -> int:
        ...

    @classmethod
    def add_result(cls, result: Dict[str, Any]):
        ...

    @classmethod
    async def fetch(cls, seq: int, timeout: Optional[float]) -> Dict[str, Any]:
        ...


class Bot(BaseBot):

    def __init__(self,
                 driver: Driver,
                 connection_type: str,
                 config: Config,
                 self_id: str,
                 *,
                 websocket: WebSocket = None):
        ...

    def type(self) -> str:
        ...

    async def handle_message(self, message: dict):
        ...

    async def call_api(self, api: str, **data) -> Union[Any, NoReturn]:
        ...

    async def send(self, event: "Event", message: Union[str, "Message",
                                                        "MessageSegment"],
                   **kwargs) -> Union[Any, NoReturn]:
        ...

    async def send_private_msg(self,
                               *,
                               user_id: int,
                               message: Union[str, Message],
                               auto_escape: bool = ...,
                               self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :说明:

          发送私聊消息。

        :参数:

          * ``user_id``: 对方 QQ 号
          * ``message``: 要发送的内容
          * ``auto_escape``: 消息内容是否作为纯文本发送（即不解析 CQ 码），只在 ``message`` 字段是字符串时有效
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def send_group_msg(self,
                             *,
                             group_id: int,
                             message: Union[str, Message],
                             auto_escape: bool = ...,
                             self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :说明:

          发送群消息。

        :参数:

          * ``group_id``: 群号
          * ``message``: 要发送的内容
          * ``auto_escape``: 消息内容是否作为纯文本发送（即不解析 CQ 码），只在 ``message`` 字段是字符串时有效
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def send_msg(self,
                       *,
                       message_type: Optional[str] = ...,
                       user_id: Optional[int] = ...,
                       group_id: Optional[int] = ...,
                       message: Union[str, Message],
                       auto_escape: bool = ...,
                       self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :说明:

          发送消息。

        :参数:

          * ``message_type``: 消息类型，支持 ``private``、``group``，分别对应私聊、群组、讨论组，如不传入，则根据传入的 ``*_id`` 参数判断
          * ``user_id``: 对方 QQ 号（消息类型为 ``private`` 时需要）
          * ``group_id``: 群号（消息类型为 ``group`` 时需要）
          * ``message``: 要发送的内容
          * ``auto_escape``: 消息内容是否作为纯文本发送（即不解析 CQ 码），只在 ``message`` 字段是字符串时有效
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def delete_msg(self,
                         *,
                         message_id: int,
                         self_id: Optional[int] = ...) -> None:
        """
        :说明:

          撤回消息。

        :参数:

          * ``message_id``: 消息 ID
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def get_msg(self,
                      *,
                      message_id: int,
                      self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :说明:

          获取消息。

        :参数:

          * ``message_id``: 消息 ID
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def get_forward_msg(self,
                              *,
                              id: int,
                              self_id: Optional[int] = ...) -> None:
        """
        :说明:

          获取合并转发消息。

        :参数:

          * ``id``: 合并转发 ID
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def send_like(self,
                        *,
                        user_id: int,
                        times: int = ...,
                        self_id: Optional[int] = ...) -> None:
        """
        :说明:

          发送好友赞。

        :参数:

          * ``user_id``: 对方 QQ 号
          * ``times``: 赞的次数，每个好友每天最多 10 次
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def set_group_kick(self,
                             *,
                             group_id: int,
                             user_id: int,
                             reject_add_request: bool = ...,
                             self_id: Optional[int] = ...) -> None:
        """
        :说明:

          群组踢人。

        :参数:

          * ``group_id``: 群号
          * ``user_id``: 要踢的 QQ 号
          * ``reject_add_request``: 拒绝此人的加群请求
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def set_group_ban(self,
                            *,
                            group_id: int,
                            user_id: int,
                            duration: int = ...,
                            self_id: Optional[int] = ...) -> None:
        """
        :说明:

          群组单人禁言。

        :参数:

          * ``group_id``: 群号
          * ``user_id``: 要禁言的 QQ 号
          * ``duration``: 禁言时长，单位秒，``0`` 表示取消禁言
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def set_group_anonymous_ban(self,
                                      *,
                                      group_id: int,
                                      anonymous: Optional[Dict[str, Any]] = ...,
                                      anonymous_flag: Optional[str] = ...,
                                      duration: int = ...,
                                      self_id: Optional[int] = ...) -> None:
        """
        :说明:

          群组匿名用户禁言。

        :参数:

          * ``group_id``: 群号
          * ``anonymous``: 可选，要禁言的匿名用户对象（群消息上报的 ``anonymous`` 字段）
          * ``anonymous_flag``: 可选，要禁言的匿名用户的 flag（需从群消息上报的数据中获得）
          * ``duration``: 禁言时长，单位秒，无法取消匿名用户禁言
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def set_group_whole_ban(self,
                                  *,
                                  group_id: int,
                                  enable: bool = ...,
                                  self_id: Optional[int] = ...) -> None:
        """
        :说明:

          群组全员禁言。

        :参数:

          * ``group_id``: 群号
          * ``enable``: 是否禁言
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def set_group_admin(self,
                              *,
                              group_id: int,
                              user_id: int,
                              enable: bool = ...,
                              self_id: Optional[int] = ...) -> None:
        """
        :说明:

          群组设置管理员。

        :参数:

          * ``group_id``: 群号
          * ``user_id``: 要设置管理员的 QQ 号
          * ``enable``: ``True`` 为设置，``False`` 为取消
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def set_group_anonymous(self,
                                  *,
                                  group_id: int,
                                  enable: bool = ...,
                                  self_id: Optional[int] = ...) -> None:
        """
        :说明:

          群组匿名。

        :参数:

          * ``group_id``: 群号
          * ``enable``: 是否允许匿名聊天
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def set_group_card(self,
                             *,
                             group_id: int,
                             user_id: int,
                             card: str = ...,
                             self_id: Optional[int] = ...) -> None:
        """
        :说明:

          设置群名片（群备注）。

        :参数:

          * ``group_id``: 群号
          * ``user_id``: 要设置的 QQ 号
          * ``card``: 群名片内容，不填或空字符串表示删除群名片
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def set_group_name(self,
                             *,
                             group_id: int,
                             group_name: str,
                             self_id: Optional[int] = ...) -> None:
        """
        :说明:

          设置群名。

        :参数:

          * ``group_id``: 群号
          * ``group_name``: 新群名
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def set_group_leave(self,
                              *,
                              group_id: int,
                              is_dismiss: bool = ...,
                              self_id: Optional[int] = ...) -> None:
        """
        :说明:

          退出群组。

        :参数:

          * ``group_id``: 群号
          * ``is_dismiss``: 是否解散，如果登录号是群主，则仅在此项为 True 时能够解散
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def set_group_special_title(self,
                                      *,
                                      group_id: int,
                                      user_id: int,
                                      special_title: str = ...,
                                      duration: int = ...,
                                      self_id: Optional[int] = ...) -> None:
        """
        :说明:

          设置群组专属头衔。

        :参数:

          * ``group_id``: 群号
          * ``user_id``: 要设置的 QQ 号
          * ``special_title``: 专属头衔，不填或空字符串表示删除专属头衔
          * ``duration``: 专属头衔有效期，单位秒，-1 表示永久，不过此项似乎没有效果，可能是只有某些特殊的时间长度有效，有待测试
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def set_friend_add_request(self,
                                     *,
                                     flag: str,
                                     approve: bool = ...,
                                     remark: str = ...,
                                     self_id: Optional[int] = ...) -> None:
        """
        :说明:

          处理加好友请求。

        :参数:

          * ``flag``: 加好友请求的 flag（需从上报的数据中获得）
          * ``approve``: 是否同意请求
          * ``remark``: 添加后的好友备注（仅在同意时有效）
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def set_group_add_request(self,
                                    *,
                                    flag: str,
                                    sub_type: str,
                                    approve: bool = ...,
                                    reason: str = ...,
                                    self_id: Optional[int] = ...) -> None:
        """
        :说明:

          处理加群请求／邀请。

        :参数:

          * ``flag``: 加群请求的 flag（需从上报的数据中获得）
          * ``sub_type``: ``add`` 或 ``invite``，请求类型（需要和上报消息中的 ``sub_type`` 字段相符）
          * ``approve``: 是否同意请求／邀请
          * ``reason``: 拒绝理由（仅在拒绝时有效）
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def get_login_info(self,
                             *,
                             self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :说明:

          获取登录号信息。

        :参数:

          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def get_stranger_info(self,
                                *,
                                user_id: int,
                                no_cache: bool = ...,
                                self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :说明:

          获取陌生人信息。

        :参数:

          * ``user_id``: QQ 号
          * ``no_cache``: 是否不使用缓存（使用缓存可能更新不及时，但响应更快）
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def get_friend_list(self,
                              *,
                              self_id: Optional[int] = ...
                             ) -> List[Dict[str, Any]]:
        """
        :说明:

          获取好友列表。

        :参数:

          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def get_group_info(self,
                             *,
                             group_id: int,
                             no_cache: bool = ...,
                             self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :说明:

          获取群信息。

        :参数:

          * ``group_id``: 群号
          * ``no_cache``: 是否不使用缓存（使用缓存可能更新不及时，但响应更快）
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def get_group_list(self,
                             *,
                             self_id: Optional[int] = ...
                            ) -> List[Dict[str, Any]]:
        """
        :说明:

          获取群列表。

        :参数:

          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def get_group_member_info(
            self,
            *,
            group_id: int,
            user_id: int,
            no_cache: bool = ...,
            self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :说明:

          获取群成员信息。

        :参数:

          * ``group_id``: 群号
          * ``user_id``: QQ 号
          * ``no_cache``: 是否不使用缓存（使用缓存可能更新不及时，但响应更快）
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def get_group_member_list(
            self,
            *,
            group_id: int,
            self_id: Optional[int] = ...) -> List[Dict[str, Any]]:
        """
        :说明:

          获取群成员列表。

        :参数:

          * ``group_id``: 群号
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def get_group_honor_info(self,
                                   *,
                                   group_id: int,
                                   type: str = ...,
                                   self_id: Optional[int] = ...
                                  ) -> Dict[str, Any]:
        """
        :说明:

          获取群荣誉信息。

        :参数:

          * ``group_id``: 群号
          * ``type``: 要获取的群荣誉类型，可传入 ``talkative`` ``performer`` ``legend`` ``strong_newbie`` ``emotion`` 以分别获取单个类型的群荣誉数据，或传入 ``all`` 获取所有数据
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def get_cookies(self,
                          *,
                          domain: str = ...,
                          self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :说明:

          获取 Cookies。

        :参数:

          * ``domain``: 需要获取 cookies 的域名
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def get_csrf_token(self,
                             *,
                             self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :说明:

          获取 CSRF Token。

        :参数:

          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def get_credentials(self,
                              *,
                              domain: str = ...,
                              self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :说明:

          获取 QQ 相关接口凭证。

        :参数:

          * ``domain``: 需要获取 cookies 的域名
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def get_record(self,
                         *,
                         file: str,
                         out_format: str,
                         self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :说明:

          获取语音。

        :参数:

          * ``file``: 收到的语音文件名（CQ 码的 ``file`` 参数），如 ``0B38145AA44505000B38145AA4450500.silk``
          * ``out_format``: 要转换到的格式，目前支持 ``mp3``、``amr``、``wma``、``m4a``、``spx``、``ogg``、``wav``、``flac``
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def get_image(self,
                        *,
                        file: str,
                        self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :说明:

          获取图片。

        :参数:

          * ``file``: 收到的图片文件名（CQ 码的 ``file`` 参数），如 ``6B4DE3DFD1BD271E3297859D41C530F5.jpg``
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def can_send_image(self,
                             *,
                             self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :说明:

          检查是否可以发送图片。

        :参数:

          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def can_send_record(self,
                              *,
                              self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :说明:

          检查是否可以发送语音。

        :参数:

          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def get_status(self,
                         *,
                         self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :说明:

          获取插件运行状态。

        :参数:

          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def get_version_info(self,
                               *,
                               self_id: Optional[int] = ...) -> Dict[str, Any]:
        """
        :说明:

          获取版本信息。

        :参数:

          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def set_restart(self,
                          *,
                          delay: int = ...,
                          self_id: Optional[int] = ...) -> None:
        """
        :说明:

          重启 OneBot 实现。

        :参数:

          * ``delay``: 要延迟的毫秒数，如果默认情况下无法重启，可以尝试设置延迟为 2000 左右
          * ``self_id``: 机器人 QQ 号
        """
        ...

    async def clean_cache(self, *, self_id: Optional[int] = ...) -> None:
        """
        :说明:

          清理数据目录。

        :参数:

          * ``self_id``: 机器人 QQ 号
        """
        ...


class Event:

    def __init__(self, raw_event: dict):
        ...

    @property
    def id(self) -> Optional[int]:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def self_id(self) -> str:
        ...

    @property
    def time(self) -> int:
        ...

    @property
    def type(self) -> str:
        ...

    @type.setter
    def type(self, value) -> None:
        ...

    @property
    def detail_type(self) -> str:
        ...

    @detail_type.setter
    def detail_type(self, value) -> None:
        ...

    @property
    def sub_type(self) -> Optional[str]:
        ...

    @sub_type.setter
    def sub_type(self, value) -> None:
        ...

    @property
    def user_id(self) -> Optional[int]:
        ...

    @user_id.setter
    def user_id(self, value) -> None:
        ...

    @property
    def group_id(self) -> Optional[int]:
        ...

    @group_id.setter
    def group_id(self, value) -> None:
        ...

    @property
    def to_me(self) -> Optional[bool]:
        ...

    @to_me.setter
    def to_me(self, value) -> None:
        ...

    @property
    def message(self) -> Optional["Message"]:
        ...

    @message.setter
    def message(self, value) -> None:
        ...

    @property
    def reply(self) -> Optional[dict]:
        ...

    @reply.setter
    def reply(self, value) -> None:
        ...

    @property
    def raw_message(self) -> Optional[str]:
        ...

    @raw_message.setter
    def raw_message(self, value) -> None:
        ...

    @property
    def plain_text(self) -> Optional[str]:
        ...

    @property
    def sender(self) -> Optional[dict]:
        ...

    @sender.setter
    def sender(self, value) -> None:
        ...


class MessageSegment:

    def __init__(self, type: str, data: Dict[str, Any]) -> None:
        ...

    def __str__(self):
        ...

    def __add__(self, other) -> "Message":
        ...

    @staticmethod
    def anonymous(ignore_failure: Optional[bool] = ...) -> "MessageSegment":
        ...

    @staticmethod
    def at(user_id: Union[int, str]) -> "MessageSegment":
        ...

    @staticmethod
    def contact_group(group_id: int) -> "MessageSegment":
        ...

    @staticmethod
    def contact_user(user_id: int) -> "MessageSegment":
        ...

    @staticmethod
    def dice() -> "MessageSegment":
        ...

    @staticmethod
    def face(id_: int) -> "MessageSegment":
        ...

    @staticmethod
    def forward(id_: str) -> "MessageSegment":
        ...

    @staticmethod
    def image(file: str,
              type_: Optional[str] = ...,
              cache: bool = ...,
              proxy: bool = ...,
              timeout: Optional[int] = ...) -> "MessageSegment":
        ...

    @staticmethod
    def json(data: str) -> "MessageSegment":
        ...

    @staticmethod
    def location(latitude: float,
                 longitude: float,
                 title: Optional[str] = ...,
                 content: Optional[str] = ...) -> "MessageSegment":
        ...

    @staticmethod
    def music(type_: str, id_: int) -> "MessageSegment":
        ...

    @staticmethod
    def music_custom(url: str,
                     audio: str,
                     title: str,
                     content: Optional[str] = ...,
                     img_url: Optional[str] = ...) -> "MessageSegment":
        ...

    @staticmethod
    def node(id_: int) -> "MessageSegment":
        ...

    @staticmethod
    def node_custom(user_id: int, nickname: str,
                    content: Union[str, "Message"]) -> "MessageSegment":
        ...

    @staticmethod
    def poke(type_: str, id_: str) -> "MessageSegment":
        ...

    @staticmethod
    def record(file: str,
               magic: Optional[bool] = ...,
               cache: Optional[bool] = ...,
               proxy: Optional[bool] = ...,
               timeout: Optional[int] = ...) -> "MessageSegment":
        ...

    @staticmethod
    def reply(id_: int) -> "MessageSegment":
        ...

    @staticmethod
    def rps() -> "MessageSegment":
        ...

    @staticmethod
    def shake() -> "MessageSegment":
        ...

    @staticmethod
    def share(url: str = ...,
              title: str = ...,
              content: Optional[str] = ...,
              img_url: Optional[str] = ...) -> "MessageSegment":
        ...

    @staticmethod
    def text(text: str) -> "MessageSegment":
        ...

    @staticmethod
    def video(file: str,
              cache: Optional[bool] = ...,
              proxy: Optional[bool] = ...,
              timeout: Optional[int] = ...) -> "MessageSegment":
        ...

    @staticmethod
    def xml(data: str) -> "MessageSegment":
        ...


class Message:

    @staticmethod
    def _construct(msg: Union[str, dict, list]) -> Iterable[MessageSegment]:
        ...
