import pandas as pd
import os
import json
import inspect
import copy
import os
from api import nse_benchmarks,request_url,BENCH_MARK_URL
import yfinance as yf



class Benchmarks: 
    BENCHMARKS = nse_benchmarks()
    MAPPINGS   = {}
    BENCHMARK_NAMES = BENCHMARKS.keys()
     
    def __init__(self,cashed = False):
        self.cashed  = cashed
        import pdb;pdb.set_trace()
        for func_name in Benchmarks.BENCHMARK_NAMES:
            setattr(self, func_name, lambda name=func_name : self._get_bench_mark_(name))

    def get_all_benchmarks(self):
        return list(Benchmarks.BENCHMARK_NAMES)
        

    def _get_bench_mark_(self,name):
        return request_url(Benchmarks.BENCHMARKS[name])

bm = Benchmarks()
print(bm.NIFTY_50())

import pdb;pdb.set_trace()
        






             


                

       




        

                       
