#!/usr/bin/env python
import argparse
import pandas as pd
#import bokeh
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column
from bokeh.core.properties import value
from bokeh.palettes import all_palettes
from bokeh.models import Legend, HoverTool, LegendItem
from bokeh.transform import linear_cmap

import pdb

def read_input(input_file) :
    pd_data = pd.read_csv(input_file, sep = "\s+" )
    return pd_data


def plotting(data, output_name, key, legend):
    output_name = output_name
    key_info = {}
    if key:
        with open(key, 'r') as f:
            for line in f:
                key_info[line.split()[0]] =  " ".join(line.split()[1:])
    
    pops = list(pd.Series.unique(data['FID'])) 
    color =  all_palettes['Inferno'][256] 
    figures=[]
    #make_figure(PCA_1_2, output_name[0], pops, color,data, key_info)
    #make_figure(PCA_1_3, output_name[1], pops, color,data, key_info) 
    figures.append(make_figure(['PC1','PC2'], output_name[1], pops, color,data, key_info, legend ))
    figures.append(make_figure(['PC1','PC3'], output_name[1], pops, color,data, key_info, legend ))
    figures.append(make_figure(['PC2','PC3'], output_name[1], pops, color,data, key_info, legend ))
    figures.append(make_figure(['PC2','PC4'], output_name[1], pops, color,data, key_info, legend ))
    figures.append(make_figure(['PC3','PC4'], output_name[1], pops, color,data, key_info, legend ))
    figures.append(make_figure(['PC3','PC5'], output_name[1], pops, color,data, key_info, legend ))
    figures.append(make_figure(['PC3','PC6'], output_name[1], pops, color,data, key_info, legend ))

    p = column(figures)
   
    show(p)


def make_figure(PCS,output_name, pops, color, data, key_info, nu_legends) :
    nu_legends = nu_legends
    fig = figure(title="PCA", toolbar_location="above", x_axis_label=PCS[0],y_axis_label=PCS[1],plot_width = 1500, plot_height = 1000 ) 
 
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
    ### Iterate, maybe just set one world group to a marker ma manualy and then just do a lookup with iterrows?  or some other     Wolof.bed or some other     
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
        elif value == 'South Asia': 
            return 'diamond_cross'
        elif value == 'Southern Africa':
            return 'inverted_triangle'
        elif value == 'Western Africa':
            return 'x'
        elif value == 'DRC':
            return 'circle_cross'
        elif value == 'wRHG':
            return 'square_cross'
        elif value == 'eRHG':
            return 'diamond'

    ki['marker'] = ki[0].apply(lookup_markers)
    #data['marker'] = data['region'].apply(lookup_markers)
   # for counter, key in enumerate(uniq_regions):
   #     key_info[key] = "{} {}".format(key_info[key], markers[counter])
    ki = ki.sort_values(0)
    ki_re = ki.reset_index()
    ki_re = ki_re.rename(columns={'index':'FID', 0:'Region'})
    data = pd.merge(data, ki_re, on = ['FID'])
    if nu_legends == '2':
        nu_legends=2
    ### 2 legends
    if nu_legends == 2:
        pdb.set_trace()
        for counter,pop in enumerate(ki.index.values):
            if counter < lenght_of_leg:
                
                leg_1.append( ( pop , [eval("fig.{}".format( ki['marker'][pop]))(x = PCS[0], y = PCS[1], color =color[colour_counter], size = 8, source = data.loc[data['FID'] == pop] ,  muted_alpha=0.2)])) 
            else:
                try:
                        leg_2.append( ( pop , [eval("fig.{}".format(ki['marker'][pop]))(x = PCS[0], y = PCS[1], color =color[colour_counter], size = 8, source = data.loc[data['FID'] == pop] ,  muted_alpha=0.2)])) 
                except:
                    pdb.set_trace()
                    print pop
            colour_counter += 2

        legend1 = Legend(items=leg_1, location = (20, 20))
        legend2 = Legend(items=leg_2, location = (25,20))
        fig.add_layout(legend1, 'left')
        fig.add_layout(legend2, 'left')
        fig.legend.label_text_font_size = '10pt' 
    
    ## 1 legend, based on Region
    
    if nu_legends == 1:
        for counter,region in enumerate(set(ki[0].values)):
            try:
                leg_1.append( ( region , [eval("fig.{}".format(data[['Region','marker']].drop_duplicates().loc[data['Region']==region].values[0].item(1) ))(x = PCS[0], y = PCS[1], color =color[colour_counter], size = 8, source = data.loc[data['Region'] == region] ,  muted_alpha=0.2)])) 
            except:
                pdb.set_trace()
                print pop
            colour_counter += 20 
        legend1 = Legend(items=leg_1, location = (0, 400))
        fig.add_layout(legend1, 'left')
    
        fig.legend.label_text_font_size = '20pt' 
    
    
    fig.legend.click_policy="mute"
    fig.add_tools(HoverTool(
        tooltips = [
            ('Population', '@FID'),
            ('Region', '@Region'),
                ]
            ))
    
    output_file(output_name)
    
    return(fig)
    #show(fig, browser = "firefox")

if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Make a scatter plot of Principal component analysis output form FlashPCA")
    parser.add_argument("-i", "--input", default = 'pcs.txt',
    help="Name of inputfile")
    parser.add_argument("-k", "--key",
    help="File with Population legend key")
    parser.add_argument("-o","--output", default = ["PCA1_vs_PCA2.html","PCA_plots.html"],
    help=  "Filename for the outputfile")
    parser.add_argument("-l","--legend", default = 1,
    help=  "Display 1 legend with Regions or 2 with Pops")

    args = parser.parse_args()

    data = read_input(args.input)

    plotting(data, args.output, args.key, args.legend)
