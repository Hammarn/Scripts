import sys


for line in sys.stdin:
	col=line.split()
	print ' '.join(col[0:4]),

	genotypes=col[4:]
	string = 'ab'*len(genotypes)
	for i,x in zip(string,col[4:]):
		if i == 'a':
			print x,
	print ''
