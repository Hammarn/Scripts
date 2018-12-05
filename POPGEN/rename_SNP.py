#!/usr/bin/env python
import pdb
import sys
from collections import OrderedDict


input_file = sys.argv[1]
output = "{}_pos_names".format(input_file) 

with open(input_file, 'r') as f:
    with open(output,'w') as w:
        for counter, line in enumerate(f,1):
            line_list = line.rstrip().split("\t")
            w.write("{}\t{}_{}\t{}\t{}\t{}\t{}\n".format(line_list[0],line_list[0],line_list[3],line_list[2],line_list[3],line_list[4],line_list[5]))

print "Output with replaced SNP names written to {}".format(output)
