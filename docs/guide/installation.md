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
