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

print(asknbid(waluty[0]))