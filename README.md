nêhiyawêwin syllabics
=====================

[syllabics.tsv][] is a tab-separated file that contains
every Canadian Aboriginal syllabic character used to write nêhiyawêwin
(Plains Cree). For each character, this file contains the following
information:

\# | Column          | Description
-- | --------------- | -----------
 1 | cans            | The syllabic character. "Cans" is the [ISO 15924][] code for the Canadian Aborignal Syllabics script.
 2 | latn            | The syllabics equivalent in Standard Roman Orthography (SRO), with circumflexes (◌̂) for long vowels.
 3 | scalar.value    | The Unicode code point written as a decimal number (See also `code.point`).
 4 | kind            | Either **syllable** (like "ᐘ"), **vowel** (like "ᐋ"), or **consonant** (like "ᐤ").
 5 | has.vowel       | `TRUE` if the syllabic "contains" a vowel (aioâêîô).
 6 | has.long.vowel  | `TRUE` when the syllabic "contains" a long vowel (âêîô)
 7 | vowel           | The vowel that the syllabic "contains", written in SRO.
 8 | has.consonant   | `TRUE` if the syllable "contains" a consonant.
 9 | consonant       | The consonant that the syllabic "contains", written in SRO.
10 | has.w           | For syllables, it's `TRUE` if the syllable has an intervening "w" like ᑢ ("twa") vs ᑕ ("ta").
11 | in.plains.cree  | `TRUE` if used in nêhiyawêwin (Y-dialect)
12 | in.woods.cree   | `TRUE` if used in nīhithawīwin (Th-dialect)
13 | in.swampy.cree  | `TRUE` if used in nêhinawêwin (N-dialect)
14 | qwerty.mnemonic | What to type on a QWERTY "build-a-syllable" layout to get this character
15 | vim.digraph     | Digraph defined in the [nêhiyawêwin Vim plugin][vim-plugin].
16 | code.point      | Unicode code point, written in "U+ notation.
17 | unicode.name    | The syllabic's canoncial name as given in the Unicode character database.

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


look-alikes.tsv
---------------

[look-alikes.tsv][] is a tab-separated file that contains characters
that are easily mistaken for more appropriate Cree syllabics characters.
These characters are [documented here][crk-docs].

Column            | Description
----------------- | -----------
lookalike         | The look-alike (that is, incorrect) character.
actual            | The correct character.
code.point        | [informative] Code point of the look-alike character in "U+" notation.
actual.code.point | [informative] Code point of the correct character in "U+" notation.
name              | [informative] The canonical name of the look-alike in the Unicode character database.


Here's an example of using [look-alikes.tsv] in a shell script to replace look-alikes in pipeline with the appropriate character.

```sh
function fixlookalikes() {
    tr $(awk -F"\t" 'NR > 1 { from=from $1; to=to $2 } END { print from, to }' < look-alikes.tsv)
}

fixlookalikes <bad-file.txt > good-file.txt
```

[look-alikes.tsv]: ./look-alikes.tsv
[crk-docs]: https://crk-orthography.readthedocs.io/en/stable/#crk_orthography.syllabics2sro


Licenses
--------

You can freely use [syllabics.tsv][] [look-alikes.tsv][] for any
purpose, without attribution. [syllabics.tsv][] and [look-alikes.tsv][]
are released under the terms of the [CC0 1.0][] license.

`syllabics.py` is licensed under the terms of the [GNU General Public
License, v3][GPLv3]. Copyright © 2018 Eddie Antonio Santos.

[CC0 1.0]: https://creativecommons.org/publicdomain/zero/1.0/
[GPLv3]: ./LICENSE
