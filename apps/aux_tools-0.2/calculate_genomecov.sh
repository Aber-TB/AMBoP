#$1 is the name of the bam file to be checked


if [ "$#" -ne 1 ]; then
    echo "calculate_genomecov.sh - M. bovis specific tool to print out specific coverage stats for reads aligned to M.bovis AF2122/97 reference genome (or variant of which has been
    chosen by user) - percentage of ref genome with at least 1 read coverage and at least 20 read coverage."
    echo "Script usage:"
    echo "calculate_genomecov.sh <bam file>"
    echo ""
    echo "Outputs the percentage of the reference genome with at least 1 read and at least 20 reads covering the site."
    echo "Note that this will create a temporary files called <bam file>.genomecov.temp, which will be removed at the end of the script."

else
    if [ -s $1 ]; then
	samtools depth -a $1 > $1.genomecov.temp;
	no_cov=$(awk 'BEGIN{nocov = 0} {if ($3 == 0) {nocov += 1}} END {print 100-nocov/4349904*100}' < $1.genomecov.temp);
	cov_20=$(awk 'BEGIN{cov = 0} {if ($3 >= 20) {cov += 1}} END {print cov/4349904*100}' < $1.genomecov.temp);
	echo -e ${1} "\t" $no_cov "\t" $cov_20  
	rm $1.genomecov.temp;
    fi
fi
