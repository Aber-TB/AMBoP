#!/usr/bin/env python3
import sys
import os 

def main(): 
    prev_position = 0
    failing_positions = []
    if len(sys.argv) > 1:
        window = int(sys.argv[1])
    else:
        window = 10
    
    lines = []
    for line in sys.stdin:
        lines.append(line)
        if line.startswith('#'):
            print(line.strip()) # this will print the header line
        else:
            current_position = int(line.split()[1])
            if current_position - window > prev_position:
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
        print("variantpositionfiltering.py - a generic tool that takes as input a vcf "
              "file from stdout and will filter out any variants where the position is "
              "within a user-defined number of base pairs of another variant reported. "
              "Both variants are then removed. If no number is supplied, 10 bp is used "
              "as default.\n"
              "Usage:\n"
              "cat my.vcf | variantpositionfiltering.py [number of base pairs]\n")
    else:
        try:
            main()
        except BrokenPipeError:
            pass
