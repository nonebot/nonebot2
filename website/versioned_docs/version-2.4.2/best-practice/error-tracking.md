---
sidebar_position: 2
description: 使用 sentry 进行错误跟踪
---

# 错误跟踪

在应用实际运行过程中，可能会出现各种各样的错误。可能是由于代码逻辑错误，也可能是由于用户输入错误，甚至是由于第三方服务的错误。这些错误都会导致应用的运行出现问题，这时候就需要对错误进行跟踪，以便及时发现问题并进行修复。NoneBot 提供了 `nonebot-plugin-sentry` 插件，支持 [sentry](https://sentry.io/) 平台，可以方便地进行错误跟踪。

## 安装插件

在使用前请先安装 `nonebot-plugin-sentry` 插件至项目环境中，可参考[获取商店插件](../tutorial/store.mdx#安装插件)来了解并选择安装插件的方式。如：

在**项目目录**下执行以下命令：

```bash
nb plugin install nonebot-plugin-sentry
```

## 使用插件

在安装完成之后，仅需要对插件进行简单的配置即可使用。

### 获取 sentry DSN

前往 [sentry](https://sentry.io/) 平台，注册并创建一个新的项目，然后在项目设置中找到 `Client Keys (DSN)`，复制其中的 `DSN` 值。

### 配置插件

:::caution 注意
错误跟踪通常在生产环境中使用，因此开发环境中 `sentry_dsn` 留空即会停用插件。
:::

在项目 dotenv 配置文件中添加以下配置即可使用：

```dotenv
SENTRY_DSN=<your_sentry_dsn>
```

## 配置项

配置项具体含义参考 [Sentry Docs](https://docs.sentry.io/platforms/python/configuration/options/)。

- `sentry_dsn: str`
- `sentry_debug: bool = False`
- `sentry_release: str | None = None`
- `sentry_release: str | None = None`
- `sentry_environment: str | None = nonebot env`
- `sentry_server_name: str | None = None`
- `sentry_sample_rate: float = 1.`
- `sentry_max_breadcrumbs: int = 100`
- `sentry_attach_stacktrace: bool = False`
- `sentry_send_default_pii: bool = False`
- `sentry_in_app_include: List[str] = Field(default_factory=list)`
- `sentry_in_app_exclude: List[str] = Field(default_factory=list)`
- `sentry_request_bodies: str = "medium"`
- `sentry_with_locals: bool = True`
- `sentry_ca_certs: str | None = None`
- `sentry_before_send: Callable[[Any, Any], Any | None] | None = None`
- `sentry_before_breadcrumb: Callable[[Any, Any], Any | None] | None = None`
- `sentry_transport: Any | None = None`
- `sentry_http_proxy: str | None = None`
- `sentry_https_proxy: str | None = None`
- `sentry_shutdown_timeout: int = 2`
