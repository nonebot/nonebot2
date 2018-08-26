from datetime import datetime

import none
import pytz
from aiocqhttp.exceptions import Error as CQHttpError


@none.scheduler.scheduled_job('cron', hour='*')
async def _():
    bot = none.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        await bot.send_group_msg(group_id=672076603,
                                 message=f'现在{now.hour}点整啦！')
    except CQHttpError:
        pass
