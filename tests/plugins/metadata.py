from pydantic import BaseModel

from nonebot.plugin import PluginMetadata


class Config(BaseModel):
    custom: str = ""


__plugin_meta__ = PluginMetadata(
    name="测试插件",
    description="测试插件元信息",
    usage="无法使用",
    config=Config,
    extra={"author": "NoneBot"},
)
