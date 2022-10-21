#!/usr/bin/env python3

#'''
#exclude_regions.py script for piped output:
#Filters out variants in a VCF file that fall within repeat regions, prophages,
#PE or PPE proteins etc that have been reported previously by Price-Carter et 
#al, 2018 DOI:10.3389/fvets.2018.00272
#Usage given if script improperly used.    
#'''


import sys
import os 

def main(): #this is the main function that will do the actual script.
    exclude_regions_file = open(sys.argv[1])
    exclude_regions = []
    for region in exclude_regions_file:
        region = region.strip().split(",")
        exclude_regions.append([int(region[0]), int(region[1])])
                  
    lines = []
    remove_variants = []
    for line in sys.stdin:
        lines.append(line.strip())
        if line.startswith('#'):
            print(line.strip())
        else:
            pos = int(line.split()[1])
            for region in exclude_regions:
                if region[0] <= pos <= region[1]:
                    remove_variants.append(pos)
                    break         
    #print(remove_variants)                
    for line in (line for line in lines if not line.startswith('#')):
        pos = int(line.split()[1])
        if pos not in remove_variants:
            print(line.strip())
    sys.stdout.flush()
            
if __name__ == "__main__":
    if os.isatty(sys.stdin.fileno()) or len(sys.argv) < 2:
        print("exclude_regions.py - generic tool that takes as input a vcf file from stdout "
              "and filters out variants that fall within regions specified in user provided "
              "exclude-regions-file.txt. "
              "Usage: \n"
              "cat my.vcf | exclude_regions.py /path/to/exclude-regions-file.txt\n")
    else:
        try:
            main()
        except BrokenPipeError:
            pass
