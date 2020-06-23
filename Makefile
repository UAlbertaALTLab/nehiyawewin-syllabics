all: syllabics.tsv crk.tsv cwd.tsv csw.tsv

syllabics.tsv: syllabics.py
	./$< > $@

crk.tsv: syllabics.tsv
	awk -F$$'\t' '$$11 == "TRUE" { print $$14 "\t" $$16 "\t" $$1 }' $< > $@

cwd.tsv: syllabics.tsv
	awk -F$$'\t' '$$12 == "TRUE" { print $$14 "\t" $$16 "\t" $$1 }' $< > $@

csw.tsv: syllabics.tsv
	awk -F$$'\t' '$$13 == "TRUE" { print $$14 "\t" $$16 "\t" $$1 }' $< > $@
