---
sidebar_position: 11
description: 部署你的机器人
---

# 部署

在编写完成后，你需要部署你的机器人来使得用户能够使用它。通常，会将机器人部署在服务器上，来保证服务持久运行。

在开发时机器人运行的环境称为开发环境，而在部署后机器人运行的环境称为生产环境。与开发环境不同的是，在生产环境中，开发者通常不能随意地修改/添加/删除代码，开启或停止服务。

## 部署前准备

在生产环境中，为确保机器人能够正常运行，你需要固定你的依赖库版本。下面提供了几种常见的文件格式与生成方式：

- `poetry.lock`

  [poetry](https://python-poetry.org/) 依赖管理工具使用的 lock 文件，通常会在安装依赖时自动生成，或者使用 `poetry lock` 来生成。

- `pdm.lock`

  [pdm](https://pdm.fming.dev/) 依赖管理工具使用的 lock 文件，通常会在安装依赖时自动生成，或者使用 `pdm lock` 来生成。

- `Pipfile.lock`

  [Pipenv](https://pipenv.pypa.io/en/latest/) 依赖管理工具使用的 lock 文件，通常会在安装依赖时自动生成，或者使用 `pipenv lock` 来生成。

- `requirements.txt`

  如果你未使用任何依赖管理工具，你可以使用 `pip freeze` 来生成这个文件。

## 使用 Docker 部署（推荐）

请自行参考 [Docker 官方文档](https://docs.docker.com/engine/install/) 安装 Docker。

在生产环境安装 [docker-compose](https://docs.docker.com/compose/) 工具以便部署机器人。

### 编译镜像与部署配置

在项目目录下添加以下两个文件（以 poetry 和 FastAPI 驱动器为例）：

```dockerfile title=Dockerfile
FROM python:3.9 as requirements-stage

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN curl -sSL https://install.python-poetry.org -o install-poetry.py

RUN python install-poetry.py --yes

ENV PATH="${PATH}:/root/.local/bin"

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN rm requirements.txt

COPY ./ /app/
```

```yaml title=docker-compose.yml
version: "3"
services:
  nonebot:
    build: .
    ports:
      - "8080:8080" # 映射端口到宿主机 宿主机端口:容器端口
    env_file:
      - ".env.prod" # fastapi 使用的环境变量文件
    environment:
      - ENVIRONMENT=prod
      - APP_MODULE=bot:app
      - MAX_WORKERS=1
    network_mode: bridge
```

配置完成后即可使用 `docker-compose up -d` 命令来启动机器人并在后台运行。

### CI/CD

配合 GitHub Actions 可以完成 CI/CD，在 GitHub 上发布 Release 时自动部署至生产环境。

在 [Docker Hub](https://hub.docker.com/) 上创建仓库，并将下方 workflow 文件中高亮行中的仓库名称替换为你的仓库名称。

前往项目仓库的 `Settings` > `Secrets` > `actions` 栏目 `New Repository Secret` 添加部署所需的密钥：

- `DOCKERHUB_USERNAME`: 你的 Docker Hub 用户名
- `DOCKERHUB_PASSWORD`: 你的 Docker Hub PAT（[创建方法](https://docs.docker.com/docker-hub/access-tokens/)）
- `DEPLOY_HOST`: 部署服务器 IP 地址
- `DEPLOY_USER`: 部署服务器用户名
- `DEPLOY_KEY`: 部署服务器私钥
- `DEPLOY_PATH`: 部署服务器上的项目路径

将以下文件添加至项目下的 `.github/workflows/` 目录下：

```yaml title=.github/workflows/build.yml {30}
name: Docker Hub Release

on:
  push:
    tags:
      - "v*"

jobs:
  docker:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Setup Docker
        uses: docker/setup-buildx-action@v1

      - name: Login to DockerHub
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_PASSWORD }}

      - name: Generate Tags
        uses: docker/metadata-action@v3
        id: metadata
        with:
          images: |
            {organization}/{repository}
          tags: |
            type=semver,pattern={{version}}
            type=sha

      - name: Build and Publish
        uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: ${{ steps.metadata.outputs.tags }}
          labels: ${{ steps.metadata.outputs.labels }}
```

```yaml title=.github/workflows/deploy.yml
name: Deploy

on:
  workflow_run:
    workflows:
      - Docker Hub Release
    types:
      - completed

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    steps:
      - name: start deployment
        uses: bobheadxi/deployments@v0.6
        id: deployment
        with:
          step: start
          token: ${{ secrets.GITHUB_TOKEN }}
          env: official-bot

      - name: remote ssh command
        uses: appleboy/ssh-action@master
        env:
          DEPLOY_PATH: ${{ secrets.DEPLOY_PATH }}
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_KEY }}
          envs: DEPLOY_PATH
          script: |
            cd $DEPLOY_PATH
            docker-compose down
            docker-compose pull
            docker-compose up -d

      - name: update deployment status
        uses: bobheadxi/deployments@v0.6
        if: always()
        with:
          step: finish
          token: ${{ secrets.GITHUB_TOKEN }}
          status: ${{ job.status }}
          deployment_id: ${{ steps.deployment.outputs.deployment_id }}
```

将上一部分的 `docker-compose.yml` 文件以及 `.env.prod` 配置文件添加至 `DEPLOY_PATH` 目录下，并修改 `docker-compose.yml` 文件中的镜像配置，替换为 Docker Hub 的仓库名称。

```diff
- build: .
+ image: {organization}/{repository}:latest
```

## 使用 Supervisor 部署

参考：[Uvicorn - Supervisor](https://www.uvicorn.org/deployment/#supervisor)

```ini
[supervisord]

[fcgi-program:nonebot]
socket=tcp://localhost:8080
command=python3 -m uvicorn --fd 0 bot:app
directory=/path/to/bot
autorestart=true
startsecs=10
startretries=3
numprocs=1
process_name=%(program_name)s-%(process_num)d
stdout_logfile=/path/to/log/nonebot.out.log
stdout_logfile_maxbytes=2MB
```

:::warning 警告
请配合虚拟环境使用，如 venv 等，请勿直接在 Linux 服务器系统环境中安装。
:::

## 使用 PM2 部署

> Todo PM2 安装教程
>
> 暂缺 pm2 安装配置教程，请自行查询有关安装说明。
>
> [pm2 安装相关搜索*bing*](https://cn.bing.com/search?q=pm2+%E5%AE%89%E8%A3%85+-csdn)

### 变量说明

文档以下变量将会使用：

`{bot_dir}` 指代 none_bot 的根目录。

`{bot_run.py}` 指代 none_bot 的根目录下启动文件。

`{bot_name}` 指代 none_bot 的命名，用于指定 pm2 别名标示。

请根据自己的情况替换变量以使用本文提供的脚本。

---

### 默认环境

> #### 说明
>
> 编者在实践中发现使用虚拟环境后再通过 `pm2` 部署 `bot` 可能会导致不能启动 chromium 导致一些插件无法使用。
>
> 推测是由于使用了非 `root` 启动 `pm2` 导致的问题，有提供解决方案。

#### 请先确保成功安装了 pm2

指令 `pm2 -V` 如返回正确的版本号，则为成功。

```shell
> pm2 -V
5.2.0
```

#### 启动

如果启动有问题请查阅 >> [教程 - 启动](https://v2.nonebot.dev/docs/tutorial/create-project#%E5%90%AF%E5%8A%A8-bot)

`pm2` 会自动将任务守护运行，不会输出日志。请使用 `pm2 log` 查看

```bash
# 启动 bot
pm2 start -n '{bot_name}' -x 'cd {bot_dir} && nb run {bot_run.py}'
```

#### 日志

- 默认**日志**
  查看最近 150 行日志

  - `pm2 log {bot_name} --lines 150`

- Minot **监控**
  - `pm2 monit`

#### 其他常用 pm2 指令

> 仅作提示常用到的 pm2 相关指令。
>
> 更多指令及其详细请移步查阅 >> [pm2\_官方文档](https://pm2.keymetrics.io/docs/usage/pm2-doc-single-page/)

- 展示当前 pm2 管理的**所有 APP**
  - `pm2 ls`
- **删除**
  - `pm2 del [id][app_name]`
- **停止**
  - `pm2 stop [id][app_name]`
- **重启**
  - `pm2 restart [id][app_name]`
- **保存**当前 APP 列表 & 恢复 APP 列表
  - `pm2 save`
  - `pm2 resurrect`
- 开启 pm2 **开机自动恢复** APP 列表
  - **说明**：
    需要执行过 `pm2 save`
    非 root 需要手动添加指令返回的环境变量
  - `pm2 startup`

---

### 虚拟环境部署

> 除了 pm2 start 以外理论上使用没有区别
>
> 如果您使用虚拟环境管理依赖，请确保已安装 nb-cli，并且已激活到当前 Bot 所在的虚拟环境。
>
> 仅尝试 poetry，其他 python 虚拟环境管理器请自测

#### 启动

```bash
# 启动 bot
pm2 start -n '{bot_name}' -x 'cd {bot_dir} && poetry run python3 {bot_run.py}'
```

#### 非 root 如果遇到 bug 请尝试

特别变量说明 `{user}` 指 poetry 的安装用户

如果直接是 root 安装的...请运行上一条指令

```bash
sudo pm2 start -n '{bot_name}' -x su - {user} -c 'cd {bot_dir} && poetry run python3 {bot_run.py}'
```
