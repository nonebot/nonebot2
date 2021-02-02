from typing import Optional

from pydantic import Field, BaseModel


class Config(BaseModel):
    secret: Optional[str] = Field(default=None, alias="ding_secret")
    access_token: Optional[str] = Field(default=None, alias="ding_access_token")

    class Config:
        extra = "ignore"
