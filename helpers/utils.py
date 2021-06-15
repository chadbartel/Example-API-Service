#!/usr/bin/env python

"""Utility helper file."""


def merge_dicts(*dict_args):
    """Merge all Python dictionaries into one."""
    dict_args = [] if dict_args is None else dict_args
    result = {}
    for d in dict_args:
        result.update(d)
    return result