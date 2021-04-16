#!/usr/bin/env python
import argparse
import pandas as pd
import natsort 
import pdb

def read_input(input_file):
    pd_data = pd.read_csv(input_file, sep = "\s+" )
    return pd_data

def clean_input(cleaning_file, output):
    cleaning_file = cleaning_file.dropna()
    #cleaning_file = cleaning_file[cleaning_file["V1"].apply(lambda x: str(x).isdigit())]
    cleaning_file.to_csv(output, mode='a' ,sep = " ", index = False, columns = ["V2","V1", "V3", "V4", "V5", "V6"], header = False, float_format =  "%.0f")


if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Cleans up the SNP file from Mosaic ancestry deconvolution")
    parser.add_argument("-i", "--input", default = 'test.txt',nargs = '+',
    help="Name of inputfile")
    parser.add_argument("-o", "--output", default = 'out_test.txt',
    help="Name of outputfile")


## todo sort the input first


    args = parser.parse_args()
    inputs =  args.input
    inputs = natsort.natsorted(inputs)
    output = args.output 
    datalist = [] 
    for chromosome in inputs:
        datalist.append(read_input(chromosome))


    for item in datalist:
        clean_input(item, args.output)

