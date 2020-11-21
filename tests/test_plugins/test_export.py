import nonebot

export = nonebot.export()
export.foo = "bar"
export["bar"] = "foo"


@export
def a():
    pass


@export.sub
def b():
    pass
