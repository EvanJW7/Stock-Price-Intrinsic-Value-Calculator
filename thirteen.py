import asyncio
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import stocks_list
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Watchlist:
    def __init__(self):
        self.stocks = stocks_list.stocks
        self.stocks_in_play = 0
        self.sizzlers = 0

    async def get_market_cap(self, stock):
        try:
            url = f'https://www.marketwatch.com/investing/stock/{stock}?mod=search_symbol'
            res = requests.get(url)
            if res.status_code != 200:
                print(f"Error on market cap request: {res.status_code}")
            soup = BeautifulSoup(res.text, 'lxml')
            mc = soup.findAll('li', class_='kv__item')[3]
            mc = mc.text[11:].strip()
        except 
            mc = "No data"
        return mc

    async def get_short_float(self, stock):
        try:
            url = f'https://www.marketwatch.com/investing/stock/{stock}?mod=search_symbol'
            res = requests.get(url)
            if res.status_code != 200:
                print(f"Error on short float request: {res.status_code}")
            soup = BeautifulSoup(res.text, 'lxml')
            sf = soup.findAll('li', class_='kv__item')[14]
            sf = sf.text[19:].strip()
        except:
            sf = "No data"
        return sf

    async def get_volatility(self, stock):
        try:
            url = f'https://www.alphaquery.com/stock/{stock}/volatility-option-statistics/180-day/historical-volatility'
            res = requests.get(url)
            if res.status_code != 200:
                print(f"Error on volatility request: {res.status_code}")
            soup = BeautifulSoup(res.content, 'lxml')
            volatility = soup.findAll('div', class_='indicator-figure-inner')[0]
            vol = float(volatility.text) * 100
            vol = round(vol, 2)
        except:
            vol = "No data"
        return vol
    
    async def get_sector(self, stock):
        try:
            url = f'https://www.marketwatch.com/investing/stock/{stock}/company-profile?mod=mw_quote_tab'
            res = requests.get(url)
            if res.status_code != 200:
                print(f"Error on volaility request: {res.status_code}")
            soup = BeautifulSoup(res.content, 'lxml')
            industry = soup.findAll('span', class_="primary")[6].text
            sector = soup.findAll('span', class_="primary")[7].text
            if len(industry) <= len(sector):
                return industry
            else:
                return sector
        except IndexError:
            return "N/A"
    
    async def get_stock_data(self, stock, i):
        try:
            ticker = yf.Ticker(stock)
            p = str(i) + 'd'
            stock_data = await asyncio.to_thread(ticker.history, period=p)
            stock_data = stock_data.reset_index()
            gap = (stock_data['Open'][99] - stock_data['High'][98]) / stock_data['High'][98] * 100
            green_initial_day = stock_data['Close'][99] > stock_data['Open'][99]
            avg_vol = stock_data['Volume'][0:99].mean()
            vol_ratio = stock_data['Volume'][99] / avg_vol
            equity_vol = stock_data['Open'][0:99].mean()* stock_data['Volume'][0:99].mean()
            if green_initial_day and round(gap) >= 3 and avg_vol >= 500000 and vol_ratio > 5:
                mc = await self.get_market_cap(stock)
                sf = await self.get_short_float(stock)
                vol = await self.get_volatility(stock)
                sector = await self.get_sector(stock)
                date = stock_data['Date'][99]
                print(f"{stock:>5}{date.strftime('%m/%d/%Y'):>14}{sector:^30}{mc:>8}{format(round(equity_vol), ','):>15}{round(gap, 2):>11}%{round(vol_ratio, 2):>11}{sf:>12}{vol:>12}%")
                self.stocks_in_play += 1
                if vol > 100:
                    self.sizzlers += 1
        except KeyError:
            logger.warning(f"Unable to get stock data for {stock} due to KeyError")
            pass
    

    async def main(self):
        tasks = []
        print("\n Stock      Date              Sector             MarketCap     EquityVol        Gap     VolRatio   ShortFloat    Vol180")
        for i in range(100, 111):
            print(f'{i}---------------------------------------------------------------------------------------------------------------------')
            for stock in self.stocks:
                tasks.append(asyncio.create_task(self.get_stock_data(stock, i)))
            await asyncio.gather(*tasks)
            tasks.clear()
        print(f"\nStocks in play: {self.stocks_in_play}")
        print(f"Sizzlers: {self.sizzlers}\n")

if __name__ == '__main__':
    my_watchlist = Watchlist()
    asyncio.run(my_watchlist.main())
    
