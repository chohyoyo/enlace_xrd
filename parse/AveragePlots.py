#%%
import sys
import matplotlib.pyplot as plt
import pandas as pd
#%%
#plt the average number of jobs per host at different concurrencies
csv_path = sys.argv[1]
df = pd.read_csv(csv_path)
df['rates']
#%%

fig1, ax1 = plt.subplots(figsize=(4,4))

width=30

x = df['concurrency']
y1 = df['rates']
y2 = [2 for i in x]

rects1 = ax1.bar(x - width/2, y1, width, label='Actual Rate')
rects2 = ax1.bar(x + width/2, y2, width, label='Expected Rate')

ax1.set_ylabel('MB/s')
ax1.set_title('Comparison of Actual vs Expected Rates')
ax1.set_xticks(x)
ax1.set_xticklabels(x)
#ax1.tick_params(labelbottom = False)
ax1.legend()

#%%
fig2, ax2 = plt.subplots(figsize=(4,4))

y3 = y1/y2

rects3 = ax2.bar(x - width/2, y3, width, label='Rate Percentage')

ax2.set_ylabel('Percent')
ax2.set_title('Percent of Expected Rate Achieved')
ax2.set_xticks(x)
ax2.set_xticklabels(x)
#ax1.tick_params(labelbottom = False)
ax2.legend()

#%%
fig3, ax3 = plt.subplots(figsize=(4,4))

width=30

empty = df['failed']
per_fail = empty/(x*5)

emptybar = ax3.bar(x - width/2, per_fail, width)

ax3.set_title('Percent of Failed Jobs')
ax3.set_xticks(x)
ax3.set_xticklabels(x)
#ax1.tick_params(labelbottom = False)
ax3.legend()

#%%
