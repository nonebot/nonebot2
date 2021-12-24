---
sidebar_position: 0
description: 通过脚手架, PyPI, GitHub 安装 NoneBot

options:
  menu:
    weight: 10
    category: guide
---

# 安装 NoneBot

:::warning 注意
请确保你的 Python 版本 >= 3.7.3。
:::

:::warning 注意
请在安装 NoneBot v2 之前卸载 NoneBot v1

```bash
pip uninstall nonebot
```

:::

## 通过脚手架安装 (推荐)

1. (可选) 使用你喜欢的 Python 环境管理工具 (如 `poetry`, `venv`, `conda` 等) 创建新的虚拟环境
2. 使用 `pip` 或 其他包管理工具 安装 `nb-cli`，`nonebot2` 会作为其依赖被一起安装

   ```bash
   pip install nb-cli
   ```

<!-- asciinema for installation -->

## 不使用脚手架 (纯净安装)

如果你不想使用脚手架，可以直接安装 `nonebot2`，并自行完成开发配置。

```bash
pip install nonebot2
# 也可以通过 poetry 安装
poetry add nonebot2
```

## 从 GitHub 安装

如果你需要使用最新的（可能**尚未发布**的）特性，可以直接从 GitHub 仓库安装：

:::warning 注意
直接从 Github 仓库中安装意味着你将使用最新提交的代码，它们并没有进行充分的稳定性测试

在任何情况下请不要将其应用于生产环境!
:::

```bash title="Install From Github"
# master分支
poetry add git+https://github.com/nonebot/nonebot2.git#master
# dev分支
poetry add git+https://github.com/nonebot/nonebot2.git#dev
```

或者在克隆 Git 仓库后手动安装：

```bash
git clone https://github.com/nonebot/nonebot2.git
cd nonebot2
poetry install --no-dev  # 推荐
pip install .  # 不推荐
```

<!-- ## 安装适配器

适配器可以通过 `nb-cli` 在创建项目时根据你的选择自动安装，也可以自行使用 `pip` 安装

```bash
pip install <adapter-name>
```

```bash
# 列出所有的适配器
nb adapter list
```

## 安装插件

插件可以通过 `nb-cli` 进行安装，也可以自行安装并加载插件。

```bash
# 列出所有的插件
nb plugin list
# 搜索插件
nb plugin search <plugin-name>
# 安装插件
nb plugin install <plugin-name>
```

如果急于上线 Bot 或想要使用现成的插件，以下插件可作为参考：

### 官方插件

- [NoneBot-Plugin-Docs](https://github.com/nonebot/nonebot2/tree/master/packages/nonebot-plugin-docs) 离线文档插件
- [NoneBot-Plugin-Test](https://github.com/nonebot/plugin-test) 本地机器人测试前端插件
- [NoneBot-Plugin-APScheduler](https://github.com/nonebot/plugin-apscheduler) 定时任务插件
- [NoneBot-Plugin-LocalStore](https://github.com/nonebot/plugin-localstore) 本地数据文件存储插件
- [NoneBot-Plugin-Sentry](https://github.com/cscs181/QQ-GitHub-Bot/tree/master/src/plugins/nonebot_plugin_sentry) Sentry 在线日志分析插件
- [NoneBot-Plugin-Status](https://github.com/cscs181/QQ-GitHub-Bot/tree/master/src/plugins/nonebot_plugin_status) 服务器状态查看插件

### 其他插件

还有更多的插件在 [这里](/store) 等着你发现～

## 安装开发环境(可选)

NoneBot v2 全程使用 `VSCode` 搭配 `Pylance` 的开发环境进行开发，在严格的类型检查下，NoneBot v2 具有完善的类型设计与声明。

在围绕 NoneBot v2 进行开发时，使用 `VSCode` 搭配 `Pylance` 进行类型检查是非常推荐的。这有利于统一代码风格及避免低级错误的发生。 -->
