#!/usr/bin/env python
# -*- coding: utf-8 -*-


def is_numeric(value):
    try:
        int(value)
    except (TypeError, ValueError):
        return False
    return True


class NotAllowedException(Exception):
    pass
