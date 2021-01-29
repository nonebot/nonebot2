from ipaddress import IPv4Address
from typing import Optional

from pydantic import BaseModel, Extra, Field


class Config(BaseModel):
    auth_key: Optional[str] = Field(None, alias='mirai_auth_key')
    host: Optional[IPv4Address] = Field(None, alias='mirai_host')
    port: Optional[int] = Field(None, alias='mirai_port')

    class Config:
        extra = Extra.ignore
