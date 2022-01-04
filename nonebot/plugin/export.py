from . import _current_plugin


class Export(dict):
    """
    :说明:

      插件导出内容以使得其他插件可以获得。

    :示例:

    .. code-block:: python

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
    """
    :说明:

      获取插件的导出内容对象

    :返回:

      - ``Export``
    """
    plugin = _current_plugin.get()
    if not plugin:
        raise RuntimeError("Export outside of the plugin!")
    return plugin.export
