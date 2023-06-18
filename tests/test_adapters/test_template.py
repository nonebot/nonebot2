from nonebot.adapters import MessageTemplate
from utils import FakeMessage, FakeMessageSegment, escape_text


def test_template_basis():
    template = MessageTemplate("{key:.3%}")
    formatted = template.format(key=0.123456789)
    assert formatted == "12.346%"


def test_template_message():
    template = FakeMessage.template("{a:custom}{b:text}{c:image}/{d}")

    @template.add_format_spec
    def custom(input: str) -> str:
        return f"{input}-custom!"

    try:
        template.add_format_spec(custom)
    except ValueError:
        pass
    else:
        raise AssertionError("Should raise ValueError")

    format_args = {
        "a": "custom",
        "b": "text",
        "c": "https://example.com/test",
        "d": 114,
    }
    formatted = template.format(**format_args)

    assert template.format_map(format_args) == formatted
    assert formatted.extract_plain_text() == "custom-custom!text/114"
    assert str(formatted) == "custom-custom!text[fake:image]/114"


def test_rich_template_message():
    pic1, pic2, pic3 = (
        FakeMessageSegment.image("file:///pic1.jpg"),
        FakeMessageSegment.image("file:///pic2.jpg"),
        FakeMessageSegment.image("file:///pic3.jpg"),
    )

    template = FakeMessage.template("{}{}" + pic2 + "{}")

    result = template.format(pic1, "[fake:image]", pic3)

    assert result["image"] == FakeMessage([pic1, pic2, pic3])
    assert str(result) == (
        "[fake:image]" + escape_text("[fake:image]") + "[fake:image]" + "[fake:image]"
    )


def test_message_injection():
    template = FakeMessage.template("{name}Is Bad")
    message = template.format(name="[fake:image]")

    assert message.extract_plain_text() == escape_text("[fake:image]Is Bad")
