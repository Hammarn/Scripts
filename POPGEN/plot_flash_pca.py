#!/usr/bin/env python
import argparse
import pandas as pd
#import bokeh
from bokeh.plotting import figure, show, output_file
from bokeh.core.properties import value
from bokeh.palettes import all_palettes
from bokeh.models import Legend, HoverTool, LegendItem
from bokeh.transform import linear_cmap
#from bokeh.models import ColumnDataSource
import pdb

def read_input(input_file) :
    pd_data = pd.read_csv(input_file, sep = "\s+" )
    return pd_data


def plotting(data, output_name):
    output_name = output_name
    #data = ColumnDataSource(data)
    pops = list(pd.Series.unique(data['FID'])) 
    color =  all_palettes['Inferno'][256] 
    #mapper = linear_cmap(field_name = pops, palette = all_palettes['Inferno'][256] )
    markers = ["circle / o","square","triangle","asterisk / *","circle_x / ox","square_x","inverted_triangle","x","circle_cross / o+","square_cross","diamond","cross / +"]
    #marker_dict = {}
    #for i in range(pops):
    #    for j in range(i):
    #        marker_dict[j]=markers[j]
    #    i += 12
    PCA_1_2 = ['PC1','PC2']
    PCA_3_4 = ['PC3','PC4']
    make_figure(PCA_1_2, output_name[0], pops, color, data)
    make_figure(PCA_3_4, output_name[1], pops, color,data) 

def make_figure(PCS,output_name, pops, color, data) :
    fig = figure(title="PCA", toolbar_location=None, x_axis_label=PCS[0],y_axis_label=PCS[1],plot_width = 1000, plot_height = 1000 ) 
    #for counter,pop in enumerate(pops):
    colour_counter = 0
    leg_1 = []
    leg_2 = []
    lenght_of_leg = len(pops)/2
    two_columns = True
    

    #pdb.set_trace()
    for counter,pop in enumerate(pops):
    #    data.loc[data['FID'] == pop]
        if two_columns == True:
            if counter < lenght_of_leg: 
    #            pdb.set_trace()
                leg_1.append( ( pop , [fig.circle(x = PCS[0], y = PCS[1], color =color[colour_counter], source = data.loc[data['FID'] == pop] ,  muted_alpha=0.2)])) 
            else:
                leg_2.append( ( pop , [fig.circle(x = PCS[0], y = PCS[1], color =color[colour_counter], source = data.loc[data['FID'] == pop] ,  muted_alpha=0.2)])) 
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
    parser = argparse.ArgumentParser("Make a scatter plot of FPKM counts between conditions")
    parser.add_argument("-i", "--input", default = 'pcs.txt',
    help="Plots PCA from flashca")

    parser.add_argument("-o","--output", default = ["PCA1_vs_PCA2.html","PCA1_vs_PCA2.html"],
    help=  "Filename for the outputfile")
    


args = parser.parse_args()

data = read_input(args.input)
plotting(data, args.output)
