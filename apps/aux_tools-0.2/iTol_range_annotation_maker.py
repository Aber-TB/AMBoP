#!/usr/bin/env python3
"""
iTol range annotation generator.
Takes in csv file with specified column headers and makes range annotation text
file ready for iTol. 
"""



import argparse
from csv import reader
from os.path import isfile
import sys

#Set up argument parser to take in arguments from the command line. 
parser = argparse.ArgumentParser(description="Generates a text file for iTol to annotate ranges. "
                                 "Maximum number of unique range labels is 30.", 
                                  usage="iTol_range_annotation_maker.py <input.csv> <column header> [--output] [-h]")
parser.add_argument('infile', metavar="Input file", type=str, help="Input csv metadata file. This should be comma "
                    " separated, and the first line should be the header that identifies what information the columns contain."
                    " The first column should contain the same leaf IDs as imported into iTOL for the annotation file to work.")
parser.add_argument('column_header', metavar="Column header", type=str, help="Name of column header in metadata csv that"
                    " you want to create the range annotation in iTOL. Note: this is case-sensitive!")
parser.add_argument('-o', type=str, help="Specify an output file to save annotation to, must be a text file (.txt).", 
                    default="itol_range_annotation.txt")

args = parser.parse_args()

hexcolours = ["#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462",
              "#B3DE69", "#FCCDE5", "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F",
              "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F",
              "#E5C494", "#B3B3B3", "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3",
              "#FF7F00", "#FFFF33", "#A65628", "#F781BF", "#999999", "#808080"] 


def main():
    # check file exists, if not, print message and exit.
    if isfile(args.infile):
        pass
    else:
        sys.exit("File " + args.infile + " not found.")

    with open(args.infile, "r") as file:
        csv_reader = reader(file)
        header = next(csv_reader)
        if args.column_header not in header:
            print("Column header provided not found in provided csv file. Argument is case-sensitive.")
            exit(2)
        else:
            for column_label in header:
                #print(column_label.lower(), args.column_header.lower())
                if column_label == args.column_header:
                    column_to_keep = int(header.index(column_label))

            uniq_col_labels = []
            colour_dict = {}
            with open(args.o, "w") as outfile:
                outfile.writelines("TREE_COLORS\nSEPARATOR COMMA\nDATA\n")
                for row in csv_reader:
                    range_label = row[column_to_keep]
                    if range_label not in uniq_col_labels:
                        uniq_col_labels.append(range_label)
                        colour_dict[range_label] = hexcolours[uniq_col_labels.index(range_label)]
                    #print(row[0]+","+"range"+","+colour_dict[range_label]+","+range_label)
                    outfile.writelines(row[0]+","+"range"+","+colour_dict[range_label]+","+range_label+"\n")
    print("iTOL Annotations saved to file " + args.o)
if __name__ == '__main__':
    main()


