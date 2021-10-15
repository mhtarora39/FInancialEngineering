##Make Rest Requests 
import os
import requests
import json
from benchmarks import Benchmarks

def build_url(url,query_dict):
    if not query_dict:
        return url 

    if url[-1] == '/':
        url = url[:-1]

    for i,key in enumerate(query_dict):
        sep = '?' if not i else '&'
        url = url + sep + key+ '=' + query_dict[key]

    return url    
         
class API:
    def __init__(self,url,query_dict,headers={'Content-Type': 'application/json'},payload="",response_type='GET'):
        self.url     = build_url(url,query_dict)
        print(self.url)
        self.headers = headers
        self.payload = payload
        self.r_type  = response_type


    def run(self):
        try:
           results = requests.request(self.r_type, self.url, headers=self.headers, data=self.payload)
           return json.loads(results.text)
        except Exception as e:
           return e




class QuandlAPI(API):
    URL    = "https://www.quandl.com/api/v3/datasets/"
    APIKEY = "R5kDgTzyAgdhraQR4-RA"

    def __init__(self,symbol,stock_ex="BSE"):
        query = {"api_key" : QuandlAPI.APIKEY}
        url   = QuandlAPI.URL + stock_ex + '/' + "BOM"+ symbol + '/' 
        super().__init__(url,query)

    def run(self):
        return super().run()

   
class ALPHA_VINTAGE_FUNCTIONS:
    class TIME_SERIES:
        TIME_SERIES_DAILY_ADJUSTED = "TIME_SERIES_DAILY_ADJUSTED"
        TIME_SERIES_DAILY = "TIME_SERIES_DAILY"
        TIME_SERIES_INTRADAY_EXTENDED = "TIME_SERIES_INTRADAY_EXTENDED"
        TIME_SERIES_INTRADAY = "TIME_SERIES_INTRADAY"
        TIME_SERIES_WEEKLY = "TIME_SERIES_WEEKLY"
        TIME_SERIES_WEEKLY_ADJUSTED = "TIME_SERIES_WEEKLY_ADJUSTED"
        TIME_SERIES_MONTHLY = "TIME_SERIES_MONTHLY"
        TIME_SERIES_MONTHLY_ADJUSTED = "TIME_SERIES_MONTHLY_ADJUSTED"
    
    class FUNDAMENTAL:
        pass

    class FOREX:
        pass

    class CRYPTOCURRENCIES:
        pass


class AlphaAPI(API):
    URL     = "https://www.alphavantage.co/"
    APIKEY  = "U0BBTNE7I4M6B8BC"
    
    @staticmethod
    def build_query(av_func,symbol,outputsize,stock_ex,interval):
        query = {}
        query['function'] = av_func
        query["symbol"] = symbol.upper() + '.' + stock_ex 
        query["outputsize"] = outputsize
        query["apikey"] = AlphaAPI.APIKEY
        if  av_func == ALPHA_VINTAGE_FUNCTIONS.TIME_SERIES.TIME_SERIES_INTRADAY:
            assert interval in [1,2,5] 
            query["interval"] = str(interval) + 'min'
        return query 

    def __init__(self,av_func:str,symbol:str,outputsize:str = 'full',stock_ex:str='BSE',interval=5):
       url   = os.path.join(AlphaAPI.URL,"query")
       query = AlphaAPI.build_query(av_func,symbol,outputsize,stock_ex,interval)
       super().__init__(url,query)

    def run(self):
        return super().run()    




#api = AlphaAPI(ALPHA_VINTAGE_FUNCTIONS.TIME_SERIES.TIME_SERIES_DAILY,"500312")

# b = Benchmarks(False)
# print(b.nifty_50.head())

# for code in b.nifty_50["BSE_CODES"]:
#     api = QuandlAPI(str(code))
#     print(api.run())



