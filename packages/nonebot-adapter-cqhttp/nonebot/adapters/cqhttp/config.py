from typing import Optional

from pydantic import Field, BaseModel


# priority: alias > origin
class Config(BaseModel):
    """
    CQHTTP 配置类

    :配置项:

      - ``access_token`` / ``cqhttp_access_token``: CQHTTP 协议授权令牌
      - ``secret`` / ``cqhttp_secret``: CQHTTP HTTP 上报数据签名口令
    """
    access_token: Optional[str] = Field(default=None,
                                        alias="cqhttp_access_token")
    secret: Optional[str] = Field(default=None, alias="cqhttp_secret")

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True
