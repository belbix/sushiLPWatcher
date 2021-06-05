from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from rich.status import Status
import time
from datetime import datetime, timezone
from csv import DictWriter
from dotenv import load_dotenv
import os

load_dotenv()

account = os.getenv('ACCOUNT')
pair = os.getenv('PAIR')

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.thegraph.com/subgraphs/name/sushiswap/matic-exchange")

# Create a GraphQL client using the defined transport
client = Client(transport=transport)
# Provide a GraphQL query
query = gql(
    """
query getLPData($userID: String!, $pairID: String!)
{
    user(id: $userID)
    {
        id
        liquidityPositions
         {
            liquidityTokenBalance
                pair(id: $pairID)
                {
                    totalSupply
                    reserveUSD
                    token0Price
                    token1Price
                }
        }
    }
}
"""
)

params = {'userID': str(account).lower(),
          'pairID': str(pair).lower()}

with Status('') as s:
    while True:
        utc_time = datetime.fromtimestamp(time.time(), timezone.utc)
        local_time = utc_time.astimezone()
        ts = local_time.strftime("%Y-%m-%d %H:%M")
        result = client.execute(query, variable_values=params)
        lp = result['user']['liquidityPositions'][0]
        share = float(lp['liquidityTokenBalance']) / float(lp['pair']['totalSupply'])
        value = share * float(lp['pair']['reserveUSD'])
        price = float(lp['pair']['token1Price'])
        d = {'date': ts, 'value': round(value, 4), 'price': round(price, 4)}
        s.update(f'{ts} | LP Value: ${value:,.2f} | Matic price: ${price:,.2f}')
        with open('history.csv', 'a+', newline='') as write_obj:
            dict_writer = DictWriter(write_obj, fieldnames=['date', 'value', 'price'])
            dict_writer.writerow(d)
        time.sleep(60)
