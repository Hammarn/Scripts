#!/usr/bin/env python
import argparse
import pandas as pd
import numpy as np
import umap
import warnings
warnings.filterwarnings('ignore')

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column
from bokeh.core.properties import value
from bokeh.palettes import all_palettes
from bokeh.models import Legend, HoverTool, LegendItem
from bokeh.transform import linear_cmap

import pdb

def read_input(input_file):
    in_data = pd.read_csv(input_file, sep = "\s+" )
    return in_data

def do_UMAP(data):
    reducer = umap.UMAP()
    data_NO_index=data.drop(data.columns[[0,1]], axis=1)
    embedding = reducer.fit_transform(data_NO_index)
    return embedding

def plotting(umaped_data, raw_data):
    umaped_df =  pd.DataFrame(data=umaped_data)

    source = pd.concat([raw_data[['FID','IID']], umaped_df], axis=1)
    source.set_index('FID')
    source  = source.rename(columns={0: "x", 1: "y"})
    pdb.set_trace()
    p = figure()
    p.circle(x='x', y='y', source=source, size=10, color='green')
    output_file('UMAP.html')
    show(p)
    return

if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Take PCA eigenvectors from FlasPCA or similar, perform UMAP dimension reduction and plot the result")
    parser.add_argument("-i", "--input", default = 'pcs.txt',
    help="Name of inputfile")

args = parser.parse_args()
data = read_input(args.input)
reduced = do_UMAP(data)
plotting(reduced, data)
