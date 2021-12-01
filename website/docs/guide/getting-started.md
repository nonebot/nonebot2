---
sidebar_position: 3

options:
  menu:
    weight: 30
    category: guide
---

# 开始使用

一切都安装成功后，你就已经做好了进行简单配置以运行一个最小的 NoneBot 实例的准备工作。

## 最小实例

如果你已经按照推荐方式安装了 `nb-cli`，使用它创建一个空项目：

```bash
nb create
```

根据引导进行项目配置，完成后会在当前目录下创建一个项目目录，项目目录内包含 `bot.py`。

如果未安装 `nb-cli`，使用你最熟悉的编辑器或 IDE，创建一个名为 `bot.py` 的文件，内容如下（这里以 CQHTTP 适配器为例）：

```python{4,6,7,10}
import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
nonebot.load_builtin_plugins()

if __name__ == "__main__":
    nonebot.run()
```

## 解读

在上方 `bot.py` 中，这几行高亮代码将依次：

1. 使用默认配置初始化 NoneBot
2. 加载 NoneBot 内置的 CQHTTP 协议适配组件  
   `register_adapter` 的第一个参数我们传入了一个字符串，该字符串将会在后文 [配置 CQHTTP 协议端](#配置-cqhttp-协议端-以-qq-为例) 时使用。
3. 加载 NoneBot 内置的插件
4. 在地址 `127.0.0.1:8080` 运行 NoneBot

在命令行使用如下命令即可运行这个 NoneBot 实例：

```bash
# nb-cli
nb run
# 其他
python bot.py
```

运行后会产生如下日志：

```plain
09-14 21:02:00 [INFO] nonebot | Succeeded to import "nonebot.plugins.base"
09-14 21:02:00 [INFO] nonebot | Running NoneBot...
09-14 21:02:00 [INFO] uvicorn | Started server process [1234]
09-14 21:02:00 [INFO] uvicorn | Waiting for application startup.
09-14 21:02:00 [INFO] uvicorn | Application startup complete.
09-14 21:02:00 [INFO] uvicorn | Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
```

## 配置协议端上报

在 `bot.py` 文件中使用 `register_adapter` 注册协议适配之后即可配置协议端来完成与 NoneBot 的通信，详细配置方法参考：

- [配置 CQHTTP](./cqhttp-guide.md)
- [配置钉钉](./ding-guide.md)
- [配置 mirai-api-http](./mirai-guide.md)

NoneBot 接受的上报地址与 `Driver` 有关，默认使用的 `FastAPI Driver` 所接受的上报地址有：

- `/{adapter name}/`: HTTP POST 上报
- `/{adapter name}/http/`: HTTP POST 上报
- `/{adapter name}/ws`: WebSocket 上报
- `/{adapter name}/ws/`: WebSocket 上报

:::warning 注意
如果到这一步你没有在 NoneBot 看到连接成功日志，比较常见的出错点包括：

- NoneBot 监听 `0.0.0.0`，然后在协议端上报配置中填了 `ws://0.0.0.0:8080/***/ws`
- 在 Docker 容器内运行协议端，并通过 `127.0.0.1` 访问宿主机上的 NoneBot
- 想从公网访问，但没有修改云服务商的安全组策略或系统防火墙
- NoneBot 所监听的端口存在冲突，已被其它程序占用
- 弄混了 NoneBot 的 `host`、`port` 参数与协议端上报配置中的 `host`、`port` 参数
- `ws://` 错填为 `http://`
- 协议端或 NoneBot 启动时遭到外星武器干扰

请尝试重启协议端 NoneBot、更换端口、修改防火墙、重启系统、仔细阅读前面的文档及提示、更新协议端 和 NoneBot 到最新版本等方式来解决。
:::
