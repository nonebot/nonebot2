from os import path

import nonebot
from demo import config

nonebot.init(config)


@nonebot.scheduler.scheduled_job('interval', seconds=20)
async def cb():
    bot_ = nonebot.get_bot()
    try:
        await bot_.send_private_msg(user_id=1002647525, message='哇')
    except Exception as e:
        nonebot.logger.exception(e)


if __name__ == '__main__':
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(path.join(path.dirname(__file__), 'plugins'),
                         'demo.plugins')
    nonebot.run(host=config.HOST, port=config.PORT)
