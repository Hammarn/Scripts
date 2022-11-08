#!/usr/bin/env python3
import pandas as pd
import argparse
import sys
import re
import sys

import pdb

pd.options.mode.chained_assignment = None

__author__ = "Rickard Hammarén @hammarn"

def read_annotation(in_file):
    in_file = in_file
    T_DF = pd.read_csv(in_file, delimiter="\t",  index_col = 0)
    return T_DF


def read_birdseed(in_file):
    in_file = in_file
    T_DF = pd.read_csv(in_file, delimiter=",",  index_col = 0)
    return T_DF


def find_genotype(genotype, ALLELE_A, ALLELE_B):
    return_genotype = ""
    try:
        for allele in genotype:
            if allele == "A":
                return_genotype = return_genotype + " " + ALLELE_A
            elif allele == "B":
                return_genotype = return_genotype + " " + ALLELE_B
    except TypeError:
        ## An empty genotype will throw a typeerror:
        ### As far as I can tell the Bordseed format will have either
        ### Both genotypes or none, never one present and one missing
        return_genotype = return_genotype + "00"


    return (return_genotype)

def replace(row, annotation):
    ALLELE_A = ""
    ALLELE_B = ""
   #Use the index of the row which is name in a lambda to get out the genoptype from the annotation file
    try:
        ALLELE_A =  annotation.loc[row.name]["Allele_A"]
        ALLELE_B =  annotation.loc[row.name]["Allele_B"]
    except KeyError:
        print("Could not find {} in annotation file".format(row.name))

    for i, item in enumerate(row):
         
        # updating the value of the row
        row[i] = find_genotype(item,ALLELE_A, ALLELE_B)
    return row

def main(arguments):
    annotation = read_annotation(arguments.annotation)

    bird = read_birdseed( arguments.birdseed)
   
    ## Tped format
    ## Chromosome dbSNP 0 Physical_Position genotypes seperated by space

    bird = bird.apply(lambda row : replace(row,annotation), axis = 1)
    ny = bird.merge(annotation[["Chromosome", "dbSNP", "Physical_Position"]], left_index = True, right_index = True)
    cols = list(ny.columns.values)
    # Move three last to first
    cols = cols[-3:] + cols[:-3]

    ny = ny[cols]
    #Inser the centimorgan field in the correct infromation (missing)
    ny.insert(2, 'cM', 0)
    ny.to_csv("{}.tped".format(arguments.output_name), index = False, header = False, sep = " ")


    print("Output tped file saved to {}.tped".format(arguments.output_name))





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
    
    parser.add_argument("-o", "--output_name", 
    help= "Base name (prefix) of the final outputfile")

    args = parser.parse_args()

    main(args)
