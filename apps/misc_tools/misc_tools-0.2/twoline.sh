#!/bin/bash

if [ "$#" -ne 1 ]; then
     echo "twoline.sh - a generic script to change a multilined FASTA file to a two lined FASTA file."
     echo "Please make sure there are no %s in the file to be changed."
     echo ""
     echo "To use:"
     echo "twoline.sh <filename> "
else

    cat <"$1" | sed 's/^>/\%>/g' | sed '/>/s/$/%/g' | tr -d '\n' | tr '\%' '\n' | sed '1d'

fi