#!/usr/bin/env python3
import pandas as pd
import argparse
import sys
import re
import sys

import pdb

def read_annotation(in_file):
    in_file = in_file
    T_DF = pd.read_csv(in_file, delimiter="\t",  index_col = 0)
    return T_DF


def read_birdseed(in_file):
    in_file = in_file
    T_DF = pd.read_csv(in_file, delimiter=",", header = None, index_col = 0)
    return T_DF


def main(arguments):
    
    annotation = read_annotation(arguments.annotation)

    bird = read_birdseed( arguments.birdseed)
    pdb.set_trace()
    print("Goodbye")





if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Converts a Birdseed file into a tped file")

    parser.add_argument("-b", "--birdseed", 
    help= "Birdseed file")

    parser.add_argument("-a", "--annotation", 
            help= """An annotation file that contains information about the SNP position and gentope in the following format
            Probe_Set_ID	dbSNP	Chromosome	Physical_Position	Allele_A	Allele_B
SNP_A-8575125	rs10458597	1	554484	C	T
SNP_A-8575115	rs9629043	1	554636	A	G
SNP_A-8575371	rs11510103	1	557616	C	T""")
    
    parser.add_argument("-o", "--output_name", nargs = '+',
    help= "Name of the final outputfile")

    args = parser.parse_args()

    main(args)
