#!/usr/bin/env python3
import sys
import os 

def main(): #this is the main function that will do the actual script.
    prev_position = 0
    failing_positions = []
    
    lines = []
    for line in sys.stdin:
        lines.append(line)
        if line.startswith('#'):
            print(line.strip()) # this will print the header line
        else:
            current_position = int(line.split()[1])
            if current_position - 10 > prev_position:
                prev_position = current_position
            else:
                failing_positions += [current_position, prev_position]
                prev_position = current_position
    
    
    for line in (line for line in lines if not line.startswith('#')):
        current_position = int(line.split()[1])
        if current_position not in failing_positions:
            print(line.strip())
    sys.stdout.flush()
            

if __name__ == "__main__":
    if os.isatty(sys.stdin.fileno()):
        print("variantpositionfiltering.py - a generic tool to filter out any" 
              "variants in a VCF file were the position is within 10 bp of "
              "another variant reported."
              "Usage: this takes as input a vcf file from stdout and will "
              "filter out any variants were the position is within 10 bp of " 
              "another variant reported.\n"
              "example of use:\n"
              "bcftools filter my.vcf | python3 variantpositionfiltering.py")
    else:
        try:
            main()
        except BrokenPipeError:
            pass
