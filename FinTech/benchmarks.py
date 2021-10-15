import pandas as pd
import os
import json
import inspect
import copy


class Benchmarks:
     
    with open('./assets/config.json') as f:
        CONFIG     = json.load(f)   
        MAPPINGS   = {}
        BENCHMARKS = list(CONFIG["BenchMarks"].keys())
        EQUITY     = "./assets/Equity.csv"


     
    def __init__(self,cashed = False):
        self.cashed  = cashed


        for func_name in Benchmarks.BENCHMARKS:
            setattr(self, func_name, lambda name=func_name : self._get_bench_mark_(name))

    
        
    def _populate_bse_codes_(self):
        if Benchmarks.MAPPINGS:
            return Benchmarks.MAPPINGS

        df = pd.read_csv(Benchmarks.EQUITY)
        codes,isin   = list(df["Security Code"]) , list(df["ISIN No"])
        for k,v in zip(isin,codes):
            Benchmarks.MAPPINGS[k] = v
     
        return Benchmarks.MAPPINGS

    
    @property
    def supported_benchmarks(self):
        return Benchmarks.BENCHMARKS

    
    def _get_path_(self,name):
        assert name in Benchmarks.BENCHMARKS,name + " BenchMark is not supported yet."
        return Benchmarks.CONFIG["BenchMarks"][name]["url"]

        
    def _get_bench_mark_(self,name):
        path = os.path.join('./assets',name+'.csv')
        if os.path.exists(path) and self.cashed:
            return pd.read_csv(path)
        
        url = self._get_path_(name)
        benchmark = pd.read_csv(url)

        mappings = self._populate_bse_codes_()
        benchmark["BSE_CODES"] = benchmark["ISIN Code"]
    
        for i,isn_code in enumerate(benchmark["ISIN Code"]):
            if benchmark["ISIN Code"][i] not in mappings:
                print("error : ",benchmark["ISIN Code"][i])
                continue
            benchmark["BSE_CODES"][i] = mappings[benchmark["ISIN Code"][i]]
            
        if self.cashed: 
           benchmark.to_csv(path)
        return benchmark






             


                

       




        

                       
