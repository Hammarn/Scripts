#!/usr/bin/env python
import sys
import re
import pdb
import os
import argparse
import plotly
from plotly import tools
import plotly.plotly as py
#import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.io as pio

import numpy as np
from collections import OrderedDict

#plotly.io.orca.config.executable ='/home/richam/miniconda2/envs/master/bin/orca'
pio.orca.config.executable ='/home/richam/miniconda2/envs/master/bin/orca'

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

def plotting(count_dict):
    # Each key is a CHR
    names = ['CEU', 'CDX', 'YRI', 'Khoisan']
    data_dict =  {}
    for key in count_dict:
            data_dict[key] = []
            Source_1 = []
            Source_2 = []
            Source_3 = []
            Source_4 = []
            Pos = [] 
            # Each i is a line in Viterbi-file i.e. a SNP
            for i in range(1,len(count_dict[key])+1):
                Pos.append(i)
                Source_1.append(count_dict[key][i][0])
                Source_2.append(count_dict[key][i][1])
                Source_3.append(count_dict[key][i][2])
                Source_4.append(count_dict[key][i][3])
            #One trace per Source population 
            for i in range(1,5):
                local_vars = vars()
                data_dict[key] = {}
                pdb.set_trace()
                data_dict[key][i] = (go.Scattergl(
                name = names[i-1],
                x = Pos,
                y = local_vars['Source_{}'.format(i)]
                ))

    fig = tools.make_subplots(rows=1, cols=22)
    for chr_num in range(1,23):
        pdb.set_trace()
        fig.append_trace(data_dict[1][chr_num] , 1, chr_num)  
        fig.append_trace(data_dict[2][chr_num] , 1, chr_num)  
        fig.append_trace(data_dict[3][chr_num] , 1, chr_num)  
        fig.append_trace(data_dict[4][chr_num] , 1, chr_num)  

    #layout = dict(showlegend=True)
    #fig = dict(data=data, layout=layout)
    py.iplot(fig, filename='WebGL_line')
    pdb.set_trace()
    pio.write_image(fig, 'fig1.svg')
    py.offline.plot(fig, filename='name.html')
    # Make these be defined on the CL later
    #hist_data = [Source_1, Source_2, Source_3, Source_4]
    #pdb.set_trace()
    #group_labels = ['CEU', 'CDX', 'YRI', 'Khoisan']
    #colors = ['#835AF1', '#7FA6EE', '#B8F7D4'] 
    #layout = go.Layout(barmode='stack')
    #fig = go.Figure(data = hist_data, layout=layout, )
    #py.iplot(fig, filename='Introgression_per_chr_AFR') 
    
    ## Subplots - make one "trace" for each chr?
    #fig = tools.make_subplots(rows=1, cols=2)

    #fig.append_trace(trace1, 1, 1)
    #fig.append_trace(trace2, 1, 2)

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
help="Viterbi output files from RFMix. Needs to contain the substring 'chrxx' where xx is the chromosome number")
    parser.add_argument("-m", "--map", nargs = '+',
help="Map file with genomic positions. Needs to contain the substring 'chrxx' where xx is the chromosome number")


    args = parser.parse_args()
    file_dict =  handle_input_files(args.viterbi) 
    count_dict = {}
    for chr_num in range(1,23): #22 chr
    #chr_num = 1  #22 chr
        print "Reading results for chr {}".format(chr_num)
        count_dict[chr_num] = read_viterbi(file_dict[str(chr_num)])
    plotting(count_dict) 
    print "hej"
