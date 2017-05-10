
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import BayesianRidge, LinearRegression
import matplotlib.pyplot as plt 




# pandas display options
pd.options.display.max_rows = 100
pd.options.display.max_columns = 25
pd.options.display.width = 1000





# read in file
def read_data(file_name):

    stock = pd.read_csv(file_name, parse_dates=True, index_col=0)        # 31747 days of data 
    n_samples = len(stock)
    
    # ditch samples with NAN values
    stock = stock.dropna(axis=0)

    # flip order from newest to oldest to oldest to newest
    stock = stock.iloc[::-1]

    # trim data
    stock = stock[['Open']]

    # convert object to floats
    stock['Open'] = pd.to_numeric(stock['Open'], errors='coerce')

    # all stock is needed to walk back dates for testing hold out data
    return stock


#############################################################################################
# load and combine stock indexes 


dow_jones = read_data('data/djia.csv')
print("Loaded DJIA", len(dow_jones))

s_p = read_data('data/S&P.csv')
print("Loaded S&P", len(s_p))

russell_2000 = read_data('data/Russell2000.csv')
print("Loaded Russell", len(russell_2000))

nasdaq = read_data('data/nasdaq.csv')
print("Loaded NASDAQ", len(nasdaq))

# VIX index that attempts to measure volatility of S&P, 
# sometimes called 'fear index'
vix = read_data('data/VIX.csv')
print("Loaded VIX", len(vix))

# gdp is only listed once a quarter  in missing days and fill missing with previous
gdp = read_data('data/US_GDP.csv')
# print(gdp)
gdp = gdp.resample("B").bfill()
print("Loaded GDP, added missing day, filled in data")


# a few missing values in here
gold = read_data('data/GOLD.csv')
gold = gold.interpolate()
print("Loaded Gold", len(gold))




# government closed some days when stock markets are open
# fill in missing values using interpolation of surrounding values
treasury = read_data('data/1yrTreasury.csv')
treasury = treasury.interpolate()
print("loaded 1 yr treasury", len(treasury))

# interpolate doesn't work here - all the dates have values until we
# merge with the rest of the data - have to fill missing dates first
bond = read_data('data/10yrbond.csv')
bond = bond.resample("B").interpolate()
print("loaded 10 yr bond", len(bond))





# rename columns before joining so we know which is which
dow_jones.columns = ['DJIA']
s_p.columns = ['S&P']
russell_2000.columns = ['Russell 2000']
nasdaq.columns = ["NASDAQ"]
vix.columns = ['VIX']
gdp.columns = ['US GDP']
gold.columns = ['Gold']
treasury.columns = ['1yr Treasury']
bond.columns = ['10yr Bond']


# combine by matching date index, missing dates will get NaN
indexes = dow_jones.join(s_p)
indexes = indexes.join(russell_2000)
indexes = indexes.join(nasdaq)
indexes = indexes.join(vix)
indexes = indexes.join(gdp)
indexes = indexes.join(gold)
indexes = indexes.join(treasury)
indexes = indexes.join(bond)

# print(indexes)


'''
# combine stock indexes into one dataframe all at once renaming columns as we go
data = pd.concat([dow_jones['Open'], s_p['Open'], russell_2000['Open'], nasdaq['Open']], axis=1, keys=['dow_jones', 'S&P', 'russell_2000', 'nasdaq'])
'''

# trim dates, VIX, Russell don't go back far,
# dates were left in earlier to all computations going back and forward in time
indexes = indexes.loc[indexes.index > '01-01-1990']
indexes = indexes.loc[indexes.index < '12-31-2016']

print(indexes)






# compare indexes
(indexes / indexes.ix[0] * 100).plot(figsize=(20,15))
plt.title("Standarized Indexes 1990-2016")
plt.savefig("StandardizedData.png")
plt.show()


