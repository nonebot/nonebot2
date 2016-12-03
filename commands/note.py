import sqlite3
from datetime import datetime

import pytz

from command import CommandRegistry
from commands import core
from interactive import *
from little_shit import get_default_db_path, get_source, get_target

__registry__ = cr = CommandRegistry()

_create_table_sql = """CREATE TABLE IF NOT EXISTS cmd_note (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  content TEXT NOT NULL,
  dt INTEGER NOT NULL,
  target TEXT NOT NULL
)"""


def _open_db_conn():
    conn = sqlite3.connect(get_default_db_path())
    conn.execute(_create_table_sql)
    conn.commit()
    return conn


_cmd_take = 'note.take'
_cmd_remove = 'note.remove'


@cr.register('记笔记', '添加笔记')
@cr.register('take', 'add', hidden=True)
@cr.restrict(group_admin_only=True)
def take(args_text, ctx_msg, allow_interactive=True):
    source = get_source(ctx_msg)
    if allow_interactive and (not args_text or has_session(source, _cmd_take)):
        # Be interactive
        return _take_interactively(args_text, ctx_msg, source)

    conn = _open_db_conn()
    dt_unix = int(datetime.now(tz=pytz.utc).timestamp())
    target = get_target(ctx_msg)
    conn.execute(
        'INSERT INTO cmd_note (content, dt, target) VALUES (?, ?, ?)',
        (args_text, dt_unix, target)
    )
    conn.commit()
    conn.close()
    core.echo('好的，记下了～', ctx_msg)


@cr.register('列出所有笔记')
@cr.register('list', hidden=True)
def list_all(_, ctx_msg):
    conn = _open_db_conn()
    target = get_target(ctx_msg)
    cursor = conn.execute('SELECT id, dt, content FROM cmd_note WHERE target = ?', (target,))
    rows = list(cursor)
    conn.close()
    if len(rows) == 0:
        core.echo('还没有笔记哦～', ctx_msg)
        return
    for row in rows:
        tz_china = pytz.timezone('Asia/Shanghai')
        dt_raw = datetime.fromtimestamp(row[1], tz=pytz.utc)
        core.echo('ID：' + str(row[0])
                  + '\n时间：' + dt_raw.astimezone(tz_china).strftime('%Y.%m.%d %H:%M')
                  + '\n内容：' + str(row[2]),
                  ctx_msg)
    core.echo('以上～', ctx_msg)


@cr.register('删除笔记')
@cr.register('remove', 'delete', hidden=True)
@cr.restrict(group_admin_only=True)
def remove(args_text, ctx_msg, allow_interactive=True):
    source = get_source(ctx_msg)
    if allow_interactive and (not args_text or has_session(source, _cmd_remove)):
        # Be interactive
        return _remove_interactively(args_text, ctx_msg, source)

    try:
        note_id = int(args_text)
    except ValueError:
        # Failed to cast
        core.echo('你输入的 ID 格式不正确哦～应该是个数字才对～', ctx_msg)
        return
    conn = _open_db_conn()
    target = get_target(ctx_msg)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cmd_note WHERE target = ? AND id = ?', (target, note_id))
    if cursor.rowcount > 0:
        core.echo('删除成功了～', ctx_msg)
    else:
        core.echo('没找到这个 ID 的笔记哦～', ctx_msg)
    conn.commit()
    conn.close()


@cr.register('清空笔记', '清空所有笔记', '删除所有笔记')
@cr.register('clear', hidden=True)
@cr.restrict(group_admin_only=True)
def clear(_, ctx_msg):
    conn = _open_db_conn()
    target = get_target(ctx_msg)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cmd_note WHERE target = ?', (target,))
    if cursor.rowcount > 0:
        core.echo('成功删除了所有的笔记，共 %s 条～' % cursor.rowcount, ctx_msg)
    else:
        core.echo('本来就没有笔记哦～', ctx_msg)
    conn.commit()
    conn.close()


_state_machines = {}


def _take_interactively(args_text, ctx_msg, source):
    def wait_for_content(s, a, c):
        core.echo('请发送你要记录的内容：', c)
        s.state += 1

    def save_content(s, a, c):
        take(a, c, allow_interactive=False)
        return True

    if _cmd_take not in _state_machines:
        _state_machines[_cmd_take] = (
            wait_for_content,  # 0
            save_content  # 1
        )

    sess = get_session(source, _cmd_take)
    if _state_machines[_cmd_take][sess.state](sess, args_text, ctx_msg):
        # Done
        remove_session(source, _cmd_take)


def _remove_interactively(args_text, ctx_msg, source):
    def wait_for_note_id(s, a, c):
        core.echo('请发送你要删除的笔记的 ID：', c)
        s.state += 1

    def remove_note(s, a, c):
        remove(a, c, allow_interactive=False)
        return True

    if _cmd_remove not in _state_machines:
        _state_machines[_cmd_remove] = (
            wait_for_note_id,  # 0
            remove_note  # 1
        )

    sess = get_session(source, _cmd_remove)
    if _state_machines[_cmd_remove][sess.state](sess, args_text, ctx_msg):
        # Done
        remove_session(source, _cmd_remove)
