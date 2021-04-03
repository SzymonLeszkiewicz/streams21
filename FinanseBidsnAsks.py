import requests
from time import sleep
from requests.exceptions import HTTPError

waluty = ('BTC', 'GAME', 'ETH')

interval = 5

def connection_test(url):
    return requests.get(url).ok


def get_offers(w):
    url = f'https://bitbay.net/API/Public/{w}/ticker.json'
    if not connection_test(url):
        return con_test(url)
    response = requests.get(url)
    return (response.json()['ask'], response.json()['bid'])


def off_dis(currency):
    for i in currency:
        try:
            a, b = get_offers(i)
            print('Offers for: ', i, '(prices in dollars)')
            print('ask: ', a)
            print('bid: ', b)
            sleep(5)
        except HTTPError as err:
            print('ERROR', err)
            break
        except Exception as err:
            print('ERROR', err)
            break


def diff_between(currency):
    for i in currency:
        ask, bid = get_offers(i)
        spread = round(100 - (1 - (ask - bid) / bid) * 100, 4)
        print("Spread for ", i)
        print(spread, '%')
        sleep(5)


def main():
    off_dis(waluty)
    while 1:
        try:
            diff_between(waluty)
        except HTTPError as http_err:
            print('ERROR', err)
            break
        except Exception as err:
            print('ERROR', err)
            break


if __name__ == '__main__':
    main()
