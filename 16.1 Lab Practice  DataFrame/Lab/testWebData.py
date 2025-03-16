import pandas_datareader.data as data
import matplotlib.pyplot as plt

all_ticker = data.get_nasdaq_symbols()

print (all_ticker.info())
print(all_ticker.head(5))

 
aapl = data.DataReader("AAPL", 
                       start='2015-1-1', 
                       end='2015-12-31', 
                       data_source='yahoo')

print(aapl.info())
print(aapl)

