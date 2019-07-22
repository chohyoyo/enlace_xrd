#%%
#!/usr/bin/env python

#This script makes four plots (Host/Eviction frequency per slot, File URL frequency, Instantaneous Rate, Total Rate) for a SINGLE concurrency
#Sample use: python3 ./LogPlots.py ./run_20190717_175123

import os
import sys
import matplotlib.pyplot as plt
import conlog_parse as cp
import parse_out as pout
import numpy as np
from collections import Counter

runDir = sys.argv[1] #the directory of the run we want to generate plots for
logfile = cp.find_conlog(runDir)

#plot hosts from conlog
parseddata = cp.parse_job_data(logfile)
procdata = cp.data_rows_by_proc(parseddata)
slothosts = cp.slothosts_to_eviction_counts(procdata)

width = 0.35

all_host_data = list(slothosts.values())
rel_host_data = all_host_data[1:] #removes the data for the ones that are under GLIDEIN_Entry_Name:Unknown
ylen = len(rel_host_data)

unk_host = all_host_data[0] #list with the number of jobs hosted[0] and evicted[1] with an unknown host
hosted_unk = str(unk_host[0])
evicted_unk = str(unk_host[1])

x = np.arange(0,ylen,1)
y1 = [item[0] for item in rel_host_data]
y2 = [item[1] for item in rel_host_data]

fig1, ax1 = plt.subplots(figsize=(15,4))
rects1 = ax1.bar(x - width/2, y1, width, label='Hosted')
rects2 = ax1.bar(x + width/2, y2, width, label='Evicted')

ax1.set_ylabel('Frequency')
ax1.set_title('SlotHosts Counts\n' + "For (GLIDEIN_Entry_Name:Unknown) " + hosted_unk +" were hosted and "+ evicted_unk +" were evicted.")
ax1.set_xticks(x)
ax1.set_xticklabels(x)
ax1.tick_params(labelbottom = False)
ax1.legend()

plt.savefig('slothosts.png')

#plot urls using output files
urllist = pout.collecturl(runDir)

counts = Counter(urllist)
no_file_count = str(counts.pop("none",None)) #removes the unsuccessful counts since they have a url listed as 'none'

labels, values = zip(*counts.items())

url_index = np.arange(0,len(labels),1)

width = 0.25

fig2, ax2 = plt.subplots(figsize=(15,4))
ax2.bar(url_index, values, align='center')
ax2.set_xticks(url_index)
ax2.set_xticklabels('URL')
ax2.set_ylabel('frequency')
ax2.set_title('File URL frequency\n' + no_file_count + " jobs with no file used.")
ax2.tick_params(labelbottom = False)

plt.savefig('URLfreq.png')

#plot rates using output files
ratedict = pout.collectrates(runDir)
labels = list(ratedict.keys())
rates = list(ratedict.values())
avg_all = str(round(pout.avgrate_everything(runDir),1))

job_index = np.arange(0,len(rates),1)

fig3, ax3 = plt.subplots(figsize = (15,4))

ax3.bar(job_index,rates,width)
ax3.set_xlabel('Job')
ax3.set_ylabel('Rate [MB/s]')
ax3.set_xticks(job_index)
ax3.set_title("Average Rate per Job. Average of run was " + avg_all + "MB/s")
ax3.tick_params(labelbottom = False)

plt.savefig('inst_rates.png')

#plots rate from total size and total time
fig4, ax4 = plt.subplots(figsize = (15,4))

total_rates = pout.collect_total_rates(runDir)

if len(total_rates) != 0:
    avg_tot_rate = str(round(sum(total_rates)/len(total_rates),2))
else:
    avg_tot_rate = "unknown"

rate_index = np.arange(0,len(total_rates),1)

ax4.bar(rate_index,total_rates,width)
ax4.set_xlabel('Job')
ax4.set_ylabel('Rate [MB/s]')
ax4.set_xticks(rate_index)
ax4.set_title("Rates from total size and total time\n" + "average of all jobs is " + avg_tot_rate + "MB/s")
ax4.tick_params(labelbottom = False)

plt.savefig('total_rates.png')


#%%
