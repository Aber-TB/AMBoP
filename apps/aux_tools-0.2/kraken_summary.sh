#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "kraken_summary.sh - a script to return the number of reads that are assigned Mycobacterium taxon as a percentage of the total reads"
    echo "Script usage:"
    echo "kraken_summary.sh <kraken output file>"
    echo "---"
    echo "Give the kraken output file (which uses --use-names to give the taxon name not just id)."
    
else
    number_of_reads=$(cat $1 | wc -l)
    number_of_mycobacterium=$(awk '{if ($3 ~ /Mycobacterium/) print $0}' $1 | wc -l)
    count=$(echo "${number_of_mycobacterium} / ${number_of_reads}*100" | bc -l)
    echo $1 ${count}    
fi
