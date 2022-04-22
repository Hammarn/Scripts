#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
import os
import random
import pandas as pd
import numpy as np
import sys

from datetime import datetime
from collections import OrderedDict
from collections import Counter
from statistics import mean

import pdb
__author__ = "Rickard Hammarén @hammarn"


def read_tped(tped):
    tped = tped
    T_DF = pd.read_csv(tped, delimiter=" ", header = None)
    #remove trailing whitespace, a bit crude though
    T_DF= T_DF.dropna(how="any", axis='columns')
    return T_DF

def read_haps(haps):
    tped = haps
    T_DF = pd.read_csv(tped, delimiter=" ", header = None)
    #remove trailing whitespace, a bit crude though
    T_DF= T_DF.dropna(how="any", axis='columns')
    
    ## Replace 0 with the first Allele
    #pdb.set_trace()
    ## below is too slow and only work for the first 4000 individuals
    #T_DF =  T_DF.iloc[:,5:-1].replace(0, T_DF[3])
    #Replace 1 with  the second allele
    #T_DF = T_DF.iloc[:,5:-1].replace(1, T_DF[4])
    return T_DF

def read_sample(sample):
    pdb.set_trace()
    return



def calculate_metrics(pop, pop_haps):

    hap_list = []
    for haplotype in pop_haps:
        hap_list.append("".join(pop_haps[haplotype].tolist()))
    
    counts = Counter(hap_list)
    p_sum = 0
    if pop == "DRC_Bangubangu":
        pdb.set_trace()
    for key in counts:
        p = (counts[key]/len(hap_list))** 2 
        p_sum += p
    HH = 1 - p_sum
    
    #            string_to_write += "{}\t{}\t{}\t{}\t{}\n".format(chr + 1, pop, window, richness, HH) 
    return  HH


def split_into_haplotypes(tped_D, K, N, tped_index_dict, chr_numb, outfile):
    ###   CHR SNP_NAME BLAJ SNP_POS 
    ###   0       1    2         3
    
    #num_individuals = N
    ##there are two columns per individual!

    ## First four columns of tped is header data ^
    #num_indv = len(CHR[0].columns) - 4
    ## Need to also read tfam

    ## SPLIT into a DF per CHR
    CHR = [y for x, y in tped_DF.groupby(0, as_index=False)]
    #first_SNP = tped_DF[3][0]
    #last_SNP = tped_DF[3].iloc[-1]


    ### Need to get the differnt lenghts
    len_dict = {}
    for i in range(0,len(CHR)):
        ## It's the length in Bp that we are after, not lenght of the list
        ## This could also be done on a .map file. i.e from 1000 genomes
        # Will it matter? Not sure, could ask 
       #try:

        if type(CHR[i][3].iloc[0]) == int or type(CHR[i][3].iloc[0]) == float:
            ## we have a tped file as input
            dataframe_column_int = 3
        else:
            dataframe_column_int = 2

        start = CHR[i][dataframe_column_int].iloc[0]
        end = CHR[i][dataframe_column_int].iloc[-1]
        lenght = end - start 
        len_dict[i] = [start, end, lenght]
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    pops = tped_index_dict.keys()

    with  open(outfile, "w") as fh:
    ### Loop through each chromsosome (i)
        for i in range(0,len(CHR)):
                #window_list_of_dict.append(i)
                #window_list_of_dict[i] = {}
                
                ### start at start
                counter =  len_dict[i][0]
                
                ## Each trip through the loop is one genetic window, defined in size by K
                while counter < len_dict[i][2]:
                    
                    ### remove SNPs in the window with MAF < 10 %
                    ## get the SNPs in the window:
                    SNPS = CHR[i][CHR[i][dataframe_column_int].between(counter, counter + K)][1]
                    if len(SNPS) == 0:
                            ## Window with no SNPS!
                            counter += K
                            continue

                    ##Check each window 
                    for x in range(0, len(SNPS) ):
                       
                        SNP_series = CHR[i][CHR[i][1]==SNPS.values[x]].squeeze()
                        
                        if dataframe_column_int == 3:
                            SNP_series = SNP_series[4:]
                        
                        else:
                            
                            Allele_1_base =  SNP_series[3] 
                            Allele_2_base =  SNP_series[4]
                            SNP_series = SNP_series[5:]
                        
                        
                        ### Get alleles
                        ## I think this whoel getting Alleles thing is reduntant
                        ### If genotype = 0
                        if dataframe_column_int == 3:
                            ### TPED
                            if len(set(SNP_series)) > 2:
                                try:
                                    zero, Allele_1, Allele_2 = sorted( set(SNP_series))
                                except:
                                    pdb.set_trace()
                            else:
                                Allele_1, Allele_2 = sorted( set(SNP_series))
                        else:
                            ## .haps by defenition
                            Allele_1 = 0
                            Allele_2 = 1
                        
                    ### Below is the code that is window dependent.
                    ### In order to reduce randomness this is repeated 10 times and only the average is saved
                    HH_dict = {}
                    richness_dict = {}
                    ## set up the empty lists
                    for pop in pops:
                        HH_dict[pop] = []
                        richness_dict[pop] = []
                        ##here 
                    for iteration in range(1,11):
                        ## Remove the row is MAF <= 10%
                        ## As long as the value within value_counts() is a string it will return a fraction, which is what we want
                        if SNP_series.value_counts("any_key")[0] <= 0.10 or SNP_series.value_counts("any_key")[1] <= 0.10: 
                            ## the dataframe is the dataframe execept the removed SNPs row
                            try:
                                CHR[i] =  CHR[i] [CHR[i][1] != SNPS.values[x]]
                            except:
                                pdb.set_trace()


                        ## Skip windows with fever than 5 SNPs 
                        if len(CHR[i][CHR[i][dataframe_column_int].between(counter, counter + K)]) < 5:
                            ## Add K to go to the next window
                            counter += K
                            continue
                        else:
                            window = CHR[i][CHR[i][dataframe_column_int].between(counter, counter + K)].sample(n=5)
                            ## Randomly dowsample to 5 SNPs
                           # window_list_of_dict[i][counter] = CHR[i][CHR[i][dataframe_column_int].between(counter, counter + K)].sample(n=5)

                                ### Randomly draw haplotypes to look at, depending on user supplied number of "chr"'
                            ### In practise the smallest sample size
                            for pop in pops:
                                if len(tped_index_dict[pop]) > chr_numb:
                                    # Downsample to chr_numb
                                    haps = random.sample(tped_index_dict[pop][1:],chr_numb)
                                else:
                                    haps = tped_index_dict[pop][1:]

                                pop_haps = window.iloc[:,np.r_[haps]]
                                if dataframe_column_int == 2:
                                    # Haps mode
                                    ## For .haps we need to replace the 0 1 with the actual nucleotides here
                                    pop_haps = pop_haps.T.replace(0, window[3]) 
                                    pop_haps = pop_haps.replace(1, window[4])
                                    ## transpose back
                                    pop_haps = pop_haps.T
                                
                                ## Metrics
                                ## len()  on a datframe is number of rows       
                                richness = len(pop_haps.T.drop_duplicates())
                                HH  = calculate_metrics(pop, pop_haps)
                                HH_dict[pop].append(HH)
                                richness_dict[pop].append(richness)    
                    
                            ## Calcultate averages at the end of 10 iterations
                            ## We only need to save/write to file is there was one sampling with values
                    
                    for pop in pops:

                        try: 
                            HH_ave = mean(HH_dict[pop])
                            richness_ave = mean(richness_dict[pop])
                            string_to_write = "{}\t{}\t{}\t{}\t{}\n".format(i + 1, pop, counter, HH_ave, richness_ave)
                            fh.write(string_to_write)
                        except:
                            ## empty window
                             counter += K
                             continue
                    ## Done with a window, on to next    
                    counter += K
             
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("Current Time =", current_time)
                print("Done with chr {}".format(i+1)) 

                

if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Takes tped files or .haps files and calulates haplotype heterozygosity in a given window")
    parser.add_argument("-t", "--tped",
        help="Name of the tped file")
    parser.add_argument("-f", "--tfam",
        help="Name of tfam file")
    parser.add_argument("-hs", "--haps", 
        help="Name of haps file")
    parser.add_argument("-s", "--sample",
        help="Name of sample file")
    parser.add_argument("-n_inds", "--number_of_individuals", default = 10,
        help="Number of individuals to extract from each pop and analyse")
    parser.add_argument("-k", "--window_size", default = 10000,
        help="size of the haplotype window to divide the genome into.")
    parser.add_argument("-o", "--outfile", default = "HH.txt",
        help="Outfile name")
    parser.add_argument('--skip', dest='skip', action='store_true',
        help="Skip populations with too small sample size")
    parser.add_argument('--no-skip', dest='skip', action='store_false',
        help="Don't skip populations with too small sample size")
    parser.set_defaults(skip=True) 
    
    args = parser.parse_args()

    ## The number of allels to look at.
    ## it was called chr in the original Schlebusch 2012 paper
    ## 2 alleles/chr per individual per population
    chr_numb = 2 * int(args.number_of_individuals)
    
    ##  Set up check to determine if we are doing tped or .haps approach?
    
    ### Set default value
    haps_check = False  


    if args.tped is not None:
        tped_DF = read_tped(args.tped)
        
        tfam_DF = read_tped(args.tfam)
        nr_ind = len(tfam_DF)
        pops = tfam_DF[0].unique()
   
    if args.haps is not None:
        haps_check = True
        tped_DF = read_haps(args.haps)
        
        tfam_DF = read_haps(args.sample)
        ## Remove the row with  0       0        0       D       D    D            B
        tfam_DF = tfam_DF[tfam_DF[0]!="0"]
        tfam_DF = tfam_DF[tfam_DF[0]!="ID_1"]
        nr_ind = len(tfam_DF)
        pops = tfam_DF[0].unique()
         
       ### We are runing using .haps files
       ## One file Chr!
    ## Get the FID from tfam in a list
    index_list =  list(tfam_DF[0])
    ## Duplicate each item in the list
    index_list = [val for val in index_list for _ in (0, 1)]
    ### add 4 to the begining of index to corresppnd to tped format
    if haps_check == True:
         index_list = [0,1,2,3,4] + index_list
    else:
        index_list = [0,1,2,3] + index_list
    
    tped_index_dict = OrderedDict()
    last_pop = "FALSE"
    
    ## Create the index list. So we know wich column of the tped that belongs to each pop.
    for index, pop in enumerate(index_list):
        if isinstance(pop, int):
            continue
        ## First time we see this pop
        if not pop in tped_index_dict:
            
            #tped_indiex_dict[pop] = []
            tped_index_dict[pop] = [index]
        ## Just add all indices, we can get the stop with [-1] later
        tped_index_dict[pop].append(index)
        #if pop != last_pop:
        #    tped_index_dict[pop].append(index)
  
    pops_to_pop = []
   ## Check input pops
    for key in tped_index_dict.keys():
       if len(tped_index_dict[key][:-1]) < chr_numb :
           
           if args.skip:
                pops_to_pop.append(key)
           else:
               print("Error!!:")
               print("Population {} has fewer indivduals than the number of minimum individuals specified '{}'".format( key, chr_numb/2) )
               sys.exit()
    for key in pops_to_pop:
        tped_index_dict.pop(key)

    ut_nam = args.outfile
    split_into_haplotypes(tped_DF, int(args.window_size), nr_ind, tped_index_dict, chr_numb, ut_nam)
    
    #with open (args.outfile, "w") as f:
    #    f.write(output_string)
    print("Goodbye!")

