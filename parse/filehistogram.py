#%%
import os
import sys

#obtain list of file URLs used in each job for the run
def parse_url(stdoutfile):
    retval=[]
    fl_handle = open(stdoutfile, 'r')
    fl_data = fl_handle.readlines()
    fl_handle.close()

    i=0
    while i < len(fl_data):
         if 'root://xrootd.t2.ucsd.edu:2040' in fl_data[i]:
            fileURL=fl_data[i].split('root://')[1]
            retval.append(fileURL)
            i += 1
         else:
            pass
            i += 1
    return retval

#gather all output files in a run folder specified by 'path and
#get parse each for the url, putting it all in a txt file

def make_url_list(runpath)
    retval = []
    for root, dirs, files in os.walk(runpath): 
        for file in files:
            if file.endswith(".out"):
                out_path = os.path.join(root,file)
                url = parse_url(out_path)
                retval.append(url)
            else:
                pass
    return retval
#%%
import pandas as pd
from collections import Counter

data = make_url_list(runpath)
count_similar = Counter()
df = pd.DataFrame.from_dict(lettter_counts, orieng = 'index')
df.plot(kind='bar')