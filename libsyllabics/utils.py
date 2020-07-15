#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from typing import Any, Iterable, TypeVar

T = TypeVar("T")


def first(it: Iterable[T]) -> T:
    """
    Returns only first element of an iterable.
    """
    return next(iter(it))


def to_r(thing: Any) -> Any:
    """
    Convert datatype to an R approved format.
    """
    if isinstance(thing, bool):
        return str(thing).upper()
    return thing
