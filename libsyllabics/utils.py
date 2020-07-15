#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from typing import Iterable, TypeVar

T = TypeVar("T")


def first(it: Iterable[T]) -> T:
    """
    Returns only first element of an iterable.
    """
    return next(iter(it))
