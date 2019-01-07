#!/usr/bin/env python
import argparse
import pandas as pd 


def main(input_file,output):
    pd_data =  pd.read_csv(input_file, sep = "\t"  )
    import pdb
    
    pd_data['last'] = pd_data['FID']
    for i in pd_data.index:
        pd_data.loc[i,'FID'] = "{}:{}".format(pd_data.loc[i,'FID'],pd_data.loc[i,'IID'])
    
    pd_data.to_csv(output, sep = "\t", index=False)

    print "Output written to {}".format(output)
    
if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("""Converts FlashPCA output into SmartPCA output
    """)
    parser.add_argument("-i", "--input", default = 'king.kin', 
help="Input file from FlashPCA to convert to SmartPCA output format.")
    parser.add_argument("-o", "--output", default = 'pca.evec', 
help="Name of Outputfile.")
args = parser.parse_args() 
main(args.input, args.output)
