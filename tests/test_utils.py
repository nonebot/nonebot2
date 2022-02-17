import json
from utils import make_fake_message


def test_dataclass_encoder():
    from nonebot.utils import DataclassEncoder

    MessageSegment = make_fake_message().get_segment_class()
    ms = MessageSegment.node_custom(
        "1234", "testtest", "test" + MessageSegment.image("url")
    )
    s = json.dumps(ms, cls = DataclassEncoder)
    assert (
        s
        == '{"type": "node", "data": {"user_id": "1234", "nickname": "testtest", "content": [{"type": "text", "data": {"text": "test"}}, {"type": "image", "data": {"url": "url"}}]}}'
    )
    s1 = json.dumps("123", cls = DataclassEncoder)
    assert s1 == '"123"'