#!/bin/sh
#$1 is the name of the input file.
#$2 is the output file.

if [ "$#" -ne 2 ]; then
    echo "blast_tophits.sh - Generic script to take the tophits of Blast output (must be format6)."
    echo "default values for -outfmt 6 are 'qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore'"
    echo -e "\n---------"
    echo "Script usage:"
    echo "tophits.sh <Blast output file> <outputfile name>"
    echo -e "\n---------"
   
else
    
sort -k1,1 -k12rn $1 | 
awk 'BEGIN {prev=""; score=""} 
           {if ($1 != prev) 
	       {print $0; prev=$1; score=$12} 
            else if ($1 == prev  && $12 >= score) 
	       {print $0; score=$12}
           }' > $2
   
fi
