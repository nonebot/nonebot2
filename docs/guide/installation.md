# 安装

## NoneBot

:::warning 注意
请确保你的 Python 版本 >= 3.7。
:::

:::warning 注意
请在安装 nonebot2 之前卸载 nonebot 1.x

```bash
pip uninstall nonebot
```

:::

### 通过脚手架安装(推荐安装方式)

1. (可选)使用你喜欢的 Python 环境管理工具创建新的虚拟环境。
2. 使用 `pip` (或其他) 安装 NoneBot 脚手架。

   ```bash
   pip install nb-cli
   ```

3. 点个 star 吧

   nonebot2: [![nb-cli](https://img.shields.io/github/stars/nonebot/nonebot2?style=social)](https://github.com/nonebot/nonebot2)

   nb-cli: [![nb-cli](https://img.shields.io/github/stars/nonebot/nb-cli?style=social)](https://github.com/nonebot/nb-cli)

### 不使用脚手架(纯净安装)

```bash
# poetry
poetry add nonebot2
# pip
pip install nonebot2
```

如果你需要使用最新的（可能**尚未发布**的）特性，可以直接从 GitHub 仓库安装：

```bash
# master
poetry add git+https://github.com/nonebot/nonebot2.git#master
# dev
poetry add git+https://github.com/nonebot/nonebot2.git#dev
```

或者克隆 Git 仓库后手动安装：

```bash
git clone https://github.com/nonebot/nonebot2.git
cd nonebot2
poetry install --no-dev  # 推荐
pip install .  # 不推荐
```

## 安装插件

插件可以通过 `nb-cli` 进行安装，也可以自行安装并加载插件。

```bash
# 列出所有的插件
nb plugin list
# 搜索插件
nb plugin search xxx
# 安装插件
nb plugin install xxx
```

如果急于上线 Bot 或想要使用现成的插件，以下插件可作为参考：

### 官方插件

~~自用插件~~ ~~确信~~

- [NoneBot-Plugin-Docs](https://github.com/nonebot/nonebot2/tree/master/packages/nonebot-plugin-docs) 离线文档插件
- [NoneBot-Plugin-Test](https://github.com/nonebot/plugin-test) 本地机器人测试前端插件
- [NoneBot-Plugin-APScheduler](https://github.com/nonebot/plugin-apscheduler) 定时任务插件
- [NoneBot-Plugin-Sentry](https://github.com/cscs181/QQ-GitHub-Bot/tree/master/src/plugins/nonebot_plugin_sentry) Sentry 在线日志分析插件
- [NoneBot-Plugin-Status](https://github.com/cscs181/QQ-GitHub-Bot/tree/master/src/plugins/nonebot_plugin_status) 服务器状态查看插件

### 其他插件

还有更多的插件在 [这里](/plugin-store.md) 等着你发现～
