import os
import importlib

from flask import Flask, request

from little_shit import *
from filter import apply_filters

app = Flask(__name__)


@app.route('/', methods=['POST'])
def _index():
    ctx_msg = request.json
    try:
        if ctx_msg.get('msg_class') != 'recv':
            raise SkipException
        if not apply_filters(ctx_msg):
            raise SkipException
    except SkipException:
        # Skip this message
        pass

    return '', 204


def _load_filters():
    filter_mod_files = filter(
        lambda filename: filename.endswith('.py') and not filename.startswith('_'),
        os.listdir(get_filters_dir())
    )
    command_mods = [os.path.splitext(file)[0] for file in filter_mod_files]
    for mod_name in command_mods:
        importlib.import_module('filters.' + mod_name)


if __name__ == '__main__':
    _load_filters()
    app.run(host=os.environ.get('HOST', '0.0.0.0'), port=os.environ.get('PORT', '8080'))
