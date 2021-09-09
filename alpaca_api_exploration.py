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

ewa = api.get_barset('EWA','day', limit=1000).df
ewc = api.get_barset('EWC','day', limit=1000).df

ewa[('EWA','time')] = ewa.index
ewa = ewa.reset_index(drop=('time',""))
ewa.columns = ewa.columns.droplevel(0)

ewc[('EWC','time')] = ewc.index
ewc = ewc.reset_index(drop=('time',""))
ewc.columns = ewc.columns.droplevel(0)

ewa = ewa.iloc[0:99]
ewc = ewc.iloc[0:99]

# ewa['close'].plot(label='EWA', figsize=(20,10), title='Closing Price by Min', use_index=True)
# ewc['close'].plot(label='EWC', use_index=True)

# plt.legend()
# plt.ylim((0,50))
# plt.show()

print(ewc['time'].iloc[0], ewa['time'].iloc[0])
print(np.corrcoef(ewa['close'],ewc["close"]))
print()

from statsmodels.tsa.stattools import coint, adfuller

print(adfuller(ewc['close']/ewa['close']))
print()

print(coint(ewa['close'],ewc['close']))

(ewa['close']/ewc['close']).plot(label='ewa/ewc', figsize=(20,8), title='ratio', use_index=True)

plt.legend()
plt.ylim((0,1))
plt.show()

