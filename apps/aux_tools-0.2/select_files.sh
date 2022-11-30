#$1 is the name of the file to be checked to see if it passes the threshold (set to 90%)


if [ "$#" -ne 3 ]; then
    echo "select_files.sh - M. bovis specific tool to copy files that pass the coverage filter into a new directory, based on >90% of the genome having either at least 1x or 10x coverage."
    echo "Script usage:"
    echo "select_files.sh <bam file> <filtering type (1 or 10)> <output directory>"
    echo "---"
    echo "Copies aligned bam files to specified output directory if they pass the filter. You must set the filtering type to either:"
    echo "1: >90% of the sites in the reference genome has a depth of >=1"
    echo "20: >90% of the sites in the reference genome has a depth of >=10."
    echo "Note that this will call calculate_genomecov.sh which creates a temporary file called <bam file>.genomecov.temp, which will be removed at the end of the script."

else
    current_dir=$(pwd)
    [ -d $3 ] || mkdir -p $3
    if [ $2 = 1 ]; then
	cov_1=$(calculate_genomecov.sh $1 |
        awk '{if ($2 >= 90) print "1"; else print "0"}')
        if [ $cov_1 = 1 ]; then
	    cd $3;
	    ln -s ${current_dir}/$1;
	    ln -s ${current_dir}/$1.bai;
	    cd ${current_dir};
	    echo "Copied $1.";
	fi;
    elif [ $2 = 10 ]; then
	cov_10=$(calculate_genomecov.sh $1 |
        awk '{if ($3 >= 90) print "1"; else print "0"}'); 
        if [ $cov_10 = 1 ]; then
	    cd $3;
            ln -s ${current_dir}/$1;
            ln -s ${current_dir}/$1.bai;
            cd ${current_dir};
	    echo "Copied $1..."
        fi;
    else
	echo "Need to specify filtering type as either 1 or 10."
    fi;
fi
