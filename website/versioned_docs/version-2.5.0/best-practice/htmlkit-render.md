---
sidebar_position: 8
description: 轻量化 HTML 绘图
---

# 轻量化 HTML 绘图

图片是机器人交互中不可或缺的一部分，对于信息展示的直观性、美观性有很大的作用。
基于 PIL 直接绘制图片具有良好的性能和存储开销，但是难以调试、维护过程式的绘图代码。
使用浏览器渲染类插件可以方便地绘制网页，且能够直接通过 JS 对网页效果进行编程，但是它占用的存储和内存空间相对可观。

NoneBot 提供的 `nonebot-plugin-htmlkit` 提供了另一种基于 HTML 和 CSS 语法的轻量化绘图选择：它基于 `litehtml` 解析库，无须安装额外的依赖即可使用，没有进程间通信带来的额外开销，且在支持 `webp` `avif` 等丰富图片格式的前提下，安装用的 wheel 文件大小仅有约 10 MB。

作为粗略的性能参考，在一台 Ryzen 7 9700X 的 Windows 电脑上，渲染 [PEP 7](https://peps.python.org/pep-0007/) 的 HTML 页面（分辨率为 800x5788，大小约 1.4MB，从本地文件系统读取 CSS）大约需要 100ms，每个渲染任务内存最高占用约为 40MB.

## 安装插件

在使用前请先安装 `nonebot-plugin-htmlkit` 插件至项目环境中，可参考[获取商店插件](../tutorial/store.mdx#安装插件)来了解并选择安装插件的方式。如：

在**项目目录**下执行以下命令：

```bash
nb plugin install nonebot-plugin-htmlkit
```

`nonebot-plugin-htmlkit` 插件目前兼容以下系统架构：

- Windows x64
- macOS arm64（M-系列芯片）
- Linux x64 （非 Alpine 等 musl 系发行版）
- Linux arm64 （非 Alpine 等 musl 系发行版）

:::caution 访问网络内容

如果需要访问网络资源（如 http(s) 网页内容），NoneBot 需要客户端型驱动器（Forward）。内置的驱动器有 `~httpx` 与 `~aiohttp`。

详见[选择驱动器](../advanced/driver.md)。

:::

## 使用插件

### 加载插件

在使用本插件前同样需要使用 `require` 方法进行**加载**并**导入**需要使用的方法，可参考 [跨插件访问](../advanced/requiring.md) 一节进行了解，如：

```python
from nonebot import require

require("nonebot_plugin_htmlkit")

from nonebot_plugin_htmlkit import html_to_pic, md_to_pic, template_to_pic, text_to_pic
```

插件会自动使用[配置中的参数](#配置-fontconfig)初始化 `fontconfig` 以提供字体查找功能。

### 渲染 API

`nonebot-plugin-htmlkit` 主要提供以下**异步**渲染函数：

#### html_to_pic

```python
async def html_to_pic(
    html: str,
    *,
    base_url: str = "",
    dpi: float = 144.0,
    max_width: float = 800.0,
    device_height: float = 600.0,
    default_font_size: float = 12.0,
    font_name: str = "sans-serif",
    allow_refit: bool = True,
    image_format: Literal["png", "jpeg"] = "png",
    jpeg_quality: int = 100,
    lang: str = "zh",
    culture: str = "CN",
    img_fetch_fn: ImgFetchFn = combined_img_fetcher,
    css_fetch_fn: CSSFetchFn = combined_css_fetcher,
    urljoin_fn: Callable[[str, str], str] = urllib3.parse.urljoin,
) -> bytes:
    ...
```

最核心的渲染函数。

`base_url` 和 `urljoin_fn` 控制着传入 `image_fetch_fn` 和 `css_fetch_fn` 回调的 url 内容。

`allow_refit` 如果为真，渲染时会自动缩小产出图片的宽度到最适合的宽度，否则必定产出 `max_width` 宽度的图片。

`max_width` 与 `device_height` 会在 `@media` 判断中被使用。

`img_fetch_fn` 预期为一个异步可调用对象（函数），接收图片 url 并返回对应 url 的 jpeg 或 png 二进制数据（`bytes`），可在拒绝加载时返回 `None`.

`css_fetch_fn` 预期为一个异步可调用对象（函数），接收目标 CSS url 并返回对应 url 的 CSS 文本（`str`），可在拒绝加载时返回 `None`.

以下为辅助的封装函数，关键字参数若未特殊说明均与 `html_to_pic` 含义相同。

#### text_to_pic

```python
async def text_to_pic(
    text: str,
    css_path: str = "",
    *,
    max_width: int = 500,
    allow_refit: bool = True,
    image_format: Literal["png", "jpeg"] = "png",
    jpeg_quality: int = 100,
) -> bytes:
    ...
```

可用于渲染多行文本。

`text` 会被放置于 `<div id="main" class="main-box"> <div class="text">` 中，可据此编写 CSS 来改变文本表现。

#### md_to_pic

```python
async def md_to_pic(
    md: str = "",
    md_path: str = "",
    css_path: str = "",
    *,
    max_width: int = 500,
    img_fetch_fn: ImgFetchFn = combined_img_fetcher,
    allow_refit: bool = True,
    image_format: Literal["png", "jpeg"] = "png",
    jpeg_quality: int = 100,
) -> bytes:
    ...
```

可用于渲染 Markdown 文本。默认为 GitHub Markdown Light 风格，支持基于 `pygments` 的代码高亮。

`md` 和 `md_path` 二选一，前者设置时应为 Markdown 的文本，后者设置时应为指向 Markdown 文本文件的路径。

#### template_to_pic

```python
async def template_to_pic(
    template_path: str | PathLike[str] | Sequence[str | PathLike[str]],
    template_name: str,
    templates: Mapping[Any, Any],
    filters: None | Mapping[str, Any] = None,
    *,
    max_width: int = 500,
    device_height: int = 600,
    base_url: str | None = None,
    img_fetch_fn: ImgFetchFn = combined_img_fetcher,
    css_fetch_fn: CSSFetchFn = combined_css_fetcher,
    allow_refit: bool = True,
    image_format: Literal["png", "jpeg"] = "png",
    jpeg_quality: int = 100,
) -> bytes:
    ...
```

渲染 jinja2 模板。

`template_path` 为 jinja2 环境的路径，`template_name` 是环境中要加载模板的名字，`templates` 为传入模板的参数，`filters` 为过滤器名 -> 自定义过滤器的映射。

### 控制外部资源获取

通过传入 `img_fetch_fn` 与 `css_fetch_fn`，我们可以在实际访问资源前进行审查，修改资源的来源，或是对 IO 操作进行缓存。

`img_fetch_fn` 预期为一个异步可调用对象（函数），接收图片 url 并返回对应 url 的 jpeg 或 png 二进制数据（`bytes`），可在拒绝加载时返回 `None`.

`css_fetch_fn` 预期为一个异步可调用对象（函数），接收目标 CSS url 并返回对应 url 的 CSS 文本（`str`），可在拒绝加载时返回 `None`.

如果你想要禁用外部资源加载/只从文件系统加载/只从网络加载，可以使用 `none_fetcher` `filesystem_***_fetcher` `network_***_fetcher`。

默认的 fetcher 行为（对于 `file://` 从文件系统加载，其余从网络加载）位于 `combined_***_fetcher`，可以通过对其封装实现缓存等操作。

## 配置项

### 配置 fontconfig

`htmlkit` 使用 `fontconfig` 查找字体，请参阅 [`fontconfig 用户手册`](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user) 了解环境变量的具体含义、如何通过编写配置文件修改字体配置等。

#### fontconfig_file

- **类型**: `str | None`
- **默认值**: `None`

覆盖默认的配置文件路径。

#### fontconfig_path

- **类型**: `str | None`
- **默认值**: `None`

覆盖默认的配置目录。

#### fontconfig_sysroot

- **类型**: `str | None`
- **默认值**: `None`

覆盖默认的 sysroot。

#### fc_debug

- **类型**: `str | None`
- **默认值**: `None`

设置 Fontconfig 的 debug 级别。

#### fc_dbg_match_filter

- **类型**: `str | None`
- **默认值**: `None`

当 `FC_DEBUG` 设置为 `MATCH2` 时，过滤 debug 输出。

#### fc_lang

- **类型**: `str | None`
- **默认值**: `None`

设置默认语言，否则从 `LOCALE` 环境变量获取。

#### fontconfig_use_mmap

- **类型**: `str | None`
- **默认值**: `None`

是否使用 `mmap(2)` 读取字体缓存。
