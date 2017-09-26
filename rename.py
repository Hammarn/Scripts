import re
import os
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    mo = re.search(r'P\d.*',f)
    if mo:
        print mo.group(0)
        os.rename(f, mo.group(0))
