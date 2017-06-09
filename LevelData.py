
# http://github.com/timestocome

# Level data so series is stationary in time
# take log of data
# save it to use in deconstructing signal to find anomolies 
# 
# https://blog.statsbot.co/time-series-anomaly-detection-algorithms-1cef5519aef2

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 


# pandas display options
pd.options.display.max_rows = 10000
pd.options.display.max_columns = 25
pd.options.display.width = 1000







######################################################################
# plot dataframe
########################################################################
def plot_dataframe(d, t):


    plt.figure(figsize=(18,18))
    plt.plot(d['NASDAQ'], label='NASDAQ')
    plt.plot(d['S&P'], label='S&P')
    plt.plot(d['Russell 2000'], label='Russell')
    plt.plot(d['DJIA'], label='DJIA')
    plt.plot(d['Gold'], label='Gold')
    plt.plot(d['1yr Treasury'], label='1yr T')
    plt.plot(d['10yr Bond'], label='10 yr bond')
    plt.plot(d['VIX'], label='VIX')
    plt.title(t)
    plt.legend(loc='best')
    plt.show()


######################################################################
# data
########################################################################
# read in datafile created in LoadAndMatchDates.py
data = pd.read_csv('StockDataWithVolume.csv', index_col='Date', parse_dates=True)
features = ['DJIA', 'S&P', 'Russell 2000', 'NASDAQ', 'VIX', 'US GDP', 'Gold', '1yr Treasury', '10yr Bond']


# fill in a couple NaN
#data.dropna()
data = data.fillna(method='ffill')



#########################################################################################
# level the series out, time series calculations all assume signal is stationary in time
########################################################################################
from sklearn import linear_model 



# add a time step 
steps = np.asarray(range(1, len(data)+1))
steps.reshape(1, -1)
data['step'] = steps

# NASDAQ
data['log NASDAQ'] = np.log(data['NASDAQ'])
model = pd.ols(x=data['step'], y=data['log NASDAQ'])
#print(model)        # print it, this is where we get the numbers for the adjustment
data['leveled log Nasdaq'] = data['log NASDAQ'] - (6.4540 + data['step'] * 0.0003)

# S&P
data['log S&P'] = np.log(data['S&P'])
model = pd.ols(x=data['step'], y=data['log S&P'])
#print(model)        # print it, this is where we get the numbers for the adjustment
data['leveled log S&P'] = data['log S&P'] - (6.0988 + data['step'] * 0.0002)


# Russell
data['log Russell'] = np.log(data['Russell 2000'])
model = pd.ols(x=data['step'], y=data['log Russell'])
#print(model)        # print it, this is where we get the numbers for the adjustment
data['leveled log Russell'] = data['log Russell'] - (5.2427 + data['step'] * 0.0003)



# DJIA
data['log DJIA'] = np.log(data['DJIA'])
model = pd.ols(x=data['step'], y=data['log DJIA'])
#print(model)        # print it, this is where we get the numbers for the adjustment
data['leveled log DJIA'] = data['log DJIA'] - (8.1711 + data['step'] * 0.0003)


# Gold
data['log Gold'] = np.log(data['Gold'])
model = pd.ols(x=data['step'], y=data['log Gold'])
#print(model)        # print it, this is where we get the numbers for the adjustment
data['leveled log Gold'] = data['log Gold'] - (5.4210 + data['step'] * 0.0003)


# 1 yr T
data['log 1yr Treasury'] = np.log(data['1yr Treasury'])
model = pd.ols(x=data['step'], y=data['log 1yr Treasury'])
#print(model)        # print it, this is where we get the numbers for the adjustment
data['leveled log 1yr Treasury'] = data['log 1yr Treasury'] - (2.5237 - data['step'] * 0.0006)



# 10 y B 
data['log 10yr Bond'] = np.log(data['10yr Bond'])
model = pd.ols(x=data['step'], y=data['log 10yr Bond'])
#print(model)        # print it, this is where we get the numbers for the adjustment
data['leveled log 10yr Bond'] = data['log 10yr Bond'] - (2.1900 - data['step'] * 0.0002)


#print(data.columns.values)
data = data[['leveled log Nasdaq','leveled log S&P', 'leveled log Russell', 'leveled log DJIA', 'leveled log Gold', 'leveled log 1yr Treasury','leveled log 10yr Bond']]

data.to_csv('LeveledLogStockData.csv')



'''
# plot to make sure things look ok
# look pretty chaotic but it should be easier to pull anomalies of it
plt.figure(figsize=(18,18))
plt.plot(data['leveled log Nasdaq'], label='NASDAQ')
plt.plot(data['leveled log S&P'], label='S&P')
plt.plot(data['leveled log Russell'], label='Russell')
plt.plot(data['leveled log DJIA'], label='DJIA')
plt.plot(data['leveled log Gold'], label='Gold')
plt.plot(data['leveled log 1yr Treasury'], label='1yr Treasury')
plt.plot(data['leveled log 10yr Bond'], label='10yr Bond')

plt.legend(loc='best')
plt.show()
'''