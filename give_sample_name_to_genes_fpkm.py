!# user/bin/env python
import os


analysis_dir=input("Path to Old RNA seq analysis dir")
output_dir =input("Direction dir")
tophat_dirs = [f for f in os.listdir(analysis_dir) if os.path.isfile(isdir)]
cufflink_dirs =[]

for directory in tophat_dirs:
    



