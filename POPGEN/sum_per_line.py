#!/usr/bin/env python
from __future__ import division
import re
import os
import sys
import pdb

input_file = sys.argv[1]
try:
    output_file = input_file.replace('.txt','') + ".percentages.txt" 
except:
    output_file = input_file + ".percentages.txt"

with open(input_file, 'r') as f:
    read_data = f.readlines()
data={}
original_order=[]
for line in read_data:
    line_list = line.rstrip().split("\t")
    #Map to turn it into a list of ints instead of str
    data[line_list[0]]=map(int,line_list[1:])
    original_order.append(line_list[0])

output_dict={}
for item in data:
    s_ = sum(data[item]) 
    output_dict[item]=[]
    for i_ in data[item]:
        #Only the denominator needs to be float to get a float as output
        output_dict[item].append(i_/float(s_))
output=str()
with open(output_file, 'w') as f:
    for indv in original_order:
        f.write(indv +' '+ ' '.join(str(p) for p in output_dict[indv]) + '\n')

