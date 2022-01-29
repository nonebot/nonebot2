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

    assert MessageSegment.text("text") + Message(
        [MessageSegment.text("text")]
    ) == Message([MessageSegment.text("text"), MessageSegment.text("text")])

    assert "text" + MessageSegment.text("text") == Message(
        [MessageSegment.text("text"), MessageSegment.text("text")]
    )


def test_message_add():
    Message = make_fake_message()
    MessageSegment = Message.get_segment_class()

    assert Message([MessageSegment.text("text")]) + MessageSegment.text(
        "text"
    ) == Message([MessageSegment.text("text"), MessageSegment.text("text")])

    assert Message([MessageSegment.text("text")]) + "text" == Message(
        [MessageSegment.text("text"), MessageSegment.text("text")]
    )

    assert Message([MessageSegment.text("text")]) + Message(
        [MessageSegment.text("text")]
    ) == Message([MessageSegment.text("text"), MessageSegment.text("text")])

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
