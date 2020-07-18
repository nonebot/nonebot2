#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional


class Event(dict):
    """
    封装从 CQHTTP 收到的事件数据对象（字典），提供属性以获取其中的字段。

    除 `type` 和 `detail_type` 属性对于任何事件都有效外，其它属性存在与否（不存在则返回
    `None`）依事件不同而不同。
    """

    @staticmethod
    def from_payload(payload: Dict[str, Any]) -> Optional["Event"]:
        """
        从 CQHTTP 事件数据构造 `Event` 对象。
        """
        try:
            e = Event(payload)
            _ = e.type, e.detail_type
            return e
        except KeyError:
            return None

    @property
    def type(self) -> str:
        """
        事件类型，有 ``message``、``notice``、``request``、``meta_event`` 等。
        """
        return self["post_type"]

    @property
    def detail_type(self) -> str:
        """
        事件具体类型，依 `type` 的不同而不同，以 ``message`` 类型为例，有
        ``private``、``group``、``discuss`` 等。
        """
        return self[f"{self.type}_type"]

    @property
    def sub_type(self) -> Optional[str]:
        """
        事件子类型，依 `detail_type` 不同而不同，以 ``message.private`` 为例，有
        ``friend``、``group``、``discuss``、``other`` 等。
        """
        return self.get("sub_type")

    @property
    def name(self):
        """
        事件名，对于有 `sub_type` 的事件，为 ``{type}.{detail_type}.{sub_type}``，否则为
        ``{type}.{detail_type}``。
        """
        n = self.type + "." + self.detail_type
        if self.sub_type:
            n += "." + self.sub_type
        return n

    @property
    def self_id(self) -> int:
        """机器人自身 ID。"""
        return self["self_id"]

    @property
    def user_id(self) -> Optional[int]:
        """用户 ID。"""
        return self.get("user_id")

    @property
    def operator_id(self) -> Optional[int]:
        """操作者 ID。"""
        return self.get("operator_id")

    @property
    def group_id(self) -> Optional[int]:
        """群 ID。"""
        return self.get("group_id")

    @property
    def discuss_id(self) -> Optional[int]:
        """讨论组 ID。"""
        return self.get("discuss_id")

    @property
    def message_id(self) -> Optional[int]:
        """消息 ID。"""
        return self.get("message_id")

    @property
    def message(self) -> Optional[Any]:
        """消息。"""
        return self.get("message")

    @property
    def raw_message(self) -> Optional[str]:
        """未经 CQHTTP 处理的原始消息。"""
        return self.get("raw_message")

    @property
    def sender(self) -> Optional[Dict[str, Any]]:
        """消息发送者信息。"""
        return self.get("sender")

    @property
    def anonymous(self) -> Optional[Dict[str, Any]]:
        """匿名信息。"""
        return self.get("anonymous")

    @property
    def file(self) -> Optional[Dict[str, Any]]:
        """文件信息。"""
        return self.get("file")

    @property
    def comment(self) -> Optional[str]:
        """请求验证消息。"""
        return self.get("comment")

    @property
    def flag(self) -> Optional[str]:
        """请求标识。"""
        return self.get("flag")

    def __repr__(self) -> str:
        return f"<Event, {super().__repr__()}>"
