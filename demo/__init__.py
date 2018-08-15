from os import path

import none
from demo import config

none.init(config)
app = none.get_bot().asgi

if __name__ == '__main__':
    none.load_builtin_plugins()
    none.load_plugins(path.join(path.dirname(__file__), 'plugins'),
                      'demo.plugins')
    none.run(host=config.HOST, port=config.PORT)
