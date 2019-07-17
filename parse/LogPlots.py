#!/usr/bin/env python

import os
import sys
import matplotlib.pyplot as plt
import conlog_parse as cp
import parse_out as pout
import numpy as np
from collections import Counter

runDir = sys.argv[1]
logfile = cp.find_conlog(runDir)

#plot hosts from conlog
parseddata = cp.parse_job_data(logfile)
procdata = cp.data_rows_by_proc(parseddata)
slothosts = cp.slothosts_to_eviction_counts(procdata)

width = 0.35

ylist = slothosts.values()
ylen = len(ylist)

x = np.arange(0,ylen,1)
y1 = [item[0] for item in ylist]
y2 = [item[1] for item in ylist]

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, y1, width, label='Hosted')
rects2 = ax.bar(x + width/2, y2, width, label='Evicted')

ax.set_ylabel('Frequency')
ax.set_title('SlotHosts Counts')
ax.set_xticks(x)
ax.set_xticklabels(x)
ax.legend()

plt.savefig('slothost.png')

#plot urls using output files
urllist = pout.collecturl(runDir)

counts = Counter(urllist)
labels, values = zip(*counts.items())

url_index = np.arange(0,len(labels),1)

width = 0.25

plt.barh(url_index, values, width)
plt.ylabel('URL')
plt.xlabel('frequency')
plt.yticks(url_index)
plt.savefig('URLfreq.png')

#plot rates using output files
ratedict = pout.collectrates(runDir)
labels = list(ratedict.keys())
rates = list(ratedict.values())
avg_all = str(round(pout.avgrate_everything(runDir),1))

job_index = np.arange(0,len(rates),1)

plt.barh(job_index,rates,width)
plt.ylabel('Job')
plt.xlabel('Rate [MB/s]')
plt.yticks(job_index)
plt.title("Average Rate per Job. Average of run was " + avg_all + "MB/s")
plt.savefig('rates.png')