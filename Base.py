# from FinTech.benchmarks import Benchmarks

# b = Benchmarks()
# import pdb;pdb.set_trace()

import http.client

conn = http.client.HTTPSConnection("stock.indianapi.in")

headers = { 'X-Api-Key': "sk-live-xUmVgtchuG0p9w1YH3bsywkJo34qbfRxcJFZJoVc" }

conn.request("GET", "/ipo", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))