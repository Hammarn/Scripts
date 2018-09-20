#!/usr/bin/env python
import sys
import re
import pdb
import os
import argparse
import pandas as pd 
import numpy as np
from collections import OrderedDict
from bokeh.layouts import row, gridplot
from bokeh.io import  export_svgs, export_png, show, output_file 
from bokeh.plotting import figure, save
from bokeh.palettes import Spectral5
#from bokeh.sampledata.autompg import autompg_clean as df
from bokeh.transform import factor_cmap
from selenium import webdriver


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
    for key in count_dict.keys():
            data_dict[key] = []
            CEU = []
            CDX = []
            YRI = []
            Khoisan = []
            Pos = [] 
            # Each i is a line in Viterbi-file i.e. a SNP
            for i in range(1,len(count_dict[key])+1):
                Pos.append(i)
                CEU.append(count_dict[key][i][0])
                CDX.append(count_dict[key][i][1])
                YRI.append(count_dict[key][i][2])
                Khoisan.append(count_dict[key][i][3])
             
            data_dict[key] = {'CEU' : pd.Series(CEU, index = Pos),
                'CDX' : pd.Series(CDX, index = Pos),
                'YRI' : pd.Series(YRI, index = Pos),
                'Khoisan' : pd.Series(Khoisan, index = Pos),
                'Chromosome' : key }
            
            data_dict[key] = pd.DataFrame(data_dict[key])    

### Actual plotting here
    data =  pd.concat([data_dict[key] for key in  data_dict.keys()])
    #p = figure(title="Genome average introgression", output_backend="webgl")
    #p.xaxis.axis_label = 'Genomic position'
    #p.yaxis.axis_label = 'Genome proportion'
    #key=1 
    

    ## Make sure we are accessing the chromosomes in the correct order
    for key in range(1,23):
        print "Buildind subplot {}".format(key)
        local_vars = vars()
        local_vars['p{}'.format(key)] = figure(plot_height=500, plot_width=500, output_backend="webgl", title="Chromosome {}".format(key) )
        local_vars['p{}'.format(key)].circle(x = data_dict[key].index.values, y = data_dict[key]['CEU'], color = "grey", legend = 'CEU'  )
        local_vars['p{}'.format(key)].circle(x = data_dict[key].index.values, y = data_dict[key]['CDX'], color = "skyblue", legend = 'CDX'  )
        local_vars['p{}'.format(key)].circle(x = data_dict[key].index.values, y = data_dict[key]['YRI'], color = "goldenrod", legend = 'YRI'  )
        local_vars['p{}'.format(key)].circle(x = data_dict[key].index.values, y = data_dict[key]['Khoisan'], color = "salmon", legend = 'Khoisan'  )
    plot_list = [local_vars['p{}'.format(i)] for i in data_dict.keys()]
    #Make one figure out of the 22 subplots
    p = row(plot_list)

    #Selenium stuff
    #options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    #webdriver = webdriver.Chrome(chrome_options=options)
    #self.webdriver = webdriver.Chrome(executable_path=find_executable('chromedriver'),
    #                                          chrome_options=options)

    #export_svgs(p, filename="Rfmix_intro.svg")
    #export_png(p, filename="Rfmix_intro.png", webdriver=self.webdriver)
    output_file("Rfmix_introgression.html")
    print "Saving to output - this could take a while.."
    save(p)
    #p = figure(title="Genome average introgression", output_backend="webgl")
    #p.xaxis.axis_label = 'Genomic position'
    #p.yaxis.axis_label = 'Genome proportion'
    
    #grid = gridplot(plot_list, plot_width=250, plot_height=250)
    #show(grid)


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
    viterbi_dict =  handle_input_files(args.viterbi) 
    map_dict = handle_input_files(args.map)

    count_dict = {}
    for chr_num in range(1,23): #22 chr
    #chr_num = 1  #22 chr
        print "Reading results for chr {}".format(chr_num)
        count_dict[chr_num] = read_viterbi(viterbi_dict[str(chr_num)])
    plotting(count_dict) 
    print "hej"
