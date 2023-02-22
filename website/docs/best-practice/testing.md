---
sidebar_position: 4
description: 使用 NoneBug 进行单元测试
---

# 单元测试

> 在计算机编程中，单元测试（Unit Testing）又称为模块测试，是针对程序模块（软件设计的最小单位）来进行正确性检验的测试工作。

为了保证代码的正确运行，我们不仅需要对错误进行跟踪，还需要对代码进行正确性检验，也就是测试。NoneBot 提供了一个测试工具——NoneBug，它是一个 [pytest](https://docs.pytest.org/en/stable/) 插件，可以帮助我们便捷地进行单元测试。

:::tip 提示
建议在阅读本文档前先阅读 [pytest 官方文档](https://docs.pytest.org/en/stable/)来了解 pytest 的相关术语和基本用法。
:::

## 安装 NoneBug

在**项目目录**下激活虚拟环境后运行以下命令安装 NoneBug：

```bash
pip install nonebug
# 或使用 poetry
poetry add nonebug
```

要运行 NoneBug 测试，还需要额外安装 pytest 异步插件 `pytest-asyncio` 或 `anyio` 以支持异步测试。文档中，我们以 `pytest-asyncio` 为例：

```bash
pip install pytest-asyncio
# 或使用 poetry
poetry add pytest-asyncio
```

## 配置测试

在开始测试之前，我们需要对测试进行一些配置，以正确启动我们的机器人。在 `tests` 目录下新建 `conftest.py` 文件，添加以下内容：

```python title=tests/conftest.py
import pytest
import nonebot
# 导入适配器
from nonebot.adapters.console import Adapter as ConsoleAdapter

@pytest.fixture(scope="session", autouse=True)
def load_bot():
    # 加载适配器
    driver = nonebot.get_driver()
    driver.register_adapter(ConsoleAdapter)

    # 加载插件
    nonebot.load_from_toml("pyproject.toml")
```

这样，我们就可以在测试中使用机器人的插件了。通常，我们不需要自行初始化 NoneBot，NoneBug 已经为我们运行了 `nonebot.init()`。如果需要自定义 NoneBot 初始化的参数，我们可以在 `conftest.py` 中添加 `pytest_configure` 钩子函数。例如，我们可以修改 NoneBot 配置环境为 `test` 并从环境变量中输入配置：

```python {3,5,7-9} title=tests/conftest.py
import os

from nonebug import NONEBOT_INIT_KWARGS

os.environ["ENVIRONMENT"] = "test"

def pytest_configure(config: pytest.Config):
    config.stash[NONEBOT_INIT_KWARGS] = {"secret": os.getenv("INPUT_SECRET")}
```

## 编写插件测试

在配置完成插件加载后，我们就可以在测试中使用插件了。NoneBug 通过 pytest fixture `app` 提供各种测试方法，我们可以在测试中使用它来测试插件。现在，我们创建一个测试脚本来测试[深入指南](../appendices/session-control.mdx)中编写的天气插件。

<detials>
  <summary>插件示例</summary>

```python title=weather/__init__.py
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import CommandArg, ArgPlainText

weather = on_command("天气", rule=to_me(), aliases={"weather", "天气预报"})

@weather.handle()
async def handle_function(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("location", args)

@weather.got("location", prompt="请输入地名")
async def got_location(location: str = ArgPlainText()):
    if location not in ["北京", "上海", "广州", "深圳"]:
        await weather.reject(f"你想查询的城市 {location} 暂不支持，请重新输入！")
    await weather.finish(f"今天{location}的天气是...")
```

</detials>

```python title=tests/test_weather.py
import pytest
from nonebug import App

@pytest.mark.asyncio
async def test_weather(app: App):
    ...
```
