from typing import Optional

from pydantic import BaseModel, Field


class Config(BaseModel):
    """
    钉钉配置类

    :配置项:

      - ``app_id`` / ``feishu_app_id``: 飞书开放平台后台“凭证与基础信息”处给出的 App ID
      - ``app_secret`` / ``feishu_app_secret``: 飞书开放平台后台“凭证与基础信息”处给出的 App Secret
      - ``encrypt_key`` / ``feishu_encrypt_key``: 飞书开放平台后台“事件订阅”处设置的 Encrypt Key
      - ``verification_token`` / ``feishu_verification_token``: 飞书开放平台后台“事件订阅”处设置的 Verification Token
      - ``tenant_access_token`` / ``feishu_tenant_access_token``: 请求飞书 API 后返回的租户密钥
    """
    app_id: Optional[str] = Field(default=None, alias="feishu_app_id")
    app_secret: Optional[str] = Field(default=None, alias="feishu_app_secret")
    encrypt_key: Optional[str] = Field(default=None, alias="feishu_encrypt_key")
    verification_token: Optional[str] = Field(default=None,
                                              alias="feishu_verification_token")
    tenant_access_token: Optional[str] = Field(
        default=None, alias="feishu_tenant_access_token")

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True
