import requests
from bs4 import BeautifulSoup

stocks = ['AAPL', 'TSLA', 'AMZN', 'MSFT', 'NVDA', 'BAC']

#Long term growth
def get_long_term_growth(stock):
    try:
        url = f'https://www.alphaquery.com/stock/{stock}/all-data-variables'
        headers = {'Accept': 'text/html'}
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f"Error on get_long_term_growth request for {stock}: {res.status_code}")
        soup = BeautifulSoup(res.text, 'lxml')
        pe = soup.find_all('td', class_='text-right')[164]
        peg = soup.findAll('td', class_='text-right')[166]
        lt_growth = (float(pe.text) / float(peg.text))
        return round(lt_growth, 2)
    except:
        print(f"Unable to get growth rate: {stock}")

#Stock beta
def get_beta(stock):
    try:
        url = f'https://www.marketwatch.com/investing/stock/{stock}?mod=search_symbol'
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Error on get_beta request for {stock}: {res.status_code}")
        soup = BeautifulSoup(res.text, 'lxml')
        beta = soup.findAll('li', class_="kv__item")[6]
        beta = float(beta.text[5:].strip())
        return beta
    except:
       print(f"Unable to get beta: {stock}")

#Total Dividend Payout Over 12 Years
def get_dividend(stock):
    try:
        url = f'https://www.marketwatch.com/investing/stock/{stock}?mod=quote_search'
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Error on get_divident request for {stock}: {res.status_code}")
        soup = BeautifulSoup(res.text, 'lxml')
        d = soup.findAll('span', class_='primary')[17]
        d = str(d.text).replace('$', '')
        dividend = (float(d) * 4 * 12)
        return dividend
    except:
        return 0

#Total assets
def get_cash(stock):
    try:
        url = f'https://www.marketwatch.com/investing/stock/{stock}/financials/balance-sheet'
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Error on get_cash request for {stock}: {res.status_code}")
        soup = BeautifulSoup(res.text, 'lxml')
        cash = soup.findAll('div', class_="cell__content")[166]
        cash = cash.text[::].strip()
        if 'M' in cash:
            cash = float(cash[:-1]) * 1000000
        elif 'B' in cash:
            cash = float(cash[:-1]) * 1000000000
        return cash
    except:
        print(f"Unable to get total cash: {stock}")

#Total liabilities
def get_debt(stock):
    try:
        url = f'https://www.marketwatch.com/investing/stock/{stock}/financials/balance-sheet'
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Error on get_debt request for {stock}: {res.status_code}")
        soup = BeautifulSoup(res.text, 'lxml')
        debt = soup.findAll('div', class_="cell__content")[390]
        debt = debt.text[::].strip()
        if 'M' in debt:
            debt = float(debt[:-1]) * 1000000
        elif 'B' in debt:
            debt = float(debt[:-1]) * 1000000000
        return debt
    except:
        print(f"Unable to get total debt: {stock}")

#Operating cash flow
def get_operating_cash(stock):
    try:
        url = f'https://www.marketwatch.com/investing/stock/{stock}/financials/cash-flow'
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Error on get_operating_cash request for {stock}: {res.status_code}")
        soup = BeautifulSoup(res.text, 'lxml')
        operating = soup.findAll('div', class_="cell__content")[134]
        operating = operating.text[::].strip()
        if 'M' in operating:
            operating = float(operating[:-1]) * 1000000
        elif 'B' in operating:
            operating = float(operating[:-1]) * 1000000000
        return operating
    except:
        print(f"Unable to get operating cash: {stock}")

#Shares outstanding
def get_shares_outstanding(stock):
    try:
        url = f'https://www.marketwatch.com/investing/{stock}/aapl?mod=search_symbol'
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Error on get_shares_outstanding request for {stock}: {res.status_code}")
        soup = BeautifulSoup(res.text, 'lxml')
        so = soup.findAll('li', class_="kv__item")[4]
        so = so.text[20:].strip()
        if 'M' in so:
            so = float(so[:-1]) * 1000000
        elif 'B' in so:
            so = float(so[:-1]) * 1000000000
        return so
    except:
        print(f"Unable to get shares outstanding: {stock}")

#Discount rate
def get_discount_rate(stock):
    try:
        beta = get_beta(stock)
        if beta < .80:
            discount_rate = .05
        elif .80 < beta <= 1:
            discount_rate = .06
        elif 1 < beta <= 1.1:
            discount_rate = .065
        elif 1.1 < beta <= 1.2:
            discount_rate = .07
        elif 1.2 < beta <= 1.3:
            discount_rate = .075
        elif 1.3 < beta <= 1.4:
            discount_rate = .08
        elif 1.4 < beta <= 1.5999:
            discount_rate = .085
        else:
            discount_rate = .09
        return discount_rate
    except:
        print(f"Unable to calculate discount rate: {stock}")
def get_intrinsic_value(stock):
    if get_long_term_growth(stock):
        lt_growth = get_long_term_growth(stock) / 100
    if get_operating_cash(stock):
        total_cash_by_yr = [get_operating_cash(stock)]
    if get_operating_cash(stock) > 0:
        x = 0
        while x < 16:
            total_cash_by_yr.append(total_cash_by_yr[-1] * (1 + lt_growth))
            x += 1
        total_cash_by_yr.pop(-1)
    discount_rates_by_year = []
    x = 1
    while x < 16:
        discount_rates_by_year.append(1 / (1 + get_discount_rate(stock)) ** x)
        x += 1
    net_discounted_cash_by_yr = []
    x = 0
    while x < 15:
        net_discounted_cash_by_yr.append(discount_rates_by_year[x] * total_cash_by_yr[x])
        x += 1
    total_cash_net = sum(net_discounted_cash_by_yr)
    if get_shares_outstanding(stock):
        gross_intrinsic_value = total_cash_net / get_shares_outstanding(stock)
        cash_per_share = get_cash(stock) / get_shares_outstanding(stock)
        debt_per_share = get_debt(stock) / get_shares_outstanding(stock)
    total_dividend_payout = get_dividend(stock)
    intrinsic_value = round(gross_intrinsic_value + total_dividend_payout + cash_per_share - debt_per_share, 2)
    return intrinsic_value

def get_current_price(stock):
    try:
        url = f'https://www.marketwatch.com/investing/stock/{stock}?mod=search_symbol'
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Error on current price URL for {stock}: {res.status_code}")
        soup = BeautifulSoup(res.text, 'lxml')
        cp = soup.findAll('li', class_="kv__item")[0]
        cp = cp.text[7:].strip()
        return float(cp)
    except:
        print(f"Unable to get current price: {stock}")

def get_discount(stock):
    discount = round(((get_intrinsic_value(stock) - get_current_price(stock)) * 100), 2)
    if discount > 50:
        recommendation = 'Strong Buy'
    elif 15 <= discount <= 50:
        recommendation = "Buy"
    elif -15 < discount < 15:
        recommendation = "Hold"
    elif -50 < discount <= -15:
        recommendation = "Sell"
    else:
        recommendation = "Strong Sell"
    return recommendation

def main():
    for stock in stocks:
        try:
            print(f"{stock} {get_long_term_growth(stock)} {get_dividend(stock)} {get_intrinsic_value(stock)}")
        except:
            continue

if __name__ == "__main__":
    main()
