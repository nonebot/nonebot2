from typing import Optional

from pydantic import Field, BaseModel


class Config(BaseModel):
    """
    钉钉配置类

    :配置项:

      - ``access_token`` / ``ding_access_token``: 钉钉令牌
      - ``secret`` / ``ding_secret``: 钉钉 HTTP 上报数据签名口令
    """
    secret: Optional[str] = Field(default=None, alias="ding_secret")
    access_token: Optional[str] = Field(default=None, alias="ding_access_token")

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True
