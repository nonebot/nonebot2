from typing import Dict, Optional

from pydantic import Field, BaseModel, AnyUrl


# priority: alias > origin
class Config(BaseModel):
    """
    CQHTTP 配置类

    :配置项:

      - ``access_token`` / ``cqhttp_access_token``: CQHTTP 协议授权令牌
      - ``secret`` / ``cqhttp_secret``: CQHTTP HTTP 上报数据签名口令
      - ``ws_urls`` / ``cqhttp_ws_urls``: CQHTTP 正向 Websocket 连接 Bot ID、目标 URL 字典
    """
    access_token: Optional[str] = Field(default=None,
                                        alias="cqhttp_access_token")
    secret: Optional[str] = Field(default=None, alias="cqhttp_secret")
    ws_urls: Dict[str, AnyUrl] = Field(default_factory=set,
                                       alias="cqhttp_ws_urls")

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True
