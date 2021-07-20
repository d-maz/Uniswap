import pandas as pd
from liq_library import get_price_history

from matplotlib import pyplot as plt
import numpy as np
import random


pool = '0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8'
#pool = '0xcbcdf9626bc03e24f779434178a73a0b4bad62ed'

history_df, pool = get_price_history(pool)

history_df['hourly_ret'] = history_df['close'].iloc[::-1].pct_change()

daily_std = history_df['hourly_ret'].std()*24**0.5

plot = history_df['hourly_ret'].hist(bins = 100)

history_df = history_df.dropna(subset=['hourly_ret'])

#bootstrap
price_paths = 10
path_length = 720 #hours
bootstrap =np.zeros(price_paths, dtype= object)
bootstrap_result =np.zeros(price_paths, dtype= object)
f = lambda x: x*random.choice([-1, 1])

for i in range(len(bootstrap)):
    bootstrap[i] = history_df['hourly_ret'].sample(n = path_length, replace = True).abs().map(f).values
    bootstrap[i] = bootstrap[i] + 1
    bootstrap[i][0] = pool['token0']['price']
    bootstrap_result[i] = np.cumprod(bootstrap[i])


#print(bootstrap[0], bootstrap_result[0])
for i in range(len(bootstrap_result)):
    plt.plot(bootstrap_result[i])
plt.ylim(min(min(x) for x in bootstrap_result)-0.5*max(max(x) for x in bootstrap_result),max(max(x) for x in bootstrap_result)*1.5)
plt.show()





