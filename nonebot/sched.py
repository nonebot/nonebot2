#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
except ImportError:
    AsyncIOScheduler = None

if AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
else:
    scheduler = None
