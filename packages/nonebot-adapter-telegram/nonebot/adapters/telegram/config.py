from typing import Optional

from pydantic import Field, BaseModel


# priority: alias > origin
class Config(BaseModel):
    """
    telegram 配置类

    :配置项:

      - ``token`` / ``telegram_token``: telegram bot token
      - ``proxy`` / ``telegram_proxy``: 自定义代理
      - ``api_server`` / ``telegram_api_server``: 自定义 API 服务器

    """

    token: Optional[str] = Field(default=None, alias="telegram_token")
    proxy: Optional[str] = Field(default=None, alias="telegram_proxy")
    url: Optional[str] = Field(default=None, alias="telegram_url")
    api_server: Optional[str] = Field(
        default="https://api.telegram.org/", alias="telegram_api_server"
    )

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True
