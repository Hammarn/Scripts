#!/usr/bin/env python
import sys
import re
import pdb
import os
import argparse
import pandas as pd 
import numpy as np

from math import pi

from collections import OrderedDict
from bokeh.models import Axis,Range1d
from bokeh.layouts import row, gridplot
from bokeh.io import  export_svgs, export_png, show, output_file 
from bokeh.plotting import figure, save
from bokeh.palettes import Spectral5
#from bokeh.sampledata.autompg import autompg_clean as df


def handle_input_files(files):
    # Figure out which chr we are working with and return them in order
    chr_pat = re.compile('chr\d+')
    chr_nm_pat = re.compile('\d+')
    file_dict = {}
    for f in files:
        full_name =  os.path.abspath(f)
        chr_plus_nm = chr_pat.search(f).group(0)
        chr_nm = chr_nm_pat.search(chr_plus_nm).group(0)
        file_dict[chr_nm] = full_name
    return file_dict


def read_viterbi(viterbi_file):
    viterbi = viterbi_file
    chr_dict = OrderedDict()
    counter=0
    with open (viterbi, 'r') as f:
        for line in f:
            ## Count occurence of each source population per line. 
            one = line.count('1')
            two = line.count('2')
            three = line.count('3')
            four = line.count('4')
            #five = line.count('5')
            #six = line.count('6')
            counter +=1
            sum_nu = sum((one,two,three,four))
            chr_dict[counter]=[one/float(sum_nu),two/float(sum_nu),three/float(sum_nu),four/float(sum_nu)]
    
    return chr_dict


def read_genetic_bim(bim_file):
    bim = bim_file 
    position_dict = OrderedDict()
    with open (bim, 'r') as f:
        for counter,line in enumerate(f, start = 1):
            position_dict[counter] = line.split("\t")[3]
            
    return position_dict

def filter_away_telemomers(count_dict, bp_dict):
    """
    takes in viterbi counts and genmic position in bps and return filtered counts
    """
    #2 Mbp
    filter_value = 2000000
    for vit_num in range(1,23):
        items  = count_dict[vit_num]
        items_to_keep = []    
        
        first =  int(bp_dict[vit_num][1]) 
        first = first + filter_value
        
        last = int(bp_dict[vit_num].items()[-1][1]) 
        last = last - filter_value
                
        
        ##print "{}".format(len(count_dict[vit_num])) 
        ## pop instead of making a new library
    #    print "Filtering away telomeric regions for chr {} this could take a while".format(vit_num) 
        for key in bp_dict[vit_num].keys():
          #  pdb.set_trace()
            if int(bp_dict[vit_num][key]) < first or int(bp_dict[vit_num][key])  > last:
                try:
                    count_dict[vit_num].pop(key)
                except KeyError:
                    continue
    return count_dict



### replace with counts dict??
    return count_dict

def plotting(count_dict, bp_dict):
    count_dict = count_dict
    bp_dict = bp_dict
    # Each key is a CHR
    names = ['CEU', 'CDX', 'YRI', 'Khoisan']
    data_dict =  {}
    counter = 0 
    for key in count_dict.keys():
            data_dict[key] = []
            CEU = []
            CDX = []
            YRI = []
            Khoisan = []
            Pos = [] 
            # Each i is a line in Viterbi-file i.e. a SNP

            for i in count_dict[key].keys():
                CEU.append(count_dict[key][i][0])
                CDX.append(count_dict[key][i][1])
                YRI.append(count_dict[key][i][2])
                Khoisan.append(count_dict[key][i][3])
                Pos.append(bp_dict[key][i])
                bp_dict[key]

            data_dict[key] = {'CEU' : pd.Series(CEU, index = Pos),
                'CDX' : pd.Series(CDX, index = Pos),
                'YRI' : pd.Series(YRI, index = Pos),
                'Khoisan' : pd.Series(Khoisan, index = Pos),
                 }#'Chromosome' : key }
            data_dict[key] = pd.DataFrame(data_dict[key])    
### Actual plotting here
    data =  pd.concat([data_dict[key] for key in  data_dict.keys()])
    #p.xaxis.axis_label = 'Genomic position'
    #p.yaxis.axis_label = 'Genome proportion'
    
    def subplot():
        ## Make sure we are accessing the chromosomes in the correct order
        for key in range(1,23):
            print "Building subplot {}".format(key)
            local_vars = vars()
            local_vars['p{}'.format(key)] = figure(plot_height=500, plot_width=500, output_backend="webgl", title="Chromosome {}".format(key) )
            local_vars['p{}'.format(key)].circle(x = data_dict[key].index.values, y = data_dict[key]['CEU'], color = "grey", legend = 'CEU'  )
            local_vars['p{}'.format(key)].circle(x = data_dict[key].index.values, y = data_dict[key]['CDX'], color = "skyblue", legend = 'CDX'  )
            local_vars['p{}'.format(key)].circle(x = data_dict[key].index.values, y = data_dict[key]['YRI'], color = "goldenrod", legend = 'YRI'  )
            local_vars['p{}'.format(key)].circle(x = data_dict[key].index.values, y = data_dict[key]['Khoisan'], color = "salmon", legend = 'Khoisan'  )
            local_vars['p{}'.format(key)].xaxis.major_label_orientation = "vertical"
            local_vars['p{}'.format(key)].xaxis[0].formatter.use_scientific = False
            local_vars['p{}'.format(key)].xaxis[0].ticker = [int(data_dict[key].first_valid_index()) ,int(data_dict[key].last_valid_index())]
            local_vars['p{}'.format(key)].x_range = Range1d(int(data_dict[key].first_valid_index()) ,int(data_dict[key].last_valid_index()))
            
            output_file("Rf_chr{}.html".format(key))
            save(local_vars['p{}'.format(key)])
            #local_vars['p{}'.format(key)].x_range = Range1d(int(data_dict[key].idxmin()[0]), int(data_dict[key].idxmax()[0]))
            #loical_vars['p{}'.format(key)].x_range = Range1d(2000000, int(data_dict[key].idxmax()[0]))
                
        
        plot_list = [local_vars['p{}'.format(i)] for i in data_dict.keys()]
        #Make one figure out of the 22 subplots
        
        p = row(plot_list)
       
         
        p.add_tools(HoverTool(
        tooltips=[
            ( 'date',   '@date{%F}'            ),
            ( 'close',  '$@{adj close}{%0.2f}' ), # use @{ } for field names with spaces
            ( 'volume', '@volume{0.00 a}'      ),
        ],

        formatters={
            'date'      : 'datetime', # use 'datetime' formatter for 'date' field
            'adj close' : 'printf',   # use 'printf' formatter for 'adj close' field
                                      # use default 'numeral' formatter for other fields
        },

        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
        )) 





        output_file("Rfmix_introgression.html")
        print "Saving to output - this could take a while.."
        save(p)
    
    subplot()
    

    #export_svgs(p, filename="Rfmix_intro.svg")
    #export_png(p, filename="Rfmix_intro.png", webdriver=self.webdriver)


def smooth_line_data(data, numpoints, sumcounts=True):
    """
    Stolen from MultiQC
    Function to take an x-y dataset and use binning to
    smooth to a maximum number of datapoints.
    """
    smoothed = {}
    for s_name, d in data.items():

        # Check that we need to smooth this data
        if len(d) <= numpoints:
            smoothed[s_name] = d
            continue

        smoothed[s_name] = OrderedDict();
        p = 0
        binsize = len(d) / numpoints
        if binsize < 1:
            binsize = 1
        binvals = []
        for x in sorted(d):
            y = d[x]
            if p < binsize:
                binvals.append(y)
                p += 1
            else:
                if sumcounts is True:
                    v = sum(binvals)
                else:
                    v = sum(binvals) / binsize
                smoothed[s_name][x] = v
                p = 0
                binvals = []
    return smoothed



if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Make a scatter plot of FPKM counts between conditions")
    parser.add_argument("-v", "--viterbi", nargs = '+',
help="Viterbi output files from RFMix. Needs to contain the substring 'chrxx' where xx is the chromosome number in the filename")
    parser.add_argument("-b", "--bim", nargs = '+',
help="Bim file with genomic positions. Needs to contain the substring 'chrxx' where xx is the chromosome number in the filename")


    args = parser.parse_args()
    viterbi_dict =  handle_input_files(args.viterbi) 
    bim_dict = handle_input_files(args.bim)
    
    count_dict = OrderedDict()
    for chr_num in range(1,23): #22 chr
    #chr_num = 1  #22 chr
        print "Reading results for chr {}".format(chr_num)
        count_dict[chr_num] = read_viterbi(viterbi_dict[str(chr_num)])
    
    bp_dict = OrderedDict()
    for chr_num in range(1,23): #22 chr
    #chr_num = 1  #22 chr
        print "Reading results for chr {}".format(chr_num)
        bp_dict[chr_num] = read_genetic_bim(bim_dict[str(chr_num)])
    
    count_dict  =  filter_away_telemomers(count_dict, bp_dict) 
    
    plotting(count_dict, bp_dict) 
    print "Goodbye"
