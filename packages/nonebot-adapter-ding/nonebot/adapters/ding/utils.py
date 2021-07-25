import hmac
import base64
import hashlib

from nonebot.utils import logger_wrapper

log = logger_wrapper("DING")


def calc_hmac_base64(timestamp: str, secret: str):
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc,
                         string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    return base64.b64encode(hmac_code)
