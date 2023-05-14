from pydantic import BaseModel

from nonebot.plugin import PluginMetadata


class Config(BaseModel):
    custom: str = ""


__plugin_meta__ = PluginMetadata(
    name="测试插件",
    description="测试插件元信息",
    usage="无法使用",
    type="application",
    homepage="https://v2.nonebot.dev",
    config=Config,
    supported_adapters={"nonebot.adapters.onebot.v11"},
    extra={"author": "NoneBot"},
)
