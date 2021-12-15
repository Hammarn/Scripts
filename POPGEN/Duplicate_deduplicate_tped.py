#!/usr/bin/env python3
# -*- coding: utf-8 -*
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import argparse
import os
import pdb
__author__ = "Rickard Hammarén @hammarn"


def read_tped(tped):
    tped = tped
    T_DF = pd.read_csv(tped, delimiter=" ", header = None)
    #remove trailing whitespace, a bit crude though
    T_DF= T_DF.dropna(how="any", axis='columns')
    return T_DF

def deduplicate_tped(tped):
    corr_cols = tped[tped.columns[4::2]]
    index = tped[tped.columns[:4]]
    deduped = pd.merge( index, corr_cols, left_index = True, right_index = True)
    return deduped

def deduplicate_tfam(tfam):
    # Remove every other line
    A_rows = tfam.iloc[::2, :]
    #Replace _A at the end of strings
    A_rows[1] = A_rows[1].str.replace("_A$","")
    return A_rows

def duplicate_tped():
    return duplicated

def duplicate_tfam():
    return duplicated


def main():
    # Command line arguments
    parser = argparse.ArgumentParser("Takes tped files or .haps files and calulates haplotype heterozygosity in a given window")
    parser.add_argument("-i", "--input",
        help="Basename of the tped/tfam file to manipulate")
    parser.add_argument("-o", "--outname",
        help="Name of the output basename")
    parser.add_argument('--duplicate', default=False, action='store_true',
        help="To duplicate or de-duplicate, default dedulicate for duplicate enter 'True'")

    args = parser.parse_args()
    print("Reading tped file, this might take a while")
    input_name = args.input
    tped = read_tped("{}.tped".format(input_name))
    tfam = read_tped("{}.tfam".format(input_name))
    
    
    
    if args.duplicate:
        pdb.set_trace()
        print("Duplicating tped")
        duplicate_tped(tped).to_csv("{}_dup.tped".format(input_name), sep = " ", index = False, header = False)  
        duplicate_tfam(tfam).to_csv("{}_dup.tfam".format(input_name), sep = " ", index = False, header = False)  
        
    
    else:
        print("De-duplicating tped")
        deduplicate_tped(tped).to_csv("{}_dedup.tped".format(input_name), sep = " ", index = False, header = False)
        deduplicate_tfam(tfam).to_csv("{}_dedup.tfam".format(input_name), sep = " ", index = False, header = False)
    

if __name__ == "__main__":
    main()      
