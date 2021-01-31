from .base import Event


class MetaEvent(Event):
    """元事件基类"""
    qq: int


class BotOnlineEvent(MetaEvent):
    """Bot登录成功"""
    pass


class BotOfflineEventActive(MetaEvent):
    """Bot主动离线"""
    pass


class BotOfflineEventForce(MetaEvent):
    """Bot被挤下线"""
    pass


class BotOfflineEventDropped(MetaEvent):
    """Bot被服务器断开或因网络问题而掉线"""
    pass


class BotReloginEvent(MetaEvent):
    """Bot主动重新登录"""
    pass