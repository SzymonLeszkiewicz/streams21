import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
import requests
from statistics import mean
from datetime import datetime, timedelta
from requests.exceptions import HTTPError
from datetime import datetime
import random
import json

inc = [[], [], []]
dec = [[], [], []]


def m(a):
    return (sum(a) + 1) / (len(a) + 1)


def cont(url):
    return requests.get(url).ok


def calc_rsi(t, da, ia, bhist):
    x = y = 1
    if len(bhist) > t:
        l = bhist[-1] - bhist[-t]
        if l > 0:
            ia.append(l)
        else:
            da.append(l)
        x = m(ia)
        y = m(da)
    return 100 - (100 / (1 + (x + 1 / y + 1)))


def vol_calc(cur, t):
    url = f'https://api.bitbay.net/rest/trading/transactions/{cur}'
    if not cont(url):
        return cont(url)
    time = int((datetime.now() - timedelta(0, t)).timestamp()) * 1000  # zmienia format na sekundowy
    par = {"fromTime": time}
    response = requests.request("GET", url, params=par)
    response.raise_for_status()
    _DATA = response.json()
    try:
        volume = _DATA['items'][0]['a']
    except IndexError:
        volume = 0.0
    return float(volume)


def asknbid(w):
    url = f'https://api.bitbay.net/rest/trading/ticker/{w}'
    if not cont(url):
        return cont(url)
    response = requests.get(url)
    a = response.json()['ticker']['lowestAsk']
    b = response.json()['ticker']['highestBid']
    return (float(a), float(b))


oferts = {}
fig, axs = plt.subplots(3, sharex=True)
pointers = [axs[0].twinx(), axs[1].twinx(), axs[2].twinx()]
for i in range(3):
    axs[i].set_zorder(1)
    axs[i].set_frame_on(False)

w = ('BTC', 'LTC', 'ETH')
choice = input("rsi czy vol ?").lower()
assert choice in ('rsi', 'vol'), 'Wybierz między RSI/VOL'
rsi_section = int(input("Wskaż przedział dla RSI"))
czas = []
vol = [[], [], []]
rsi = [[], [], []]
srednie = [[], [], []]


def data_check(data):
    pass


def otwarcie():
    with open("history.txt") as plik:
        plik = json.load(plik)
    return plik


def srednia(data, waluta):
    kupna = data['kupno'][waluta]
    sprzedaz = data['sprzedaz'][waluta]
    print(kupna)
    print(sprzedaz)
    if sprzedaz != []:
        zarobek = 0
        licznik = 0
        for i in sprzedaz:
            licznik += i[0]  # ile sprzedano
            zarobek += i[0] * i[1]
        # licznik = 10
        colicznik = licznik
        wydatek = 0
        for i in kupna:
            if licznik > 0:
                licznik -= i[0]
                wydatek += i[0] * i[1]
        # print('zarobek',zarobek  )
        # print('wydatek', wydatek)
        # print('wynik', zarobek - wydatek)
    wynik = zarobek - wydatek
    klicznik, ksuma = 0, 0
    kupnaposprzedazy = kupna.copy()
    to_remove = []
    for i in range(len(kupna)):
        if colicznik >= kupna[i][0]:
            colicznik -= kupna[i][0]
            to_remove.append(i)
        else:
            kupnaposprzedazy[i][0] -= colicznik
            colicznik = 0
    l = 0
    for i in to_remove:
        kupnaposprzedazy.pop(i - l)
        l += 1
    for i in kupnaposprzedazy:
        klicznik += i[0]
        ksuma += i[1] * i[0]

    if colicznik == 0 and klicznik != 0:
        return (ksuma) / (klicznik), wynik
    return 0, 0


def animate(i):
    for i in w:
        if i + 'asks' not in oferts.keys():
            oferts[i + 'asks'] = []
            oferts[i + 'bids'] = []
        oferts[i + 'asks'].append(asknbid(i + '-PLN')[0])
        oferts[i + 'bids'].append(asknbid(i + '-PLN')[1])
        oferts[i + 'asks'] = oferts[i + 'asks'][-5:]
        oferts[i + 'bids'] = oferts[i + 'bids'][-5:]
    oferts_list = list(oferts.values())
    now = datetime.now()
    czas.append(now.strftime("%H:%M:%S"))
    for i, ax in enumerate(axs):

        axs[i].cla()
        pointers[i].cla()
        vol[i].append(vol_calc(f'{w[i]}-PLN', 100))
        rsi[i].append(calc_rsi(rsi_section, dec[i], inc[i], oferts_list[2 * i + 1]))
        srednie[i] = srednia(otwarcie(), w[i])[0]
        print('final', srednie[0])
        info = str(srednia(otwarcie(), w[i])[1])
        c = 'green'
        if info[0] == '-':
            c = 'red'
        pointers[i].text(0.95, 0.05, info,
                         verticalalignment='bottom', horizontalalignment='right',
                         transform=ax.transAxes,
                         color=c, fontsize=12)
        axs[i].plot(czas[-5:], [srednie[i]] * len(czas[-5:]), '--', label='avg')
        axs[i].plot(czas[-5:], oferts_list[2 * i], label=w[i] + ' asks')
        axs[i].plot(czas[-5:], oferts_list[2 * i + 1], label=w[i] + ' bids')
        axs[i].legend(loc='upper left')

        axs[i].set_title(w[i])

        if choice == 'vol':
            pointers[i].bar(czas[-5:], vol[i][-5:], width=0.2, label="vol", color='silver')
            pointers[i].legend(loc='lower left')
        else:
            pointers[i].plot(czas[-5:], rsi[i][-5:], color='hotpink', label=f'{w[i]} RSI')

            pointers[i].legend(loc='lower left')


ani = FuncAnimation(fig, animate, interval=1000)
plt.show()
