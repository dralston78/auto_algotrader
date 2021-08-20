import pandas as pd
import numpy
import bs4
import string
import requests
from datetime import datetime

#set up webscraping
alphabet = list(string.ascii_uppercase)
NYSEsym = []
for letter in alphabet:
    url = 'https://eoddata.com/stocklist/NYSE/{}.htm'.format(letter)
    resp = requests.get(url)
    site = resp.content
    soup = bs4.BeautifulSoup(site, 'html.parser')
    table = soup.find('table', {"class": 'quotes'})
    for row in table.findAll('tr')[1:]:
        NYSEsym.append(row.findAll('td')[0].text.rstrip())

# print(NYSEsym)
for symbol in NYSEsym:
    symbol = symbol.replace('.', '-').split('-')[0]

#spot where maybe we could just import from tdameritrade library
data_list = []

for symbol in NYSEsym:
    url = "https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format(symbol)

    parameters = {
        'api': None, #my key
        'periodType': 'month',
        'frequencyType': 'daily',
        'frequency': "1",
        'startDate' : datetime.strptime('2020-10-30', r'%Y-%m-%d').timestamp(),
        'endDate' : datetime.strptime('2020-10-30', r'%Y-%m-%d').timestamp(),
        'needExtendedHoursData' : 'true'
    }

    req = requests.get(url=url,params=parameters)
    data_list.append(req.json())

symbl, open, high, low, close, volume, date = [],[],[],[],[],[],[]

for data in data_list:
    try:
        symbl_name = data['symbol'] 
    except KeyError:
        symbl_name = numpy.nan
    try:
        for each in data['candles']:
            symbl.append(symbl_name),
            open.append(each['open']),
            high.append(each['high']),
            low.append(each['low']),
            close.append(each['close']),
            volume.append(each['volume']),
            date.append(each['datetime'])
    except KeyError:
        pass

data_frame = pd.DataFrame(
    {
        'symbol' : symbl,
        'open' : open,
        'high' : high,
        'low' : low,
        'close' : close,
        'volume' : volume,
        'date' : date
    }
)