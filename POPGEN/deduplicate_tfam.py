import sys

for line in sys.stdin:
	col=line.split()
	if '_A' in col[1]:
		print col[0],col[1].rstrip('_A'),' '.join(col[2:])
