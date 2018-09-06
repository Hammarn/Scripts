#!/usr/bin/env python
import sys
import re
import pdb
import os

from collections import OrderedDict



def read_viterbi(chr_n, vriterbi_file ):
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

def handle_input_files(files):
    # Figure out which chr we are working with and return them in order
    chr_pat = re.compile('chr\d+')
    chr_nm_pat re.compile('\d+')
    file_dict = {}
    for f in files:
        full_name =  os.path.basename(f)
        chr_plus_nm = chr_pat.search(f).group(1)
        chr_nm = chr_nm_pat.search(chr_plus_nm)
        file_dict[chr_nm] = full_name
    return file_dict

if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Make a scatter plot of FPKM counts between conditions")
    parser.add_argument("-v", "--viterbi", nargs = '+'
help="Viterbi output files from RFMix. Needs to contain the substring 'chrxx' where xx is the chromosome number")
    parser.add_argument("-m", "--map", nargs = '+'
help="Map file with genomic positions. Needs to contain the substring 'chrxx' where xx is the chromosome number")


    args = vars(parser.parse_args())

    file_dict =  handle_input_files(args.v) 
    count_dict = {}
    for chr_num in range(1,23) #22 chr
        count_dict[chr_nm] = read_viterbi(chr_num, file_dict[chr_num])


