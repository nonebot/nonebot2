"""
事件处理函数
============

该模块实现事件处理函数的封装，以实现动态参数等功能。
"""

import inspect
from typing import Any, List, Dict, Type, Union, Optional, TYPE_CHECKING
from typing import ForwardRef, _eval_type  # type: ignore

from nonebot.log import logger
from nonebot.typing import T_Handler, T_State

if TYPE_CHECKING:
    from nonebot.matcher import Matcher
    from nonebot.adapters import Bot, Event


class HandlerMeta(type):
    if TYPE_CHECKING:
        func: T_Handler
        signature: inspect.Signature
        bot_type: Type["Bot"]
        event_type: Optional[Type["Event"]]
        state_type: Optional[T_State]
        matcher_type: Optional[Type["Matcher"]]

    def __repr__(self) -> str:
        return (f"<Handler {self.func.__name__}(bot: {self.bot_type}, "
                f"event: {self.event_type}, state: {self.state_type}, "
                f"matcher: {self.matcher_type})>")

    def __str__(self) -> str:
        return repr(self)


class Handler(metaclass=HandlerMeta):
    """事件处理函数类"""

    def __init__(self, func: T_Handler):
        """装饰事件处理函数以便根据动态参数运行"""
        self.func: T_Handler = func
        """
        :类型: ``T_Handler``
        :说明: 事件处理函数
        """
        self.signature: inspect.Signature = self.get_signature()
        """
        :类型: ``inspect.Signature``
        :说明: 事件处理函数签名
        """

    def __repr__(self) -> str:
        return (f"<Handler {self.func.__name__}(bot: {self.bot_type}, "
                f"event: {self.event_type}, state: {self.state_type}, "
                f"matcher: {self.matcher_type})>")

    def __str__(self) -> str:
        return repr(self)

    async def __call__(self, matcher: "Matcher", bot: "Bot", event: "Event",
                       state: T_State):
        BotType = ((self.bot_type is not inspect.Parameter.empty) and
                   inspect.isclass(self.bot_type) and self.bot_type)
        if BotType and not isinstance(bot, BotType):
            logger.debug(
                f"Matcher {matcher} bot type {type(bot)} not match annotation {BotType}, ignored"
            )
            return

        EventType = ((self.event_type is not inspect.Parameter.empty) and
                     inspect.isclass(self.event_type) and self.event_type)
        if EventType and not isinstance(event, EventType):
            logger.debug(
                f"Matcher {matcher} event type {type(event)} not match annotation {EventType}, ignored"
            )
            return

        args = {"bot": bot, "event": event, "state": state, "matcher": matcher}
        await self.func(
            **{
                k: v
                for k, v in args.items()
                if self.signature.parameters.get(k, None) is not None
            })

    @property
    def bot_type(self) -> Union[Type["Bot"], inspect.Parameter.empty]:
        """
        :类型: ``Union[Type["Bot"], inspect.Parameter.empty]``
        :说明: 事件处理函数接受的 Bot 对象类型"""
        return self.signature.parameters["bot"].annotation

    @property
    def event_type(
            self) -> Optional[Union[Type["Event"], inspect.Parameter.empty]]:
        """
        :类型: ``Optional[Union[Type[Event], inspect.Parameter.empty]]``
        :说明: 事件处理函数接受的 event 类型 / 不需要 event 参数
        """
        if "event" not in self.signature.parameters:
            return None
        return self.signature.parameters["event"].annotation

    @property
    def state_type(self) -> Optional[Union[T_State, inspect.Parameter.empty]]:
        """
        :类型: ``Optional[Union[T_State, inspect.Parameter.empty]]``
        :说明: 事件处理函数是否接受 state 参数
        """
        if "state" not in self.signature.parameters:
            return None
        return self.signature.parameters["state"].annotation

    @property
    def matcher_type(
            self) -> Optional[Union[Type["Matcher"], inspect.Parameter.empty]]:
        """
        :类型: ``Optional[Union[Type["Matcher"], inspect.Parameter.empty]]``
        :说明: 事件处理函数是否接受 matcher 参数
        """
        if "matcher" not in self.signature.parameters:
            return None
        return self.signature.parameters["matcher"].annotation

    def get_signature(self) -> inspect.Signature:
        wrapped_signature = self._get_typed_signature()
        signature = self._get_typed_signature(False)
        self._check_params(signature)
        self._check_bot_param(signature)
        self._check_bot_param(wrapped_signature)
        signature.parameters["bot"].replace(
            annotation=wrapped_signature.parameters["bot"].annotation)
        if "event" in wrapped_signature.parameters and "event" in signature.parameters:
            signature.parameters["event"].replace(
                annotation=wrapped_signature.parameters["event"].annotation)
        return signature

    def update_signature(
        self, **kwargs: Union[None, Type["Bot"], Type["Event"], Type["Matcher"],
                              T_State, inspect.Parameter.empty]
    ) -> None:
        params: List[inspect.Parameter] = []
        for param in ["bot", "event", "state", "matcher"]:
            sig = self.signature.parameters.get(param, None)
            if param in kwargs:
                sig = inspect.Parameter(param,
                                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                                        annotation=kwargs[param])
            if sig:
                params.append(sig)

        self.signature = inspect.Signature(params)

    def _get_typed_signature(self,
                             follow_wrapped: bool = True) -> inspect.Signature:
        signature = inspect.signature(self.func, follow_wrapped=follow_wrapped)
        globalns = getattr(self.func, "__globals__", {})
        typed_params = [
            inspect.Parameter(
                name=param.name,
                kind=param.kind,
                default=param.default,
                annotation=param.annotation if follow_wrapped else
                self._get_typed_annotation(param, globalns),
            ) for param in signature.parameters.values()
        ]
        typed_signature = inspect.Signature(typed_params)
        return typed_signature

    def _get_typed_annotation(self, param: inspect.Parameter,
                              globalns: Dict[str, Any]) -> Any:
        try:
            if isinstance(param.annotation, str):
                return _eval_type(ForwardRef(param.annotation), globalns,
                                  globalns)
            else:
                return param.annotation
        except Exception:
            return param.annotation

    def _check_params(self, signature: inspect.Signature):
        if not set(signature.parameters.keys()) <= {
                "bot", "event", "state", "matcher"
        }:
            raise ValueError(
                "Handler param names must in `bot`/`event`/`state`/`matcher`")

    def _check_bot_param(self, signature: inspect.Signature):
        if not any(
                param.name == "bot" for param in signature.parameters.values()):
            raise ValueError("Handler missing parameter 'bot'")
