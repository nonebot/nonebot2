#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class PausedException(Exception):
    """Block a message from further handling and try to receive a new message"""
    pass


class RejectedException(Exception):
    """Reject a message and return current handler back"""
    pass


class FinishedException(Exception):
    """Finish handling a message"""
    pass
