#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from abc import ABC, abstractmethod
from collections import OrderedDict
from functools import total_ordering
from typing import Any, Dict
from unicodedata import name, normalize

from .utils import to_r

COMBINING_CIRCUMFLEX_ACCENT = "\u0302"  # ◌̂

__all__ = [
    "Consonant",
    "Syllabic",
    "Syllable",
    "Vowel",
]


@total_ordering
class Syllabic(ABC):
    """
    Abstract base class for any syllabic character.

    Important subclasses:
     - Syllable
     - Vowel
     - Consonant
    """

    __slots__ = ("character",)

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
        return f"U+{self.scalar_value:04X}"

    @property
    def kind(self) -> str:
        """
        Return 'syllable', 'vowel', or 'consonant' as appropriate?
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

    @property
    @abstractmethod
    def qwerty_mnemonic(self) -> str:
        """
        Return a mnemonic to type it on a qwerty keyboard.
        """

    @property
    @abstractmethod
    def in_plains_cree(self) -> bool:
        """
        Is this in Plains Cree?
        """

    @property
    def in_woods_cree(self) -> bool:
        """
        Is this in Woods Cree?
        """
        # Woods Cree includes ALL OF THE WESTERN CREE SYLLABICS!
        return True

    @property
    def in_swampy_cree(self) -> bool:
        """
        Is this in Woods Cree?
        """
        # ¯\_(ツ)_/¯
        return self.in_plains_cree

    def to_dict(self) -> Dict[str, Any]:
        attrs = [
            ("character", "cans"),
            ("sro", "latn"),
            ("scalar_value", "scalar.value"),
            ("kind", ""),
            ("has_vowel", "has.vowel"),
            ("has_long_vowel", "has.long.vowel"),
            ("vowel_with_length", "vowel"),
            ("has_consonant", "has.consonant"),
            ("consonant", "consonant"),
            ("has_w", "has.w"),
            ("in_plains_cree", "in.plains.cree"),
            ("in_woods_cree", "in.woods.cree"),
            ("in_swampy_cree", "in.swampy.cree"),
            ("qwerty_mnemonic", "qwerty.mnemonic"),
            ("vim_digraph", "vim.digraph"),
            ("code_point", "code.point"),
            ("name", "unicode.name"),
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

    VOWELS = "AEIO"

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
        return normalize("NFC", self.vowel + COMBINING_CIRCUMFLEX_ACCENT)

    @property
    def has_long_vowel(self) -> bool:
        if self.vowel == "e":
            return True
        elif len(self.syllable) < 2:
            return False
        elif self.syllable[-1] == self.syllable[-2]:
            return True
        return False

    @property
    def _qwerty_mnemonic_for_vowel(self) -> str:
        if self.vowel == "e" or not self.has_long_vowel:
            return self.vowel
        else:
            return self.vowel * 2

    @classmethod
    def new(cls, character: str) -> "SyllabicWithVowelBase":
        syllable_name = name(character).split()[-1]
        if syllable_name[0:1] in cls.VOWELS:
            return Vowel(character)
        else:
            return Syllable(character)


class Syllable(SyllabicWithVowelBase):
    has_consonant = True

    @property
    def consonant(self) -> str:
        if self.syllable.startswith("TH"):
            return "th"
        return self.syllable[0].lower()

    @property
    def is_labialized(self) -> bool:
        return "W" in self.syllable[1:]

    @property
    def has_w(self) -> bool:
        return self.is_labialized or self.consonant == "w"

    @property
    def sro(self) -> str:
        c = self.consonant
        w = "w" if self.is_labialized else ""
        v = self.vowel_with_length
        return f"{c}{w}{v}"

    @property
    def vim_digraph(self) -> str:
        consonant = self.consonant

        if len(consonant) > 1:
            return ""

        vowel = self.vowel
        if self.is_labialized:
            consonant = consonant.upper()
        if self.vowel != "e" and self.has_long_vowel:
            vowel = vowel.upper()
        return consonant + vowel

    @property
    def in_plains_cree(self):
        return self.consonant != "th"

    @property
    def qwerty_mnemonic(self):
        return f"{self.consonant}{self.is_labialized and 'w' or ''}{self._qwerty_mnemonic_for_vowel}"


class Vowel(SyllabicWithVowelBase):
    has_consonant = False

    @property
    def sro(self) -> str:
        return self.vowel_with_length

    @property
    def vim_digraph(self):
        cont = ":" if self.has_long_vowel else "."
        return self.vowel + cont

    @property
    def qwerty_mnemonic(self):
        return self._qwerty_mnemonic_for_vowel

    @property
    def in_plains_cree(self):
        return True


class Consonant(Syllabic):
    has_vowel = False
    has_consonant = True

    @property
    def consonant(self):
        if self.sro == "hk":
            raise AttributeError("Not a simple consonant")
        return self.sro

    @property
    def sro(self) -> str:
        description = self.name[len("CANADIAN SYLLABICS ") :]
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
            "TH-CREE TH": "th",
            "FINAL RING": "w",
            "HK": "hk",
            # Used in loanwords only:
            "MEDIAL L": "l",
            "MEDIAL R": "r",
        }
        return consonants[description]

    @property
    def vim_digraph(self):
        if self.sro == "hk":
            return "hk"
        elif self.sro == "th":
            # XXX: no digraphs for th cree :/
            return ""
        return self.sro + "."

    @property
    def in_plains_cree(self):
        return self.sro != "th"

    @property
    def qwerty_mnemonic(self):
        return self.sro
