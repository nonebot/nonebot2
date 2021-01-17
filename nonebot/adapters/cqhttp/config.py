from typing import Optional

from pydantic import Field, BaseModel


# priority: alias > origin
class Config(BaseModel):
    access_token: Optional[str] = Field(default=None,
                                        alias="cqhttp_access_token")
    secret: Optional[str] = Field(default=None, alias="cqhttp_secret")

    class Config:
        extra = "ignore"
