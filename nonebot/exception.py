#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class IgnoredException(Exception):
    """
    Raised by event_preprocessor indicating that
    the bot should ignore the event
    """

    def __init__(self, reason):
        """
        :param reason: reason to ignore the event
        """
        self.reason = reason


class PausedException(Exception):
    """Block a message from further handling and try to receive a new message"""
    pass


class RejectedException(Exception):
    """Reject a message and return current handler back"""
    pass


class FinishedException(Exception):
    """Finish handling a message"""
    pass


class ApiNotAvailable(Exception):
    """Api is not available"""
    pass
