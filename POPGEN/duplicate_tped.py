import sys

for line in sys.stdin:
	col=line.split()
	print ' '.join(col[0:4]),
	for x in col[4:]:
		print x,x,
	print ''
