""" test version """

import nonebot


def test_version():
    """ test version. """
    assert nonebot.__version__[:3] in ["2.0"]
    assert ".".join(nonebot.VERSION)[:3] in ["2.0"]
