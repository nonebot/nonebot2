from nonebot.plugin import PluginManager, _managers


def test_load_plugin_name():
    m = PluginManager(plugins=["dynamic.manager"])
    try:
        _managers.append(m)

        # load by plugin id
        module1 = m.load_plugin("manager")
        # load by module name
        module2 = m.load_plugin("dynamic.manager")
        assert module1
        assert module2
        assert module1 is module2
    finally:
        _managers.remove(m)
