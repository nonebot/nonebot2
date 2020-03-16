# 安装

## NoneBot

::: warning 注意
请确保你的 Python 版本 >= 3.7。
:::

可以使用 pip 安装已发布的最新版本：

```bash
pip install nonebot
```

如果你需要使用最新的（可能尚未发布的）特性，可以克隆 Git 仓库后手动安装：

```bash
git clone https://github.com/richardchien/nonebot.git
cd nonebot
python setup.py install
```

以上命令中的 `pip`、`python` 可能需要根据情况换成 `pip3`、`python3`。

## 酷Q

前往 酷Q 官方论坛的 [版本发布](https://cqp.cc/b/news) 页面根据需要下载最新版本的 酷Q Air 或 Pro，解压后启动 `CQA.exe` 或 `CQP.exe` 并登录 QQ 机器人账号。

如果你的操作系统是 Linux 或 macOS，可以使用版本发布页中 酷Q 官方提供的 Docker 镜像，也可以直接跳至下一个标题，使用 CQHTTP 插件官方提供的 Docker 镜像。

::: tip 提示
如果这是你第一次使用 酷Q，建议完成它自带的新手教程，以对 酷Q 的运行机制有所了解。
:::

## CQHTTP 插件

前往 [CQHTTP 插件文档](https://cqhttp.cc/docs/)，按照其教程的「使用方法」安装插件。安装后，请先使用默认配置运行，并查看 酷Q 日志窗口的输出，以确定插件的加载、配置的生成和读取、插件版本等符合预期。

::: warning 注意
请确保你安装的插件版本 >= 4.8，通常建议插件在大版本内尽量及时升级至最新版本。
:::
