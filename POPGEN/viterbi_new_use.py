#!/usr/bin/env python
import sys
import re
import pdb
import os

from collections import OrderedDict



def read_viterbi(viterbi_file, chr_nr):
    viterbi = viterbi_file
    chr_dict = OrderdDict()
    counter=0
    with open (viterbi, 'r') as f:
        for line in f:
            ## Count occurence of each source population per line. 
            one = line.count('1')
            two = line.count('2')
            three = line.count('3')
            four = line.count('4')
            five = line.count('5')
            six = line.count('6')
            counter +=1 
            chr_dict[counter]=[one,two,three,four,five,six]
    
    return chr_dict

def handle_input files(files):
    # Figure out which chr we are working with and return them in order
    pattern = re.compile('chr\d+')
    
    return file_order

if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Make a scatter plot of FPKM counts between conditions")
    parser.add_argument("-v", "--viterbi", nargs = '+'
help="Viterbi output files from RFMix. Needs to contain the substring 'chrxx' where xx is the chromosome number")
    parser.add_argument("-m", "--map", nargs = '+'
help="Map file with genomic positions. Needs to contain the substring 'chrxx' where xx is the chromosome number")


    args = vars(parser.parse_args())

    
    
    # Repeat fr each chrom

