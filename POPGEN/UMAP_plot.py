#!/usr/bin/env python
import argparse
import pandas as pd
import numpy as np
import umap
import warnings
import sys
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

def plotting(umaped_data, raw_data, output, key_file):
    key=key_file
    print "Building plot"
    umaped_df =  pd.DataFrame(data=umaped_data)

    source = pd.concat([raw_data[['FID','IID']], umaped_df], axis=1)
    source.set_index('FID')
    source  = source.rename(columns={0: "x", 1: "y"})
    p = figure(title="UMAP of first 10 PCs", toolbar_location="above", x_axis_label="UMAP 1",y_axis_label="UMAP 2",plot_width = 1500, plot_height = 1000)
    
    fids = source.FID.unique()
    lenght_of_leg = len(fids)/2
    colours = inferno(len(fids))
    leg_1 = []
    leg_2 = [] 
    if key:
        key_info = {}
        try:
            with open(key, 'r') as f:
                for line in f:
                    key_info[line.split()[0]] =  " ".join(line.split()[1:]) 
        except  IOError:
            print "Could not open the file '{}'".format(key)
            sys.exit()

        regions = set(key_info.values())
        colours = inferno(len(regions))
        
        ki= (pd.Series(key_info)).to_frame()
        ki = ki.sort_values(0)
        ki_re = ki.reset_index()
        ki_re = ki_re.rename(columns={'index':'FID', 0:'Region'})
        source = pd.merge(source, ki_re, on = ['FID'])

        
        for counter,region in enumerate(regions):
            ## Legend takes "Text to print", figure object
            ##todo make a list/DF with pops for each region so that can be used below:
            leg_1.append(( region, [p.circle(x='x', y='y', source=source.loc[source['Region'] == region ], size=9, color=colours[counter], muted_alpha=0.2 ) ] ))
        legend1 = Legend(items=leg_1, location = (0, 400))
        p.add_layout(legend1, 'left')
        p.legend.label_text_font_size = '18pt'
    
    
    else:
        for counter,pop in enumerate(fids):
            ## Legend takes "Text to print", figure object.
            ## This is here being parsed through a list. Makes it easy to add additional legends later if I want to
             if counter < lenght_of_leg:
                leg_1.append(( pop, [p.circle(x='x', y='y', source=source.loc[source['FID'] == pop], size=6, color=colours[counter], muted_alpha=0.2 ) ] ))
   
             else:
                leg_2.append(( pop, [p.circle(x='x', y='y', source=source.loc[source['FID'] == pop], size=6, color=colours[counter], muted_alpha=0.2 ) ] ))

        legend1 = Legend(items=leg_1, location = (20, 20))
        legend2 = Legend(items=leg_2, location = (25,20))
        p.add_layout(legend1, 'left')
        p.add_layout(legend2, 'left')
        p.legend.label_text_font_size = '10pt' 

    p.legend.click_policy="mute"
    p.add_tools(HoverTool(
     tooltips = [
         ('Population', '@FID'),
         ('Region', '@Region'),
         ('Individual', '@IID'),
             ]
         ))
    
    
    outfile=output
    print "Saving output to {}.html".format(outfile) 
    output_file('{}.html'.format(outfile))
   
    show(p)
    return

if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Take PCA eigenvectors from FlashPCA or similar, perform UMAP dimension reduction and plot the result")
    parser.add_argument("-i", "--input", default = 'pcs.txt',
    help="Name of inputfile")
    parser.add_argument("-o", "--output", default = 'UMAP',
    help="Name of outputfile")
    parser.add_argument("-k", "--key",
    help="File with Population legend key")


args = parser.parse_args()
data = read_input(args.input)
reduced = do_UMAP(data)
plotting(reduced, data, args.output, args.key)
