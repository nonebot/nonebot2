---
sidebar_position: 3
description: 依赖注入
---

# 依赖注入

`nonebot-plugin-orm` 提供了强大且灵活的依赖注入，可以方便地帮助你获取数据库会话和查询数据。

## 数据库会话

### AsyncSession

新数据库会话，常用于有独立的数据库操作逻辑的插件。

```python {13,26}
from nonebot import on_message
from nonebot.params import Depends
from nonebot_plugin_orm import AsyncSession, Model, async_scoped_session
from sqlalchemy.orm import Mapped, mapped_column

message = on_message()


class Message(Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


async def get_message(session: AsyncSession) -> Message:
    # 等价于 session = get_session()
    async with session:
        msg = Message()

        session.add(msg)
        await session.commit()
        await session.refresh(msg)

        return msg


@message.handle()
async def _(session: async_scoped_session, msg: Message = Depends(get_message)):
    await session.rollback()  # 无法回退 get_message() 中的更改
    await message.send(str(msg.id))  # msg 被存储，msg.id 递增
```

### async_scoped_session

数据库作用域会话，常用于事件响应器和有与响应逻辑相关的数据库操作逻辑的插件。

```python {13，26}
from nonebot import on_message
from nonebot.params import Depends
from nonebot_plugin_orm import Model, async_scoped_session
from sqlalchemy.orm import Mapped, mapped_column

message = on_message()


class Message(Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


async def get_message(session: async_scoped_session) -> Message:
    # 等价于 session = get_scoped_session()
    msg = Message()

    session.add(msg)
    await session.flush()
    await session.refresh(msg)

    return msg


@message.handle()
async def _(session: async_scoped_session, msg: Message = Depends(get_message)):
    await session.rollback()  # 可以回退 get_message() 中的更改
    await message.send(str(msg.id))  # msg 没有被存储，msg.id 不变
```

## 查询数据

### Model

支持类作为依赖。

```python
from typing import Annotated

from nonebot.params import Depends
from nonebot_plugin_orm import Model
from sqlalchemy.orm import Mapped, mapped_column


def get_id() -> int: ...


class Message(Model):
    id: Annotated[Mapped[int], Depends(get_id)] = mapped_column(
        primary_key=True, autoincrement=True
    )


async def _(msg: Message):
    # 等价于 msg = (
    #     await (await session.stream(select(Message).where(Message.id == get_id())))
    #     .scalars()
    #     .one_or_none()
    # )
    ...
```

### SQLDepends

参数为一个 SQL 语句，决定依赖注入的内容，SQL 语句中可以使用子依赖。

```python {11-13}
from nonebot.params import Depends
from nonebot_plugin_orm import Model, SQLDepends
from sqlalchemy import select


def get_id() -> int: ...


async def _(
    model: Model = SQLDepends(select(Model).where(Model.id == Depends(get_id))),
): ...
```

参数可以是任意 SQL 语句，但不建议使用 `select` 以外的语句，因为语句可能没有返回值（`returning` 除外），而且代码不清晰。

### 类型标注

类型标注决定依赖注入的数据结构，主要影响以下几个层面：

- 迭代器（`session.execute()`）或异步迭代器（`session.stream()`）
- 标量（`session.execute().scalars()`）或元组（`session.execute()`）
- 一个（`session.execute().one_or_none()`，注意 `None` 时可能触发 [重载](../../../appendices/overload#重载)）或全部（`session.execute()` / `session.execute().all()`）
- 连续（`session().execute()`）或分块（`session.execute().partitions()`）

具体如下（可以使用父类型作为类型标注）：

- ```python
  async def _(rows_partitions: AsyncIterator[Sequence[Tuple[Model, ...]]]):
      # 等价于 rows_partitions = await (await session.stream(sql).partitions())

      async for partition in rows_partitions:
          for row in partition:
              print(row[0], row[1], ...)
  ```

- ```python
  async def _(model_partitions: AsyncIterator[Sequence[Model]]):
      # 等价于 model_partitions = await (await session.stream(sql).scalars().partitions())

      async for partition in model_partitions:
          for model in partition:
              print(model)
  ```

- ```python
  async def _(row_partitions: Iterator[Sequence[Tuple[Model, ...]]]):
      # 等价于 row_partitions = await session.execute(sql).partitions()

      for partition in rows_partitions:
          for row in partition:
              print(row[0], row[1], ...)
  ```

- ```python
  async def _(model_partitions: Iterator[Sequence[Model]]):
      # 等价于 model_partitions = await (await session.execute(sql).scalars().partitions())

      for partition in model_partitions:
          for model in partition:
              print(model)
  ```

- ```python
  async def _(rows: sa_async.AsyncResult[Tuple[Model, ...]]):
      # 等价于 rows = await session.stream(sql)

      async for row in rows:
          print(row[0], row[1], ...)
  ```

- ```python
  async def _(models: sa_async.AsyncScalarResult[Model]):
      # 等价于 models = await session.stream(sql).scalars()

      async for model in models:
          print(model)
  ```

- ```python
  async def _(rows: sa.Result[Tuple[Model, ...]]):
      # 等价于 rows = await session.execute(sql)

      for row in rows:
          print(row[0], row[1], ...)
  ```

- ```python
  async def _(models: sa.ScalarResult[Model]):
      # 等价于 models = await session.execute(sql).scalars()

      for model in models:
          print(model)
  ```

- ```python
  async def _(rows: Sequence[Tuple[Model, ...]]):
      # 等价于 rows = await (await session.stream(sql).all())

      for row in rows:
            print(row[0], row[1], ...)
  ```

- ```python
  async def _(models: Sequence[Model]):
      # 等价于 models = await (await session.stream(sql).scalars().all())

      for model in models:
          print(model)
  ```

- ```python
  async def _(row: Tuple[Model, ...]):
      # 等价于 row = await (await session.stream(sql).one_or_none())

      print(row[0], row[1], ...)
  ```

- ```python
  async def _(model: Model):
      # 等价于 model = await (await session.stream(sql).scalars().one_or_none())

      print(model)
  ```
