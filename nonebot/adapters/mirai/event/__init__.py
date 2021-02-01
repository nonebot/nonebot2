"""
\:\:\: warning 
事件中为了使代码更加整洁, 我们采用了与PEP8相符的命名规则取代Mirai原有的驼峰命名

部分字段可能与文档在符号上不一致
\:\:\:
"""
from .base import (Event, GroupChatInfo, GroupInfo, PrivateChatInfo,
                   UserPermission)
from .message import *
from .notice import *
from .request import *
