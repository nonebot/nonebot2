from os import path

import none

import config

if __name__ == '__main__':
    none.init(config)
    none.load_plugins(path.join(path.dirname(__file__), 'awesome', 'plugins'),
                      'awesome.plugins')
    none.run()
