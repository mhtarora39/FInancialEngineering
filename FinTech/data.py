import api
import pandas as pd
from breeze_connect import BreezeConnect
from stocks import AssetInfo

"""
from breeze_connect import BreezeConnect

# Initialize SDK
breeze = BreezeConnect(api_key="your_api_key")

# Obtain your session key from https://api.icicidirect.com/apiuser/login?api_key=YOUR_API_KEY
# Incase your api-key has special characters(like +,=,!) then encode the api key before using in the url as shown below.
import urllib
print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus("your_api_key"))

# Generate Session
breeze.generate_session(api_secret="your_secret_key",
                        session_token="your_api_session")

# Generate ISO8601 Date/DateTime String
import datetime
iso_date_string = datetime.datetime.strptime("28/02/2021","%d/%m/%Y").isoformat()[:10] + 'T05:30:00.000Z'
iso_date_time_string = datetime.datetime.strptime("28/02/2021 23:59:59","%d/%m/%Y %H:%M:%S").isoformat()[:19] + '.000Z'
        """


class ICICIAPI:
    instance_ = None
    API_KEY   = ""
    SESSION_KEY = ""
    API_SEC = ""

    def __init__(self,api_key,session_key,api_sec):
        if not (ICICIAPI.instance_ != None and 
           api_key == ICICIAPI.API_KEY and 
           ICICIAPI.SESSION_KEY == session_key
           and ICICIAPI.SECRET_KEY == api_sec):
            ## TODO check if session is valid or not.
           ICICIAPI.instance_ = BreezeConnect(api_key=api_key)
           ICICIAPI.instance_.generate_session(api_secret=api_sec,session_token=session_key)
        
        self.ins = ICICIAPI.instance_
    
    
    def get_history(self,asset_info):
        historical_data = self.ins.get_historical_data(
            stock_code=asset_info.symbol,
            exchange_code=asset_info.exchange,
            interval=asset_info.interval,
            from_date=asset_info.from_date,
            to_date=asset_info.to_date,
            product_type="cash",
        )
        ## Populate Stack Object
        return historical_data
    

if __name__ == "__main__":
    connect = ICICIAPI("API_KEY","SESSION_KEY","SECRET_KEY")
    asset_info = AssetInfo("ITC","2025-01-01T07:00:00.000Z","2025-01-24T07:00:00.000Z")
    print(connect.get_history(asset_info))