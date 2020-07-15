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

import csv
import sys
from string import printable as ascii_printable
from typing import Set

from libsyllabics.types import Consonant, Syllabic, Syllable, Vowel
from libsyllabics.utils import first


def create_tsv() -> None:
    """
    Print all syllabics in order.
    """
    any_syllablic = first(plains_cree_syllabics)
    fields = any_syllablic.to_dict().keys()
    writer = csv.DictWriter(sys.stdout, fieldnames=fields, delimiter="\t")
    writer.writeheader()
    for syllabic in plains_cree_syllabics:
        writer.writerow(syllabic.to_dict())


def create_vim_digraphs() -> None:
    """
    Generates a .vim file that defines a bunch of digraphs.
    """
    all_digraphs: Set[str] = set()
    for syllabic in plains_cree_syllabics:
        if not syllabic.in_plains_cree:
            continue
        digraph = syllabic.vim_digraph
        assert len(digraph) == 2, f"not exactly 2 characters: {syllabic}"
        assert digraph not in all_digraphs, f"Already saw digraph: {syllabic}"
        assert all(
            c in ascii_printable for c in digraph
        ), f"Non-ASCII digraph: {digraph}"

        print(
            f"digraph {digraph} {syllabic.scalar_value:d}",
            f'" {syllabic.character} {syllabic.code_point} {syllabic.name}',
        )
        all_digraphs.add(digraph)


def print_roster():
    for syllabic in roster:
        print(syllabic.character)


if __name__ == "__main__":
    if "--legacy" in sys.argv[1:]:
        from libsyllabics.legacy_roster import plains_cree_syllabics

    if "--vim" in sys.argv[1:]:
        create_vim_digraphs()
    elif "--roster" in sys.argv[1:]:
        print_roster()
    else:
        create_tsv()
