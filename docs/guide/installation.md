# 安装

## NoneBot

::: warning 注意
请确保你的 Python 版本 >= 3.6。
:::

可以使用 pip 安装已发布的最新版本：

```bash
pip install none-bot
```

如果你需要使用最新的（可能还没发布的）特性，可以克隆 Git 仓库后手动安装：

```bash
git clone https://github.com/richardchien/none-bot.git
cd none-bot
python setup.py install
```

以上命令中的 `pip`、`python` 可能需要根据情况换成 `pip3`、`python3`。

## 酷 Q

前往酷 Q 官方论坛的 [版本发布](https://cqp.cc/b/news) 页面根据需要下载最新版本的酷 Q Air 或 Pro，解压后启动 `CQA.exe` 或 `CQP.exe` 完成新手教程。

如果你使用 Linux 或 macOS，可以使用版本发布页中酷 Q 官方提供的 Docker 镜像，或直接跳至下一个标题，使用 CoolQ HTTP API 插件官方提供的 Docker 镜像。

## CoolQ HTTP API 插件

前往 [CoolQ HTTP API 插件官方文档](https://cqhttp.cc/docs/)，按照其教程安装插件。安装后，请先使用默认配置运行，查看酷 Q 日至窗口的输出，以确定插件的加载、配置的生成和读取、插件版本符合预期。

::: warning 注意
请确保你安装的插件版本 >= 4.2，通常建议插件在大版本内尽量及时升级至最新版本。
:::
