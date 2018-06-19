nêhiyawêwin syllabics
=====================

[syllabics.tsv][] is a tab-separated file that contains
every Canadian Aboriginal syllabic character used to write nêhiyawêwin
(Plains Cree). For each character, this file contains the following
information:

Column         | Description
-------------- | -----------
cans           | The syllabic character. "Cans" is the [ISO 15924][] code for the Canadian Aborignal Syllabics script.
latn           | The syllabics equivalent in Standard Roman Orthography (SRO), with circumflexes (◌̂) for long vowels.
scalar.value   | The Unicode code point written as a decimal number (See also `code.point`).
kind           | Either **syllable** (like "ᐘ"), **vowel** (like "ᐋ"), or **consonant** (like "ᐤ").
has.vowel      | `TRUE` if the syllabic "contains" a vowel (aioâêîô).
has.long.vowel | `TRUE` when the syllabic "contains" a long vowel (âêîô)
vowel          | The vowel that the syllabic "contains", written in SRO.
has.consonant  | `TRUE` if the syllable "contains" a consonant.
consonant      | The consonant that the syllabic "contains", written in SRO.
has.w          | For syllables, it's `TRUE` if the syllable has an intervening "w" like ᑢ ("twa") vs ᑕ ("ta").
vim.digraph    | Digraph defined in the [nêhiyawêwin Vim plugin][vim-plugin].
code.point     | Unicode code point, written in "U+ notation.
unicode.name   | The syllabic's canoncial name as given in the Unicode character database.

[syllabics.tsv]: ./syllabics.tsv
[ISO 15924]: https://www.unicode.org/iso15924/iso15924-num.html
[vim-plugin]: https://github.com/eddieantonio/vim-nehiyawewin


syllabics.py
------------

[syllabics.py][] is the Python file that generated [syllabics.tsv][]. It
can also be used to generate a list of Vim digraphs (c.f., [the Vim
plugin][vim-plugin]). If you want to run [syllabics.py][], you'll need
Python 3.6.

[syllabics.py]: ./syllabics.py

Licenses
--------

You can freely use [syllabics.tsv][] for any purpose, without
attribution. [syllabics.tsv][] is released under the terms of the [CC0
1.0][] license.

`syllabics.py` is licensed under the terms of the [GNU General Public
License, v3][GPLv3]. Copyright © 2018 Eddie Antonio Santos.

[CC0 1.0]: https://creativecommons.org/publicdomain/zero/1.0/
[GPLv3]: ./LICENSE
