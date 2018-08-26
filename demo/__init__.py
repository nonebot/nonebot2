from os import path

import none
from demo import config

none.init(config)


@none.scheduler.scheduled_job('interval', seconds=20)
async def cb():
    bot_ = none.get_bot()
    try:
        await bot_.send_private_msg(user_id=1002647525, message='哇')
    except Exception as e:
        none.logger.exception(e)


if __name__ == '__main__':
    none.load_builtin_plugins()
    none.load_plugins(path.join(path.dirname(__file__), 'plugins'),
                      'demo.plugins')
    none.run(host=config.HOST, port=config.PORT)
