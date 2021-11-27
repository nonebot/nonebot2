---
contentSidebar: true
sidebarDepth: 0
---

# NoneBot.exception 模块

## 异常

下列文档中的异常是所有 NoneBot 运行时可能会抛出的。
这些异常并非所有需要用户处理，在 NoneBot 内部运行时被捕获，并进行对应操作。


## _exception_ `NoneBotException`

基类：`Exception`


* **说明**

    所有 NoneBot 发生的异常基类。



## _exception_ `ParserExit`

基类：`nonebot.exception.NoneBotException`


* **说明**

    `shell command` 处理消息失败时返回的异常



* **参数**

    
    * `status`


    * `message`



## _exception_ `ProcessException`

基类：`nonebot.exception.NoneBotException`


* **说明**

    事件处理过程中发生的异常基类。



## _exception_ `IgnoredException`

基类：`nonebot.exception.ProcessException`


* **说明**

    指示 NoneBot 应该忽略该事件。可由 PreProcessor 抛出。



* **参数**

    
    * `reason`: 忽略事件的原因



## _exception_ `MockApiException`

基类：`nonebot.exception.ProcessException`


* **说明**

    指示 NoneBot 阻止本次 API 调用或修改本次调用返回值，并返回自定义内容。可由 api hook 抛出。



* **参数**

    
    * `result`: 返回的内容



## _exception_ `StopPropagation`

基类：`nonebot.exception.ProcessException`


* **说明**

    指示 NoneBot 终止事件向下层传播。



* **用法**

    在 `Matcher.block == True` 时抛出。



## _exception_ `MatcherException`

基类：`nonebot.exception.NoneBotException`


* **说明**

    所有 Matcher 发生的异常基类。



## _exception_ `SkippedException`

基类：`nonebot.exception.MatcherException`


* **说明**

    指示 NoneBot 立即结束当前 `Handler` 的处理，继续处理下一个 `Handler`。



* **用法**

    可以在 `Handler` 中通过 `Matcher.skip()` 抛出。



## _exception_ `PausedException`

基类：`nonebot.exception.MatcherException`


* **说明**

    指示 NoneBot 结束当前 `Handler` 并等待下一条消息后继续下一个 `Handler`。
    可用于用户输入新信息。



* **用法**

    可以在 `Handler` 中通过 `Matcher.pause()` 抛出。



## _exception_ `RejectedException`

基类：`nonebot.exception.MatcherException`


* **说明**

    指示 NoneBot 结束当前 `Handler` 并等待下一条消息后重新运行当前 `Handler`。
    可用于用户重新输入。



* **用法**

    可以在 `Handler` 中通过 `Matcher.reject()` 抛出。



## _exception_ `FinishedException`

基类：`nonebot.exception.MatcherException`


* **说明**

    指示 NoneBot 结束当前 `Handler` 且后续 `Handler` 不再被运行。
    可用于结束用户会话。



* **用法**

    可以在 `Handler` 中通过 `Matcher.finish()` 抛出。



## _exception_ `AdapterException`

基类：`nonebot.exception.NoneBotException`


* **说明**

    代表 `Adapter` 抛出的异常，所有的 `Adapter` 都要在内部继承自这个 `Exception`



* **参数**

    
    * `adapter_name: str`: 标识 adapter



## _exception_ `NoLogException`

基类：`nonebot.exception.AdapterException`


* **说明**

    指示 NoneBot 对当前 `Event` 进行处理但不显示 Log 信息，可在 `get_log_string` 时抛出



## _exception_ `ApiNotAvailable`

基类：`nonebot.exception.AdapterException`


* **说明**

    在 API 连接不可用时抛出。



## _exception_ `NetworkError`

基类：`nonebot.exception.AdapterException`


* **说明**

    在网络出现问题时抛出，如: API 请求地址不正确, API 请求无返回或返回状态非正常等。



## _exception_ `ActionFailed`

基类：`nonebot.exception.AdapterException`


* **说明**

    API 请求成功返回数据，但 API 操作失败。
