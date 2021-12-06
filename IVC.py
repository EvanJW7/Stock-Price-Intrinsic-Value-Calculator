#ENTER ANY NUMBER OF STOCKS YOU WANT
stocks = ['SPOT', 'AAPL', 'COIN', 'ZM', 'AMZN', 'NFLX', 'SHOP', 'TSLA', 'LC', 'NVDA', 'F', 'WMT']
data = list()
import requests
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup
print ("{:<6} {:>13} {:>20} {:>18} {:>13} {:>18}".format('Stock','Est.Growth','Intrinsic Value','Current Price','Discount', 'Recommendation'))
print('----------------------------------------------------------------------------------------------')
for stock in stocks:
    #EPS
    try:
        url = f'https://www.alphaquery.com/stock/{stock}/all-data-variables'
        headers = {'Accept': 'text/html'}
        res = requests.get(url, headers = headers)
        soup = BeautifulSoup(res.text, 'lxml')
        PE = soup.find_all('td', class_ = 'text-right')[164]
        PEG = soup.findAll('td', class_ = 'text-right')[166]
        LTGrowth = (float(PE.text)/float(PEG.text))
        LTGrowth = round(LTGrowth, 2)
    except:
        continue 
    
    #PREVIOUS OPERATING CASH GROWTH
    try:
        url = f'http://www.aastocks.com/en/usq/analysis/company-fundamental/cash-flow?symbol={stock}'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        point1 = float(soup.findAll('td')[130].text.replace(',',''))
        point2 = float(soup.findAll('td')[131].text.replace(',',''))
        point3 = float(soup.findAll('td')[132].text.replace(',',''))
        point4 = float(soup.findAll('td')[133].text.replace(',',''))
        point5 = float(soup.findAll('td')[134].text.replace(',',''))
     
        growth1 = ((point2-point1)/abs(point1))*100
        if growth1 > 100:
            growth1 = 100
        elif growth1 <-100:
            growth1 = -100
        growth2 = ((point3-point2)/abs(point2))*100
        if growth2 > 100:
            growth2 = 100
        elif growth2 <-100:
            growth2 = -100
        growth3 = ((point4-point3)/abs(point3))*100
        if growth3 > 100:
            growth3 = 100
        elif growth3 <-100:
            growth3 = -100
        growth4 = ((point5-point4)/abs(point4))*100
        if growth4 > 100:
            growth4 = 100
        elif growth4 <-100:
            growth4 = -100
        
        operating_cash_growth = ((growth1+growth2+growth3+growth4)/4)
        operating_cash_growth = round(operating_cash_growth, 2)
        
        if point1<point2 and point2<point3 and point3<point4 and point4<point5:
            actual_growth = LTGrowth*.75 + operating_cash_growth*.25
        else:
            actual_growth = LTGrowth*.50 + operating_cash_growth*.50
    except:
        actual_growth = LTGrowth

    #DIVIDEND
    try:
        url = f'https://www.marketwatch.com/investing/stock/{stock}?mod=quote_search'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        divid = soup.findAll('span', class_ = 'primary')[17]
        divid = str(divid.text).replace('$', '')
        dividend = (float(divid)*4*10)
    except:
        dividend = 0

    #OPERATING CASH TTM 
    try:
        stock = yf.Ticker(stock)
        operating_cash = float(stock.info['operatingCashflow']) 
    except ValueError:
        url = f'http://www.aastocks.com/en/usq/analysis/company-fundamental/cash-flow?symbol={stock}'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        cash = soup.findAll('td')[134].text
        operating_cash = float(cash.replace(',',''))*1000000
    except:
        continue
    
   
   
   #CURRENT DISCOUNT RATE
    try:
        beta = stock.info['beta']
        if beta < .80:
            discountrate = .05
        elif .80<beta<=1:
            discountrate = .06
        elif 1<beta<=1.1:
            discountrate = .065
        elif 1.1<beta<=1.2:
            discountrate = .07
        elif 1.2<beta<=1.3:
            discountrate = .075
        elif 1.3<beta<=1.4:
            discountrate = .08
        elif 1.4<beta<=1.5999:
            discountrate = .085
        else:
            discountrate = .09
    except:
        discountrate = .06
        
    #PROJECTED CASH FLOW BY YEAR
    actual_growth = actual_growth/100
    if operating_cash > 0:
        total_cash_yr1 = (operating_cash *(1+actual_growth))
        total_cash_yr2 = total_cash_yr1*(1+actual_growth)
        total_cash_yr3 = total_cash_yr2*(1+actual_growth)
        total_cash_yr4 = total_cash_yr3*(1+actual_growth)
        total_cash_yr5 = total_cash_yr4*(1+actual_growth)
        total_cash_yr6 = total_cash_yr5*(1+actual_growth)
        total_cash_yr7 = total_cash_yr6*(1+actual_growth)
        total_cash_yr8 = total_cash_yr7*(1+actual_growth)
        total_cash_yr9 = total_cash_yr8*(1+actual_growth)
        total_cash_yr10 = total_cash_yr9*(1+actual_growth)
    else:
        total_cash_yr1 = operating_cash
        #print(total_cash_yr1)
        total_cash_yr2 =  operating_cash - operating_cash*actual_growth
        #print(f'Cash yr 2: {total_cash_yr2}')
        total_cash_yr3 = total_cash_yr2 + ((operating_cash-total_cash_yr2)*-1)*(1+actual_growth)
        #print(total_cash_yr3)
        total_cash_yr4 = total_cash_yr3 + ((total_cash_yr2-total_cash_yr3)*-1)*(1+actual_growth)
        #print(total_cash_yr4)
        total_cash_yr5 = total_cash_yr4 + ((total_cash_yr3-total_cash_yr4)*-1)*(1+actual_growth)
        #print(total_cash_yr5)
        total_cash_yr6 = total_cash_yr5 + ((total_cash_yr4 - total_cash_yr5)*-1)*(1+actual_growth)
        #print(total_cash_yr6)
        total_cash_yr7 = total_cash_yr6 + ((total_cash_yr5 - total_cash_yr6)*-1)*(1+actual_growth)
        #print(total_cash_yr7)
        total_cash_yr8 = total_cash_yr7 + ((total_cash_yr6 - total_cash_yr7)*-1)*(1+actual_growth)
        #print(total_cash_yr8)
        total_cash_yr9 = total_cash_yr8 + ((total_cash_yr7- total_cash_yr8)*-1)*(1+actual_growth)
        #print(total_cash_yr9)
        total_cash_yr10 = total_cash_yr9 + ((total_cash_yr8 - total_cash_yr9)*-1)*(1+actual_growth)
        #print(total_cash_yr10)
    
    
    #DISCOUNT RATES PER YEAR
    dr1 = 1/(1+discountrate)
    dr2 = 1/(1+discountrate)**2
    dr3 = 1/(1+discountrate)**3
    dr4 = 1/(1+discountrate)**4
    dr5 = 1/(1+discountrate)**5
    dr6 = 1/(1+discountrate)**6
    dr7 = 1/(1+discountrate)**7
    dr8 = 1/(1+discountrate)**8
    dr9 = 1/(1+discountrate)**9
    dr10 = 1/(1+discountrate)**10
    
    #DISCOUNTED CASH BY YEAR
    net_yr1 = dr1 * total_cash_yr1
    net_yr2 = dr2 * total_cash_yr2
    net_yr3 = dr3 * total_cash_yr3
    net_yr4 = dr4 * total_cash_yr4
    net_yr5 = dr5 * total_cash_yr5
    net_yr6 = dr6 * total_cash_yr6
    net_yr7 = dr7 * total_cash_yr7
    net_yr8 = dr8 * total_cash_yr8
    net_yr9 = dr9 * total_cash_yr9
    net_yr10 = dr10 * total_cash_yr10
    
    #SHARES OUTSTANDING
    try:
        shares_outstanding = stock.info['sharesOutstanding']
    except:
        continue
    
    #COMPANY NAME
    company_name = stock.info['shortName']
    
    #TICKER SYMBOL
    symbol = stock.info['symbol']
    
    #TOTAL CASH
    try:
        total_cash_final = stock.info['totalCash']
        total_cash_final = float(total_cash_final)
    except:
        continue
        
    #TOTAL DEBT
    try:
        total_debt_final = stock.info['totalDebt']
        total_debt_final = float(total_debt_final)
    except:
        continue

    #TOTAL CASH FLOW OVER 10 YEARS
    total_net_cash = net_yr1 + net_yr2 + net_yr3 + net_yr4 + net_yr5 + net_yr6 +net_yr7+net_yr8+net_yr9 + net_yr10
    
    #GROSS INTRINSIC VALUE
    try:
        gross_intrinsic_value = total_net_cash/shares_outstanding
    except:
        continue
    
    #CASH PER SHARE
    cash_per_share = total_cash_final/shares_outstanding
    
    #DEBT PER SHARE
    debt_per_share = total_debt_final/shares_outstanding
    
    #FINAL
    intrinsic_value_final = gross_intrinsic_value + dividend + cash_per_share - debt_per_share
    intrinsic_value_final = "{:.2f}".format(intrinsic_value_final)
    intrinsic_value_final = float(intrinsic_value_final)
    if intrinsic_value_final <0:
        intrinsic_value_final = 0
        
    #currentprice
    current_price = stock.info['currentPrice']
    current_price = round(current_price, 2)

    discount = ((intrinsic_value_final-current_price)/current_price)*100

    #OPTIONAL DATAFRAME FORMAT OF THE DATA, USE THIS IF YOU WANT TO EXPORT TO EXCEL
    data.append({
        'Company': company_name,
        'Ticker': symbol,
        'Proj. EPS Growth': "{:.1f}".format(LTGrowth),
        'Final Growth': "{:.1f}".format(actual_growth),
        'Stock Intrinsic Value': intrinsic_value_final,
        'Current Price': current_price,
        'Discount %': "{:.1f}".format(discount)
    })
    df = pd.DataFrame(data)
   

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
    
    actual_growth = round(actual_growth*100, 2)
    discount = round(discount, 2)
   
    print(f"{symbol:<5}{actual_growth:>12}%{intrinsic_value_final:>19}{current_price:>20}{discount:>15}%{recommendation:>18}")

    
