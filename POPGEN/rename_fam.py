#!/usr/bin/env python
import argparse
import pandas as pd
import os

def read_input(input_file):
    pd_data = pd.read_csv(input_file, sep = "\s+", header = None)
    return pd_data

def rename_fam(data,key):
    ## The actual replacement through dataframe lookup
    ## Replace every instance of the column 1 in key with column 2
    data = data.replace(dict(zip(key[0], key[1] )))
    ## get out the name of the famfile
    input_name = vars(args)["fam"]
    name_list = input_name.split(".")

    if len(name_list) == 2:
        ## We have a sane file name
        backup_name = name_list[0] + "_backup." + name_list[1]
        os.popen("cp {} {}".format(input_name, backup_name) )
    
    else:
        ## madness
        backup_name = input_name + "_backup"
        os.popen("cp {} {}".format(input_name, backup_name) )

    print("Backup inputfile saved to {}".format(backup_name))
    data.to_csv(input_name, sep=" ", index=False, header=False)
    print("Renamed file saved to {}".format(input_name))

if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("""Renames the FID/POPs in a .fam file or similar from plink.
    The keyfile shoudl have the following format:
    POP1_old_name POP1_new_name
    POP2_old_name POP2_new_name
    ...              ...
    """)
    parser.add_argument("-f", "--fam",
    help="Name of fam or tfam")
    parser.add_argument("-k", "--key",
    help="Name of the key-file")

    args = parser.parse_args()
    data = read_input(args.fam)
    key = read_input(args.key)
    rename_fam(data,key)
