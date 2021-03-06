#!/bin/bash -l 

#script to be used with AMBoP to get read statistics. Takes inspiration from Richard Ellis' ReadStats.sh at https://github.com/ellisrichardj/BovTB-nf/tree/master/bin.

if [ "$#" -eq 0 ]; then
    echo "reads_stats.sh - a generic script to return a comma separated list of read statistics for a sample. Must supply sample name and AMBoP config file. If files not found, provide path. Inspired by Richard Ellis' ReadStats.sh available at https://github.com/ellisrichardj/BovTB-nf/tree/master/bin."
    echo "Script usage:"
    echo "reads_stats.sh <sample name> <AMBoP config file>"
    echo ""
    echo "i.e. read_stats.sh SRR12345678"
    exit
fi


isolate_ID=$1
[ -f $2 ] && source $2 || { echo "$2 - config file not found"; exit; } 
source $2  #to get $DATAPATH, $REFPATH, $MYPATH


raw_reads_f=$(zgrep -c "^+$" ${DATAPATH}/${isolate_ID}_${FORWARDPATTERN}) 
raw_reads_r=$(zgrep -c "^+$" ${DATAPATH}/${isolate_ID}_${REVERSEPATTERN})
trimmed_pairedreads_f=$(zgrep -c "^+$" ${MYPATH}/trimmed_reads/${isolate_ID}_1_trim_paired.fastq.gz)
trimmed_pairedreads_r=$(zgrep -c "^+$" ${MYPATH}/trimmed_reads/${isolate_ID}_2_trim_paired.fastq.gz)


module load samtools
deduped_aligned_reads=$(samtools view -c ${MYPATH}/bams/${isolate_ID}_sorted_nodups.bam)
samtools depth -a ${MYPATH}/bams/${isolate_ID}_sorted_nodups.bam > ${MYPATH}/bams/${isolate_ID}_depth.txt
avg_read_depth=$(awk '{sum+=$3} END {print sum/NR}' ${MYPATH}/bams/${isolate_ID}_depth.txt)
zero_coverage_count=$(awk '$3<1 {++count} END {print count}' ${MYPATH}/bams/${isolate_ID}_depth.txt)
Total_ref_sites=$(awk '{++count} END {print count}' ${MYPATH}/bams/${isolate_ID}_depth.txt)
rm -f ${MYPATH}/bams/${isolate_ID}_depth.txt


percent_after_trim_f=$(echo "scale=4; (${trimmed_pairedreads_f}/${raw_reads_f}*100)" | bc)
percent_after_trim_r=$(echo "scale=4; (${trimmed_pairedreads_r}/${raw_reads_r}*100)" | bc)
trimmed_reads_total=$(echo "${trimmed_pairedreads_f}+${trimmed_pairedreads_r}" | bc)
percent_after_trim_total=$(echo "scale=4; ( ${trimmed_reads_total} / ( ${raw_reads_f} + ${raw_reads_r} ) *100 )" | bc)
percent_mapped=$(echo "scale=4; (${deduped_aligned_reads}/(${trimmed_reads_total})*100)" | bc)
genome_cov=$(echo "scale=4; (100-(${zero_coverage_count}/${Total_ref_sites}*100))" | bc)

#Define thresholds for flag assignment

    mindepth=10 # require an average of at least 10 reads per site 
    min_percent_mapped=60 # require at least 60% of data maps to genome
    minreads=600000 # require at least 600,000 raw reads per sample

# This section assigns 'flags' based on the number of reads and the proportion mapping to reference genome
    
if [ ${avg_read_depth%%.*} -ge ${mindepth} ] && [ ${percent_mapped%%.*} -ge ${min_percent_mapped} ] && [ ${trimmed_reads_total} -ge ${minreads} ]; then 
    flag="[P]Pass";
elif [ ${avg_read_depth%%.*} -ge ${mindepth} ] && [ ${percent_mapped%%.*} -lt ${min_percent_mapped} ] && [ ${trimmed_reads_total} -ge ${minreads} ]; then
    flag="[p]Pass, Impure Sample";
elif [ ${avg_read_depth%%.*} -lt ${mindepth} ] && [ ${percent_mapped%%.*} -lt ${min_percent_mapped} ] && [ ${trimmed_reads_total} -ge ${minreads} ]; then 
    flag="[!]Contaminated";
elif [ ${avg_read_depth%%.*} -lt ${mindepth} ] && [ ${trimmed_reads_total} -lt ${minreads} ]; then 
    flag="[#]InsufficientData"
else flag="[?]CheckRequired";
fi

#If the file passed, then Look at VCF files 
if [ -f ${MYPATH}/variants/${isolate_ID}.vcf.gz ]; then
    Total_SNP_Count=$(zgrep -v "#" ${MYPATH}/variants/${isolate_ID}.vcf.gz | wc -l);
    sample_column=$(zcat ${MYPATH}/variants/APHA2021_filtered_merged.vcf.gz | awk -v isolate=${isolate_ID} '/#CHROM/{for (i=1; i<=NF; i++) {if ($i ~isolate) {print i} } }' );
    SNP_Count_After_Filtering=$(zcat ${MYPATH}/variants/APHA2021_filtered_merged.vcf.gz | grep -v "^#" | cut -f ${sample_column} | grep -c -v "\.\:\." )
else
    Total_SNP_Count="Did not pass filter";
    SNP_Count_After_Filtering="Did not pass filter";
fi

#Total_SNP_Count=$(zgrep -v "#" ${MYPATH}/variants/${isolate_ID}.vcf.gz | wc -l)
#sample_column=$(zcat ${MYPATH}/variants/APHA2021_filtered_merged.vcf.gz | awk -v isolate=${isolate_ID} '/#CHROM/{for (i=1; i<=NF; i++) {if ($i ~isolate) {print i} } }' )
#SNP_Count_After_Filtering=$(zcat ${MYPATH}/variants/APHA2021_filtered_merged.vcf.gz | grep -v "^#" | cut -f ${sample_column} | grep -c -v "\.\:\." )

# Print out the values to stdout

echo "#Sample,Raw_Reads_F,Raw_Reads_R,Trimmed_Reads_F,%After_Trim_F,Trimmed_Reads_R,%After_Trim_R,Total_Trimmed_Reads,%Total_Trimmed_Reads,Aligned_Deduped_Reads,%_Aligned,Average_Read_Depth,Avg_Genome_Coverage,Outcome,Total_SNP_Count,SNP_Count_After_Filtering" 

echo "${isolate_ID},${raw_reads_f},${raw_reads_r},${trimmed_pairedreads_f},${percent_after_trim_f},${trimmed_pairedreads_r},${percent_after_trim_r},${trimmed_reads_total},${percent_after_trim_total},${deduped_aligned_reads},${percent_mapped},${avg_read_depth},${genome_cov},${flag},${Total_SNP_Count},${SNP_Count_After_Filtering}"
