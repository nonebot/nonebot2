from ipaddress import IPv4Address
from typing import Optional

from pydantic import BaseModel, Extra, Field


class Config(BaseModel):
    """
    Mirai 配置类

    :必填:

      - ``auth_key`` / ``mirai_auth_key``: mirai-api-http 的 auth_key
      - ``mirai_host``: mirai-api-http 的地址
      - ``mirai_port``: mirai-api-http 的端口
    """
    auth_key: Optional[str] = Field(None, alias='mirai_auth_key')
    host: Optional[IPv4Address] = Field(None, alias='mirai_host')
    port: Optional[int] = Field(None, alias='mirai_port')

    class Config:
        extra = Extra.ignore
        allow_population_by_field_name = True
