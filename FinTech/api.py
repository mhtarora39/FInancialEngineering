##Make Rest Requests 
import os
import requests
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import brotli
import yfinance as yf
from io import StringIO
from urllib.parse import quote


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



# NSE URL for NIFTY50 constituents
BENCH_MARK_URL = "https://www.nseindia.com/api/equity-stockIndices?csv=true&index={}&selectValFormat=crores"
BASE_URL = 'https://www.nseindia.com/'
ALL_INDICIS = "https://www.nseindia.com/api/allIndices?csv=true"


def get_headers():
    return {
        'Host': 'www.nseindia.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, ',
        'X-Requested-With': 'XMLHttpRequest',
        'DNT': '1',
        'content-type': 'text/csv',
        'Connection': 'keep-alive',
    }

def fetch_cookies():
    response = requests.get(BASE_URL, timeout=30, headers=get_headers())
    if response.status_code != requests.codes.ok:
        #logging.error("Fetched url: %s with status code: %s and response from server: %s" % (
        #    BASE_URL, response.status_code, response.content))
        raise ValueError("Please try again in a minute.")
    return response.cookies.get_dict()


def request_url(url):
    try:
        #print(f"sending request : {url}" )
        response = requests.get(url, headers=get_headers(),cookies=fetch_cookies())

        if response.status_code == 200:
            if response.headers.get('Content-Encoding') == 'br':
                # Decompress Brotli content
                try:
                    decompressed_data = brotli.decompress(response.content)
                    # Decode to string
                except:
                    decompressed_data = response.content
                csv_data = decompressed_data.decode('utf-8')
                # Read the CSV data into a DataFrame
                df = pd.read_csv(StringIO(csv_data))
                return df
        else:
            raise(f"Failed to fetch data. Status code: {response.status_code}")
        
    except Exception as e:
        print(f"Exception : {e}")
        return ""
    

def nse_benchmarks(url=ALL_INDICIS,bm_url=BENCH_MARK_URL):
    index_mappings = {}
    # Make a GET request to fetch the data
    df  = request_url(url)
    for index in df["INDEX \n"]:
        index_mappings[index.replace(' ','_')] = BENCH_MARK_URL.format(quote(index))
    return index_mappings


# df = nse_benchmarks()
# import pdb; pdb.set_trace();
