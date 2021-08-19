# IntrinsicValueCalculator
Stock price intrinsic value calculator
#ENTER ANY NUMBER OF STOCKS YOU WANT, THIS JUST HAPPENS TO BE THE SP500
stocks = ['AAPL','MSFT','AMZN','MRK','GOOG','GOOGL','FB','TSLA','V','JPM','JNJ','SHOP', 'JD', 'NIO', 'WMT','NVDA',
          'PYPL','MA','DIS','PG','UNH','HD','BAC','INTC','NFLX','CMCSA','ADBE','CRM','ABT','VZ','NKE','XOM',
          'KO','T','AVGO','TMO','LLY','CSCO','PFE','PEP','ABBV','ORCL','CVX','DHR','ACN','QCOM','TXN','MDT','MCD',
          'NEE','COST','TMUS','WFC','UNP','HON','UPS','MS','AMGN','PM','C','BMY','LIN','LOW','BA','SBUX','CHTR','INTU',
          'NOW','SCHW','BLK','AMD','RTX','CAT','AMAT','GS','EL','IBM','AXP','GE','MMM','AMT','DE','MU','TGT','LMT',
          'SYK','ISRG','CVS','BKNG','LRCX','FIS','SPGI','GILD','TJX','MO','ATVI','ZTS','PLD','MDLZ','GM','TFC','BDX',
          'CB','FISV','USB','PNC','ANTM','ILMN','CI','ADP','CCI','FDX','CSX','CME','ADSK','CL','COP','DUK','NSC',]
          #'SHW','ICE','ITW','SO','EQIX','ECL','ADI','GPN','HCA','TWTR','MMC','D','APD','COF','VRTX','EW','BSX',
          #'MCO','KLAC','AON','REGN','EMR','MET','ETN','PGR','HUM','DG','MNST','NOC','ALGN','FCX','WM','GD','NEM',
          #'IDXX','F','STZ','SNPS','KMB','LVS','DOW','MCHP','TEL','KHC','EBAY','ROST','BIIB','WBA','MAR','EA','APTV',
          #'CMG','EXC','CDNS','APH','CTSH','ROP','PSA','BAX','A','SYY','DXCM','AEP','LHX','DLR','DD','JCI','BK','SLB'
          #'TROW','TRV','INFO','EOG','VIAC','IQV','MSCI','AIG','CTAS','CMI','SPG','TT','SRE','PH','HPQ','XLNX',
          #'PSX','ANSS','GIS','KMI','IFF','MPC','CNC','CTVA','PCAR','ZBH','AFL','PRU','LYB','XEL','PPG','CARR','PAYX',
          #'SWKS','YUM','VFC','HLT','HSY','ALL','BBY','ORLY','ADM','TDG','MSI','LUV','VRSK','GLW','BLL','DFS','PXD',
          #'WLTW','PEG','AWK','ROK','SBAC','RSG','ETSY','DHI','MCK','ES','DAL','MTD','RMD','KEYS','FRC','WELL','CPRT',
          #'AME','WMB','SWK','OTIS','VLO','SIVB','LEN','FAST','FTNT','AZO','STT','WY','ZBRA','MXIM','AMP','KR',
          #'WEC','HRL','GRMN','DLTR','CCL','EQR','AVB','ODFL','OXY','ENPH','ANET','BKR','TSN','FITB','TER','ED',
          #'CBRE','NDAQ','FTV','DTE','ARE','MKC','CLX','O','LH','AJG','VRSN','FLT','TTWO','PAYC','CERN','CDW','VTRS',
          #'SYF','WST','EIX','PPL','VMC','HOLX','EXPE','EFX','ABC','DISCK','DISCA','CTLT','URI','NTRS','OKE','MKTX',
          #'WDC','MLM','QRVO','CHD','KMX','GWW','K','RF','IP','KEY','BIO','AES','KSU','MTB','TYL','COO','HES','ALB',
          #'TSCO','VTR','TFX','TRMB','ETR','FOX','FOXA','HPE','ULTA','HAL','IR','CFG','LYV','ROL','INCY','AEE','XYL',
          #'RCL','AMCR','FE','WAT','MPWR','HIG','ESS','DOV','NUE','MGM','NVR','DISH','BR','CTXS','STX','DRI',
          #'CAG','DGX','PKI','PEAK','RJF','VAR','AKAM','CMS','IT','MAA','EXPD','STE','JBHT','DRE','EXR','NTAP',
          #'CE','HBAN','WAB','CAH','LDOS','EMN','AVY','IEX','DPZ','PFG','J','GPC','CINF','ABMD','BXP','TDY','UAL',
          #'BEN','OMC','FMC','NWSA','DVN','WYNN','CPB','NWS','MAS','IPGP','POOL','L','LUMN','FFIV','SJM','PKG','UDR',
          #'NLOK','PHM','WHR','HAS','EVRG','HWM','MHK','WRB','CHRW','FBHS','LNT','XRAY','TXT','CNP','ATO','MOS','WRK',
          #'LKQ','DVA','LW','JKHY','AAL','HST','FANG','UHS','TPR','PWR','BWA','AAP','IVZ','LNC','SNA','ALLE','NWL',
          #'HSIC','NRG','WU','GL','IPG','CF','TAP','RE','AOS','IRM','UAA','UA','CMA','PNR','REG','GPS','NI','PNW',
          #'RHI','ZION','NLSN','RL','JNPR','NCLH','FRT','KIM','MRO','ALK','AIZ','COG','FLIR','VNO','HII','APA','PVH',
          #'SEE','PBCT','DXC','HBI','PRGO','NOV','LEG','VNT','HFC']
stocks_final = []
print ("{:<6} {:>1} {:>16} {:>14} {:>9}".format('Stock','Est.Growth','Intrinsic Value','Current Price','Discount'))
print('-----------------------------------------------------------')
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
        nextyear = soup.findAll('th', class_ = "table__cell")[9].text
        nextyear2 = soup.findAll('th', class_ = "table__cell")[10].text
        nextyear3 = soup.findAll('th', class_ = "table__cell")[11].text
        nextyear = float(nextyear)
        nextyear2 = float(nextyear2)
        nextyear3 = float(nextyear3)
        a = 100 - (nextyear/nextyear2)*100
        b = 100 - (nextyear2/nextyear3)*100
        EPSGrowth = (a+b)/2
        EPSGrowth = format(EPSGrowth, ".4")
        EPSGrowth = float(EPSGrowth)
        EPSGrowth6to10 = EPSGrowth * .75
    except:
        url = f'https://www.marketwatch.com/investing/stock/{stock}/analystestimates?mod=mw_quote_tab'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        nextyear = soup.findAll('th', class_ = "table__cell")[18].text
        nextyear2 = soup.findAll('th', class_ = "table__cell")[19].text
        nextyear3 = soup.findAll('th', class_ = "table__cell")[20].text
        nextyear = float(nextyear)
        nextyear2 = float(nextyear2)
        nextyear3 = float(nextyear3)
        a = 100 - (nextyear/nextyear2)*100
        b = 100 - (nextyear2/nextyear3)*100
        EPSGrowth = (a+b)/2
        EPSGrowth = format(EPSGrowth, ".4")
        EPSGrowth = float(EPSGrowth)
        EPSGrowth6to10 = EPSGrowth * .75 
    #OPERATING CASH TTM
    try:
        stock = yf.Ticker(stock)
        operating_cash = stock.info['operatingCashflow']
        operating_cash = float(operating_cash)
        
    except:
        operating_cash = 0
    

        
    #CURRENT DISCOUNT RATE
    discountrate = (.25/100)
    
    #PROJECTED CASH FLOW BY YEAR
    total_cash_yr1 = operating_cash *(1+EPSGrowth/100)
    total_cash_yr2 = total_cash_yr1*(1+EPSGrowth/100)
    total_cash_yr3 = total_cash_yr2*(1+EPSGrowth/100)
    total_cash_yr4 = total_cash_yr3*(1+EPSGrowth/100)
    total_cash_yr5 = total_cash_yr4*(1+EPSGrowth/100)
    total_cash_yr6 = total_cash_yr5*(1+EPSGrowth6to10/100)
    total_cash_yr7 = total_cash_yr6*(1+EPSGrowth6to10/100)
    total_cash_yr8 = total_cash_yr7*(1+EPSGrowth6to10/100)
    total_cash_yr9 = total_cash_yr8*(1+EPSGrowth6to10/100)
    total_cash_yr10 = total_cash_yr9*(1+EPSGrowth6to10/100)
    
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
        total_cash_final = 2000000000
        total_cash_final = float(total_cash_final)
        
    #TOTAL DEBT
    try:
        total_debt_final = stock.info['totalDebt']
        total_debt_final = float(total_debt_final)
    except:
        total_debt_final = 1000000000
        total_debt_final = float(total_debt_final)
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
    try: 
        current_price = stock.info['bid']
        current_price = float(current_price)
        if current_price == 0:
            current_price = current_price + 1000
    except: 
        current_price = 1000
        
    discount = ((intrinsic_value_final-current_price)/current_price)*100
    discount = "{:.2f}".format(discount)
    stock = stock
    stocks_final.append([symbol, intrinsic_value_final, current_price, discount])
    datalist = [symbol, intrinsic_value_final, current_price, discount]
    
    print(f"{symbol:<5}{EPSGrowth:>9}%{intrinsic_value_final:>14}{current_price:>16}{discount:>13}%")
