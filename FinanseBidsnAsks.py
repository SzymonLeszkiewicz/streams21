import requests
from time import sleep
from requests.exceptions import HTTPError

waluty = ('BTC', 'GAME', 'ETH')


def con_test(url):
    return requests.get(url).ok


for i in waluty:
    print(con_test(f'https://bitbay.net/API/Public/{i}/ticker.json'))
