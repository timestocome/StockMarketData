

# http://github.com/timestocome

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from scipy import signal


# find best and worst weeks for Nasdaq


data = pd.read_csv('nasdaq.csv')

# scale data
data = np.log(data[['Open']])

# level data
ix = np.arange(0, len(data))
dx = (data['Open'].iloc[len(data)-1] - data['Open'].iloc[0]) / len(data)
data['dx'] = dx * ix
data['Leveled'] = data['Open'] - data['dx'] 

data = data[['Open', 'Leveled']]
data['dx'] = data['Leveled'] - data['Leveled'].shift(1)

# smooth daily changes
data['smoothed_dx'] = data['dx'].rolling(window=21).mean()
data = data.dropna()


data['Bear'] = data['smoothed_dx'].apply(lambda z: 0 if z > 0 else 1)
data['Bull'] = data['smoothed_dx'].apply(lambda z: 1 if z > 0 else 0)

ix = np.arange(0, len(data))


plt.figure(figsize=(30,16))
plt.title('Monthly Nasdaq Bull/Bear Market')
plt.plot(data['Open'])
plt.scatter(ix, data['Bull'] * data['Leveled'] + 1, c='green')
plt.scatter(ix, data['Bear'] * data['Leveled'], c='red')
plt.savefig('MontlyBullBear.png')
plt.show()


