#!/usr/bin/env python
import pandas as pd
import argparse
import sys

import pdb

def read_input(input_file, header):
    if not header:
        DF = pd.read_csv(input_file[0], sep = "\s+" , header = None)
    if header:
        DF = pd.read_csv(input_file[0], sep = "\s+" )
    return DF

def save(bim, snp, filename):
        new_frame = bim.merge(snp, left_on=3, right_on = "V4" )
        new_frame[[1,0,2,3,4,5]].to_csv(filename[0], sep = " ", index = False, header = False)

if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Fix SNP file")
    parser.add_argument("-b", "--bim", nargs = '+',
    help= "bim file ")
    parser.add_argument("-s", "--snp", nargs = '+',
    help= "The SNP file from MOSAIC")

    args = parser.parse_args()
    filename = args.snp 
    
    
    bim = read_input(args.bim, None)
    snp = read_input(args.snp, True)
    save(bim, snp, filename)
