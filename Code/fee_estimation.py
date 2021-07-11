import numpy as np
import math
from matplotlib import pyplot as plt
import requests
import json
import pandas as pd
from liquidity import calc_liquidity


current_price = 2133
upper_price = 2445
lower_price = 1855
real_quantity = 6

Liquidity, USDC_required = calc_liquidity(current_price,upper_price,lower_price,real_quantity)
print(type(Liquidity), type(USDC_required))

print('Liquidity: ', round(Liquidity[0],2), '\n' 'USDC required: ', round(USDC_required[0],2))

pool_address = ['0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640', #usdc eth 0.05 
    '0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8', #usdc eth 0.3
    '0xc2e9f25be6257c210d7adf0d4cd6e3e881ba25f8', #dai eth 0.3
    '0x60594a405d53811d3bc4766596efd80fd545a270',  #dai eth 0.05
    '0x4e68ccd3e89f51c3074ca5072bbac773960dfa36', #usdt eth 0.3
    '0x11b815efb8f581194ae79006d24e0d814b7697f6' #usdt eth 0.05
    ] #

#pool_address = ['0xcbcdf9626bc03e24f779434178a73a0b4bad62ed']
url = 'https://api.flipsidecrypto.com/api/v2/queries/79d15dfa-8714-4256-86b1-ae4dfd37b747/data/latest'

response = requests.get(url)
df = pd.DataFrame(response.json())
sdf = df[df['POOL_ADDRESS'].isin(pool_address)]
sdf = sdf.reset_index()

pool_ownership = Liquidity[0]/(np.array(sdf['ACTIVE_LIQUIDITY'])) #+ Liquidity[0])
daily_fees = np.array(sdf['MAX(FEE_PERCENT)']) / 100 * np.array(sdf['MAX(DAY_VOL_USD)'])
weekly_fees = np.array(sdf['MAX(FEE_PERCENT)']) / 100 * np.array(sdf['MAX(WEEK_VOL_USD)'])

for index, value in enumerate(pool_ownership):
    print(index)
    print('Estimated pool share in', sdf["POOL_NAME"][index], 'is:', round(value*100,3), '%')
    print('Estimated daily fees is $', round(value*daily_fees[index],2))
    print('Estimated weekly fees is $', round(value*weekly_fees[index],2))

