import quandl
import pandas as pd
quandl.ApiConfig.api_key = "R5kDgTzyAgdhraQR4-RA"
data = quandl.get("EOD/AAPL", start_date="2020-01-01", end_date="2025-01-01")

# The returned object is already a pandas DataFrame
print(type(data)) 