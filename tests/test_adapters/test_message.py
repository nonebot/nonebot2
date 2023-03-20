import pytest
from pydantic import ValidationError, parse_obj_as

from utils import make_fake_message


def test_segment_add():
    Message = make_fake_message()
    MessageSegment = Message.get_segment_class()

    assert MessageSegment.text("text") + MessageSegment.text("text") == Message(
        [MessageSegment.text("text"), MessageSegment.text("text")]
    )

    assert MessageSegment.text("text") + "text" == Message(
        [MessageSegment.text("text"), MessageSegment.text("text")]
    )

    assert (
        MessageSegment.text("text") + Message([MessageSegment.text("text")])
    ) == Message([MessageSegment.text("text"), MessageSegment.text("text")])

    assert "text" + MessageSegment.text("text") == Message(
        [MessageSegment.text("text"), MessageSegment.text("text")]
    )


def test_segment_validate():
    Message = make_fake_message()
    MessageSegment = Message.get_segment_class()

    assert parse_obj_as(
        MessageSegment,
        {"type": "text", "data": {"text": "text"}, "extra": "should be ignored"},
    ) == MessageSegment.text("text")

    with pytest.raises(ValidationError):
        parse_obj_as(MessageSegment, "some str")

    with pytest.raises(ValidationError):
        parse_obj_as(MessageSegment, {"data": {}})


def test_segment():
    Message = make_fake_message()
    MessageSegment = Message.get_segment_class()

    assert len(MessageSegment.text("text")) == 4
    assert MessageSegment.text("text") != MessageSegment.text("other")
    assert MessageSegment.text("text").get("data") == {"text": "text"}
    assert list(MessageSegment.text("text").keys()) == ["type", "data"]
    assert list(MessageSegment.text("text").values()) == ["text", {"text": "text"}]
    assert list(MessageSegment.text("text").items()) == [
        ("type", "text"),
        ("data", {"text": "text"}),
    ]

    origin = MessageSegment.text("text")
    copy = origin.copy()
    assert origin is not copy
    assert origin == copy


def test_message_add():
    Message = make_fake_message()
    MessageSegment = Message.get_segment_class()

    assert (
        Message([MessageSegment.text("text")]) + MessageSegment.text("text")
    ) == Message([MessageSegment.text("text"), MessageSegment.text("text")])

    assert Message([MessageSegment.text("text")]) + "text" == Message(
        [MessageSegment.text("text"), MessageSegment.text("text")]
    )

    assert (
        Message([MessageSegment.text("text")]) + Message([MessageSegment.text("text")])
    ) == Message([MessageSegment.text("text"), MessageSegment.text("text")])

    assert "text" + Message([MessageSegment.text("text")]) == Message(
        [MessageSegment.text("text"), MessageSegment.text("text")]
    )

    msg = Message([MessageSegment.text("text")])
    msg += MessageSegment.text("text")
    assert msg == Message([MessageSegment.text("text"), MessageSegment.text("text")])


def test_message_getitem():
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

    assert message[:2] == Message(
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


def test_message_validate():
    Message = make_fake_message()
    MessageSegment = Message.get_segment_class()

    Message_ = make_fake_message()

    assert parse_obj_as(Message, Message([])) == Message([])

    with pytest.raises(ValidationError):
        parse_obj_as(Message, Message_([]))

    assert parse_obj_as(Message, "text") == Message([MessageSegment.text("text")])

    assert parse_obj_as(Message, {"type": "text", "data": {"text": "text"}}) == Message(
        [MessageSegment.text("text")]
    )

    assert parse_obj_as(
        Message,
        [MessageSegment.text("text"), {"type": "text", "data": {"text": "text"}}],
    ) == Message([MessageSegment.text("text"), MessageSegment.text("text")])

    with pytest.raises(ValidationError):
        parse_obj_as(Message, object())
