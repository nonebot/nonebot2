import base64 as b64lib
import hashlib

from command import CommandRegistry
from commands import core

__registry__ = cr = CommandRegistry()


@cr.register('base64')
def base64(args_text, ctx_msg, internal=False):
    encoded = b64lib.b64encode(args_text.encode('utf-8')).decode('utf-8')
    core.echo(encoded, ctx_msg, internal)
    return encoded


@cr.register('base64_decode', 'base64-decode', 'base64d')
def base64(args_text, ctx_msg, internal=False):
    decoded = b64lib.b64decode(args_text.encode('utf-8')).decode('utf-8')
    core.echo(decoded, ctx_msg, internal)
    return decoded


@cr.register('md5')
def md5(args_text, ctx_msg, internal=False):
    encoded = hashlib.md5(args_text.encode('utf-8')).hexdigest()
    core.echo(encoded, ctx_msg, internal)
    return encoded


@cr.register('sha1')
def sha1(args_text, ctx_msg, internal=False):
    encoded = hashlib.sha1(args_text.encode('utf-8')).hexdigest()
    core.echo(encoded, ctx_msg, internal)
    return encoded


@cr.register('sha256')
def sha1(args_text, ctx_msg, internal=False):
    encoded = hashlib.sha256(args_text.encode('utf-8')).hexdigest()
    core.echo(encoded, ctx_msg, internal)
    return encoded
