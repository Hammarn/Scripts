#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import re
import os
from collections import OrderedDict

__author__ = "Rickard Hammarén @hammarn"

def handle_input_files(files):
    # Figure out which chr we are working with and return them in order
    chr_pat = re.compile('chr\d+')
    uppercase = re.compile('CHR\d+')
    chr_nm_pat = re.compile('\d+')
    file_dict = {}
    for f in files:
        full_name =  os.path.abspath(f)
        try:
            chr_plus_nm = chr_pat.search(f).group(0)
        except AttributeError,TypeError:
            chr_plus_nm = uppercase.search(f).group(0)

        chr_nm = chr_nm_pat.search(chr_plus_nm).group(0)
        file_dict[chr_nm] = full_name
    return file_dict


def read_viterbi(viterbi_file):
    viterbi = viterbi_file
    chr_dict = OrderedDict()
    counter=0
    with open (viterbi, 'r') as f:
        for line in f:
            counter +=1
            chr_dict[counter]=line

    return chr_dict

def read_FB(Fb_file):
    Fb_file = Fb_file
    FB = pd.read_csv(Fb_file, delimiter=" ", header = None)
    #remove trailing whitespace, a bit crude though
    FB = FB.dropna(how="any", axis='columns')
    return FB

def read_genetic_map(map_file):
    map = map_file 
    position_dict = OrderedDict()
    map_contents =  OrderedDict()
    with open (map, 'r') as f:
        for counter,line in enumerate(f, start = 1):
            position_dict[counter] = line.split("\t")[0]
            map_contents[counter] = line
    return position_dict, map_contents


def filter_away_telemomers(count_dict, bp_dict):
    """
    takes in viterbi counts and genomic position in bps and return filtered counts
    """
    ##Centromere locations:
    ##chrom left.base right.base
    centromeres ={ 
             1 : (121535434,124535434),
             2 : (92326171,95326171),
             3 : (90504854,93504854),
             4 : (49660117,52660117),
             5 : (46405641,49405641),
             6 : (58830166,61830166),
             7:  (58054331,61054331),
             8 : (43838887,46838887),
             9 : (47367679,50367679),
             10 : (39254935,42254935),
             11 : (51644205,54644205),
             12 : (34856694,37856694),
             13 : (16000000,19000000),
             14 : (16000000,19000000),
             15 : (17000000,20000000),
             16 : (35335801,38335801),
             17 : (22263006,25263006),
             18 : (15460898,18460898),
             19 : (24681782,27681782),
             20 : (26369569,29369569),
             21 : (11288129,14288129),
             22 : (13000000,16000000)
             }
    
    #2 Mbp
    filter_value = 2000000
    # vit_num is the Chromosome in question
    for vit_num in range(1,23):
        items  = count_dict[vit_num]
        items_to_keep = []    
        
        #first =  int(bp_dict[vit_num][1]) 
        #first = first + filter_value
        first = filter_value
        last = int(bp_dict[vit_num].items()[-1][1]) 
        last = last - filter_value
        left_cent =centromeres[vit_num][0] - filter_value
        right_cent =centromeres[vit_num][1] + filter_value
        
        ##print "{}".format(len(count_dict[vit_num])) 
        ## pop instead of making a new library
    #    print "Filtering away telomeric regions for chr {} this could take a while".format(vit_num) 
        for key in bp_dict[vit_num].keys():
            #  pdb.set_trace()
            ## Check if in telomere region
            if int(bp_dict[vit_num][key]) < first or int(bp_dict[vit_num][key])  > last:
                ## Check if in Centromere region
                if int(bp_dict[vit_num][key]) > left_cent or int(bp_dict[vit_num][key]) < right_cent:
                    try:
                        count_dict[vit_num].pop(key)
                    except KeyError:
                        continue
    return count_dict


#def save_output():


if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Filters viterbi files from RFMIX, 2Mb for the telomere and centromere")
    parser.add_argument("-v", "--viterbi", nargs = '+',
        help="Viterbi output files from RFMix. Needs to contain the substring 'chrxx' where xx is the chromosome number in the filename")
    parser.add_argument("-m", "--map", nargs = '+',
        help="Map file with genomic positions. Needs to contain the substring 'chrxx' where xx is the chromosome number in the filename")

    args = parser.parse_args()
    viterbi_dict =  handle_input_files(args.viterbi) 
    map_dict = handle_input_files(args.map)

    count_dict = OrderedDict()
    for chr_num in range(1,23): #22 chr
    #chr_num = 1  #22 chr
        print "Reading results for chr {}".format(chr_num)
        count_dict[chr_num] = read_viterbi(viterbi_dict[str(chr_num)])
    
    #count_dict[22] = read_viterbi(viterbi_dict["22"])
    ## FB 

    bp_dict = OrderedDict()
    for chr_num in range(1,23): #22 chr
    #chr_num = 1  #22 chr
        print "Reading map file for chr {}".format(chr_num)
        bp_dict[chr_num], map_dict[chr_num]  = read_genetic_map(map_dict[str(chr_num)])
        
    
    count_dict  =  filter_away_telemomers(count_dict, bp_dict) 
    
    for chr_num in range(1,23): #22 chr$():
        viterbi_out = "Filtered_viterbi_chr{}.Viterbi.txt".format(chr_num)
        map_out = "Filtered_viterbi_chr{}.map".format(chr_num)
        
        with open(viterbi_out,"w") as f:
            for value in count_dict[chr_num].values():
                f.write(value)
        with open(map_out, "w") as f:
            for key in count_dict[chr_num].keys():
                f.write(map_dict[chr_num][key])


    #if not args.forward_backwards:
    #plotting(count_dict, bp_dict,FB_dict, backup_dict,args.print_FB,args.names ) 
    print "Goodbye"
