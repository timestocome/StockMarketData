

# http://github.com/timestocome

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt


# use data leveled, log'd and otherwise smoothed in 
# https://github.com/timestocome/StockMarketData
# to do some analysis

# http://www.mdpi.com/1999-4893/5/4/588
# after I started working through the algorithm
# it became clear it's not so different than convolution
# and convolution might be easier and faster so shifted 
# to using the built in scipy.signal library
# The signal still needs to be stationary (rotated to x axis) in time
# and for stocks because of inflation you'll need a log index or the 
# older ones will be too small to catch 
#
# to find the bottoms of the Nasdad flip signal around the x axis and 
# repeat


# import data that we've rotated to x axis to make stationary in time (see section 1 of above paper)
# and scaled by taking the log
data = pd.read_csv('LeveledLogStockData.csv', index_col=0, parse_dates=True)

features = ['Nasdaq', 'S&P', 'Russell', 'DJIA', 'Gold', '1yr T', '10yr Bond']
data.columns = ['Nasdaq', 'S&P', 'Russell', 'DJIA', 'Gold', '1yr T', '10yr Bond']




# try nasdaq
from scipy import signal

# find peaks
peak_ix = signal.find_peaks_cwt(data['Nasdaq'], np.arange(1, 253))
peaks = np.zeros(len(data))
for i in peak_ix:
    peaks[i] = 1
data['Nasdaq_peaks'] = peaks


# find floors
data['Flipped Nasdaq'] = data['Nasdaq'] * -1.0
floor_ix = signal.find_peaks_cwt(data['Flipped Nasdaq'], np.arange(1, 253))
floors = np.zeros(len(data))
for i in floor_ix:
    floors[i] = 1
data['Nasdaq_floors'] = floors


# plt data
plt.figure(figsize=(18,16))
plt.plot(data['Nasdaq'] + 1.0, label='Nasdaq')
plt.plot(data['Nasdaq_peaks'] * 3., label='Peaks', alpha=0.5)
plt.plot(data['Nasdaq_floors'] * 3., label='Floors', alpha=0.5)
plt.grid('on')
plt.legend(loc='best')
plt.title("Top Peaks, Floors in Nasdaq 1990-2106")
#plt.savefig("FindStockIndexInflections.png")
plt.show()



