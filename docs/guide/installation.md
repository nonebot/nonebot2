# 安装

## NoneBot

:::warning 注意
请确保你的 Python 版本 >= 3.7。
:::

请在安装 nonebot2 之前卸载 nonebot 1.x

```bash
pip uninstall nonebot
pip install nonebot2
```

如果你需要使用最新的（可能尚未发布的）特性，可以直接从GitHub仓库安装：

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

## 额外依赖

### APScheduler

A task scheduling library for Python.

可用于计划任务，后台执行任务等

```bash
pip install nonebot2[scheduler]
poetry add nonebot2[scheduler]
```

[View On GitHub](https://github.com/agronholm/apscheduler)

### NoneBot-Test

A test frontend for nonebot2.

通过前端展示 nonebot 已加载的插件以及运行状态，同时可以用于模拟发送事件测试机器人

```bash
pip install nonebot2[test]
poetry add nonebot2[test]
```

[View On GitHub](https://github.com/nonebot/nonebot-test)

### CLI

CLI for nonebot2.

一个多功能脚手架

```bash
pip install nonebot2[cli]
poetry add nonebot2[cli]
```

[View On GitHub](https://github.com/yanyongyu/nb-cli)

### 我全都要

```bash
pip install nonebot2[full]
poetry add nonebot2[full]
```

```bash
pip install nonebot2[cli,scheduler]
poetry add nonebot2[cli,scheduler]
```
