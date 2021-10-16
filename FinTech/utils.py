import json
import pandas as pd

def isinToToken(filePath,destination): 
    
    with open(filePath) as f:
        json_file = json.load(f)
    
    isin_to_token = {}
    
    for item in json_file:
        
        symbols = item["symbol"].split("-")
        if len(symbols) == 1:
           symbols.append("Other")

        if symbols[-1] not in isin_to_token:
            isin_to_token[symbols[-1]] = {}
 
        isin_to_token[symbols[-1]][item["name"]] = item["token"]
    
    with open(destination,"w+") as f:
        json.dump(isin_to_token,f) 


if __name__ == "__main__":
    isinToToken("./assets/OpenAPIScripMaster.json","./assets/isinToToken.json")




