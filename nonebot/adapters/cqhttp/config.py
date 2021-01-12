from typing import Optional

from pydantic import Field, BaseSettings


class Config(BaseSettings):
    cqhttp_access_token: Optional[str] = Field(default=None,
                                               alias="access_token")
    cqhttp_secret: Optional[str] = Field(default=None, alias="secret")

    class Config:
        extra = "ignore"
