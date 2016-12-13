#! user/bin/env python
##Super quick and dirty bot seems to work
## argv 1 absolute path to OLD RNA pipeline analysis dir
## argv 2 where you want the files copied to

import os
import re
import shutil
import sys

analysis_dir = sys.argv[1]
output_dir=os.path.abspath(sys.argv[2])
os.chdir(analysis_dir)
tophat_dirs = [f for f in os.listdir(analysis_dir) if os.path.isdir(f)]
regex = re.compile('cufflinks_out_(P\d.*)')
regex_cuff = re.compile('cufflinks_out_*')
for directory in tophat_dirs:
    os.chdir(analysis_dir)
    cuff_dirs=[f for f in os.listdir(os.path.abspath(directory)) if regex_cuff.match(f)]
    os.chdir(directory)
    for i in cuff_dirs:
        os.chdir(i)
        sample_name = regex.match(i).group()
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            mo = re.search(r'genes.fpkm_tracking',f)
            if mo:
                shutil.copy(f,output_dir)
                os.chdir(output_dir)
                os.rename(f, "{}.genes.fpkm_tracking".format(sample_name))


