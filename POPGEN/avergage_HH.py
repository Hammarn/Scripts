#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
import os
import random
import functools
import pandas as pd
import numpy as np

from datetime import datetime
from collections import OrderedDict
from collections import Counter
from statistics import mean

import pdb
__author__ = "Rickard Hammarén @hammarn"

def read_HH(input_file):
    """
    Takes the HH file object and returns a pandas dataframe
    """
    df =  pd.read_csv(input_file, delimiter="\t", header = None)
    return df

def find_S_from_filename(files):
    S_pat = re.compile('\d+')
    
    file_dict = {}
    for f in files:
        S = S_pat.search(f).group(0)
        file_dict[int(S)] = read_HH(f)
    return file_dict

def average_d(HH_dict):
    # Chr avg. HH_dict[93000].groupby([0,1]).mean()
    for key in HH_dict.keys():
        HH_dict[key] = HH_dict[key].groupby(1).mean()
        HH_dict[key]["S"] = key 
    merged_DF = pd.concat(HH_dict.values())
     #                                        how='outer'), data_frames)
    return merged_DF



if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Takes the output from the HH script and averages each run and returns one file with all results")
    parser.add_argument("-i", "--input", nargs = "+",
        help="A list of the outputfiles from HH.py to use as input")
    parser.add_argument("-o", "--outfile", default = "HH.txt",
        help="Outfile name")

    args = parser.parse_args()

    HH_files = args.input
    HH_dict = find_S_from_filename( HH_files )
    merged_DF =  average_d( HH_dict)
   # df.to_csv(r'Path where you want to store the exported CSV file\File Name.csv', index = False)
    cwd = os.getcwd()
    path = cwd + "/" + args.outfile
    merged_DF.to_csv(path, header = False)

