import pandas as pd
from liq_library import get_price_history

from matplotlib import pyplot as plt
import numpy as np
import random


pool = '0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8'
#pool = '0xcbcdf9626bc03e24f779434178a73a0b4bad62ed'
pool = '0xcbcdf9626bc03e24f779434178a73a0b4bad62ed'

history_df, pool = get_price_history(pool)

history_df['hourly_ret'] = history_df['close'].iloc[::-1].pct_change()

daily_std = history_df['hourly_ret'].std()*24**0.5

#plot = history_df['hourly_ret'].hist(bins = 100)

history_df = history_df.dropna(subset=['hourly_ret'])

#bootstrap
nprice_paths = 10000
path_length = 720 #hours
bootstrap =np.zeros([nprice_paths,path_length])
price_path =np.zeros([nprice_paths,path_length])
f = lambda x: x*random.choice([-1, 1])

for i in range(len(bootstrap)):
    bootstrap[i] = history_df['hourly_ret'].sample(n = path_length, replace = True).abs().map(f).values
    bootstrap[i] = bootstrap[i] + 1
    bootstrap[i][0] = pool['token0']['price']
    price_path[i] = list(np.cumprod(bootstrap[i]))


#print(bootstrap[0], bootstrap_result[0])
#for i in range(len(bootstrap_result)):
#    plt.plot(bootstrap_result[i])
#plt.ylim(min(min(x) for x in bootstrap_result)-0.5*max(max(x) for x in bootstrap_result),max(max(x) for x in bootstrap_result)*1.5)
#plt.show()


#calculate percentage of time 
current_price = pool['token0']['price']
spread = 0.08

#metric 1: percentage of pools in range in given hour
metric1 = []
for i in range(path_length):
    temp = price_path[:,i]
    metric1.append(np.count_nonzero(temp[np.logical_and(temp > current_price*1/(1+spread), temp < current_price*(1+spread))])/nprice_paths)

fig,axs = plt.subplots(3)
plt.title(f'spread = {spread}')
axs[0].plot(metric1)

#metric 2: histogram of percentage of time each pool is in range
metric2 = []
for i in range(nprice_paths):
    temp = price_path[i,:]
    metric2.append(np.count_nonzero(temp[np.logical_and(temp > current_price*1/(1+spread), temp < current_price*(1+spread))])/path_length)

axs[1].hist(metric2,bins=100)

#metric 3: avg/median, min time to exit range
metric3 = []

for path in range(nprice_paths):
    metric3.append(next((i for i,value in enumerate(price_path[path,:]) if (value < current_price*1/(1+spread) or value > current_price*(1+spread))),720))

print(np.mean(metric3), np.min(metric3), np.median(metric3))

axs[2].hist(metric3, bins=100)

plt.show()

# calculate expected gains for given spread and given capital level

# calculate losses for each end price (relative to cash, half/half, all eth start)

# calculate expected gain

# figure out how the risk metrics fit in?
