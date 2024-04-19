from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="测试插件3",
    description="测试继承适配器, 使用内置适配器全名",
    usage="无法使用",
    type="application",
    homepage="https://nonebot.dev",
    supported_adapters={
        "nonebot.adapters.onebot.v11",
        "nonebot.adapters.onebot.v12",
        "~qq",
    },
    extra={"author": "NoneBot"},
)
