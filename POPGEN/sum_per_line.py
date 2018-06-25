#!/usr/bin/env python
from __future__ import division
import re
import os
import sys
import pdb
input_file = sys.argv[1]
with open(input_file, 'r') as f:
    read_data = f.readlines()

data={}
original_order=[]
for line in read_data:
    line_list = line.rstrip().split(" ")
    #Map to turn it into a list of ints instead of str
    data[line_list[0]]=map(int,line_list[1:])
    original_order.append(line_list[0])

output_dict={}
for item in data:
    s_ = sum(data[item]) 
    output_dict[item]=[]
    for i_ in data[item]: 
        output_dict[item].append(i_/float(s_))

pdb.set_trace()
print output_dict
