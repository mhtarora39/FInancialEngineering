import benchmarks
import api
import pandas as pd
import datetime


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
             
            data                                  ``= api.QuandlAPI(str(bse_code))
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


