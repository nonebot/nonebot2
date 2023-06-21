from pydantic import BaseModel

from nonebot.adapters import Adapter
from nonebot.plugin import PluginMetadata


class Config(BaseModel):
    custom: str = ""


class FakeAdapter(Adapter):
    ...


__plugin_meta__ = PluginMetadata(
    name="测试插件",
    description="测试插件元信息",
    usage="无法使用",
    type="application",
    homepage="https://nonebot.dev",
    config=Config,
    supported_adapters={"~onebot.v11", "plugins.metadata:FakeAdapter"},
    extra={"author": "NoneBot"},
)
