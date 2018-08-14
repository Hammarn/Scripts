import sys

input_file = sys.argv[1]

with open(input_file,'r') as f:
    for line in f:
        col=line.split()
        if '_A' in col[1]:
            print col[0],col[1].rstrip('_A'),' '.join(col[2:])
