# interpolate cM positions from map data.
from numpy import *
from scipy.interpolate import interp1d

from sys import argv

mapfile, cmmap, outfilename = argv[1:]
print argv[1:]

# use plink-formatted input file here.
print 'reading in base positions for array'
bps = array([line.strip().split()[3] for line in file(mapfile)],dtype=int)

# read in genetic map data. chr will be read as last value before '.'
print 'reading in reference map data'
chr = mapfile.split('_')[-1].split('.')[0].replace('chr','')
print 'current chromosome is:',chr

# read in data, include a 0 to trap variants that are before the start of the hapmap data (just in case)
gmapdata = vstack((zeros(3) , array([line.strip().split() for line in file(cmmap).readlines()[1:]],dtype=float)))

print 'interpolating data...'

hapmap_cms = interp1d(gmapdata[:,0],gmapdata[:,2])
interp_cms = hapmap_cms(bps)
print 'writing output...'
savetxt(outfilename , interp_cms , fmt='%.6f' , delimiter='\n')
print 'done with %s' % (outfilename)
