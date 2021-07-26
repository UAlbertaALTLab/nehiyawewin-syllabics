#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re
from itertools import chain
from typing import Any, Dict, NamedTuple, Optional, Set
from unicodedata import name

from .types import Consonant, Syllabic, SyllabicWithVowelBase, Syllable, Vowel
from .utils import first

roster: Set[Syllabic] = set()
onsets_nucleus = {}  # type: ignore

# Matches an optional onset and a vowel.
pattern = re.compile(r"^(?:[PTCKSMNWY]W?)?([AIOE])\1?$")

# Partial Unicode names and their SRO equivalents.
consonants = {
    "WEST-CREE P": "p",
    "FINAL ACUTE": "t",
    "FINAL GRAVE": "k",
    "FINAL SHORT HORIZONTAL STROKE": "c",
    "WEST-CREE M": "m",
    "FINAL RIGHT HALF RING": "n",
    "FINAL TOP HALF RING": "s",
    "FINAL DOUBLE SHORT VERTICAL STROKES": "h",
    "FINAL PLUS": "y",
    "WOODS-CREE FINAL TH": "th",
    "FINAL RING": "w",
    "HK": "hk",
    # Used in loanwords only:
    "MEDIAL L": "l",
    "MEDIAL R": "r",
}


def choose_appropriate_variant(variants) -> None:
    for graph, desc in variants:
        if (
            "WEST-CREE" in desc
            or "WOODS-CREE" in desc
            # XXX: for some reason nw- syllabics with dot to the right are labelled as
            # OJIBWAY ¯\_(ツ)_/¯
            or "OJIBWAY" in desc
        ):
            roster.add(SyllabicWithVowelBase.new(graph))
            return
    for graph, desc in variants:
        if len(desc) == 0:
            roster.add(SyllabicWithVowelBase.new(graph))
            return
    raise ValueError(graph)


UNIFIED_CANADIAN_ABORGINAL_SYLLABICS = range(0x1400, 0x1680)
UNIFIED_CANADIAN_ABORGINAL_SYLLABICS_EXTENDED = range(0x18B0, 0x18F6)
ALL_SYLLABICS = chain(
    UNIFIED_CANADIAN_ABORGINAL_SYLLABICS, UNIFIED_CANADIAN_ABORGINAL_SYLLABICS_EXTENDED
)

# Find all elligible syllabics.
for i in ALL_SYLLABICS:
    graph = chr(i)
    c, s, *desc = name(graph).split()
    assert f"{c} {s}" == "CANADIAN SYLLABICS", f"{graph} {name(graph)}"

    syllable = desc[-1]
    desc_str = " ".join(desc)

    # XXX: this is... not great :/
    if pattern.match(syllable):
        variants = onsets_nucleus.setdefault(syllable, set())
        variants.add((graph, tuple(desc[:-1])))
    elif desc_str in consonants:
        roster.add(Consonant(character=graph))
    elif "TH-CREE" in desc:
        # Skip the mysterious East Cree style TH final (this is gross):
        if desc[-1] != "TH":
            variants = onsets_nucleus.setdefault(syllable, set())
            variants.add((graph, tuple(desc[:-1])))
    elif "WOODS-CREE" in desc and "THW" in desc_str:
        variants = onsets_nucleus.setdefault(syllable, set())
        variants.add((graph, tuple(desc[:-1])))


# For syllabics with multiple variants, pick the most appropriate one.
for syllable, variants in onsets_nucleus.items():
    if len(variants) > 1:
        choose_appropriate_variant(variants)
    else:
        graph, desc = first(variants)
        if "CARRIER" in desc:
            continue
        roster.add(SyllabicWithVowelBase.new(graph))

plains_cree_syllabics = sorted(roster)
