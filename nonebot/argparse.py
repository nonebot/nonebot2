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

    def _session_finish(self, message):
        if self.session and isinstance(self.session, CommandSession):
            self.session.finish(message)

    def _print_message(self, message, file=None):
        # do nothing
        pass

    def exit(self, status=0, message=None):
        raise ParserExit(status=status, message=message)

    def parse_args(self, args=None, namespace=None):
        try:
            return super().parse_args(args=args, namespace=namespace)
        except ParserExit as e:
            if e.status == 0:
                # --help
                self._session_finish(self.usage or self.format_help())
            else:
                self._session_finish('参数不足或不正确，请使用 --help 参数查询使用帮助')
