"""本模块是 {ref}`nonebot.matcher.Matcher.permission` 的类型定义。

每个{ref}`事件响应器 <nonebot.matcher.Matcher>`
拥有一个 {ref}`nonebot.permission.Permission`，其中是 `PermissionChecker` 的集合。
只要有一个 `PermissionChecker` 检查结果为 `True` 时就会继续运行。

FrontMatter:
    sidebar_position: 6
    description: nonebot.permission 模块
"""

from nonebot.params import EventType
from nonebot.adapters import Bot, Event
from nonebot.internal.permission import USER as USER
from nonebot.internal.permission import User as User
from nonebot.internal.permission import Permission as Permission


class Message:
    """检查是否为消息事件"""

    __slots__ = ()

    def __repr__(self) -> str:
        return "Message()"

    async def __call__(self, type: str = EventType()) -> bool:
        return type == "message"


class Notice:
    """检查是否为通知事件"""

    __slots__ = ()

    def __repr__(self) -> str:
        return "Notice()"

    async def __call__(self, type: str = EventType()) -> bool:
        return type == "notice"


class Request:
    """检查是否为请求事件"""

    __slots__ = ()

    def __repr__(self) -> str:
        return "Request()"

    async def __call__(self, type: str = EventType()) -> bool:
        return type == "request"


class MetaEvent:
    """检查是否为元事件"""

    __slots__ = ()

    def __repr__(self) -> str:
        return "MetaEvent()"

    async def __call__(self, type: str = EventType()) -> bool:
        return type == "meta_event"


MESSAGE: Permission = Permission(Message())
"""匹配任意 `message` 类型事件

仅在需要同时捕获不同类型事件时使用，优先使用 message type 的 Matcher。
"""
NOTICE: Permission = Permission(Notice())
"""匹配任意 `notice` 类型事件

仅在需要同时捕获不同类型事件时使用，优先使用 notice type 的 Matcher。
"""
REQUEST: Permission = Permission(Request())
"""匹配任意 `request` 类型事件

仅在需要同时捕获不同类型事件时使用，优先使用 request type 的 Matcher。
"""
METAEVENT: Permission = Permission(MetaEvent())
"""匹配任意 `meta_event` 类型事件

仅在需要同时捕获不同类型事件时使用，优先使用 meta_event type 的 Matcher。
"""


class SuperUser:
    """检查当前事件是否是消息事件且属于超级管理员"""

    __slots__ = ()

    def __repr__(self) -> str:
        return "Superuser()"

    async def __call__(self, bot: Bot, event: Event) -> bool:
        try:
            user_id = event.get_user_id()
        except Exception:
            return False
        return (
            f"{bot.adapter.get_name().split(maxsplit=1)[0].lower()}:{user_id}"
            in bot.config.superusers
            or user_id in bot.config.superusers  # 兼容旧配置
        )


SUPERUSER: Permission = Permission(SuperUser())
"""匹配任意超级用户事件"""

__autodoc__ = {
    "Permission": True,
    "Permission.__call__": True,
    "User": True,
    "USER": True,
}
