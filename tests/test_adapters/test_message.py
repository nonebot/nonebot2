from utils import make_fake_message


def test_message_template():
    from nonebot.adapters import MessageTemplate

    Message = make_fake_message()

    template = MessageTemplate("{a:custom}{b:text}{c:image}", Message)

    @template.add_format_spec
    def custom(input: str) -> str:
        return input + "-custom!"

    formatted = template.format(a="test", b="test", c="https://example.com/test")
    assert formatted.extract_plain_text() == "test-custom!test"
    assert str(formatted) == "test-custom!test[fake:image]"


def test_message_slice():

    Message = make_fake_message()
    MessageSegment = Message.get_segment_class()

    message = Message(
        [
            MessageSegment.text("test"),
            MessageSegment.image("test2"),
            MessageSegment.image("test3"),
            MessageSegment.text("test4"),
        ]
    )

    assert message[0] == MessageSegment.text("test")

    assert message[0:2] == Message(
        [MessageSegment.text("test"), MessageSegment.image("test2")]
    )

    assert message["image"] == Message(
        [MessageSegment.image("test2"), MessageSegment.image("test3")]
    )

    assert message["image", 0] == MessageSegment.image("test2")
    assert message["image", 0:2] == message["image"]

    assert message.index(message[0]) == 0
    assert message.index("image") == 1

    assert message.get("image") == message["image"]
    assert message.get("image", 114514) == message["image"]
    assert message.get("image", 1) == Message([message["image", 0]])

    assert message.count("image") == 2
