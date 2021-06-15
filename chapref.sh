#/bin/bash
# Script to identify references that are present but not defined in a given LaTeX file
# These are likely cross-chapter references, and ought to be called out as such in the text

# References found in the file
grep -o '\\ref{[a-zA-Z:_0-9]*}' $1.tex | cut -d '{' -f 2 | cut -d'}' -f 1 | sort -u > refs.txt

# Labels defined in the file
grep -o '\\label{[a-zA-Z:_0-9]*}' $1.tex | cut -d '{' -f 2 | cut -d'}' -f 1 | sort -u > labels.txt

# Want listing of every reference not defined as a label
for ref in `diff -d refs.txt labels.txt | grep '<' | cut -d ' ' -f 2 | grep -v 'chap:'`
do
    grep '\label{'$ref'}' *_chap.tex
done

# Clean up
rm refs.txt
rm labels.txt
