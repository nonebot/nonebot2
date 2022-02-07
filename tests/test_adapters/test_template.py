from utils import make_fake_message


def test_template_basis():
    from nonebot.adapters import MessageTemplate

    template = MessageTemplate("{key:.3%}")
    formatted = template.format(key=0.123456789)
    assert formatted == "12.346%"


def test_template_message():
    from nonebot.adapters import MessageTemplate

    Message = make_fake_message()

    template = MessageTemplate("{a:custom}{b:text}{c:image}", Message)

    @template.add_format_spec
    def custom(input: str) -> str:
        return input + "-custom!"

    try:
        template.add_format_spec(custom)
    except ValueError:
        pass
    else:
        raise AssertionError("Should raise ValueError")

    format_args = {"a": "custom", "b": "text", "c": "https://example.com/test"}
    formatted = template.format(**format_args)

    assert template.format_map(format_args) == formatted
    assert formatted.extract_plain_text() == "custom-custom!text"
    assert str(formatted) == "custom-custom!text[fake:image]"
