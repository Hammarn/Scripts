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

def save(bim, ref, filename):

        new_frame = bim.merge(ref, left_on=3, right_on = "Position(bp)" )
        new_frame[[0,1,"Map(cM)",3,4,5]].to_csv(filename[0], sep = " ", index = False, header = False)

if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Add Cm info from reference file to plink .bim file")
    parser.add_argument("-b", "--bim", nargs = '+',
    help= "bim file ")
    parser.add_argument("-r", "--ref", nargs = '+',
    help= "reference file, i.e genetic_map_GRCh37_chr1.txt")

    args = parser.parse_args()
    filename = args.bim 
    
    
    bim = read_input(args.bim, None)
    ref = read_input(args.ref, True)
    save(bim, ref, filename)
