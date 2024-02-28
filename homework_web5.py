import platform
import aiohttp
import asyncio
from datetime import datetime, timedelta



async def fetch_currency_rate(session:aiohttp.ClientSession, date: datetime):
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date.strftime("%d.%m.%Y")}'
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"Error status: {response.status} for {url}")
    except aiohttp.client_exceptions.ClientConnectorError as err:
            print(f'Connection error: {url}', str(err))
 
 
async def get_currency_rates(session: aiohttp.ClientSession, index_days: int):
    if index_days > 10:
        index_days = 10
        print("You can see the exchange rate no more than 10 days ago")
    dates = [datetime.today() - timedelta(days=i) for i in range(index_days)]
    # async with aiohttp.ClientSession() as session:
    results = []
    for date in dates:
        result = await fetch_currency_rate(session, date)
        if result:
            currency_data = result.get('exchangeRate', [])
            formatted_data = {
                date.strftime('%d.%m.%Y'): {
                    currency['currency']: {
                        'sale': currency.get('saleRate'),
                        'purchase': currency.get('purchaseRate')
                    }
                    for currency in currency_data
                    if currency['currency'] in ['EUR', 'USD']
                }
            }
            results.append(formatted_data)
    return results

async def main(index_days: int):
    async with aiohttp.ClientSession() as session:
        rates = await get_currency_rates(session, index_days)
        print(rates)

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(2))
 

