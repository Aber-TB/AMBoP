#!/usr/bin/env python3
"""
iTol binary annotation generator.
Takes in a vcf file and creates a text file ready for iTol tree annotation. The annotation consists of a binary matrix
that will show presence/absence of SNPs for samples in different sites to allow identification of those that are common
to certain clades manually.
"""

import argparse
import csv
import itertools
from os.path import isfile
import sys

# set list of colour hex codes to loop over for the annotation file:
hexcolours = ["#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462",
              "#B3DE69", "#FCCDE5", "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F",
              "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F",
              "#E5C494", "#B3B3B3", "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3",
              "#FF7F00", "#FFFF33", "#A65628", "#F781BF", "#999999", "#808080"]

# Set up argument parser to take in arguments from the command line.
parser = argparse.ArgumentParser(description="Generates a text file for iTol to annotate presence of absence of SNP"
                                             " from a supplied VCF file.",
                                 usage="iTol_binary_annotation_maker.py <input.vcf> [--position_file] [--output] [-h]")
parser.add_argument('infile', metavar="input.vcf", type=str, help="Input vcf file. This should be a standard VCF file"
                                                                  " and should contain a double hashed header line (##) that shows column labels.")
parser.add_argument('-o', type=str, help="Specify an output file to save annotation to, must be a text file (.txt).",
                    default="itol_binary_annotation.txt")
parser.add_argument('--position_file', metavar="<list_of_positions.txt>", type=str, help="Specify a file that contains "
                                                                                         "a list of positions that should be filtered out and used in the annotation file. This can be used "
                                                                                         "to reduce the number of annotations given to iTol.")

args = parser.parse_args()


def main():
    if not isfile(args.infile):
        sys.exit("File " + args.infile + " not found.")
    # check supplied input file exists, if not, print message and exit.

    table = []
    fieldcolours = []
    fieldlabels = []
    sample_labels = ["#"]
    filtered_positions = []

    with open(args.infile, "r") as vcf_file:
        # check whether a position_file has been supplied as an argument:
        if args.position_file is not None:
            with open(args.position_file, "r") as filter_file:
                for pos in filter_file:
                    # for each position given in the file (one line per position), add it to the list:
                    filtered_positions.append(pos.strip())

        for line in vcf_file:
            line = line.rstrip()

            if line.startswith('#CHROM'):
                # get column header names from header. Note that index 9:end will be sample names:
                line = line.strip().split("\t")[9:]
                for samplename in line:
                    sample_labels.append(samplename.split("_")[0])
                table.append(sample_labels)

            elif not line.startswith("##"):
                position_row = []
                position = line.strip().split("\t")[1]
                position_row.append(position)
                samples = line.split("\t")[9:]
                for sample in samples:
                    if sample == '.:.':
                        position_row.append(0)  # absent, append a zero
                    else:
                        position_row.append(1)  # present, append a one.
                # Within the loop, the position_row variable is a list (per SNP position) and 0/1 for presence/absence.
                # Now check if there is a file provided that contains a list of positions to filter out and keep:
                if filtered_positions:  # check if filtered positions list is not empty
                    if position_row[0] in filtered_positions:
                        table.append(position_row)
                        # Also add the position to a new list to add into the itol annotation file for field labels:
                        fieldlabels.append(position_row[0])
                else:
                    table.append(position_row)
                    fieldlabels.append(position_row[0])

        fieldcolours += list(itertools.islice(itertools.cycle(hexcolours), len(fieldlabels)))
    # transpose the table to be positions as columns and samples as rows
    table2 = zip(*table)

    print("Created", len(fieldlabels), "annotations each for", len(sample_labels), "samples. Saving to file.")

    with open(args.o, "w", newline='') as outputfile:
        outputwriter = csv.writer(outputfile, delimiter=',')
        outputfile.writelines("DATASET_EXTERNALSHAPE\nSEPARATOR COMMA\nDATASET_LABEL,SNP positions\nCOLOR,#ff0000\n")
        outputfile.writelines("FIELD_COLORS,")
        outputwriter.writerow(fieldcolours)
        outputfile.writelines("\nFIELD_LABELS,")
        outputwriter.writerow(fieldlabels)
        outputfile.writelines("\nDATA\n")
        for row in table2:
            if not row[0] == "#":
                outputwriter.writerow(row)


if __name__ == '__main__':
    main()
