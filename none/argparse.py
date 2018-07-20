from argparse import *


class ParserExit(RuntimeError):
    def __init__(self, status=0, message=None):
        self.status = status
        self.message = message


class ArgumentParser(ArgumentParser):
    """
    An ArgumentParser wrapper that avoid printing messages to
    standard I/O.
    """

    def _print_message(self, *args, **kwargs):
        # do nothing
        pass

    def exit(self, status=0, message=None):
        raise ParserExit(status=status, message=message)
