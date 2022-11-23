---
sidebar_position: 10
description: 扩展自定义服务端 API
---

# 添加自定义 API

由于 NoneBot2 可以使用 `ReverseDriver` （即服务端框架）来进行驱动，因此可以将 NoneBot2 来作为一个服务端程序来提供 API 接口等功能。

在扩展 API 之前，你首先需要确保 NoneBot2 使用的是 `ReverseDriver`，详情可以参考 [选择驱动器](./choose-driver.md)。下面我们以 FastAPI 驱动器为例，来演示如何添加自定义 API。

## 获取 APP 实例

在定义 API 接口之前，需要先获取到驱动器框架的 APP 实例。

```python {4}
import nonebot
from fastapi import FastAPI

app: FastAPI = nonebot.get_app()

@app.get("/api")
async def custom_api():
    return {"message": "Hello, world!"}
```

## 添加接口

在获取到当前驱动器的 APP 实例后，即可以直接使用驱动器框架提供的方法来添加 API 接口。

在下面的代码中，我们添加了一个 `GET` 类型的 `/api` 接口，具体方法参考 [FastAPI 文档](https://fastapi.tiangolo.com/)。

```python {6-8}
import nonebot
from fastapi import FastAPI

app: FastAPI = nonebot.get_app()

@app.get("/api")
async def custom_api():
    return {"message": "Hello, world!"}
```
