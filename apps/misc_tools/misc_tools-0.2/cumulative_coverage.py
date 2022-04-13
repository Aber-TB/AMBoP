#!/usr/bin/env python3
"""
Script to take input from stdin and print out the percentage of sites that has
5x, 10x and 20x coverage (doesn't include sites with 0 coverage). Takes input 
from stdout from Samtools stats:
samtools stats my_file.bam | grep ^COV | cut -f 2- . If there are any errors, 
output lines will start with a #
Last edited 11/10/2021
"""

import os
import sys

if not os.isatty(sys.stdin.fileno()):
    prev=0
    cumulative_dict = {'5': "-", '10': "-", '20': "-"}


    for line in sys.stdin:
        line=line.split()
        if int(line[2]) >0:
            cumulative_dict[line[1]] = int(line[2]) + prev
            prev +=int(line[2])
            last = line[1]
#print(cumulative_dict)    
    
    try:
        total = cumulative_dict[last]
        percent_cov5 = round(cumulative_dict['5']/total*100, 3)
        percent_cov10 = round(cumulative_dict['10']/total*100, 3)
        percent_cov20 = round(cumulative_dict['20']/total*100, 3)
                    
        print(f"Percentage of sites with coverage of 1-5=\t {percent_cov5}%\n"
              f"Percentage of sites with coverage of 1-10=\t {percent_cov10}%\n"
              f"Percentage of sites with coverage of 1-20=\t {percent_cov20}%")
    except:
        print("#There may be no sites with 5x, 10x or 20x coverage, indicated below by a dash")
        print("#Coverage, cumulative count:")
        for key,value in cumulative_dict.items():
            print("#"+key, value)
else:
    print("cumulative_coverage.py - Generic script to take input from stdin and print out the"
          "percentage of ref genome sites that has 5x, 10x and 20x coverage." 
          "Usage: this takes input from stdout from Samtools stats:\n"
          "samtools stats my_file.bam | grep ^COV | cut -f 2- | "
          "cumulative_coverage \n"
          "if there are any errors, output lines will start with a #")
