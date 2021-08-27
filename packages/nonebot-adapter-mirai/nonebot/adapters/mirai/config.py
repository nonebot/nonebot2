from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Extra, Field
from pydantic.networks import AnyUrl


class Config(BaseModel):
    """
    Mirai 配置类

    :必填:

      - ``verify_key`` / ``mirai_verify_key``: mirai-api-http 的 verify_key
      - ``mirai_host``: mirai-api-http 的地址
      - ``mirai_port``: mirai-api-http 的端口
    """
    verify_key: Optional[str] = Field(None, alias='mirai_verify_key')
    ws_urls: Optional[Dict[AnyUrl, Union[List[int],
                                         int]]] = Field(None,
                                                        alias='mirai_ws_urls')

    class Config:
        extra = Extra.ignore
        allow_population_by_field_name = True
