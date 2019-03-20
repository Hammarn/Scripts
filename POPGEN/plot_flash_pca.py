#!/usr/bin/env python
import argparse
import pandas as pd
#import bokeh
from bokeh.plotting import figure, show, output_file
from bokeh.core.properties import value
from bokeh.palettes import all_palettes
from bokeh.models import Legend, HoverTool, LegendItem
from bokeh.transform import linear_cmap

import pdb

def read_input(input_file) :
    pd_data = pd.read_csv(input_file, sep = "\s+" )
    return pd_data


def plotting(data, output_name, key):
    output_name = output_name
    key_info = {}
    if key:
        with open(key, 'r') as f:
            for line in f:
                key_info[line.split()[0]] =  " ".join(line.split()[1:])
    
    pops = list(pd.Series.unique(data['FID'])) 
    color =  all_palettes['Inferno'][256] 
    PCA_1_2 = ['PC1','PC2']
    PCA_1_3 = ['PC1','PC3']
    PCA_3_4 = ['PC3','PC4']
    make_figure(PCA_1_2, output_name[0], pops, color,data, key_info)
    make_figure(PCA_1_3, output_name[1], pops, color,data, key_info) 
    make_figure(PCA_3_4, output_name[1], pops, color,data, key_info) 

def make_figure(PCS,output_name, pops, color, data, key_info) :
    fig = figure(title="PCA", toolbar_location=None, x_axis_label=PCS[0],y_axis_label=PCS[1],plot_width = 1000, plot_height = 1000 ) 
    if key_info: 
        uniq_regions = set(key_info.values()) 
        numer_of_regions = len(uniq_regions)
        uniq_regions = list(uniq_regions)
    
    colour_counter = 0
    leg_1 = []
    leg_2 = []
    lenght_of_leg = len(pops)/2
    two_columns = True
    

    markers = ["circle","square","triangle","asterisk","circle_x","square_x","inverted_triangle","x","circle_cross","square_cross","diamond","cross"]
### use dataframe instead of dict for storing the key info:
### YRI|"West Africa"|circle|color_num
    ### Iterate, maybe just set one world group to a marker ma manualy and then just do a lookup with iterrows? or some other     
    ki= (pd.Series(key_info)).to_frame()
    
    def lookup_markers(value):
        if value == 'East Asia':
            return 'circle'
        elif value == 'Eastern Africa':
            return 'square'
        elif value == 'Europe':
            return "triangle"
        elif value == 'Middle East':
            return "asterisk"
        elif value == 'Northern Africa':
            return 'circle_x'
        elif value == 'South East Asia':
            return 'square_x'
        elif value == 'Southern Africa':
            return 'inverted_triangle'
        elif value == 'Western Africa':
            return 'x'

    pdb.set_trace()
    ki['marker'] = ki[0].apply(lookup_markers)
    
    for counter, key in enumerate(uniq_regions):
        key_info[key] = "{} {}".format(key_info[key], markers[counter])
             
    for counter,pop in enumerate(pops):
     
        if counter < lenght_of_leg: 
            pdb.set_trace()
            leg_1.append( ( pop , [eval("fig.{}".format(key_info[pop].split()[-1]))(x = PCS[0], y = PCS[1], color =color[colour_counter], source = data.loc[data['FID'] == pop] ,  muted_alpha=0.2)])) 
        else:
            leg_2.append( ( pop , [eval("fig.{}".format(key_info[pop].split()[-1]))(x = PCS[0], y = PCS[1], color =color[colour_counter], source = data.loc[data['FID'] == pop] ,  muted_alpha=0.2)])) 
    colour_counter += 2

    legend1 = Legend(items=leg_1, location = (20, 20))
    legend2 = Legend(items=leg_2, location = (25,20))
    
    fig.add_layout(legend1, 'left')
    fig.add_layout(legend2, 'left')
    fig.legend.label_text_font_size = "8px" 
    fig.legend.click_policy="mute"
    
    fig.add_tools(HoverTool(
        tooltips = [
            ('Population', '@FID'),
                ]
            ))
    
    output_file(output_name)
    show(fig, browser = "firefox")

if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Make a scatter plot of Principal component analysis output form FlashPCA")
    parser.add_argument("-i", "--input", default = 'pcs.txt',
    help="Name of inputfile")
    parser.add_argument("-k", "--key",
    help="File with Population legend key")
    parser.add_argument("-o","--output", default = ["PCA1_vs_PCA2.html","PCA1_vs_PCA2.html"],
    help=  "Filename for the outputfile")
    

args = parser.parse_args()

data = read_input(args.input)
plotting(data, args.output, args.key)
