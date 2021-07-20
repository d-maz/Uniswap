#tutorial https://youtu.be/l2rzT_Dp4T0?t=477
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime
import pandas as pd

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
        volumeUSD
        feesUSD
        token0Price
        token1Price
        txCount
        liquidity
        volumeToken0
        volumeToken1
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

  df[['periodStartUnix']] = df['periodStartUnix'].apply(datetime.fromtimestamp)
  df[['close', 'token0Price', 'token1Price', 'liquidity', 'volumeToken0', 'volumeToken1']]= df[['close','token0Price', 'token1Price', 'liquidity', 'volumeToken0', 'volumeToken1']].applymap(float)
  #plot = df.plot(x = 'periodStartUnix', y='close')

  #plot.set_xlabel('Date')
  #plot.set_ylabel(f'Relative Price')

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

