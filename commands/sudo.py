from command import CommandRegistry
from commands import core

__registry__ = cr = CommandRegistry()


@cr.register('test')
@cr.restrict(full_command_only=True, superuser_only=True)
def test(_, ctx_msg):
    core.echo('Your are the superuser!', ctx_msg)
