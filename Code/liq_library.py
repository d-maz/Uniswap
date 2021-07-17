import numpy as np
import math
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime
import pandas as pd
from requests.api import get


def calc_liquidity(current_price, upper_price, lower_price, x_real, x = 'optional'):

    coeff = np.array([current_price - upper_price,2*x_real*current_price,current_price*x_real**2]).flatten()

    x_virtual_upper = np.roots(coeff)

    L = math.sqrt(upper_price)*x_virtual_upper[(x_virtual_upper > 0)]
    
    y_real = L**2/(x_real+L/math.sqrt(upper_price)) - L*math.sqrt(lower_price)

    return L#, y_real


def get_price_history(pool = '0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8'):
  
  sample_transport=RequestsHTTPTransport(
    url='https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3',
    verify=True,
    retries=5,
  )
  
  client = Client(
    transport=sample_transport
  )

  #pool = '0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8' sample pool
  #pool = '0x88977729330e55aa7111fec4967d8a561ac7c741' sample pool2

  query = gql(f'''
  query {{
    pool(id: "{pool}")
    {{
      token0 {{
        id
        symbol
      }}
      token1 {{
          id
          symbol
        }}
      poolHourData(first:1000, orderBy:periodStartUnix, orderDirection: desc) {{
        periodStartUnix
        id
        close
        token0Price
        token1Price
        txCount
        liquidity
      }}
      token0Price
      token1Price
      liquidity
      liquidityProviderCount
    }}
  }}
  ''')

  response = client.execute(query)

  df = pd.DataFrame(response['pool']['poolHourData'])

  df['periodStartUnix'] = df['periodStartUnix'].apply(datetime.fromtimestamp)
  df[['close', 'token0Price', 'token1Price', 'liquidity']]= df[['close','token0Price', 'token1Price', 'liquidity']].applymap(float)

  token0 = {
    'id': response['pool']['token0']['id'],
    'symbol' : response['pool']['token0']['symbol'],
    'price' : float(response['pool']['token0Price'])}
  
  token1 = {
    'id': response['pool']['token1']['id'],
    'symbol' : response['pool']['token1']['symbol'],
    'price' : float(response['pool']['token1Price'])}

  pool = {
    'pool': pool,
    'active_liquidity': float(response['pool']['liquidity']),
    'provider_count' : response['pool']['liquidityProviderCount']
  }
  
  return df, token0, token1, pool
