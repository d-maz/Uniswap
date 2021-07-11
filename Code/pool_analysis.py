import numpy as np
import math
from matplotlib import pyplot as plt
import requests
import json
import pandas as pd
from liq_library import calc_liquidity

url = 'https://api.flipsidecrypto.com/api/v2/queries/eaad960d-2c48-4f95-abbf-51da8197689e/data/latest'

response = requests.get(url)
price_df = pd.DataFrame(response.json())

url = 'https://api.flipsidecrypto.com/api/v2/queries/79d15dfa-8714-4256-86b1-ae4dfd37b747/data/latest'

response = requests.get(url)
pool_df = pd.DataFrame(response.json())

#pool_df['PRICE'] = pool_df[['TOKEN1_ADDRESS']].applymap(lambda x: price_df[price_df['TOKEN_ADDRESS'] == x]['PRICE'].values) 

usd_quant = 5000
variance = 0.2

pool_df['XREAL'] = usd_quant/pool_df[['TOKEN1_ADDRESS']].applymap(lambda x: price_df[price_df['TOKEN_ADDRESS'] == x]['PRICE'].values) 

pool_df['UPPER_PRICE'] = pool_df['PRICE']*(1+variance)
pool_df['LOWER_PRICE'] = pool_df['PRICE']*(1-variance)

current_price = pool_df['PRICE'].values
upper_price = pool_df['UPPER_PRICE'].values
lower_price = pool_df['LOWER_PRICE'].values
real_quantity = pool_df['XREAL'].values

pool_df = pool_df[pool_df['XREAL'].map(len) == 1]


pool_df['LIQUID'] = pool_df.apply(lambda x : calc_liquidity(x['PRICE'], x['UPPER_PRICE'], x['LOWER_PRICE'], x['XREAL'], x), axis=1)

pool_df['OWNERSHIP'] = pool_df['LIQUID'].values/(pool_df['ACTIVE_LIQUIDITY'].values+pool_df['LIQUID'].values)

pool_df['DAILY_FEES'] = pool_df['OWNERSHIP'].values*pool_df['MAX(DAY_VOL_USD)'].values*pool_df['MAX(FEE_PERCENT)'].values/100
pool_df['WEEKLY_FEES'] = pool_df['OWNERSHIP'].values*pool_df['MAX(WEEK_VOL_USD)'].values*pool_df['MAX(FEE_PERCENT)'].values/100
fee_df = pool_df[['POOL_NAME','DAILY_FEES', 'WEEKLY_FEES', 'OWNERSHIP', 'MAX(WEEK_VOL_USD)', 'MAX(DAY_VOL_USD)']]#.sort_values('DAILY_FEES', ascending=False)
fee_df['DAILY_FEES'] = fee_df[['DAILY_FEES']].applymap(lambda x : np.round(np.asscalar(x),2))
fee_df['WEEKLY_FEES'] = fee_df[['WEEKLY_FEES']].applymap(lambda x : np.round(np.asscalar(x),2))

fee_df = fee_df[fee_df['DAILY_FEES'].notna()].sort_values('DAILY_FEES', ascending=False)




