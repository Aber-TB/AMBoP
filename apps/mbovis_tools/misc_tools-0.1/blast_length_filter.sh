#!/bin/sh
#$1 is the name of the input file.
#$2 is the output file.
#$3 is the minimum percentage of either query or subject sequence that should align. 
if [ "$#" -ne 3 ]; then
    echo " "
    echo "  |  blast_length_filter.sh - Generic script to filter BLAST output based on sequence length."
    echo "  |  Input must be the output of BLAST when run with the argument -outfmt \"6 std qlen slen qcovs\""
    echo "  |  Script usage:"
    echo "  |  length_filter.sh <BLAST tab output file> <outputfile name> <integer or float number>"
    echo "  |  --------- "
    echo "  |  For example: length_filter.sh my_blast.tab my_filters.out 80"
    echo -e "  |  --------\n\n"
else
    cat $1 |
    awk -v val=$3} '{
                   min_q=$13*val*0.01; min_s=$14*val*0.01
                   }
                   {if ($13 <= $14 && $4 >= min_q)
                          print $0;
                   else if ($14 <= $13 && $4 >= min_s)
                          print $0;
                   }' > $2

fi

