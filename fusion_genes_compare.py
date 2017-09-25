#!/usr/bin/env python 
import os
import re
import argparse
import sys


def read_files_store_data(input_files,output_file):
    star_dict={}
    fc_dict={}
    for input_file in input_files:
        if input_file.endswith("star-fusion.fusion_candidates.final.abridged"):
           #We have a star fusion file
           # Send to STAR fusion dict
            with open(input_file, 'r') as f:
                for line in f:
                    if line.startswith("#"):
                        #Skip header
                            continue
                    else:
                        fusion=line.split("\t")[0]
                        # If we want to store to metadata then that can be inserted here
                        fusion=fusion.split("--")
                        fusion=[item.rstrip() for item in fusion]
                        star_dict[fusion[0]]=fusion[1]
            #print star_dict
        elif input_file.endswith("summary_candidate_fusions.txt"):
           
            #We have a Fusion catcher file
           # Send to FusionCatcher dict
            with open(input_file, 'r') as f:
                for line in f:
                    if line.startswith("  * "):
                        #import pdb
                        #pdb.set_trace()
                        fusion=line.split(" ")[3]
                        fusion=fusion.split("--")
                        fusion=[item.rstrip() for item in fusion]
                        fc_dict[fusion[0]]=fusion[1]

        else:
           print"Found file with incorect file ending, omitting file {}".format(input_file)
    make_report(star_dict, fc_dict, output_file)



def make_report(star_dict, fc_dict, output_file):
    content=str()
    content+="## Number of Fusion genes detected with STAR-fusion: {} \n".format(len(star_dict))
    content+="## Number of Fusion genes detected with FusionCatcher: {} \n".format(len(fc_dict))
    gene_in_both=[]
    gene_star_only=[]
    gene_fc_only=[]

    for gene_A,gene_B in star_dict.items():
        if gene_B in fc_dict:
            gene_in_both.append(gene_B)
        if gene_A not in fc_dict:
            gene_star_only.append(gene_A)
        if gene_B not in fc_dict:
            gene_star_only.append(gene_B)

    for gene_A,gene_B in fc_dict.items():
        if gene_A in star_dict:
            gene_in_both.append(gene_A)
        if gene_B in star_dict:
            gene_in_both.append(gene_B)
        if gene_A not in star_dict:
            gene_fc_only.append(gene_A)
        if gene_B not in star_dict:
            gene_fc_only.append(gene_B)
    content +="##BOTH,STAR-FUSION,FUSIONCATCHER\n"
    maxlen = max([len(l) for l in [gene_in_both,gene_star_only,gene_fc_only]])
    for idx in range(0, maxlen-1):
	astr = gene_in_both[idx] if len(gene_in_both) > idx else ''
	bstr = gene_star_only[idx] if len(gene_star_only) > idx else ''
	cstr = gene_fc_only[idx] if len(gene_fc_only) > idx else ''
	content += "{}\t{}\t{}\n".format(astr, bstr, cstr)    
 
    with open(output_file, 'w') as f:
        f.write(content)
     
     
   



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Compare two list of fusion genes and give which fusions are found in both """)
    parser.add_argument("input_files", metavar='Input file', nargs='+', default='.',
                                   help="Input files from STAR fusion and Fusion catcher ")
    parser.add_argument("output_file", metavar='Output file', nargs='?', default='fusion_comparison.txt',
                                   help="File to save output to. ")
    args = parser.parse_args() 
    #merge_files(args.input_dir, args.dest_dir)
    read_files_store_data(args.input_files,args.output_file)
