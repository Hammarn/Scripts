import sys


input_file = sys.argv[1]
with open (input_file, 'r') as f:
    for line in f:
        col=line.split()
        print ' '.join(col[0:4]),

        genotypes=col[4:]
        string = 'ab'*len(genotypes)
        for i,x in zip(string,col[4:]):
            if i == 'a':
                print x,
        print ''
