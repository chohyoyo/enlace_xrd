#%%
import sys
import matplotlib.pyplot as plt
import pandas as pd
#%%
csv_path = sys.argv[1] #
org_df = pd.read_csv(csv_path)

print(org_df)

df = org_df.groupby(['concurrency']).mean()
print(df)

#%%
#Bar Graph of Actual/Expected Rates of Varying Concurrencies

fig1, ax1 = plt.subplots(figsize = (6,6))

width=50
df = df.reset_index()
x = df['concurrency']
rates_in_MB = df['rates']
exp_rates_in_MB = df['exp rates']
rates_in_Mbps = [rate*8 for rate in rates_in_MB]
exp_rates = [expect_rate*8 for expect_rate in exp_rates_in_MB]
exp_rate = exp_rates[0]

rects1 = ax1.bar(x - width/2, rates_in_Mbps, width, label='Actual Rate')
rects2 = ax1.bar(x + width/2, exp_rates, width, label='Expected Rate')

for a,b in zip(x - width/2,rates_in_Mbps):
        plt.text(a,b,str(round(b,2)))

ax1.set_ylabel('Mbps')
ax1.set_xlabel('concurrency')
ax1.set_title('Comparison of Actual vs Expected Rates \n')
ax1.set_xticks(x)
ax1.set_xticklabels(x)

plt.grid(b=True, which='major',color='#999999',linestyle='-')
plt.minorticks_on()
plt.grid(b=True,which='minor',color='#999999',linestyle='-',alpha=0.2)
#ax1.tick_params(labelbottom = False)
ax1.legend(loc="lower right")

plt.savefig("comparison.png",transparent=True)
print("Saved plot for rate comparisons")
#%%
#Plot for percent of expected rate achieved

fig2, ax2 = plt.subplots(figsize = (6,6))

percent_rate = [(rate/exp)*100 for rate,exp in zip(rates_in_Mbps,exp_rates)]

rects3 = ax2.bar(x, percent_rate, width, label='Rate Percentage')

ax2.set_ylabel('Percent Achieved')
ax2.set_xlabel('Concurrency')
ax2.set_title('Percent of Expected Rate Achieved\n')
ax2.set_xticks(x)
ax2.set_xticklabels(x)
#ax1.tick_params(labelbottom = False)

for a,b in zip(x,percent_rate):
       plt.text(a,b+1,str(round(b,2)))

plt.savefig("percent_achieved.png", transparent=True)
print("Saved plot for percent of expected rate achieved.")

#%%
#Plot for the number of failed jobs

fig3, ax3 = plt.subplots(figsize = (6,6))

width=50

empty = org_df['failed']
list_empty = list(empty)
print(list_empty)

if sum(list_empty) == 0:
       print("No failed jobs")
       ax3.set_title("No failed jobs")
else:
       emptybar = ax3.bar(x, list_empty, width,label="Failed Jobs")
       
       ax3.set_xlabel('Concurrency')
       ax3.set_ylabel('Number Failed')
       ax3.set_title('Total Number of Failed Jobs\n')
       ax3.set_xticks(x)
       ax3.set_xticklabels(x)
       #ax1.tick_params(labelbottom = False)
       ax3.legend()
       
       for a,b in zip(x,empty):
              plt.text(a,b,str(round(b,2)))
              

plt.savefig("Average_Number_of_Failed_Jobs.png", transparent = True)
print("Saved plot for number of jobs failed.")
#%%
#Plot for the average number of jobs hosted by a slot

fig4, ax4 = plt.subplots(figsize=(6,6))

width=50

host = df['hosted']

hostbar = ax4.bar(x, host, width,label="Number Hosted")

ax4.set_xlabel('Concurrency')
ax4.set_ylabel('Number Hosted')
ax4.set_title('Average Number of Hosted Jobs per Slot\n')
ax4.set_xticks(x)
ax4.set_xticklabels(x)
ax4.legend()

plt.savefig("Avg_Number_Hosted_Jobs.png",transparent=True)

print("Saved plot for average number of jobs hosted.")
#%%
