#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright (C) 2018  Eddie Antonio Santos <easantos@ualberta.ca>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
Hacky script to iterate through the Unicode names database, and find all
syllabics that are used to write nêhiyawêwin.

Generates a either a tab-separated values file with header, or a series of Vim
digraph definitions for each character.
"""

import re
import csv
import sys
from abc import ABC, abstractmethod
from functools import total_ordering
from string import printable as ascii_printable
from typing import NamedTuple, Set, Dict, Optional, Any
from unicodedata import name, normalize
from collections import OrderedDict

COMBINING_CIRCUMFLEX_ACCENT = '\u0302'  # ◌̂

# Matches an optional onset and a coda.
pattern = re.compile(r'^(?:[PTCKSMNWY]W?)?([AIOE])\1?$')

# Partial Unicode names and their SRO equivilent.
codas = {
    'WEST-CREE P':                            'p',
    'FINAL ACUTE':                            't',
    'FINAL GRAVE':                            'k',
    'FINAL SHORT HORIZONTAL STROKE':          'c',
    'WEST-CREE M':                            'm',
    'FINAL RIGHT HALF RING':                  'n',
    'FINAL TOP HALF RING':                    's',
    'FINAL DOUBLE SHORT VERTICAL STROKES':    'h',
    'FINAL PLUS':                             'y',
    'FINAL RING':                             'w',
    'HK':                                     'hk',
}

roster: Set['Syllabic'] = set()
onsets_nucleus = {}  # type: ignore


@total_ordering
class Syllabic(ABC):
    """
    Abstract base class for any syllabic character.

    Important subclasses:
     - Syllable
     - Vowel
     - Final
    """
    __slots__ = 'character',

    has_vowel: bool
    has_consonant: bool

    def __init__(self, character: str) -> None:
        assert len(character) == 1
        self.character = character

    @property
    def code_point(self) -> str:
        """
        Return the code point in U+ notation.
        """
        assert self.scalar_value <= 0xFFFF
        return f'U+{self.scalar_value:04X}'

    @property
    def kind(self) -> str:
        """
        Return 'syllable', 'vowel', or 'final' as appropriate?
        """
        return type(self).__name__.lower()

    @property
    def name(self) -> str:
        """
        Return the Unicode name of the character.
        """
        return name(self.character)

    @property
    def scalar_value(self) -> int:
        """
        Return the code point of the character.
        """
        return ord(self.character)

    @property
    @abstractmethod
    def sro(self) -> str:
        """
        Return the syllabic in Standard Roman Orthography.
        """

    @property
    @abstractmethod
    def vim_digraph(self) -> str:
        """
        Return an appropriate Vim digraph for this character.
        """

    def to_dict(self) -> Dict[str, Any]:
        attrs = [
            ('character', 'cans'),
            ('sro', 'latn'),
            ('scalar_value', 'scalar.value'),
            ('kind', ''),
            ('has_vowel', 'has.vowel'),
            ('has_long_vowel', 'has.long.vowel'),
            ('vowel_with_length', 'vowel'),
            ('has_consonant', 'has.consonant'),
            ('consonant', 'consonant'),
            ('is_labialized', 'has.w'),
            ('vim_digraph', 'vim.digraph'),
            ('code_point', 'code.point'),
            ('name', 'unicode.name'),
        ]

        def generate_pairs():
            for attr, alias in attrs:
                try:
                    value = getattr(self, attr)
                except (AttributeError, ValueError):
                    value = None
                yield (alias or attr, to_r(value))
        return OrderedDict(generate_pairs())

    def __lt__(self, other):
        if not isinstance(other, Syllabic):
            return NotImplemented
        return self.scalar_value < other.scalar_value

    def __eq__(self, other):
        if not isinstance(other, Syllabic):
            return NotImplemented
        return self.scalar_value == other.scalar_value

    def __hash__(self):
        return hash(self.character)

    def __repr__(self):
        clsname = type(self).__qualname__
        return f"{clsname}({self.character!r})"


class SyllabicWithVowelBase(Syllabic):
    """
    Base class for any syllabic that has a vowel.
    """
    VOWELS = 'AEIO'

    has_vowel = True

    @property
    def syllable(self) -> str:
        _canadian, _syllabics, *_, syllable = self.name.split()
        return syllable

    @property
    def vowel(self) -> str:
        last_char = self.syllable[-1]
        assert last_char in self.VOWELS
        return last_char.lower()

    @property
    def vowel_with_length(self) -> str:
        if not self.has_long_vowel:
            return self.vowel
        return normalize('NFC', self.vowel + COMBINING_CIRCUMFLEX_ACCENT)

    @property
    def has_long_vowel(self) -> bool:
        if self.vowel == 'e':
            return True
        elif len(self.syllable) < 2:
            return False
        elif self.syllable[-1] == self.syllable[-2]:
            return True
        return False

    @classmethod
    def new(cls, character: str) -> 'SyllabicWithVowelBase':
        syllable_name = name(character).split()[-1]
        if syllable_name[0:1] in cls.VOWELS:
            return Vowel(character)
        else:
            return Syllable(character)


class Syllable(SyllabicWithVowelBase):
    has_consonant = True

    @property
    def consonant(self) -> str:
        return self.syllable[0].lower()

    @property
    def is_labialized(self) -> bool:
        return self.syllable[1:2] == 'W'

    @property
    def sro(self) -> str:
        c = self.consonant
        w = 'w' if self.is_labialized else ''
        v = self.vowel_with_length
        return f"{c}{w}{v}"

    @property
    def vim_digraph(self) -> str:
        consonant = self.consonant
        vowel = self.vowel
        if self.is_labialized:
            consonant = consonant.upper()
        if self.vowel != 'e' and self.has_long_vowel:
            vowel = vowel.upper()
        return consonant + vowel


class Vowel(SyllabicWithVowelBase):
    has_consonant = False

    @property
    def sro(self) -> str:
        return self.vowel_with_length

    @property
    def vim_digraph(self):
        cont = ':' if self.has_long_vowel else '.'
        return self.vowel + cont


class Final(Syllabic):
    has_vowel = False
    has_consonant = True

    @property
    def consonant(self):
        if self.sro == 'hk':
            raise AttributeError('Not a simple final')
        return self.sro

    @property
    def sro(self) -> str:
        description = self.name[len('CANADIAN SYLLABICS '):]
        return codas[description]

    @property
    def vim_digraph(self):
        if self.sro == 'hk':
            return 'hk'
        return self.sro + '.'


def choose_appropriate_variant(variants) -> None:
    for graph, desc in variants:
        if 'WEST-CREE' in desc:
            roster.add(SyllabicWithVowelBase.new(graph))
            return
    for graph, desc in variants:
        if len(desc) == 0:
            roster.add(SyllabicWithVowelBase.new(graph))
            return
    raise ValueError(graph)


def first(it):
    return next(iter(it))


def to_r(thing: Any) -> Any:
    """
    Convert datatype to an R approved format.
    """
    if isinstance(thing, bool):
        return str(thing).upper()
    return thing


# Find all elligible syllabics.
for i in range(0x1400, 0x1680):
    graph = chr(i)
    c, s, *desc = name(graph).split()
    assert f'{c} {s}' == 'CANADIAN SYLLABICS', f'{graph} {name(graph)}'

    syllable = desc[-1]
    desc_str = ' '.join(desc)

    if pattern.match(syllable):
        variants = onsets_nucleus.setdefault(syllable, set())
        variants.add((graph, tuple(desc[:-1])))
    elif desc_str in codas:
        roster.add(Final(character=graph))

# For syllabics with multiple variants, pick the most appropriate one.
for syllable, variants in onsets_nucleus.items():
    if len(variants) > 1:
        choose_appropriate_variant(variants)
    else:
        graph, desc = first(variants)
        if 'CARRIER' in desc:
            continue
        roster.add(SyllabicWithVowelBase.new(graph))


plains_cree_syllabics = sorted(roster)


def create_tsv() -> None:
    """
    Print all syllabics in order.
    """
    any_syllablic = first(plains_cree_syllabics)
    fields = any_syllablic.to_dict().keys()
    writer = csv.DictWriter(sys.stdout,
                            fieldnames=fields,
                            delimiter='\t')
    writer.writeheader()
    for syllabic in plains_cree_syllabics:
        writer.writerow(syllabic.to_dict())


def create_vim_digraphs() -> None:
    """
    Generates a .vim file that defines a bunch of digraphs.
    """
    all_digraphs: Set[str] = set()
    for syllabic in plains_cree_syllabics:
        digraph = syllabic.vim_digraph
        assert len(digraph) == 2, f"not exactly 2 characters: {syllabic}"
        assert digraph not in all_digraphs, f"Already saw digraph: {syllabic}"
        assert all(c in ascii_printable for c in digraph), (
                f"Non-ASCII digraph: {digraph}"
        )

        print(f"digraph {digraph} {syllabic.scalar_value:d}",
              f"\" {syllabic.character} {syllabic.code_point} {syllabic.name}")
        all_digraphs.add(digraph)


if __name__ == '__main__':
    if '--vim' in sys.argv[1:]:
        create_vim_digraphs()
    else:
        create_tsv()
