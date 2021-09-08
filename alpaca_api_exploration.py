import alpaca_trade_api as trade_api
from alpaca_trade_api.rest import TimeFrame

import numpy as np
import pandas as pd

import time 
import datetime

from matplotlib import pyplot as plt

secret_key = 'aDSoaExVioIazecs8qazUNvxA5wURwgpwNLUsfc7'
public_key = 'PKSKA0TN1WBU9APZICDB'
base_url = 'https://paper-api.alpaca.markets'

# APCA_API_KEY_ID=public_key
# APCA_API_SECRET_KEY=secret_key
# APCA_API_BASE_URL=base_url

# api = trade_api.REST(key_id=APCA_API_KEY_ID,api_version='v2')
api = trade_api.REST(key_id= public_key, secret_key=secret_key, base_url=base_url, api_version='v2') # For real trading, don't enter a base_url

ewa = api.get_barset('EWA','day', limit=100).df
ewc = api.get_barset('EWC','day', limit=100).df

ewa[('EWA','time')] = ewa.index
ewa = ewa.reset_index(drop=('time',""))
ewa.columns = ewa.columns.droplevel(0)

ewc[('EWC','time')] = ewc.index
ewc = ewc.reset_index(drop=('time',""))
ewc.columns = ewc.columns.droplevel(0)

ewa['close'].plot(label='EWA', figsize=(20,10), title='Closing Price by Min', use_index=True)
ewc['close'].plot(label='EWC', use_index=True)

plt.legend()
plt.ylim((0,50))
# plt.show()

print(ewc['time'].iloc[0], ewa['time'].iloc[0])
print(np.corrcoef(ewa['close'],ewc["close"]))

from statsmodels.tsa.stattools import coint, adfuller

def stationarity(a, cutoff = 0.05):
  a = np.ravel(a)
  if adfuller(a)[1] < cutoff:
    print('The series is stationary')
    print('p-value = ', adfuller(a)[1])
  else:
    print('The series is NOT stationary')
    print('p-value = ', adfuller(a)[1])

print(stationarity(ewc['close']/ewa['close']))
print(coint(ewc['close'],ewa['close']))
