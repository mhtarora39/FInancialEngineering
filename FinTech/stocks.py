class Stock:
    def __init__(self,symbol,type="",isin="",price="",date=""):
        self.type = type
        self.symbol = symbol
        self.isin = isin
        self.date = date
        self.price = price

    def to_dict(self):
        return {
            "type" : self.type,
            "symbol" : self.symbol,
            "isin" : self.isin,
            "date" : self.date,
            "price" : self.price,
        }
    
class AssetInfo:
    def __init__(self,symbol,from_date,to_date,interval="1day",exchange="NSE"):
        self.symbol = symbol
        self.from_date = from_date
        self.to_date = to_date
        self.stock   = Stock(symbol)
        self.exchange = exchange
        self.interval = interval
    

    
 