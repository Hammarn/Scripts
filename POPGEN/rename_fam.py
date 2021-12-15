#!/usr/bin/env python
import argparse
import pandas as pd

def read_input(input_file) :
    pd_data = pd.read_csv(input_file, sep = "\s+" )
    return pd_data



if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Make a scatter plot of Principal component analysis output form FlashPCA")
    parser.add_argument("-i", "--input",
    help="Name of inputfile")

    args = parser.parse_args()

    data = read_input(args.input)
