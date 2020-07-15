all: syllabics.tsv crk.tsv cwd.tsv csw.tsv

syllabics.tsv: syllabics.py
	./$< --legacy > $@

HEADER := qwerty cans code.point

crk.tsv: syllabics.tsv
	tr ' ' $$'\t' <<<'$(HEADER)' > $@
	awk -F$$'\t' '$$11 == "TRUE" { print $$14 "\t" $$1 "\t" $$16 }' $< >> $@

cwd.tsv: syllabics.tsv
	tr ' ' $$'\t' <<<'$(HEADER)' > $@
	awk -F$$'\t' '$$12 == "TRUE" { print $$14 "\t" $$1 "\t" $$16 }' $< >> $@

csw.tsv: syllabics.tsv
	tr ' ' $$'\t' <<<'$(HEADER)' > $@
	awk -F$$'\t' '$$13 == "TRUE" { print $$14 "\t" $$1 "\t" $$16 }' $< >> $@
