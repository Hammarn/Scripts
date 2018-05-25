import sys

for line in sys.stdin:
	col=line.split()
	print col[0],col[1]+'_A',' '.join(col[2:])
	print col[0],col[1]+'_B',' '.join(col[2:])
