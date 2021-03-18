"""
事件处理函数
===========

该模块实现事件处理函数的封装，以实现动态参数等功能。
"""

import inspect
from typing_extensions import Literal
from typing import Any, List, Dict, Type, Union, Optional, TYPE_CHECKING
from typing import ForwardRef, _eval_type  # type: ignore

from nonebot.log import logger
from nonebot.typing import T_Handler, T_State

if TYPE_CHECKING:
    from nonebot.matcher import Matcher
    from nonebot.adapters import Bot, Event


class HandlerMeta(type):
    ...


class Handler(metaclass=HandlerMeta):
    """事件处理函数类"""

    def __init__(self, func: T_Handler, module: Optional[str] = None):
        self.func: T_Handler = func
        """
        :类型: ``T_Handler``
        :说明: 事件处理函数
        """
        self.module: Optional[str] = module
        """
        :类型: ``Optional[str]``
        :说明: 事件处理函数所在模块名称
        """
        self.signature: inspect.Signature = self.get_signature()
        """
        :类型: ``inspect.Signature``
        :说明: 事件处理函数签名
        """

    async def __call__(self, matcher: "Matcher", bot: "Bot", event: "Event",
                       state: T_State):
        params = {
            param.name: param.annotation
            for param in self.signature.parameters.values()
        }

        BotType = ((params["bot"] is not inspect.Parameter.empty) and
                   inspect.isclass(params["bot"]) and params["bot"])
        if BotType and not isinstance(bot, BotType):
            logger.debug(
                f"Matcher {matcher} bot type {type(bot)} not match annotation {BotType}, ignored"
            )
            return

        EventType = ((params["event"] is not inspect.Parameter.empty) and
                     inspect.isclass(params["event"]) and params["event"])
        if EventType and not isinstance(event, EventType):
            logger.debug(
                f"Matcher {matcher} event type {type(event)} not match annotation {EventType}, ignored"
            )
            return

        args = {"bot": bot, "event": event, "state": state, "matcher": matcher}
        await self.func(
            **{k: v for k, v in args.items() if params[k] is not None})

    @property
    def bot_type(self) -> Type["Bot"]:
        return self.signature.parameters["bot"].annotation

    @property
    def event_type(self) -> Optional[Type["Event"]]:
        if "event" not in self.signature:
            return None
        return self.signature.parameters["event"].annotation

    @property
    def state_type(self) -> Optional[T_State]:
        if "state" not in self.signature:
            return None
        return self.signature.parameters["state"].annotation

    @property
    def matcher_type(self) -> Optional[Type["Matcher"]]:
        if "matcher" not in self.signature:
            return None
        return self.signature.parameters["matcher"].annotation

    def get_signature(self) -> inspect.Signature:
        wrapped_signature = self._get_typed_signature()
        signature = self._get_typed_signature(False)
        self._check_params(signature)
        self._check_bot_param(signature)
        self._check_bot_param(wrapped_signature)
        signature.parameters["bot"].annotation = wrapped_signature.parameters[
            "bot"].annotation
        if "event" in wrapped_signature.parameters and "event" in signature.parameters:
            signature.parameters[
                "event"].annotation = wrapped_signature.parameters[
                    "event"].annotation
        return signature

    def update_signature(
        self, **kwargs: Union[None, Type["Bot"], Type["Event"], Type["Matcher"],
                              T_State]
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
        globalns = getattr(self, "__globals__", {})
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
        if not set(signature.parameters.keys()) < {
                "bot", "event", "state", "matcher"
        }:
            raise ValueError(
                "Handler param names must in `bot`/`event`/`state`/`matcher`")

    def _check_bot_param(self, signature: inspect.Signature):
        if not any(
                param.name == "bot" for param in signature.parameters.values()):
            raise ValueError("Handler missing parameter 'bot'")
