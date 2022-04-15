#$1 the sequence to be reversed
#!/bin/bash


if [ "$#" -ne 1 ]; then
    echo "reversecomp.bash - a generic script to reverse complement given sequence."
    echo "Uysage: enter sequence to be reversed."
    echo "reversecomp.bash <seq>"
else
    echo $1 | grep '^[ATCG]' | rev | tr 'ATCG' 'TAGC'
fi