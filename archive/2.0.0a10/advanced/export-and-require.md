# 跨插件访问

由于 `nonebot2` 独特的插件加载机制，在使用 python 原有的 import 机制来进行插件之间的访问时，很可能会有奇怪的或者意料以外的情况发生。为了避免这种情况的发生，您可以有两种方法来实现跨插件访问：

1. 将插件间的要使用的公共代码剥离出来，作为公共文件或者文件夹，提供给插件加以调用。
2. 使用 `nonebot2` 提供的 `export` 和 `require` 机制，来实现插件间的互相调用。

第一种方法比较容易理解和实现，这里不再赘述，但需要注意的是，请不要将公共文件或者公共文件夹作为**插件**被 `nonebot2` 加载。

下面将介绍第二种方法—— `export` 和 `require` 机制：

## 使用 export and require

现在，假定有两个插件 `pluginA` 和 `pluginB`，需要在 `pluginB` 中调用 `pluginA` 中的一个变量 `varA` 和一个函数 `funcA`。

在上面的条件中涉及到了两种操作：一种是在 `pluginA` 的 `导出对象` 操作；而另一种是在 `pluginB` 的 `导入对象` 操作。在 `nonebot2` 中，`导出对象` 的操作用 `export` 机制来实现，`导入对象` 的操作用 `require` 机制来实现。下面，我们将逐一进行介绍。

:::warning 警告

使用这个方法进行跨插件访问时，**需要先加载`导出对象`的插件，再加载`导入对象`的插件。**

:::

### 使用 export

在 `pluginA` 中，我们调用 `export` 机制 `导出对象`。

在 `export` 机制调用前，我们需要保证导出的对象已经被定义，比如：

```python
varA = "varA"


def funcA():
    return "funcA"
```

在确保定义之后，我们可以从 `nonebot.plugin` 导入 `export()` 方法, `export()` 方法会返回一个特殊的字典 `export`：

```python
from nonebot.plugin import export

export=export()
```

这个字典可以用来装载导出的对象，它的 key 是对象导出后的命名，value 是对象本身，我们可以直接创建新的 `key` - `value` 对导出对象：

```python
export.vA = varA
export.fA = funcA
```

除此之外，也支持 `嵌套` 导出对象：

```python
export.sub.vA = varA
export.sub.fA = funcA
```

特别地，对于 `函数对象` 而言，`export` 支持用 `装饰器` 的方法来导出，因此，我们可以这样定义 `funcA`：

```python
@export.sub
def funcA():
    return "funcA"
```

或者:

```python
@export
def funcA():
    return "funcA"
```

通过 `装饰器` 的方法导出函数时，命名固定为函数的命名，也就是说，上面的两个例子等同于：

```python
export.sub.funcA = funcA

export.funcA = funcA
```

这样，我们就成功导出 `varA` 和 `funcA` 对象了。

下面我们将介绍如何在 `pluginB` 中导入这些对象。

### 使用 require

在 `pluginB` 中，我们调用 `require` 机制 `导入对象`。

:::warning 警告

在导入来自其他插件的对象时, 请确保导出该对象的插件在引用该对象的插件之前加载。如果该插件并未被加载，则会尝试加载，加载失败则会返回 `None`。

:::

我们可以从 `nonebot.plugin` 中导入 `require()` 方法：

```python
from nonebot.plugin import require
```

`require()` 方法的参数是插件名, 它会返回在指定插件中，用 `export()` 方法创建的字典。

```python
require_A = require('pluginA')
```

在之前，这个字典已经存入了 `'vA'` - `varA`, `'fA'` - `funcA` 或 `'funcA'` - `funcA` 这样的 `key` - `value` 对。因此在这里我们直接用 `属性` 的方法来获取导入对象:

```python
varA = require_A.vA
funcA = require_A.fA or require_A.funcA
```

这样，我们就在 `pluginB` 中成功导入了 `varA` 和 `funcA` 对象了。
