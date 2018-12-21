from django.shortcuts import render
from django.http import JsonResponse

#importing packages
import requests
from nsepy import get_history
import pandas as pd
from datetime import datetime,date,timedelta, time

fnoStocks = []
# Create your views here.

def show_html(request):
	if request.method == "GET":
		global fnoStocks
		fnoStocks = []
		#Fetch FNO Stocks
		url= 'https://www.nseindia.com/live_market/dynaContent/live_watch/stock_watch/foSecStockWatch.json'
		r = requests.get(url)
		data = r.json()
		stockList = data['data']
		for symbol in stockList:
			fno = (symbol['symbol'])
			fnoStocks.append(fno)
		fnoStocks.sort()
		
		try:
			print("In try...")
			today = date.today()
			data_complete = pd.read_csv("data_complete"+str(today)+".csv", index_col = False)
		except:
			print("In except...")
			#Identify Correct Dates
			nse_holidays = [date(2018,1,26),date(2018,2,13),date(2018,2,19),date(2018,3,2),date(2018,3,29),date(2018,3,30),date(2018,4,30),date(2018,5,1),date(2018,8,15),date(2018,8,17),date(2018,8,22),date(2018,9,13),date(2018,9,20),date(2018,10,2),date(2018,10,18),date(2018,11,7),date(2018,11,8),date(2018,11,9),date(2018,11,23),date(2018,12,25)]
			today = date.today()
			days_7 = []
			day_offset = 1
			sev_days = 0
			while True:
				required_date = today - timedelta(days=day_offset)
				day_offset+=1
				if(required_date.weekday() < 5 and required_date not in nse_holidays):
					days_7.append(required_date)
				sev_days = len(days_7)
				if(sev_days>6):
					break
			#dataframe containing complete stock details
			data_complete = pd.DataFrame(columns = ['Date', 'Symbol', 'Series', 'Prev Close', 'Open', 'High', 'Low', 'Last', 'Close', 'VWAP', 'Volume', 'Turnover', 'Trades', 'Deliverable Volume','%Deliverble'])
			for stock in fnoStocks:
				try:
					print(stock)
					data_latest = get_history(symbol=stock, start=days_7[6], end=days_7[0])
					data_latest = data_latest.reset_index()
					data_complete = pd.concat([data_complete,data_latest])
				except:
					pass
			
			data_complete.to_csv("data_complete"+str(today)+".csv")

	return render(request,'weekend/week_end.html')


def high(request):
	if request.method == "GET":
		Weekend6 = []
		Weekend5 = []
		Weekend4 = []
		Weekend3 = []
		Weekend2 = []
		Weekend1 = []
		today = date.today()
		data_complete = pd.read_csv("data_complete"+str(today)+".csv")
		data_complete = data_complete.set_index('Unnamed: 0') 
		print("Data_complete")
		print(data_complete)
		print("FNO Stocks")
		print(fnoStocks)
		#weekend
		for stock in fnoStocks:
			try:
#Weekend High
				if (data_complete.loc[data_complete['Symbol'] == stock]['High'][6]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][5]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][4]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][3]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][2]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][1]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][0]):
					Weekend6.append(stock)
				
				if (data_complete.loc[data_complete['Symbol'] == stock]['High'][6]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][5]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][4]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][3]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][2]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][1] and
					stock not in Weekend6):
					Weekend5.append(stock)
				
				if (data_complete.loc[data_complete['Symbol'] == stock]['High'][6]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][5]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][4]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][3]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][2] and
					stock not in Weekend5 and stock not in Weekend6):
					Weekend4.append(stock)
				
				if (data_complete.loc[data_complete['Symbol'] == stock]['High'][6]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][5]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][4]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][3] and
					stock not in Weekend4 and stock not in Weekend5 and stock not in Weekend6):
					Weekend3.append(stock)
				
				if (data_complete.loc[data_complete['Symbol'] == stock]['High'][6]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][5]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][4] and
					stock not in Weekend3 and stock not in Weekend4 and stock not in Weekend5 and stock not in Weekend6):
					Weekend2.append(stock)
				
				if (data_complete.loc[data_complete['Symbol'] == stock]['High'][6]<
					data_complete.loc[data_complete['Symbol'] == stock]['High'][5] and
					stock not in Weekend2 and stock not in Weekend3 and stock not in Weekend4 and stock not in Weekend5 and stock not in Weekend6):
					Weekend1.append(stock)


			except:
				pass

		#Fetch stock values  
		print("=================================================")
		print('Stocks in Weekend High Level 1')
		print(*Weekend1,sep ='   ')
		print("=================================================")
		print('Stocks in Weekend High Level 2')
		print(*Weekend2,sep ='   ')
		print("=================================================")
		print('Stocks in Weekend High Level 3')
		print(*Weekend3,sep ='   ')
		print("=================================================")
		print('Stocks in Weekend High Level 4')
		print(*Weekend4,sep ='   ')
		print("=================================================")
		print('Stocks in Weekend High Level 5')
		print(*Weekend5,sep ='   ')
		print("=================================================")
		print('Stocks in Weekend High Level 6')
		print(*Weekend6,sep ='   ')
		
		#Initialise Weekend High Dictionary
		weekendhigh = {}
		weekendhigh["Weekend_6"] = {}
		weekendhigh["Weekend_5"] = {}
		weekendhigh["Weekend_4"] = {}
		weekendhigh["Weekend_3"] = {}
		weekendhigh["Weekend_2"] = {}
		weekendhigh["Weekend_1"] = {}
        #Add price info to the result
		for stock in Weekend6:
			price = data_complete.loc[data_complete['Symbol'] == stock]['High'][6]
			price_info = {stock:price}
			weekendhigh["Weekend_6"].update(price_info)
		for stock in Weekend5:
			price = data_complete.loc[data_complete['Symbol'] == stock]['High'][6]
			price_info = {stock:price}
			weekendhigh["Weekend_5"].update(price_info)
		for stock in Weekend4:
			price = data_complete.loc[data_complete['Symbol'] == stock]['High'][6]
			price_info = {stock:price}
			weekendhigh["Weekend_4"].update(price_info)
		for stock in Weekend3:
			price = data_complete.loc[data_complete['Symbol'] == stock]['High'][6]
			price_info = {stock:price}
			weekendhigh["Weekend_3"].update(price_info)
		for stock in Weekend2:
			price = data_complete.loc[data_complete['Symbol'] == stock]['High'][6]
			price_info = {stock:price}
			weekendhigh["Weekend_2"].update(price_info)
		for stock in Weekend1:
			price = data_complete.loc[data_complete['Symbol'] == stock]['High'][6]
			price_info = {stock:price}
			weekendhigh["Weekend_1"].update(price_info)



	return JsonResponse(weekendhigh)

def low(request):
    if request.method == "GET":
        Weekend6_Low = []
        Weekend5_Low = []
        Weekend4_Low = []
        Weekend3_Low = []
        Weekend2_Low = []
        Weekend1_Low = []        
        today = date.today()		
        data_complete = pd.read_csv("data_complete"+str(today)+".csv")
        data_complete = data_complete.set_index('Unnamed: 0') 
        print("Data_complete")
        print(data_complete)
        print("FNO Stocks")
        print(fnoStocks)
        #weekend
        for stock in fnoStocks:
            try:
        
                if(data_complete.loc[data_complete['Symbol'] == stock]['Low'][6]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][5]>    
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][4]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][3]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][2]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][1]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][0]):    
                    Weekend6_Low.append(stock)    
        
                if (data_complete.loc[data_complete['Symbol'] == stock]['Low'][6]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][5]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][4]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][3]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][2]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][1] and
                    stock not in Weekend6_Low):
                    Weekend5_Low.append(stock)
                
                if (data_complete.loc[data_complete['Symbol'] == stock]['Low'][6]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][5]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][4]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][3]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][2] and
                    stock not in Weekend5_Low and stock not in Weekend6_Low):
                    Weekend4_Low.append(stock)
                
                if (data_complete.loc[data_complete['Symbol'] == stock]['Low'][6]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][5]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][4]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][3] and
                    stock not in Weekend4_Low and stock not in Weekend5_Low and stock not in Weekend6_Low):
                    Weekend3_Low.append(stock)
                
                if (data_complete.loc[data_complete['Symbol'] == stock]['Low'][6]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][5]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][4] and
                    stock not in Weekend3_Low and stock not in Weekend4_Low and stock not in Weekend5_Low and stock not in Weekend6_Low):
                    Weekend2_Low.append(stock)
                
                if (data_complete.loc[data_complete['Symbol'] == stock]['Low'][6]>
                    data_complete.loc[data_complete['Symbol'] == stock]['Low'][5] and
                    stock not in Weekend2_Low and stock not in Weekend3_Low and stock not in Weekend4_Low and stock not in Weekend5_Low and stock not in Weekend6_Low):
                    Weekend1_Low.append(stock)


            except:
                pass

        #Fetch stock values  
        print("=================================================")
        print('Stocks in Weekend Low Level 1')
        print(*Weekend1_Low,sep ='   ')
        print("=================================================")
        print('Stocks in Weekend Low Level 2')
        print(*Weekend2_Low,sep ='   ')
        print("=================================================")
        print('Stocks in Weekend Low Level 3')
        print(*Weekend3_Low,sep ='   ')
        print("=================================================")
        print('Stocks in Weekend Low Level 4')
        print(*Weekend4_Low,sep ='   ')
        print("=================================================")
        print('Stocks in Weekend Low Level 5')
        print(*Weekend5_Low,sep ='   ')
        print("=================================================")
        print('Stocks in Weekend Low Level 6')
        print(*Weekend6_Low,sep ='   ')			

        #Initialise Weekend High Dictionary
        weekendlow = {}
        weekendlow["Weekend_6"] = {}
        weekendlow["Weekend_5"] = {}
        weekendlow["Weekend_4"] = {}
        weekendlow["Weekend_3"] = {}
        weekendlow["Weekend_2"] = {}
        weekendlow["Weekend_1"] = {}
        
        #Add price info to the result
        for stock in Weekend6_Low:
            price = data_complete.loc[data_complete['Symbol'] == stock]['Low'][6]
            price_info = {stock:price}
            weekendlow["Weekend_6"].update(price_info)
        for stock in Weekend5_Low:
            price = data_complete.loc[data_complete['Symbol'] == stock]['Low'][6]
            price_info = {stock:price}
            weekendlow["Weekend_5"].update(price_info)
        for stock in Weekend4_Low:
            price = data_complete.loc[data_complete['Symbol'] == stock]['Low'][6]
            price_info = {stock:price}
            weekendlow["Weekend_4"].update(price_info)
        for stock in Weekend3_Low:
            price = data_complete.loc[data_complete['Symbol'] == stock]['Low'][6]
            price_info = {stock:price}
            weekendlow["Weekend_3"].update(price_info)
        for stock in Weekend2_Low:
            price = data_complete.loc[data_complete['Symbol'] == stock]['Low'][6]
            price_info = {stock:price}
            weekendlow["Weekend_2"].update(price_info)
        for stock in Weekend1_Low:
            price = data_complete.loc[data_complete['Symbol'] == stock]['Low'][6]
            price_info = {stock:price}
            weekendlow["Weekend_1"].update(price_info)        

    return JsonResponse(weekendlow)