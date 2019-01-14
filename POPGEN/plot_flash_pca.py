#!/usr/bin/env python
import argparse
import pandas as pd
#import bokeh
from bokeh.plotting import figure, show, output_file
from bokeh.core.properties import value
from bokeh.palettes import all_palettes
from bokeh.models import Legend, HoverTool
#from bokeh.models import ColumnDataSource
import pdb

def read_input(input_file):
    pd_data = pd.read_csv(input_file, sep = "\s+" )
    return pd_data


def plotting(data):
    #data = ColumnDataSource(data)
    pops = list(pd.Series.unique(data['FID'])) 
    color =  all_palettes['Inferno'][256] 

    fig = figure(title="PCA", toolbar_location=None, x_axis_label='PCA 1',y_axis_label='PCA 2',) 
    #for counter,pop in enumerate(pops):
    counter = 0
    for pop in pops:
    #    data.loc[data['FID'] == pop]
        fig.circle(x = 'PC1', y = 'PC2', legend = 'FID' ,color =color[counter],   source = data.loc[data['FID'] == pop] ,  muted_alpha=0.2)    
        counter += 2 
    fig.legend.label_text_font_size = "8px" 
    fig.legend.click_policy="mute"
    fig.add_tools(HoverTool(
        tooltips = [
            ('Population', '@FID'),
                ]
            ))
    show(fig, browser = "firefox")
if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Make a scatter plot of FPKM counts between conditions")
    parser.add_argument("-i", "--input", default = 'pcs.txt',
help="Plots PCA from flashca")

args = parser.parse_args()
data = read_input(args.input)
plotting(data)
