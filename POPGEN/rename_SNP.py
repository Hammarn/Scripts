#!/usr/bin/env python
import pdb
import sys
from collections import OrderedDict


input_file = sys.argv[1]

with open(input_file, 'r') as f:
    data = OrderedDict()
    original_order=[]
    for counter, line in enumerate(f,1):
        line_list = line.rstrip().split("\t")
        data[counter] = "{}\t{}_{}\t{}\t{}\t{}\t{}\n".format(line_list[0],line_list[0],line_list[3],line_list[2],line_list[3],line_list[4],line_list[5])


print "Done with reading {}, now writing output".format(input_file)
output = "{}_pos_names".format(input_file) 
with open(output,'w') as f:
    for key in data.keys():
        f.write(data[key])

print "Output with replaced SNP names written to {}".format(output)
