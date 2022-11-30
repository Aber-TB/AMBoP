#!/usr/bin/env python3
import sys
import os

def main():
    taxon_dict = {}
    if len(sys.argv) != 2:
        print("Please provide path to kraken output file.")
        sys.exit()

    with open(sys.argv[1]) as krakenfile:
        for rawread in krakenfile:
            splitrawread = rawread.split("\t")
            uniqread = splitrawread[1]
            taxon = splitrawread[2]
            if "Mycobacterium" not in taxon:
                taxon_dict[uniqread] = taxon

    contaminants = []
    total_reads = 0
    for aligned_read in sys.stdin:
        total_reads += 1
        aligned_read_id = aligned_read.split("\t")[0]
        if aligned_read_id in taxon_dict:
            contaminants.append(taxon_dict[aligned_read_id])

    total_contams = len(contaminants)
    percentage_contams = total_contams / total_reads * 100

    print(percentage_contams, "%", ":",  "; ".join(set(contaminants)))

    sys.stdout.flush()

if __name__ == "__main__":
    if os.isatty(sys.stdin.fileno()):
        print("find_contaminants.py"
              "Find aligned read contaminants in bamfile.\n"
              "Use samtools view to visualise the bamfile, then pipe it to this python script and provide the path to the kraken file.\n"
              "Output is a percentage of the number of contaminants as a total of all reads that aligned, then a colon, followed by a"
              "semicolon separated list of kraken taxa the contaminants are assigned as.\n"
              "---\n"
              "eg samtools view my_aligned_reads.bam | find_contaminants.py my_kraken_file.kraken")
    else:
        main()
