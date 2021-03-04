#!/usr/bin/env python
import sys
import re
import pdb
import os
import copy
import argparse
import pandas as pd 
import numpy as np

from math import pi

from collections import OrderedDict
from bokeh.models import Axis,Range1d, HoverTool, Legend
from bokeh.layouts import row, gridplot
from bokeh.io import  show, output_file 
from bokeh.plotting import figure, save
from bokeh.palettes import Spectral5


import pdb

def handle_input_files(files):
    # Figure out which chr we are working with and return them in order
    chr_pat = re.compile('chr\d+')
    uppercase = re.compile('CHR\d+')
    chr_nm_pat = re.compile('\d+')
    file_dict = {}
    for f in files:
        full_name =  os.path.abspath(f)
        try:
            chr_plus_nm = chr_pat.search(f).group(0)
        except AttributeError,TypeError:
            chr_plus_nm = uppercase.search(f).group(0)

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
            five = line.count('5')
            six = line.count('6')
            seven = line.count('7')
            counter +=1
            sum_nu = sum((one,two,three,four, five, six, seven))
            try:
                chr_dict[counter]=[one/float(sum_nu),two/float(sum_nu),three/float(sum_nu),four/float(sum_nu),five/float(sum_nu),six/float(sum_nu),seven/float(sum_nu) ]
            except:
                print("OOps")
                pdb.set_trace()

                x= 0     
    return chr_dict

def read_FB(Fb_file):
    Fb_file = Fb_file
    FB = pd.read_csv(Fb_file, delimiter=" ", header = None)
    #remove trailing whitespace, a bit crude though
    FB = FB.dropna(how="any", axis='columns')
    return FB

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
        
        #first =  int(bp_dict[vit_num][1]) 
        #first = first + filter_value
        first = filter_value
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


def plotting(count_dict, bp_dict, FB_dict, backup_dict, print_FB, names):
    count_dict = count_dict
    bp_dict = bp_dict
    # Each key is a CHR
    #get names from user instead
    #names = ['CEU', 'CDX', 'YRI', 'Khoisan']
    data_dict =  {}
    counter = 0 
    for key in count_dict.keys():
            data_dict[key] = []
            A_1 = []
            A_2 = []
            A_3 = []
            A_4 = []
            A_5 = [] 
            A_6 = [] 
            A_7 = [] 
            Pos = [] 
            # Each i is a line in Viterbi-file i.e. a SNP
            for i in count_dict[key].keys():
                A_1.append(count_dict[key][i][0])
                A_2.append(count_dict[key][i][1])
                A_3.append(count_dict[key][i][2])
                A_4.append(count_dict[key][i][3])
                A_5.append(count_dict[key][i][4])
                A_6.append(count_dict[key][i][5])
                A_7.append(count_dict[key][i][6])
                Pos.append(bp_dict[key][i])
                
                bp_dict[key]

            data_dict[key] = {'{}'.format(names[0]) : pd.Series(A_1, index = Pos),
                '{}'.format(names[1]) : pd.Series(A_2, index = Pos),
                '{}'.format(names[2]) : pd.Series(A_3, index = Pos),
                '{}'.format(names[3]) : pd.Series(A_4, index = Pos),
                '{}'.format(names[4]) : pd.Series(A_5, index = Pos),
                '{}'.format(names[5]) : pd.Series(A_6, index = Pos),
                '{}'.format(names[6]) : pd.Series(A_7, index = Pos),
                 }#'Chromosome' : key }
            data_dict[key] = pd.DataFrame(data_dict[key])    
    data =  pd.concat([data_dict[key] for key in  data_dict.keys()])
    #p.xaxis.axis_label = 'Genomic position'
    #p.yaxis.axis_label = 'Genome proportion'
   
    #FB_dict
    ## EXTRACTING stuff
    ## each row is one SNP in both viterbi and FB
    ## Find interesting viterbi rows
    ## return the corresponding rows in FB, should be fine to print for now.
    ## Threshold? if proporion CEU is < 95%??
    
    ### FIltering for backup FB
    # SNP numer / row numer sohuld now be the same right? so can use count dict to filter out the SNPS?
    
    count_DFs={}
    for i in range(1,23):
        count_DFs[i]=pd.DataFrame.from_dict(count_dict[i],'index')
    if FB_dict:
        #count_dict to dataframe=
        # Every fourth column in the dataframe
        output_dict={}
        #for i in range(1,3):
        for i in range(1,23):
            fourth=FB_dict[i].columns[::4]
            khoisan = FB_dict[i].columns[3::4] 
            print"Looking through SNP on chr{}".format(i)
            ## return a list of indicies(i.e SNS) for each CHR

            indicies  = count_DFs[i].loc[count_DFs[i][0]< 1].index.tolist()
            ##BP to DF
            bp_dict[i] = pd.DataFrame.from_dict(bp_dict[i],'index')
            bp_dict[i]=bp_dict[i].rename(index=str, columns={0: "BP"})
            #Both need to be 0-indexed
            bp_dict[i]= bp_dict[i].reset_index(drop=True)
            ##add BP pos 
            FB_dict[i]=pd.concat([bp_dict[i],FB_dict[i]],  axis=1, join='inner') 
            
            ## add chr num to FB
            #FB_dict[i]['CHR']=i
            short_rows = FB_dict[i].iloc[indicies]
            short_rows.to_csv("ROH_SNPS_chr{}.txt".format(i), index= False)


    ## need to add in 

### Actual plotting here
   # print "Not plotting"
   # sys.exit() 
    ## Make sure we are accessing the chromosomes in the correct order
    for key in range(1,23):
        print "Building subplot {}".format(key)
        TOOLTIPS=[
            #( "index", "$index"      ),
            ( 'X',   '$x'            ),
            ( 'Y',   '$y'            ),
        ]
        local_vars = vars()
        ### Name of pop from variable instead of hardcoded!!
        
        local_vars['p{}'.format(key)] = figure(plot_height=500, plot_width=500, output_backend="webgl", title="Chromosome {}".format(key))
        local_vars['p{}'.format(key)].circle(x = data_dict[key].index.values, y = data_dict[key][names[0]],  color = "grey"   )
        local_vars['p{}'.format(key)].circle(x = data_dict[key].index.values, y = data_dict[key][names[1]],  color = "skyblue"  )
        local_vars['p{}'.format(key)].circle(x = data_dict[key].index.values, y = data_dict[key][names[2]],  color = "goldenrod"  )
        local_vars['p{}'.format(key)].circle(x = data_dict[key].index.values, y = data_dict[key][names[3]],  color = "salmon"  )
        local_vars['p{}'.format(key)].circle(x = data_dict[key].index.values, y = data_dict[key][names[4]],  color = "deeppink"  )
        local_vars['p{}'.format(key)].circle(x = data_dict[key].index.values, y = data_dict[key][names[5]],  color = "darkviolet"  )
        local_vars['p{}'.format(key)].circle(x = data_dict[key].index.values, y = data_dict[key][names[6]],  color = "red"  )
        local_vars['p{}'.format(key)].xaxis.major_label_orientation = "vertical"
        local_vars['p{}'.format(key)].xaxis[0].formatter.use_scientific = False
        local_vars['p{}'.format(key)].xaxis[0].ticker = [int(data_dict[key].first_valid_index()) ,int(data_dict[key].last_valid_index())]
        local_vars['p{}'.format(key)].x_range = Range1d(int(data_dict[key].first_valid_index()) ,int(data_dict[key].last_valid_index()))
        legend = Legend(items = [names[1], names[2], names[3], names[4], names[5], names[6], ])

        #output_file("Rf_chr{}.html".format(key))
        #export_svgs(local_vars['p{}'.format(key)], filename="Rfmix_intro_{}.svg".format(key))
        #save(local_vars['p{}'.format(key)])
            
    [local_vars['p{}'.format(i)] for i in data_dict.keys()].add_layout(legend, 'right')
    plot_list = [local_vars['p{}'.format(i)] for i in data_dict.keys()]
    #Make one figure out of the 22 subplots
    p =gridplot(plot_list, ncols=10) 
    #p = row(plot_list)
   
    output_file("Rfmix_introgression.html")
    print "Saving to output - this could take a while.."
    save(p)

if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Plot output from RFMIX")
    parser.add_argument("-v", "--viterbi", nargs = '+',
        help="Viterbi output files from RFMix. Needs to contain the substring 'chrxx' where xx is the chromosome number in the filename")
    parser.add_argument("-b", "--bim", nargs = '+',
        help="Bim file with genomic positions. Needs to contain the substring 'chrxx' where xx is the chromosome number in the filename")
    parser.add_argument("-fb", "--forward-backwards", nargs = '+',
        help="ForwardBackward file from RFMix. Needs to contain the substring 'chrxx' where xx is the chromosome number in the filename")
    parser.add_argument("-PFB", "--print_FB", default=True,
    help="If FB positions should be revealed")
    parser.add_argument("-n", "--names", nargs = '+',
        help="Names of the populations in order separate by space. eg. YRI CEU HAN ")

    args = parser.parse_args()
    viterbi_dict =  handle_input_files(args.viterbi) 
    bim_dict = handle_input_files(args.bim)
    if args.forward_backwards:
        FB_dict = handle_input_files(args.forward_backwards)

    count_dict = OrderedDict()
    for chr_num in range(1,23): #22 chr
    #chr_num = 1  #22 chr
        print "Reading results for chr {}".format(chr_num)
        count_dict[chr_num] = read_viterbi(viterbi_dict[str(chr_num)])
    ## FB 
    if args.forward_backwards:
        for chr_num in range(1,23): #22 chr
            print "Reading FB file for chr {}".format(chr_num)
            FB_dict[chr_num] = read_FB(FB_dict[str(chr_num)])

    bp_dict = OrderedDict()
    for chr_num in range(1,23): #22 chr
    #chr_num = 1  #22 chr
        print "Reading bim file for chr {}".format(chr_num)
        bp_dict[chr_num] = read_genetic_bim(bim_dict[str(chr_num)])
    backup_dict = copy.deepcopy(count_dict) 
    count_dict  =  filter_away_telemomers(count_dict, bp_dict) 
    
    if not args.forward_backwards:
            FB_dict = 0
    plotting(count_dict, bp_dict,FB_dict, backup_dict,args.print_FB,args.names ) 
    print "Goodbye"
