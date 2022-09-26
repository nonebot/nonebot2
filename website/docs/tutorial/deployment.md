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
- `DEPLOY_HOST`: 部署服务器的 SSH 地址
- `DEPLOY_USER`: 部署服务器用户名
- `DEPLOY_KEY`: 部署服务器私钥 ([创建方法](https://github.com/appleboy/ssh-action#setting-up-a-ssh-key))
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
        uses: bobheadxi/deployments@v1
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
        uses: bobheadxi/deployments@v0.6.2
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

:::tip 提示
在阅读这一节的过程中, 你总是可以参照 [PM2 官方文档](https://pm2.keymetrics.io/docs/usage/quick-start/) 来得到更多的信息
:::

### 安装 PM2

需要有 NodeJS 10+环境来运行 PM2, ~~(什么 NTR)~~

然后通过以下命令安装即可:

```shell
npm install -g pm2
```

在安装完成后, 执行以下指令, 如果得到类似的输出则说明你安装成功了 PM2:

```shell
$ pm2 -V
5.2.0
```

### 在后台运行进程

:::tip 提示
以下步骤要求您在您 Bot 的工作目录下执行

如果您使用了虚拟环境, 请确保 Bot 启动命令能在虚拟环境中正常执行

换言之, Bot 程序需要在当前终端环境下正常运行
:::

#### 启动 Bot 进程

```shell
$ pm2 start "python -m nb_cli run" # 或者直接 nb run 也行

[PM2] Starting /usr/bin/bash in fork_mode (1 instance)
[PM2] Done.
┌─────┬────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id  │ name   │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├─────┼────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0   │ nb run │ default     │ N/A     │ fork    │ 93061    │ 0s     │ 0    │ online    │ 0%       │ 8.3mb    │ mix      │ disabled │
└─────┴────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
```

此时 Bot 进程就在后台运行了, 注意到表格第一列的 ID, 它可以用来查看和控制进程的状态

#### 在虚拟环境下启动 Bot 进程（以 Poetry 为例）

再次提醒注意必须先切换到 Bot 的工作目录下

```shell
# 获取虚拟环境路径
$ poetry env info | grep virtualenv.*python | awk '{print $2}'
/home/noah/.cache/pypoetry/virtualenvs/none-bot-guhZIsCX-py3.8/bin/python

# 此处在 interpreter 后填入上述虚拟环境路径，在 name 处填入想取的项目名
$ pm2 start ./bot.py --name=zhenxun --interpreter /home/noah/.cache/pypoetry/virtualenvs/none-bot-guhZIsCX-py3.8/bin/python

[PM2] Starting /home/noah/zhenxun_bot/bot.py in fork_mode (1 instance)
[PM2] Done.
┌─────┬──────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id  │ name             │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├─────┼──────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 1   │ zhenxun          │ default     │ N/A     │ fork    │ 2515037  │ 0s     │ 0    │ online    │ 0%       │ 8.1mb    │ noah     │ disabled │
└─────┴──────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
```

此时 Bot 进程就在后台运行了, 注意到表格第一列的 ID 和第二列的 name, 它们都可以用来查看和控制进程的状态

#### 常用命令

更具体的用法请移步 PM2 官方文档, ~~如果想要详细示例建议直接上手试试~~

其中命令中的所有`<id>`应该替换为上文启动进程后返回的 ID

- 查看最近 150 行日志

  - `pm2 log <id> --lines 150`

- 实时监控所有进程日志

  - `pm2 monit`

- 展示当前 PM2 管理的所有进程

  - `pm2 ls`

- 停止某个进程

  - `pm2 stop <id>`

- 删除某个进程

  - `pm2 del <id>`

- 重启某个进程

  - `pm2 restart <id>`

- 保存当前进程列表

  - `pm2 save`

- 恢复保存的进程列表

  - `pm2 resurrect`

- 设置开机自动启动进程列表
  - `pm2 startup`
  - 需要执行过 `pm2 save`  
    如果不是 root 用户执行, 则需要手动添加指令返回的环境变量
