import jieba

from command import CommandRegistry

__registry__ = cr = CommandRegistry()


@cr.register('process')
@cr.restrict(full_command_only=True)
def process(args_text, ctx_msg, internal=False):
    print('自然语言消息处理', args_text)
    print(list(jieba.cut_for_search(args_text)))
