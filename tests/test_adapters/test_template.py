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
