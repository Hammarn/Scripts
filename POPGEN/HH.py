#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
import os
import random
import pandas as pd
import numpy as np

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

def calculate_metrics(pop, pop_haps):

    hap_list = []
    for haplotype in pop_haps:
        hap_list.append("".join(pop_haps[haplotype].tolist()))
    
    counts = Counter(hap_list)
    p_sum = 0
    for key in counts:
        p = counts[key]/len(hap_list) ** 2 
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
        start = CHR[i][3].iloc[0]
        end = CHR[i][3].iloc[-1]
        lenght = end - start 
        len_dict[i] = [start, end, lenght]
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)


    pops = tfam_DF[0].unique()
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
                    SNPS = CHR[i][CHR[i][3].between(counter, counter + K)][1]
                    if len(SNPS) == 0:
                            ## Window with no SNPS!
                            counter += K
                            continue

                    ##Check each window 
                    for x in range(0, len(SNPS) ):
                       
                        try:
                            SNP_series = CHR[i][CHR[i][1]==SNPS.values[x]].squeeze()
                            SNP_series = SNP_series[4:]
                        except:
                            pdb.set_trace()
                        ### Get alleles
                        ### If genotype = 0

                        if len(set(SNP_series)) > 2:
                            try:
                                zero, Allele_1, Allele_2 = sorted( set(SNP_series))
                            except:
                                pdb.set_trace()
                        else:
                            Allele_1, Allele_2 = sorted( set(SNP_series))
                  
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
                        if SNP_series.value_counts(Allele_1)[0] <= 0.10 or SNP_series.value_counts(Allele_1)[1] <= 0.10: 
                            ## the dataframe is the dataframe execept the removed SNPs row
                            try:
                                CHR[i] =  CHR[i] [CHR[i][1] != SNPS.values[x]]
                            except:
                                pdb.set_trace()
                        ## Skip windows with fever than 5 SNPs 
                        if len(CHR[i][CHR[i][3].between(counter, counter + K)]) < 5:
                            ## Add K to go to the next window
                            counter += K
                            continue
                        else:
                            window = CHR[i][CHR[i][3].between(counter, counter + K)].sample(n=5)
                            ## Randomly dowsample to 5 SNPs
                           # window_list_of_dict[i][counter] = CHR[i][CHR[i][3].between(counter, counter + K)].sample(n=5)

                                ### Randomly draw haplotypes to look at, dependet on user supplied number of "chr"'
                            ### In practise the smallest sample size
                            for pop in pops:
                                if len(tped_index_dict[pop]) > chr_numb:
                                    haps = random.sample(tped_index_dict[pop][1:],chr_numb)
                                    ## get out the haps
                                    pop_haps = window.iloc[:,np.r_[haps]]
                                    richness = len(pop_haps.T.drop_duplicates())
                                    HH  = calculate_metrics(pop, pop_haps)
                                    HH_dict[pop].append(HH)
                                    richness_dict[pop].append(richness)    

                                else:
                                    haps = tped_index_dict[pop][1:]
                                    ## get out the haps
                                    pop_haps = window.iloc[:,np.r_[haps]]
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
    parser = argparse.ArgumentParser("Takes tped files and calulates haplotype heterozygosity in a given window")
    parser.add_argument("-t", "--tped",
        help="Name of the tped file")
    parser.add_argument("-f", "--tfam",
        help="Name of tfam file")
    parser.add_argument("-n_inds", "--number_of_individuals", default = 10,
        help="Number of individuals to extract from each pop and analyse")
    parser.add_argument("-k", "--window_size", default = 10000,
        help="size of the haplotype window to divide the genome into.")
    parser.add_argument("-o", "--outfile", default = "HH.txt",
        help="Outfile name")

    
    args = parser.parse_args()

    ## The number of allels to look at.
    ## it was called chr in the original Schlebusch 2012 paper
    ## 2 alleles/chr per individual per population
    chr_numb = 2 * int(args.number_of_individuals)
    tped_DF = read_tped(args.tped)
    
    tfam_DF = read_tped(args.tfam)
    nr_ind = len(tfam_DF)
    pops = tfam_DF[0].unique()

    ## Get the FID from tfam in a list
    index_list =  list(tfam_DF[0])
    ## Duplicate each item in the list
    index_list = [val for val in index_list for _ in (0, 1)]
    ### add 4 to the begining of index to corresppnd to tped format
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
    ut_nam = args.outfile
    split_into_haplotypes(tped_DF, int(args.window_size), nr_ind, tped_index_dict, chr_numb, ut_nam)
    
    #with open (args.outfile, "w") as f:
    #    f.write(output_string)
    print("Goodbye!")

