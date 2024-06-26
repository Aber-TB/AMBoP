'''Take in the variants_in_functional genes.csv from AMBoP, and return a count table for COG functional groups
 (allocated a letter) per sample.'''

import collections

with open("variants_in_functional_genes.csv") as csv:
    samples_dict = collections.defaultdict(lambda: collections.defaultdict(int))
    for line in csv:
        if line.startswith('#'):
            continue
        line = line.strip().split(",")
        samples_list = line[4].strip()
        func_group = line[22].strip()
        func_group = [*func_group]
        for sample in samples_list.split(";"):
            if len(func_group) == 0:
                func = "no COG"
                samples_dict[sample][func] += 1
            for func in func_group:
                samples_dict[sample][func] += 1

all_cogs = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "T", "U", "V", "Y",
            "Z", "R", "S", "-", "no COG"]

outfile = open('COG_count_table_per_sample.csv', 'w')

outfile.write("Samples,"+",".join(all_cogs)+'\n')

for sample, cog_dict in samples_dict.items():
    outfile.write(sample)
    for cog in all_cogs:
        outfile.write(','+str(cog_dict[cog]))
    outfile.write('\n')

'''Do the same here for the reference genome'''
with open("mbovisAF212297_ref_functional_annotations.csv") as csv_refgenome:
    ref_dict = collections.defaultdict(int)
    for line in csv_refgenome:
        if line.startswith("#"):
            continue
        line = line.strip().split(",")
        func_group = line[12].strip()
        if len(func_group) == 0:
            func = "no COG"
            ref_dict[func] += 1
        for func in func_group:
            ref_dict[func] += 1

outfile2 = open('COG_counts_for_reference.csv', 'w')
for key, value in ref_dict.items():
    outfile2.write(str(key) + "," + str(value)+"\n")
