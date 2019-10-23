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
from bokeh.palettes import inferno

import pdb

def read_input(input_file):
    print "Reading data.."
    in_data = pd.read_csv(input_file, sep = "\s+" )
    return in_data

def do_UMAP(data):
    print "Performing dimensionality reduction"
    reducer = umap.UMAP()
    data_NO_index=data.drop(data.columns[[0,1]], axis=1)
    embedding = reducer.fit_transform(data_NO_index)
    return embedding

def plotting(umaped_data, raw_data, output):
    print "Building plot"
    umaped_df =  pd.DataFrame(data=umaped_data)

    source = pd.concat([raw_data[['FID','IID']], umaped_df], axis=1)
    source.set_index('FID')
    source  = source.rename(columns={0: "x", 1: "y"})
    #pdb.set_trace()
    p = figure(title="UMAP of first 10 PCs", toolbar_location="above", x_axis_label="UMAP 1",y_axis_label="UMAP 2",plot_width = 1500, plot_height = 1000)
    
    fids = source.FID.unique()
    colours = inferno(len(fids))
    leg_1 = []
    for counter,pop in enumerate(fids):
           
        ## Legend takes "Text to print", figure object.
        ## This is here being parsed through a list. Makes it easy to add additional legends later if I want to
        leg_1.append(( pop, [p.circle(x='x', y='y', source=source.loc[source['FID'] == pop], size=6, color=colours[counter], muted_alpha=0.2 ) ] ))
    
    legend1 = Legend(items=leg_1)#, location = (20, 20))
    p.add_layout(legend1, 'left') 

    #data.loc[data['Region'] == region]
   

    p.legend.click_policy="mute"
    p.add_tools(HoverTool(
     tooltips = [
         ('Population', '@FID'),
             ]
         ))
    
    
    outfile=output
    print "Saving output to {}.html".format(outfile) 
    output_file('{}.html'.format(outfile))
   
    show(p)
    return

if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Take PCA eigenvectors from FlasPCA or similar, perform UMAP dimension reduction and plot the result")
    parser.add_argument("-i", "--input", default = 'pcs.txt',
    help="Name of inputfile")
    parser.add_argument("-o", "--output", default = 'UMAP',
    help="Name of outputfile")

args = parser.parse_args()
data = read_input(args.input)
reduced = do_UMAP(data)
plotting(reduced, data, args.output)
