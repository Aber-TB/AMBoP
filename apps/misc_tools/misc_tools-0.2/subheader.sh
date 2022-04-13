#$1 is the name ofthe run"
#$2 is the memory i.e. 2G
#$3 is the number of threads
#$4 is the email address

if [ "$#" -ne 4 ]; then
    echo " subheader.sh - a generic script to print out an SGE submission file. "
    echo "Script usage:"
    echo "subheader.sh <Run Name> <Max Memory> <Number of Threads> <Email/User>"
    echo ""
    echo "i.e. subheader.sh newblast 2G 8 jef11"
else

    echo "#$ -e $PWD/$1.error"
    echo "#$ -o $PWD/$1.output"
    echo "#$ -N $1"
    echo "#$ -cwd"
    echo "#$ -j y"
    echo "#$ -pe multithread $3"
    echo "#$ -S /bin/bash"
    echo "#$ -m eas"
    echo "#$ -M $4@aber.ac.uk"
    echo "#$ -V"
    echo "#$ -v MALLOC_ARENA_MAX=1"
    echo "#$ -l h_vmem=$2"
  

    echo "cd $PWD"
fi
