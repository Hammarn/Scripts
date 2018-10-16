#!/usr/bin/env python
####      Input: ped file outputfile
####
####



import sys
import pdb


def read_ped(input_f):
    data_dict = {} 
    with open(input_f, 'r') as f:
        counter = 1 
        for line in f:
            line = line.split()
            if line[0].startswith('Family'):
                #Header
                continue
            data_dict[counter] = line
            counter += 1
    return(data_dict)
def filter_by_fam(datadict,filter_dict):
    keep = []
    for key in filter_dict.keys():
        for data_key in datadict.keys():
            if datadict[data_key][1] == filter_dict[key][1]:
                keep.append(data_key)
    for key in datadict.keys():
        if key not in keep:
            datadict.pop(key)
    return datadict
#    pdb.set_trace()

def write_fam(data_dict, fam_name):
    
    
    with open(fam_name, 'w') as f:
        for key in data_dict.keys():
            f.write('{} {} {} {} {} -9\n'.format( data_dict[key][6],data_dict[key][1],data_dict[key][2],data_dict[key][3],data_dict[key][4] ))


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_name = sys.argv[2]
    filter_fam = sys.argv[3]

    datadict = read_ped(input_file)
    filter_dict = read_ped(filter_fam)
    datadict = filter_by_fam(datadict,filter_dict)
    write_fam(datadict , output_name ) 
