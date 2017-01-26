#! user/bin/env python
## Messy but gets the job done
## argv 1 absolute path to OLD RNA pipeline analysis dir
## argv 2 Outputdir 

import os
import re
import shutil
import sys

analysis_dir = sys.argv[1]
output_dir=os.path.abspath(sys.argv[2])
os.chdir(analysis_dir)
#To find NGI sample names 
regex = re.compile('cufflinks_out_(P\d.*)')
#To find the cufflink dirs
regex_cuff = re.compile('cufflinks_out_*')
# get all dirs
tophat_dirs = [f for f in os.listdir(analysis_dir) if os.path.isdir(f)]
#iterate through the dirs and find the cuflinks dir. In there find the genes.fpkm file, 
#move it to the outdir and rename it by the sample name
for directory in tophat_dirs:
    os.chdir(analysis_dir)
    cuff_dirs=[f for f in os.listdir(os.path.abspath(directory)) if regex_cuff.match(f)]
    os.chdir(directory)
    for i in cuff_dirs:
        os.chdir(i)
        sample_name = regex.match(i).group(1)
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            mo = re.search(r'genes.fpkm_tracking',f)
            if mo:
                shutil.copy(f,output_dir)
                os.chdir(output_dir)
                os.rename(f, "OLD_{}.genes.fpkm_tracking.txt".format(sample_name))


