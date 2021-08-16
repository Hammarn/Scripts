#!/usr/bin/env python3
import pandas as pd
import argparse
import sys
import re
import sys

import pdb
pd.options.mode.chained_assignment = None  # default='warn'


__author__ = "Rickard Hammarén @hammarn"


def read_input(in_file):
    in_file = in_file
    T_DF = pd.read_csv(in_file, delimiter="\t", header = None)
    return T_F

def determine_chr(in_file):
    
    return 

def main(arguments):
    input_files = arguments.input
    bims = arguments.bim
    output_name = arguments.output_name
    chr_pat = re.compile('chr\d+')
    haplo_num_pat = re.compile('hap_\d+')
    
    file_dict = {}
    # needed for later,will contain value of each raw bam
    geno_dict = {}

    ## Sort in Alphanumerical instead of just aplhabetical
    input_files.sort(key=lambda f: int(re.sub('\D', '', f)))
    bims.sort(key=lambda f: int(re.sub('\D', '', f)))

    for num,bim in enumerate(bims):
        geno_dict[num] = read_input(bim) 
        file_dict[num] = read_input(bim) 
        ## Save only the Snp-location in the DF
        file_dict[num]=file_dict[num][[0,1,2,3]]
        file_dict[num].columns = ["CHR","SNP_name","CM", "SNP"]
    

    for f in input_files:
        ##ahplotype:  haplo_num_pat.search(f).group(0).split("_")[1]
        ## CHR num :  chr_pat.search(f).group(0).split("chr")[1]
        CHR_num = chr_pat.search(f).group(0).split("chr")[1]
        ## Account for 0 indexing in the dict
        CHR_num = int(CHR_num) - 1
        hap_num = haplo_num_pat.search(f).group(0).split("_")[1]
        try:
            new_df = read_input(f)
            new_df.columns = ["SNP", "hap_{}".format(hap_num)]


        except pd.errors.EmptyDataError:
            ## File is empty, instead return a DF of Zero 
            ## double [[ to keep it a DF
            new_df =  geno_dict[int(CHR_num)][[3]]
            new_df.columns = ["SNP"]
            new_df["hap_{}".format(hap_num)] = "0"
        
        ## merge will only work if all the data is of the same type
        file_dict[int(CHR_num)] =  file_dict[int(CHR_num)].astype(str)
        new_df = new_df.astype(str)

        file_dict[int(CHR_num)] = file_dict[int(CHR_num)].merge(new_df, left_on ="SNP", right_on ="SNP", how = "outer",left_index=False, right_index=False).fillna("0")
        #delete after each run through
        del new_df

    #number_ind = int(hap_num)/2
    
    for CHR in file_dict.keys():
        file_dict[CHR].to_csv("{}.tped".format(output_name[0]), index = False, header = False, sep = " ", mode = "a")

    print("Output written to {}.tped".format(output_name[0]))

if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Aggregate the .bimlike file from Mosaic_get_anc_snps.R into a tped file")
    parser.add_argument("-i", "--input", nargs = '+',
    help= "A list of input files from the Mosaic_get_anc_snps.R script")
   
    parser.add_argument("-b", "--bim", nargs = '+',
    help= "A bim-file per Chromosome")
    
    parser.add_argument("-o", "--output_name", nargs = '+',
    help= "Name of the population to create the final tped for")

    args = parser.parse_args()
    
    main(args) 
