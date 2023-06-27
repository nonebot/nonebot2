from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="测试插件2",
    description="测试继承适配器",
    usage="无法使用",
    type="application",
    homepage="https://nonebot.dev",
    supported_adapters={"~onebot.v11", "~onebot.v12"},
    extra={"author": "NoneBot"},
)
