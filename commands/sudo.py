import sqlite3

from command import CommandRegistry, split_arguments
from commands import core
from little_shit import get_default_db_path, get_target

__registry__ = cr = CommandRegistry()

_create_table_sql = """CREATE TABLE IF NOT EXISTS blocked_target_list (
  target TEXT NOT NULL
)"""


def _open_db_conn():
    conn = sqlite3.connect(get_default_db_path())
    conn.execute(_create_table_sql)
    conn.commit()
    return conn


@cr.register('test')
@cr.restrict(full_command_only=True, superuser_only=True)
def test(_, ctx_msg):
    core.echo('Your are the superuser!', ctx_msg)


@cr.register('block')
@cr.restrict(full_command_only=True, superuser_only=True)
@split_arguments(maxsplit=2)
def block(_, ctx_msg, argv=None):
    def _send_error_msg():
        core.echo('参数不正确。\n\n正确使用方法：\nsudo.block wx|qq <account-to-block>', ctx_msg)

    if len(argv) != 2:
        _send_error_msg()
        return

    via, account = argv
    # Get a target using a fake context message
    target = get_target({
        'via': via,
        'type': 'friend_message',
        'sender_uid': account,
        'sender_account': account
    })

    if not target:
        _send_error_msg()
        return

    conn = _open_db_conn()
    conn.execute('INSERT INTO blocked_target_list (target) VALUES (?)', (target,))
    conn.commit()
    conn.close()
    core.echo('成功屏蔽用户 ' + account, ctx_msg)


@cr.register('block_list', 'block-list')
@cr.restrict(full_command_only=True, superuser_only=True)
def block_list(_, ctx_msg, internal=False):
    conn = _open_db_conn()
    cursor = conn.execute('SELECT target FROM blocked_target_list')
    blocked_targets = list(set([x[0] for x in list(cursor)]))  # Get targets and remove duplications
    conn.close()
    if internal:
        return blocked_targets
    if blocked_targets:
        # `t[1:]` to reply user account, without target prefix 'p'.
        # This is a shit code, and should be changed later sometime.
        core.echo('已屏蔽的用户：\n' + ', '.join([t[1:] for t in blocked_targets]), ctx_msg)
    else:
        core.echo('还没有屏蔽过用户', ctx_msg)


@cr.register('unblock')
@cr.restrict(full_command_only=True, superuser_only=True)
@split_arguments(maxsplit=2)
def unblock(_, ctx_msg, argv=None):
    def _send_error_msg():
        core.echo('参数不正确。\n\n正确使用方法：\nsudo.unblock wx|qq <account-to-unblock>', ctx_msg)

    if len(argv) != 2:
        _send_error_msg()
        return

    via, account = argv
    # Get a target using a fake context message
    target = get_target({
        'via': via,
        'type': 'friend_message',
        'sender_uid': account,
        'sender_account': account
    })

    if not target:
        _send_error_msg()
        return

    conn = _open_db_conn()
    conn.execute('DELETE FROM blocked_target_list WHERE target = ?', (target,))
    conn.commit()
    conn.close()
    core.echo('成功取消屏蔽用户 ' + account, ctx_msg)
