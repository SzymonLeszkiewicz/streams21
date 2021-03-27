import requests
from time import sleep
from requests.exceptions import HTTPError

waluty = ('BTC', 'GAME', 'ETH')


def con_test(url):
    return requests.get(url).ok


def asknbid(w):
    url = f'https://bitbay.net/API/Public/{w}/ticker.json'
    if not con_test(url):
        return con_test(url)
    response = requests.get(url)
    a = response.json()['ask']
    b = response.json()['bid']
    return a, b

def off_dis(currency):
    for i in currency:
        try:
            a, b = asknbid(i)
            print('Offers for: ', i, '(prices in dollars)')
            print('ask: ', a)
            print('bid: ', b)
            sleep(5)
        except:
            print("Connection Error")

def diff_between(currency):
    for i in currency:
        try:
            ask, bid = asknbid(i)
            spread = round(100 - (1 - (ask - bid) / bid) * 100, 4)
            print("Spread for ", i)
            print(spread, '%')
            sleep(5)
        except:
            print("Connection Error")

off_dis(waluty)
while 1:
    diff_between(waluty)
