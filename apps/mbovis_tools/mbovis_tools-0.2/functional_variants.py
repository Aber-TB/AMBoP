#!/usr/bin/env python3
"""
Script to output two files: 
    all_interesting_pos.tsv contains those positions in the reference genome with
    identified variants in samples, the number of samples that had this alternate 
    and the sample names. 
    
    variants_in_functional_genes.csv contains these variant positions that fall 
    within genes/coding regions, with all the information from the gff and eggnog 
    annotations for each gene that the variant is in. 
"""

import sys
import os 

def main(): 
    #vcf_file = Taken from stdin. - relative path which should work from within the GitHub repo 
    gff_file = open("../../../../reference_genome/mbovisAF212297_ref_functional_annotations.csv")

    #First add lines into a list to iterate over them later. 
    lines = [] 
    #for a list of sample names from the vcf header
    sample_list = [] 
    #dictionary of key = position, value = ref, alt, #samples, sample names, snpEff info
    var_dict = {} 
    for line in sys.stdin:
        lines.append(line) #make list of lines
        if line.startswith('#CHROM'): 
            #get column header names from header. Note that index 9:end will be sample names.
            sample_list = line.strip().split("\t") 
        elif not line.startswith("##"):
            #get variant info from each line
            position = line.strip().split("\t")[1]
            reference = [line.strip().split("\t")[3]]
            #add in a replace to capture multiple alleles as alternatives and stop columns messing up.
            alternate = [line.strip().split("\t")[4].replace(",", ";")]
            #if there is snpeff info, then get out key parts to keep for the main output file:
            info = line.split("\t")[7]
            for field in info.split(";"):
                if "EFF=" in field:
                    field = field.split(",")[0].replace("=", "|").replace("(", "|")
                    effect = field.split("|")[1]
                    effect_impact = field.split("|")[2]
                    functional_class = field.split("|")[3]
                    codon_change = field.split("|")[4]
                    aminoacid_change = field.split("|")[5].split("/")[0].split(".")[1]
                    EFF = [effect, effect_impact, functional_class, codon_change, aminoacid_change]
                else:
                    #if there is no snpEff info in the vcf, just output N/A in these columns.
                    EFF=["N/A", "N/A", "N/A", "N/A", "N/A"]
            #split up the sample columns in the vcf 
            GTPL = line.strip().split("\t")[9:len(line.split("\t"))]
            samples_with_var = []
            #For each sample, get the file name, if it has the variant, add to a 
            #list and count the number of samples for each variant.
            for sample in GTPL:
                if sample != ".:.":
                    samplename = sample_list[GTPL.index(sample)+9].split("_")[0]
                    samples_with_var.append(samplename)
                    number_of_samples = [str(len(samples_with_var))]
            var_dict[position] = reference + alternate + number_of_samples + samples_with_var + EFF
            sys.stdout.flush()

    #Send this info to a tab-separated file called "all_interesting_pos.tsv". 
    with open("./all_interesting_pos.tsv", "w") as newfile:
        newfile.writelines("Position\tRef\tAlt\tCount\tSamples\n")
        for key,value in var_dict.items():
            newline = (key + "\t" + "\t".join(value[0:3]) + "\t" + ",".join(value[3:-len(EFF)]) + "\n")
            newfile.writelines(newline)


    #make dict of gene start and end as key and rest of line in file as value. 
    annotations_dict = {}
    for gene in (gene for gene in gff_file if not gene.startswith('#')):
        startpos = int(gene.strip().split(",")[4]) 
        endpos = int(gene.strip().split(",")[5])
        annotations_dict[startpos, endpos] = gene

    #Write the file variants_in_functional_genes.csv.
    with open("./variants_in_functional_genes.csv", "w") as outfile:
        outfile.writelines("#Variant Position,Reference allele,Alternate allele,"
                           "Number of Samples,Sample Names,SNP Effect,"
                           "Effect Impact,Functional Effect,Codon Change,"
                           "Amino Acid Change,Gene locus Tag,Chromosome,"
                           "Source,Type,Start(nucl),End(nucl),"
                           "Length(nucl),Strand,Gene Product,Gene Name,"
                           "Protein Name,COG,Functional Category,Description,"
                           "Gene name,EC,KEGG orthology,Transporter codes,CAZy,"
                           "PFAMs\n")    
        for var_key, var_value in var_dict.items():
            #for each variant in the vcf file 
            for annotation_key, annotation_value in annotations_dict.items():
                #for each gene annotation, check whether the variant falls within those start and end positions.
                 if annotation_key[0] <= int(var_key) <= annotation_key[1]:
                     output = var_key, ",", ",".join(var_value[0:3]), ",", ";".join(var_value[3:-len(EFF)]),",", ",".join(var_value[-len(EFF):]), ",", annotation_value
                     outfile.writelines(output)

            
if __name__ == "__main__":
    if os.isatty(sys.stdin.fileno()):
        print("Usage: this takes as input a vcf file from stdout and will "
              "output two files: "
              "all_interesting_pos.tsv contains those positions in the reference genome with"
              "identified variants in samples, the number of samples that had this alternate"
              "and the sample names.\n"
              "variants_in_functional_genes.csv contains these variant positions that fall" 
              "within genes/coding regions, with all the information from the gff and eggnog" 
              "annotations for each gene that the variant is in.\n"
              "example of use:\n"
              "cat my.vcf | functional_variants.py")
    else:
        try:
            main()
        except BrokenPipeError:
            pass 
 
