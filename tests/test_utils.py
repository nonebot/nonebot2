import json

from utils import make_fake_message
from nonebot.utils import DataclassEncoder


def test_dataclass_encoder():
    simple = json.dumps("123", cls=DataclassEncoder)
    assert simple == '"123"'

    Message = make_fake_message()
    MessageSegment = Message.get_segment_class()
    ms = MessageSegment.nested(Message(MessageSegment.text("text")))
    s = json.dumps(ms, cls=DataclassEncoder)
    assert (
        s
        == '{"type": "node", "data": {"content": [{"type": "text", "data": {"text": "text"}}]}}'
    )
