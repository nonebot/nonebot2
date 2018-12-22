from argparse import *

from .command import CommandSession


class ParserExit(RuntimeError):
    def __init__(self, status=0, message=None):
        self.status = status
        self.message = message


class ArgumentParser(ArgumentParser):
    """
    An ArgumentParser wrapper that avoid printing messages to
    standard I/O.
    """

    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        super().__init__(*args, **kwargs)

    def _print_message(self, *args, **kwargs):
        # do nothing
        pass

    def exit(self, status=0, message=None):
        raise ParserExit(status=status, message=message)

    def parse_args(self, args=None, namespace=None):
        def finish(msg):
            if self.session and isinstance(self.session, CommandSession):
                self.session.finish(msg)

        if not args:
            finish(self.usage)
        else:
            try:
                return super().parse_args(args=args, namespace=namespace)
            except ParserExit as e:
                if e.status == 0:
                    # --help
                    finish(self.usage)
                else:
                    finish('参数不足或不正确，请使用 --help 参数查询使用帮助')
