# 开始使用

一切都安装成功后，你就已经做好了进行简单配置以运行一个最小的 NoneBot 实例的准备。

## 最小实例

使用你最熟悉的编辑器或 IDE，创建一个名为 `bot.py` 的文件，内容如下：

```python
import nonebot

if __name__ == '__main__':
    nonebot.init()
    nonebot.load_builtin_plugins()
    nonebot.run(host='127.0.0.1', port=8080)
```

`if __name__ == '__main__'` 语句块的这几行代码将依次：

1. 使用默认配置初始化 NoneBot 包
2. 加载 NoneBot 内置的插件
3. 在地址 `127.0.0.1:8080` 运行 NoneBot

:::tip 提示
这里 `nonebot.run()` 的参数 `host='127.0.0.1'` 表示让 NoneBot 监听本地环回地址，如果你的 酷Q 运行在非本机的其它位置，例如 Docker 容器内、局域网内的另一台机器上等，则这里需要修改 `host` 参数为希望让 CQHTTP 插件访问的 IP。如果不清楚该使用哪个 IP，或者希望本机的所有 IP 都被监听，可以使用 `0.0.0.0`。
:::

在命令行使用如下命令即可运行这个 NoneBot 实例：

```bash
python bot.py
```

运行后会产生如下日志：

```
[2020-03-16 15:50:26,166 nonebot] INFO: Succeeded to import "nonebot.plugins.base"
[2020-03-16 15:50:26,166 nonebot] INFO: Running on 127.0.0.1:8080
Running on http://127.0.0.1:8080 (CTRL + C to quit)
[2020-03-16 15:50:26,177] Running on 127.0.0.1:8080 over http (CTRL + C to quit)
```

除此之外可能有一些红色的提示信息如 `ujson module not found, using json` 等，可以忽略。

## 配置 CQHTTP 插件

单纯运行 NoneBot 实例并不会产生任何效果，因为此刻 酷Q 这边还不知道 NoneBot 的存在，也就无法把消息发送给它，因此现在需要对 CQHTTP 插件做一个简单的配置来让它把消息等事件上报给 NoneBot。

如果你在之前已经按照 [安装](/guide/installation.md) 的建议使用默认配置运行了一次 CQHTTP 插件，此时 酷Q 的 `data/app/io.github.richardchien.coolqhttpapi/config/` 目录中应该已经有了一个名为 `<user-id>.json` 的文件（`<user-id>` 为你登录的 QQ 账号）。修改这个文件，**修改如下配置项（如果不存在相应字段则添加）**：

:::warning 注意
如果使用 CQHTTP 插件官方 Docker 镜像运行 酷Q，则配置文件所在目录可能是 `app/io.github.richardchien.coolqhttpapi/config/`。
:::

```json
{
    "ws_reverse_url": "ws://127.0.0.1:8080/ws/",
    "use_ws_reverse": true,
    "enable_heartbeat": true
}
```

:::tip 提示
**这里的 `127.0.0.1:8080` 对应 `nonebot.run()` 中传入的 `host` 和 `port`**，如果在 `nonebot.run()` 中传入的 `host` 是 `0.0.0.0`，则插件的配置中需使用任意一个能够访问到 NoneBot 所在环境的 IP，**不要直接填 `0.0.0.0`**。特别地，如果你的 酷Q 运行在 Docker 容器中，NoneBot 运行在宿主机中，则默认情况下这里需使用 `172.17.0.1`（即宿主机在 Docker 默认网桥上的 IP，不同机器有可能不同，如果是 Linux 系统，可以使用 `ip addr show docker0 | grep -Po 'inet \K[\d.]+'`来获取需要填入的ip；如果是 macOS 系统或者 Windows 系统，可以考虑使用 `host.docker.internal`，具体解释详见 Docker 文档的 [Use cases and workarounds](https://docs.docker.com/docker-for-mac/networking/#use-cases-and-workarounds) 的「I WANT TO CONNECT FROM A CONTAINER TO A SERVICE ON THE HOST」小标题）。
:::

如果你的 CQHTTP 插件版本低于 v4.14.0，还需要删除配置文件中已有的 `ws_reverse_api_url` 和 `ws_reverse_event_url` 两项。

修改之后，在 酷Q 的应用菜单中重启 CQHTTP 插件，或直接重载应用，以使新的配置文件生效。

## 历史性的第一次对话

一旦新的配置文件正确生效之后，NoneBot 所在的控制台（如果正在运行的话）应该会输出类似下面的内容（两条访问日志）：

```
[2020-03-16 15:50:26,435] 127.0.0.1:56363 GET /ws/ 1.1 101 - 7982
[2020-03-16 15:50:26,438] 127.0.0.1:56364 GET /ws/ 1.1 101 - 8977
```

这表示 CQHTTP 插件已经成功地连接上了 NoneBot，与此同时，CQHTTP 的日志控制台（和日志文件）中也会输出反向 WebSocket 连接成功的日志。

:::warning 注意
如果到这一步你没有看到上面这样的成功日志，CQHTTP 的日志中在不断地重连或无反应，请注意检查配置中的 IP 和端口是否确实可以访问。比较常见的出错点包括：

- NoneBot 监听 `0.0.0.0`，然后在 CQHTTP 配置中填了 `ws://0.0.0.0:8080/ws/`
- 在 Docker 容器内运行 酷Q 和 CQHTTP，并通过 `127.0.0.1` 访问宿主机上的 NoneBot
- 想从公网访问，但没有修改云服务商的安全组策略或系统防火墙
- NoneBot 所监听的端口存在冲突，已被其它程序占用
- 弄混了 NoneBot 的 `host`、`port` 参数与 CQHTTP 配置中的 `host`、`port` 参数
- 使用旧版 CQHTTP 插件，且没有删除 `ws_reverse_api_url` 和 `ws_reverse_event_url`
- 使用旧版 CQHTTP 插件，且丢失了 `ws://127.0.0.1:8080/ws/` 结尾的 `/`
- `ws://` 错填为 `http://`
- 酷Q 或 CQHTTP 插件启动时遭到外星武器干扰

请尝试重启 CQHTTP、重启 酷Q、重启 NoneBot、更换端口、修改防火墙、重启系统、仔细阅读前面的文档及提示、更新 CQHTTP 和 NoneBot 到最新版本等方式来解决。
:::

现在，尝试向你的 QQ 机器人账号发送如下内容：

```
/echo 你好，世界
```

到这里如果一切 OK，你应该会收到机器人给你回复了 `你好，世界`。这一历史性的对话标志着你已经成功地运行了一个 NoneBot 的最小实例，开始了编写更强大的 QQ 机器人的创意之旅！
