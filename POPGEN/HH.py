#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
import os
import random
import pandas as pd

from datetime import datetime
from collections import OrderedDict

import pdb
__author__ = "Rickard Hammarén @hammarn"


def read_tped(tped):
    tped = tped
    T_DF = pd.read_csv(tped, delimiter=" ", header = None)
    #remove trailing whitespace, a bit crude though
    T_DF= T_DF.dropna(how="any", axis='columns')
    return T_DF


def split_into_haplotypes(tped_D, K, N, tped_index_dict, chr_numb):
    ###   CHR SNP_NAME BLAJ SNP_POS 
    ###   0       1    2         3
    
    num_individuals = N
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
       #except:
        #   pdb.set:trace()
         #  print("hej")
   
    window_list_of_dict = []
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)


### Loop through and add K to start

    for i in range(0,len(CHR)):
        window_dict = {}
        ### start at start
        counter =  len_dict[i][0]
        
        ## Each trip through the loop is one genetic window, defined in size by K
        while counter < len_dict[i][2]:
            
            
            ### remove SNPs in the window with MAF < 10 %
            ## get the SNPs in the winow:
            SNPS = CHR[i][CHR[i][3].between(counter, counter + K)][1]

            ##Check if the range is e

            for x in range(0, len(SNPS) ):
               
                try:
                    SNP_series= CHR[i][CHR[i][1]==SNPS.values[x]].squeeze()
                    SNP_series = SNP_series[4:]
                    pdb.set_trace()
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
                ## Remove the row is MAF <= 10%
                if SNP_series.value_counts(Allele_1)[0] or SNP_series.value_counts(Allele_1)[1] <= 0.10:
                    ## the dataframe is the dataframe execept the removed SNPs row
                    try:
                        CHR[i] =  CHR[i] [CHR[i][1] != SNPS.values[x]]
                    except:
                        pdb.set_trace()
            ## Skip windows with fever than 5 SNPs 
            if len(CHR[i][CHR[i][3].between(counter, counter + K)]) < 5:
                counter += K
                continue
            else:
                ## Randomly dowsample to 5 SNPs
                window_dict[counter] = CHR[i][CHR[i][3].between(counter, counter + K)].sample(n=5)
                counter += K
        window_list_of_dict.append(window_dict)

    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    pdb.set_trace()
    ## chr_numb is the number of alleles to keep/extract from each pop.
    

    print("End of split")
    

### Get only one pop from tfam:
# tfam_DF[tfam_DF[0]=="YRI"]

    pops = tfam_DF[0].unique()

    ## need to find out each POPS order in the tped
    ##  it is from the order of the tfam
    ## but transposed 

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
            
            #tped_index_dict[pop] = []
            tped_index_dict[pop] = [index]
        ## Just add all indices, we can get the stop with [-1] later
        tped_index_dict[pop].append(index)
        #if pop != last_pop:
        #    tped_index_dict[pop].append(index)

    pdb.set_trace()
    split_into_haplotypes(tped_DF, args.window_size, nr_ind, tped_index_dict, chr_numb)
    
    print("Goodbye!")

