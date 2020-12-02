import base64
import hashlib
import hmac
from typing import TYPE_CHECKING

from nonebot.utils import logger_wrapper

if TYPE_CHECKING:
    from nonebot.drivers import BaseDriver
log = logger_wrapper("DING")


def check_legal(timestamp, remote_sign, driver: "BaseDriver"):
    """
    1. timestamp 与系统当前时间戳如果相差1小时以上，则认为是非法的请求。

    2. sign 与开发者自己计算的结果不一致，则认为是非法的请求。

    必须当timestamp和sign同时验证通过，才能认为是来自钉钉的合法请求。
    """
    # 目前先设置成 secret
    # TODO 后面可能可以从 secret[adapter_name] 获取
    app_secret = driver.config.secret  # 机器人的 appSecret
    if not app_secret:
        # TODO warning
        log("WARNING", "No ding secrets set, won't check sign")
        return True
    app_secret_enc = app_secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, app_secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(app_secret_enc,
                         string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return remote_sign == sign
