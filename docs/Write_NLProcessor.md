# 编写自然语言处理器

`nl_processors` 目录中所有不以 `_` 开头的 `.py` 文件会被加载进程序，一般把自然语言处理器（后面称 NL 处理器）放在这个目录里。对于临时不需要的 NL 处理器，可以通过在文件名前加 `_` 来屏蔽掉。

## 流程

程序执行时 `natural_language.process` 命令会调用 `nl_processor.py` 中的 `parse_potential_commands` 函数来解析可能的等价命令，此函数会对消息文本进行分词，然后进行关键词匹配（关键词在注册 NL 处理器是传入），并调用所有匹配到的 NL 处理器，每个 NL 处理器会返回 None 或一个四元组（从 0 到 3 分别是：置信度（0~100）、命令名、参数、已解析到的数据）。

完成后，`parse_potential_commands` 把所有非 None 的结果放在一个 list 返回给 `natural_language.process` 命令，该命令再从中选择置信度最高，且超过 60 的命令执行（在调用之前会把已解析到的数据放在消息上下文的 `parsed_data` 字段）。如果没有置信度超过 60 的命令，则调用 `config.py` 中 `fallback_command_after_nl_processors` 字段指定的命令。

## 写法

由以上流程可知，在编写 NL 处理器时需要注册关键词，然后返回一个包含可能的等价命令和置信度的四元组。例子如下：

```python
from nl_processor import as_processor


@as_processor(keywords=('翻译(为|成|到)?', '.+(文|语)'))
def _processor(sentence, segmentation):
	return 90, 'translate.translate_to', '', None
```

注意关键词需要传入一个可迭代对象，每个元素为一个正则表达式字符串；函数接收的参数有且只有两个必填项，第一个为原文本字符串，第二个为使用 jieba 分词之后的分词列表，每个元素都包含 `flag` 和 `word` 两个属性（是对象的属性，不是字典的键），分别是词性标记（jieba 分词的词性标记见 [ICTCLAS 汉语词性标注集](https://gist.github.com/luw2007/6016931#ictclas-汉语词性标注集)）和词语的字符串。