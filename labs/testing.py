from datetime import datetime, timedelta
import polars as pl
import os

import requests



link = os.getenv('API_URL')
response = requests.get(link)
result = response.json()

result:dict = result.get('Time Series FX (Daily)')

# api = os.getenv('Alpha_Vantage_API_KEY')
# url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=V&apikey={api}'


# data = requests.get(url)
# result = data.json()

# Extract the "Time Series (Daily)" part of the response
# time_series = result.get("Weekly Time Series", {})

print(result)

data = []

for tanggal, value in result.items():
    data.append({
        "date":tanggal,
        'open': value['1. open'],
        'close': value['4. close']  ,
        'low': value['3. low']  ,
        'high': value['2. high'] 
    })


df = pl.LazyFrame(data).collect()

# df = df.with_columns(pl.col("date").str.strptime(pl.Date, "%Y-%m-%d"))
desire_time = datetime.now() - timedelta(days=30)

# Define the schema explicitly after conversion
df = df.filter([pl.col('date') > str(desire_time) ]).with_columns([
    pl.col("open").cast(pl.Float64),
    pl.col("close").cast(pl.Float64),
    pl.col("low").cast(pl.Float64),
    pl.col("high").cast(pl.Float64)
])

test = df.with_columns([
        pl.col('date').str.to_date()
    ]).select(pl.all())

heads = test.head(10)

# print(heads.to_dict())
# print('''++++++++++++++++++++++++++++++++++++++
#       ++++++++++++++++++++++++++++++++++++++
#       ++++++++++++++++++++++++++++++++++++++
#       ++++++++++++++++++++++++++++++++++++++''')

print(heads.to_dicts())

print('''++++++++++++++++++++++++++++++++++++++
      ++++++++++++++++++++++++++++++++++++++
      ++++++++++++++++++++++++++++++++++++++
      ++++++++++++++++++++++++++++++++++++++''')

# for data in heads.iter_rows():
#     print(data)

# print('''++++++++++++++++++++++++++++++++++++++
#     ++++++++++++++++++++++++++++++++++++++
#     ++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++''')

# print(heads.to_series())

print(type(desire_time))
# print(test.head(5))
# print(test)
# print(df.tail(10))
# print(test)