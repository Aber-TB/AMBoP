# The Centre of Excellence for Bovine Tuberculosis (CBTB) - Aberystwyth M.Bovis Pipeline (AMBoP)
## Contacts: Jess Friedersdorff  *jess@friedersdorff.com* - Nicholas Dimonaco *nicholas@dimonaco.co.uk*



### Software and versions used:
* trimmomatic 0.39 - https://github.com/usadellab/Trimmomatic
* bwa 0.7.17 - https://github.com/lh3/bwa
* samtools 1.5 - https://github.com/samtools/samtools
* bcftools 1.13 - https://github.com/samtools/bcftools
* snp-sites 2.5.1 - https://github.com/sanger-pathogens/snp-sites
* RAxML 8.2.12 - https://github.com/stamatak/standard-RAxML
* iqtree 1.6.12 - https://github.com/Cibiv/IQ-TREE
* snpEff 5.0e - https://github.com/pcingola/SnpEff


## Pipeline Overview: - *Incomplete*
Aberystwyth M. bovis Pipeline (AMBoP) is a pipeline (HPC Module) that takes raw sequence data, runs all the tools needed to find SNPs and 
then outputs functional information about these SNPs and builds trees.
![AMBoP_1.5.3_Menu.png](AMBoP_1.5.3_Menu.png)

1. Reads in the config file, makes directories.
2. Trimmomatic (with full list of adapters, see appendix 1, their source is in the sequence name) ILLUMINACLIP:trimmomatic_adapters.fasta:2:30:10:2 SLIDINGWINDOW:10:20 MINLEN:50. AVGQUAL:20 – the sliding window cut off is based on the badger culling trial paper (van Tonder et al., 2021).
4. Removes unnecessary unpaired files.
5. Aligns reads to reference using BWA mem, default settings.
6. Fed straight into Samtools which removes any secondary alignments (-F 256) and sorts bam file.
7. Duplicates removed from bam file using Samtools and indexed. Old bams removed, only deduped and sorted retained.
8. Mapping checks carried out using calculate_genomecov.sh creating bamfile_coverage.list.
9. Files selected that pass using select_files.sh which keeps any files with over 90% of the genome covered by at least 1 read. These passed files are symbolically linked in a new directory.
10. Bcftools mpileup used to call SNPs, with -d 1000 (1000 reads called per position), then bcftools call with –ploidy, multiallelic caller and returning variants only (removing indels).
11. Each vcf file (one per sample) is then filtered using 4 cut offs set by the config file. The defaults in the config file are those used for Mycobacterium bovis analysis (https://github.com/ellisrichardj/BovTB-nf) and can be found in other publications. The settings as defaults are DP>=10 (At least 10 reads needed to cover a site) & MQ>=30 (mapping quality at least 30) & DP4[2]>=1 & DP4[3]>=1 (at least 1 forward read and 1 reverse read covering the site) & (DP4[2]+DP4[3])/(DP4[0]+DP4[1]+DP4[2]+DP4[3])>=95 (allele supported by 95% of the reads covering the site). See appendix for more explanations.
12. Also run through variantpositionfiltering.py and exclude_regions.py which will filter out SNPs within 10bp of each other SNPs and ignores SNPs in regions known as regions of variance of higher mutation (PE/PPE etc) as published previously (Price-Carter et al., 2018).
13. Filtered vcf files (one for each sample) are then compressed with bgzip, indexed with bcftools, then all files merged using bcftools. Files are merged in 2 steps (because bcftools does not like handling >1021 files in one go) – subsets of 500 files are merged first, then those subsets are merged. These extra files are not deleted just yet because they are relatively small in size even for a data set of ~2000 samples.
14. Filtered and merged vcf file is then compressed and indexed.
15. Bcftools query and consensus used to create fasta file of whole genome for each sample (including their SNP sites). All fasta files catenated together into one “alignment” file.
16. Snp-sites used to find SNPs across all samples and make pseudo-genome sequence for each. Also used to calculate how many constant sites there are.
17. RAxML used to build tree using maximum likelihood, with fast bootstraps (100), seeds set to 12345, and GTRCAT model.
18. IQTree used to build tree using model prediction and fast bootstraps (1000).
19. SnpEff used to predict effect of SNPs and then also run functional_variants.py to find those SNPs within functional genes.
20. Some read statistics are calculated from raw reads, trimmed reads, aligned bam files and from the vcf files and put together into a csv file using read_stats.sh found in the mbovis_tools-0.1 module.
21. Finally there is a clear up phase. A final_files directory is made here, and all the functional outputs (SnpEff and functional_variants.py outputs), all input and output tree files from both RAxML and IQTree, the merged vcf file and the bam file coverage list file are all copied into this directory.
22. Then directories may be deleted, depending on what is specified in the config file by the user. Options are “TRIMMEDREADS” to remove trimmed reads, “BAMS” to remove bam files, “PASSEDFILES” to remove the directory with the symbolically links bam files that passed the genome coverage filter, “FASTA” which removes all the FASTA files, and “VARIANTS” which removes the variants directory containing all the individual vcfs, or “ALL” which will remove all of the listed.

## Pipeline User Definable Parameters:

1.	MYPATH – Path to output directory.
2.	DATAPATH - Path to raw data (as fastq.gz files, paired reads only)
3.	REFPATH - Path to the reference mbovis genome fasta file (mbovisAF212297 – provided).
4.	AUX_TOOLS - Set path to where the aux_tools directory is.
5.	ADAPTERS - Path to the Illumina adapters for Trimmomatic read trimming (provided).
6.	REF_FUNC_ANNO - Path to the csv file used to transfer EggNOG functions to SNP calls.
7.	UNIQ - 'Experiment' appendix to be used in file output.
8.	FORWARDPATTERN - Sets the sample raw read file pattern for forward reads.
9.	REVERSEPATTERN - Sets the sample raw read file patterns for reverse reads.
10.	FASTQC – set to true or false – whether or not to perform FastQC quality checking on raw reads.
11.	TRIM_FASTQC - set to true or false – whether or not to perform FastQC quality checking on trimmed reads.
12.	ILLUMINACLIP - Set which adapter and other illumina-specific sequences to be cut from the read.
13.	SLIDINGWINDOW - Set sliding window size to analyse average quality of read.
14.	MINLEN - Set minimum allowed length of read.
15.	AVGQUAL - Set the average quality score used to remove read.
16.	THREADS - Number of CPU threads to be used for each tool stage.
17.	BWA_THREADS - Number of CPU threads to be used specifically for bwa.
18.	MQ - SNP mapping quality.
19.	DP - SNP read depth.
20.	DP4F - Number of supporting forward reads.
21.	DP4R - Number of supporting reverse reads.
22.	SUPPORT - Percentage of reads needed to support an alternative site.
23.	SNPEFF_DB – the name of the SnpEff database (this can be one of the default SnpEff databases they provide or one readily made, check the SnpEff manual for this)
24.	CLEANUP - Sets which files to clean up after completed runtime (options are NONE, TRIMMEDREADS, BAMS, PASSEDFILES, FASTA, VARIANTS).

