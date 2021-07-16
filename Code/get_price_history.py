#tutorial https://youtu.be/l2rzT_Dp4T0?t=477
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime


sample_transport=RequestsHTTPTransport(
   url='https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3',
   verify=True,
   retries=5,
)
client = Client(
   transport=sample_transport
)

pool = '0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8'

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
    poolHourData(first:100, orderBy:periodStartUnix, orderDirection: desc) {{
      periodStartUnix
      id
      close
      volumeUSD
      feesUSD
      token0Price
      token1Price
      txCount
    }}
    token0Price
    token1Price
  }}
}}
''')

response = client.execute(query)

data = response['pool']['poolHourData']

print(data[0]['close'], datetime.fromtimestamp(data[0]['periodStartUnix']))