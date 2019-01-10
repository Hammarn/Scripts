#!/usr/bin/env python
import pandas as pd
import bokeh

def read_input(input_file):
    pd_data = pd.read_csv(input_file, sep = "\s+" )
    return pd_data


if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Make a scatter plot of FPKM counts between conditions")
    parser.add_argument("-i", "--input", default = 'pca.txt',
help="Output pca.txt file from flashpca")


args = parser.parse_args()
data = read_input(args.input)
