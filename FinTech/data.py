import benchmarks
import api
import pandas as pd
import datetime
import json
from smartapi import SmartConnect


# ONE_MINUTE	   1 Minute
# THREE_MINUTE	   3 Minute
# FIVE_MINUTE	   5 Minute
# TEN_MINUTE	   10 Minute
# FIFTEEN_MINUTE   15 Minute
# THIRTY_MINUTE	   30 Minute
# ONE_HOUR	       1 Hour
# ONE_DAY	       1 Day


# Interval         	Max Days in one Request
# ONE_MINUTE	    30
# THREE_MINUTE	    90
# FIVE_MINUTE    	90
# TEN_MINUTE	    90
# FIFTEEN_MINUTE	180
# THIRTY_MINUTE	    180
# ONE_HOUR       	365
# ONE_DAY	        2000


#URL:               https://smartapi.angelbroking.com/docs/Historical

#Example:           https://github.com/angelbroking-github/smartapi-python

#Credential.Json


''' 
{
API_KEY   : "XYX",
CLIENT_ID : "XYX",
PASSWD    : "XYX",
}
'''

# from smartapi import SmartConnect #or from smartapi.smartConnect import SmartConnect
# #import smartapi.smartExceptions(for smartExceptions)

# #create object of call
# obj=SmartConnect(api_key="your api key",
#                 #optional
#                 #access_token = "your access token",
#                 #refresh_token = "your refresh_token")

# #login api call

# data = obj.generateSession("Your Client ID","Your Password")

# try:
#     status=["FORALL"] #should be a list
#     page=1
#     count=10
#     lists=obj.gttLists(status,page,count)
# except Exception as e:
#     print("GTT Rule List failed: {}".format(e.message))

# #Historic api
# try:
#     historicParam={
#     "exchange": "NSE",
#     "symboltoken": "3045",
#     "interval": "ONE_MINUTE",
#     "fromdate": "2021-02-08 09:00", 
#     "todate": "2021-02-08 09:16"
#     }
#     obj.getCandleData(historicParam)

Angelheader = {
    "exchange": "NSE",
    "symboltoken": "3045",
    "interval": "ONE_MINUTE",
    "fromdate": "2021-02-10 09:15",
    "todate": "2021-02-10 09:16"
}

class GetEODDataQuandel:
    def __init__(self,index,cacheing=False,time='max'):
        self.benchmark = benchmarks.Benchmarks(cacheing)
        self.index     = index
        self.time      = time

    def run(self):
        assert self.index in self.benchmark.supported_benchmarks, 'Supported Benchmarks : {} '.format(self.benchmark.supported_benchmarks)     
        stock_frame  = getattr(self.benchmark,self.index)()
        eod_data     = {}
        dates        = set()
        
        for i in range(stock_frame.shape[0]):
            
            bse_code                                         = stock_frame['BSE_CODES'][i]
            eod_data[stock_frame["Symbol"][i]]               = {}
            eod_data[stock_frame["Symbol"][i]]["Date"]       = []
            eod_data[stock_frame["Symbol"][i]]["EOD Prices"] = []
             
            data                                  = api.QuandlAPI(str(bse_code))
            try:
               json_data                          = data.run()
               data_points                        = json_data['dataset']['data']
            except:
                continue

            for data in data_points:
                
                eod_data[stock_frame["Symbol"][i]]["Date"].append(data[0])
                dates.add(data[0])#datetime.datetime.strptime(data[0], "%Y-%m-%d").date())
                eod_data[stock_frame["Symbol"][i]]["EOD Prices"].append(data[4])
                

        
        index             = pd.DatetimeIndex(list(dates))
        eod_frame         = pd.DataFrame(columns=list(eod_data.keys()),index=index)

        for sym in eod_data:
            for i,date in enumerate(eod_data[sym]["Date"]):
                eod_frame[sym][date] = eod_data[sym]["EOD Prices"][i]   
        
        return eod_frame


class GetDataFromAngelBroking:

    def __init__(self,credFilePath,mode="EQ"):

        ## ToDo Add verification of each string 

        with open(credFilePath) as f:
            creds    = json.load(f)

        self.obj          = SmartConnect(api_key=creds["API_KEY"])
        data              = self.obj.generateSession(creds["CLIENT_ID"],creds["PASSWD"])
        self.refreshToken = data['data']['refreshToken']
        
        with open("./assets/isinToToken.json") as f:
            self.lookup = json.load(f)[mode]


    def getHistoric(self,isin,interval,fromdate,todate):
        
        # historicParam={
        # "exchange": "NSE",
        # "symboltoken": "3045",
        # "interval": "ONE_MINUTE",
        # "fromdate": "2021-02-08 09:00", 
        # "todate": "2021-02-08 09:16"
        # }

        token                      = self.lookup[isin]
        Angelheader["interval"]    = interval
        Angelheader["fromdate"]    = fromdate
        Angelheader["todate"]      = todate
        Angelheader["symboltoken"] = token
        
        return  self.obj.getCandleData(Angelheader)["data"]


    def getBenchmarkData(self,index,interval,fromdate,todate):
        
        ##                            Frame of Sorted Dates 
        ##       -------Stock Name1-------       , --------Stock Name 2-------
        ## Date1 open, high, low, close, volume    open, high, low, close, volume
        ## Date2 open, high, low, close, volume    open, high, low, close, volume

        self.benchmark = benchmarks.Benchmarks(False)
        self.index     = index
        assert self.index in self.benchmark.supported_benchmarks, 'Supported Benchmarks : {} '.format(self.benchmark.supported_benchmarks)     
        stock_frame  = getattr(self.benchmark,self.index)()
        df = {}
        import time
    
        for stock in stock_frame:
           dataSeries = self.getHistoric(stock,interval,fromdate,todate)
           time.sleep(1)
           df[stock] = pd.DataFrame(columns=["Date","Open","High","Low","Close","Volume"],data = dataSeries).set_index("Date")
        
        df = pd.concat(df,axis=1)

        return df

                




            
if __name__ == "__main__":

    obj = GetDataFromAngelBroking("cred.json")
    df  = obj.getBenchmarkData("nifty_50","ONE_DAY","2017-02-06 09:16","2021-10-16 09:00")   
    import pdb;pdb.set_trace()

       






        


