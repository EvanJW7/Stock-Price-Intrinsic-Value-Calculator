import asyncio
import aiohttp
from bs4 import BeautifulSoup

stocks = ['AAPL', 'TSLA', 'AMZN', 'MSFT', 'NVDA', 'BAC']

async def get_long_term_growth(session, stock):
    try:
        url = f'https://www.alphaquery.com/stock/{stock}/all-data-variables'
        headers = {'Accept': 'text/html'}
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                print(f"Error on get_long_term_growth request for {stock}: {response.status}")
                return None
            content = await response.text()
            soup = BeautifulSoup(content, 'lxml')
            pe = soup.find_all('td', class_='text-right')[164]
            peg = soup.findAll('td', class_='text-right')[166]
            lt_growth = (float(pe.text) / float(peg.text))
            return round(lt_growth, 2)
    except Exception as e:
        print(f"Unable to get growth rate: {stock}")
        print(e)
        return None

# Define other asynchronous functions similarly...

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for stock in stocks:
            tasks.append(get_long_term_growth(session, stock))
            # Append other asynchronous function calls here

        results = await asyncio.gather(*tasks)

        for stock, result in zip(stocks, results):
            if result is not None:
                print(f"{stock} Long Term Growth: {result}")
            else:
                print(f"{stock} - Error retrieving data")

if __name__ == "__main__":
    asyncio.run(main())
