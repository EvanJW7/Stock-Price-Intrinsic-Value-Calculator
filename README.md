# IntrinsicValueCalculator
Stock price intrinsic value calculator
stocks = ['TSLA', 'SPOT', 'ZM', 'ROKU']
data = list()
import requests
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup
for stock in stocks:
    #EPS
    try:
        url = f'https://www.marketwatch.com/investing/stock/{stock}/analystestimates?mod=mw_quote_tab'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        nextyear = float(soup.findAll('th', class_ = "table__cell")[9].text.replace(',',''))
        nextyear2 = float(soup.findAll('th', class_ = "table__cell")[10].text.replace(',',''))
        if nextyear2 == 0:
            nextyear2 = .01
        nextyear3 = float(soup.findAll('th', class_ = "table__cell")[11].text.replace(',',''))
        if nextyear3 == 0:
            nextyear3 = .01
        a = 100 - (nextyear/nextyear2)*100
        b = 100 - (nextyear2/nextyear3)*100
        EPSGrowth = (a+b)/2
        EPSGrowth = float(format(EPSGrowth, ".4"))
        if EPSGrowth >100:
            EPSGrowth = (EPSGrowth*.005)+100
        if EPSGrowth < -100:
            EPSGrowth = (EPSGrowth*.05)-100
    except:
        EPSGrowth = 10
    #PREVIOUS OPERATING CASH GROWTH
    try:
        url = f'http://www.aastocks.com/en/usq/analysis/company-fundamental/cash-flow?symbol={stock}'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        point1 = float(soup.findAll('td')[131].text.replace(',',''))
        point2 = float(soup.findAll('td')[132].text.replace(',',''))
        point3 = float(soup.findAll('td')[133].text.replace(',',''))
        point4 = float(soup.findAll('td')[134].text.replace(',',''))
        if point1 <0:
            growth1 = ((point2-point1)/point1)*-1
        else:
            growth1 = (point2-point1)/point1
        if point2 <0:
            growth2 = ((point3-point2)/point2)*-1
        else:
            growth2 = (point3-point2)/point2
        if point3 <0:
            growth3 = ((point4-point3)/point3)*-1
        else:
            growth3 = (point4-point3)/point3
        growth_final = ((growth1*.10 + growth2*.30 + growth3*.60)*100)
    except:
        growth_final = EPSGrowth
    actual_growth = EPSGrowth*.90 + growth_final*.10
    if stock == 'COIN':
        actual_growth = 0
    growth6to10 = actual_growth * .50
    
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
        if .80<beta<=1:
            discountrate = .06
        if 1<beta<=1.1:
            discountrate = .065
        if 1.1<beta<=1.2:
            discountrate = .07
        if 1.2<beta<=1.3:
            discountrate = .075
        if 1.3<beta<=1.4:
            discountrate = .08
        if 1.4<beta<=1.5999:
            discountrate = .085
        if beta>= 1.6:
            discountrate = .09
    except:
        discountrate = .06
      
    #PROJECTED CASH FLOW BY YEAR
    total_cash_yr1 = operating_cash *(1+actual_growth/100)
    total_cash_yr2 = total_cash_yr1*(1+actual_growth/100)
    total_cash_yr3 = total_cash_yr2*(1+actual_growth/100)
    total_cash_yr4 = total_cash_yr3*(1+actual_growth/100)
    total_cash_yr5 = total_cash_yr4*(1+actual_growth/100)
    total_cash_yr6 = total_cash_yr5*(1+growth6to10/100)
    total_cash_yr7 = total_cash_yr6*(1+growth6to10/100)
    total_cash_yr8 = total_cash_yr7*(1+growth6to10/100)
    total_cash_yr9 = total_cash_yr8*(1+growth6to10/100)
    total_cash_yr10 = total_cash_yr9*(1+growth6to10/100)
    
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
    except KeyError:
        continue
    #COMPANY NAME
    company = stock.info['shortName']
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
    #GROSS
    gross_intrinsic_value = total_net_cash/shares_outstanding
    #CASH PER SHARE
    cash_per_share = total_cash_final/shares_outstanding
    #DEBT PER SHARE
    debt_per_share = total_debt_final/shares_outstanding
    #FINAL
    intrinsic_value_final = gross_intrinsic_value + cash_per_share - debt_per_share
    intrinsic_value_final = "{:.2f}".format(intrinsic_value_final)
    intrinsic_value_final = float(intrinsic_value_final)
    #currentprice

    current_price = stock.info['currentPrice']
    current_price = round(current_price, 2)
    company_name = stock.info['shortName']
    discount = ((intrinsic_value_final-current_price)/current_price)*100
    data.append({
        'Company': company_name,
        'Ticker': symbol,
        'Proj. EPS Growth': "{:.1f}".format(EPSGrowth),
        'Prev. OC Growth': "{:.1f}".format(growth_final),
        'Final Growth': "{:.1f}".format(actual_growth),
        'Stock Intrinsic Value': intrinsic_value_final,
        'Current Price': current_price,
        'Discount %': "{:.1f}".format(discount)
    })
df = pd.DataFrame(data)
df
