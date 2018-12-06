#!/usr/bin/env python
import argparse
import pandas as pd 


def main(input_file, coefficient,output):
    pd_data =  pd.read_csv(input_file, sep = "\t"  )

    bigger =  pd_data.loc[pd_data['Kinship'] > coefficient ]
    with open(output,'w') as w:
        for index, row in bigger.iterrows():
            w.write("{}\t{}\n".format(row['FID'],row['ID1']))

    print "Output written to {}".format(output)
# pd_data.sort_values(by = ['Kinship'], ascending = False )
    
if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("""Takes a  king.kin file as input and a value to filter on. Returns a file that plink can use to remove those individuals from the analysis.
    """)
    parser.add_argument("-i", "--input", default = 'king.kin', 
help="Input file from king to analyse.")
    parser.add_argument("-o", "--output", default = 'indvs_to_remove_due_to_king_related.txt', 
help="Name of Outputfile.")
    parser.add_argument("-k", "--kinship", nargs = 1, default = 0.09,
help="Kinship Coefficient to use. Default is 0.09")
args = parser.parse_args() 
main(args.input,args.kinship, args.output)
