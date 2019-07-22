#%%
import sys
import conlog_parse as cp
import pandas as pd
#%%
#plt the average number of jobs per host at different concurrencies
csv_path = '/home/harper/enlace/parsed.csv'
df = pd.read_csv(csv_path,index_col=0)

print(df)

#%%
