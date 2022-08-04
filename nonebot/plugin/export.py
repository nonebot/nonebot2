"""本模块定义了插件导出的内容对象。

在新版插件系统中，推荐优先使用直接 import 所需要的插件内容。

FrontMatter:
    sidebar_position: 4
    description: nonebot.plugin.export 模块
"""

import warnings

from . import _current_plugin_chain


class Export(dict):
    """插件导出内容以使得其他插件可以获得。

    用法:
        ```python
        nonebot.export().default = "bar"

        @nonebot.export()
        def some_function():
            pass

        # this doesn't work before python 3.9
        # use
        # export = nonebot.export(); @export.sub
        # instead
        # See also PEP-614: https://www.python.org/dev/peps/pep-0614/
        @nonebot.export().sub
        def something_else():
            pass
        ```
    """

    def __call__(self, func, **kwargs):
        self[func.__name__] = func
        self.update(kwargs)
        return func

    def __setitem__(self, key, value):
        super().__setitem__(key, Export(value) if isinstance(value, dict) else value)

    def __setattr__(self, name, value):
        self[name] = Export(value) if isinstance(value, dict) else value

    def __getattr__(self, name):
        if name not in self:
            self[name] = Export()
        return self[name]


def export() -> Export:
    """获取当前插件的导出内容对象"""
    warnings.warn(
        "nonebot.export() is deprecated. "
        "See https://github.com/nonebot/nonebot2/issues/935.",
        DeprecationWarning,
    )
    plugins = _current_plugin_chain.get()
    if not plugins:
        raise RuntimeError("Export outside of the plugin!")
    return plugins[-1].export
