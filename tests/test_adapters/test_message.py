import pytest
from pydantic import ValidationError, parse_obj_as

from nonebot.adapters import Message
from utils import FakeMessage, FakeMessageSegment


def test_segment_data():
    assert len(FakeMessageSegment.text("text")) == 4
    assert FakeMessageSegment.text("text").get("data") == {"text": "text"}
    assert list(FakeMessageSegment.text("text").keys()) == ["type", "data"]
    assert list(FakeMessageSegment.text("text").values()) == ["text", {"text": "text"}]
    assert list(FakeMessageSegment.text("text").items()) == [
        ("type", "text"),
        ("data", {"text": "text"}),
    ]


def test_segment_equal():
    assert FakeMessageSegment("text", {"text": "text"}) == FakeMessageSegment(
        "text", {"text": "text"}
    )
    assert FakeMessageSegment("text", {"text": "text"}) != FakeMessageSegment(
        "text", {"text": "other"}
    )
    assert FakeMessageSegment("text", {"text": "text"}) != FakeMessageSegment(
        "other", {"text": "text"}
    )


def test_segment_add():
    assert FakeMessageSegment.text("text") + FakeMessageSegment.text(
        "text"
    ) == FakeMessage([FakeMessageSegment.text("text"), FakeMessageSegment.text("text")])

    assert FakeMessageSegment.text("text") + "text" == FakeMessage(
        [FakeMessageSegment.text("text"), FakeMessageSegment.text("text")]
    )

    assert (
        FakeMessageSegment.text("text") + FakeMessage([FakeMessageSegment.text("text")])
    ) == FakeMessage([FakeMessageSegment.text("text"), FakeMessageSegment.text("text")])

    assert "text" + FakeMessageSegment.text("text") == FakeMessage(
        [FakeMessageSegment.text("text"), FakeMessageSegment.text("text")]
    )


def test_segment_validate():
    assert parse_obj_as(
        FakeMessageSegment,
        {"type": "text", "data": {"text": "text"}, "extra": "should be ignored"},
    ) == FakeMessageSegment.text("text")

    with pytest.raises(ValidationError):
        parse_obj_as(FakeMessageSegment, "some str")

    with pytest.raises(ValidationError):
        parse_obj_as(FakeMessageSegment, {"data": {}})


def test_segment_join():
    seg = FakeMessageSegment.text("test")
    iterable = [
        FakeMessageSegment.text("first"),
        FakeMessage(
            [FakeMessageSegment.text("second"), FakeMessageSegment.text("third")]
        ),
    ]

    assert seg.join(iterable) == FakeMessage(
        [
            FakeMessageSegment.text("first"),
            FakeMessageSegment.text("test"),
            FakeMessageSegment.text("second"),
            FakeMessageSegment.text("third"),
        ]
    )


def test_segment_copy():
    origin = FakeMessageSegment.text("text")
    copy = origin.copy()
    assert origin is not copy
    assert origin == copy


def test_message_add():
    assert (
        FakeMessage([FakeMessageSegment.text("text")]) + FakeMessageSegment.text("text")
    ) == FakeMessage([FakeMessageSegment.text("text"), FakeMessageSegment.text("text")])

    assert FakeMessage([FakeMessageSegment.text("text")]) + "text" == FakeMessage(
        [FakeMessageSegment.text("text"), FakeMessageSegment.text("text")]
    )

    assert (
        FakeMessage([FakeMessageSegment.text("text")])
        + FakeMessage([FakeMessageSegment.text("text")])
    ) == FakeMessage([FakeMessageSegment.text("text"), FakeMessageSegment.text("text")])

    assert "text" + FakeMessage([FakeMessageSegment.text("text")]) == FakeMessage(
        [FakeMessageSegment.text("text"), FakeMessageSegment.text("text")]
    )

    msg = FakeMessage([FakeMessageSegment.text("text")])
    msg += FakeMessageSegment.text("text")
    assert msg == FakeMessage(
        [FakeMessageSegment.text("text"), FakeMessageSegment.text("text")]
    )


def test_message_getitem():
    message = FakeMessage(
        [
            FakeMessageSegment.text("test"),
            FakeMessageSegment.image("test2"),
            FakeMessageSegment.image("test3"),
            FakeMessageSegment.text("test4"),
        ]
    )

    assert message[0] == FakeMessageSegment.text("test")

    assert message[:2] == FakeMessage(
        [FakeMessageSegment.text("test"), FakeMessageSegment.image("test2")]
    )

    assert message["image"] == FakeMessage(
        [FakeMessageSegment.image("test2"), FakeMessageSegment.image("test3")]
    )

    assert message["image", 0] == FakeMessageSegment.image("test2")
    assert message["image", 0:2] == message["image"]

    assert message.index(message[0]) == 0
    assert message.index("image") == 1

    assert message.get("image") == message["image"]
    assert message.get("image", 114514) == message["image"]
    assert message.get("image", 1) == FakeMessage([message["image", 0]])

    assert message.count("image") == 2


def test_message_validate():
    assert parse_obj_as(FakeMessage, FakeMessage([])) == FakeMessage([])

    with pytest.raises(ValidationError):
        parse_obj_as(type("FakeMessage2", (Message,), {}), FakeMessage([]))

    assert parse_obj_as(FakeMessage, "text") == FakeMessage(
        [FakeMessageSegment.text("text")]
    )

    assert parse_obj_as(
        FakeMessage, {"type": "text", "data": {"text": "text"}}
    ) == FakeMessage([FakeMessageSegment.text("text")])

    assert parse_obj_as(
        FakeMessage,
        [FakeMessageSegment.text("text"), {"type": "text", "data": {"text": "text"}}],
    ) == FakeMessage([FakeMessageSegment.text("text"), FakeMessageSegment.text("text")])

    with pytest.raises(ValidationError):
        parse_obj_as(FakeMessage, object())


def test_message_contains():
    message = FakeMessage(
        [
            FakeMessageSegment.text("test"),
            FakeMessageSegment.image("test2"),
            FakeMessageSegment.image("test3"),
            FakeMessageSegment.text("test4"),
        ]
    )

    assert message.has(FakeMessageSegment.text("test")) is True
    assert FakeMessageSegment.text("test") in message
    assert message.has("image") is True
    assert "image" in message

    assert message.has(FakeMessageSegment.text("foo")) is False
    assert FakeMessageSegment.text("foo") not in message
    assert message.has("foo") is False
    assert "foo" not in message


def test_message_only():
    message = FakeMessage(
        [
            FakeMessageSegment.text("test"),
            FakeMessageSegment.text("test2"),
        ]
    )

    assert message.only("text") is True
    assert message.only(FakeMessageSegment.text("test")) is False

    message = FakeMessage(
        [
            FakeMessageSegment.text("test"),
            FakeMessageSegment.image("test2"),
            FakeMessageSegment.image("test3"),
            FakeMessageSegment.text("test4"),
        ]
    )

    assert message.only("text") is False

    message = FakeMessage(
        [
            FakeMessageSegment.text("test"),
            FakeMessageSegment.text("test"),
        ]
    )

    assert message.only(FakeMessageSegment.text("test")) is True


def test_message_join():
    msg = FakeMessage([FakeMessageSegment.text("test")])
    iterable = [
        FakeMessageSegment.text("first"),
        FakeMessage(
            [FakeMessageSegment.text("second"), FakeMessageSegment.text("third")]
        ),
    ]

    assert msg.join(iterable) == FakeMessage(
        [
            FakeMessageSegment.text("first"),
            FakeMessageSegment.text("test"),
            FakeMessageSegment.text("second"),
            FakeMessageSegment.text("third"),
        ]
    )


def test_message_include():
    message = FakeMessage(
        [
            FakeMessageSegment.text("test"),
            FakeMessageSegment.image("test2"),
            FakeMessageSegment.image("test3"),
            FakeMessageSegment.text("test4"),
        ]
    )

    assert message.include("text") == FakeMessage(
        [
            FakeMessageSegment.text("test"),
            FakeMessageSegment.text("test4"),
        ]
    )


def test_message_exclude():
    message = FakeMessage(
        [
            FakeMessageSegment.text("test"),
            FakeMessageSegment.image("test2"),
            FakeMessageSegment.image("test3"),
            FakeMessageSegment.text("test4"),
        ]
    )

    assert message.exclude("image") == FakeMessage(
        [
            FakeMessageSegment.text("test"),
            FakeMessageSegment.text("test4"),
        ]
    )
