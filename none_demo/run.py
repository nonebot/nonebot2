from os import path

import none

from none_demo import config

bot = none.create_bot(config)

none.load_builtin_plugins()
plugin_dir = path.join(path.dirname(__file__), 'plugins')
none.load_plugins(plugin_dir, 'none_demo.plugins')

app = bot.asgi

if __name__ == '__main__':
    bot.run(host=config.HOST, port=config.PORT)
