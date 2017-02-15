import os

from flask import Flask, request

from little_shit import SkipException, load_plugins
from filter import apply_filters
from msg_src_adapter import get_adapter

app = Flask(__name__)


@app.route('/<string:via>/<string:login_id>', methods=['POST'], strict_slashes=False)
def _handle_via_account(via: str, login_id: str):
    ctx_msg = request.json
    ctx_msg['via'] = via
    ctx_msg['login_id'] = login_id
    return _main(ctx_msg)


def _main(ctx_msg: dict):
    try:
        adapter = get_adapter(ctx_msg.get('via'), ctx_msg.get('login_id'))
        if not adapter:
            raise SkipException
        ctx_msg = adapter.unitize_context(ctx_msg)
        if not apply_filters(ctx_msg):
            raise SkipException
    except SkipException:
        # Skip this message
        pass

    return '', 204


if __name__ == '__main__':
    load_plugins('msg_src_adapters')
    load_plugins('filters')
    app.run(host=os.environ.get('HOST', '0.0.0.0'), port=os.environ.get('PORT', '8080'))
