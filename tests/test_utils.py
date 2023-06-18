import json

from nonebot.utils import DataclassEncoder
from utils import FakeMessage, FakeMessageSegment


def test_dataclass_encoder():
    simple = json.dumps("123", cls=DataclassEncoder)
    assert simple == '"123"'

    ms = FakeMessageSegment.nested(FakeMessage(FakeMessageSegment.text("text")))
    s = json.dumps(ms, cls=DataclassEncoder)
    assert (
        s
        == '{"type": "node", "data": {"content": [{"type": "text", "data": {"text": "text"}}]}}'
    )
