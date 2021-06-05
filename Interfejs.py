from tkinter import *
import json


def writeFile():
    file = open('history.txt', 'w')
    if ks.get().lower() == 'kupno':
        data['kupno'][waluta.get().upper()].append((int(ilosc.get()), int(cena.get())))
    else:
        data['sprzedaz'][waluta.get().upper()].append((int(ilosc.get()), int(cena.get())))
    json.dump(data, file)
    file.close()


w = ('BTC', 'LTC', 'ETH')
# data = {'kupno': {w[0]: [], w[1]: [], w[2]: []},
#         'sprzedaz': {w[0]: [], w[1]: [], w[2]: []}}
# {"kupno": {"BTC": [], "LTC": [], "ETH": []}, "sprzedaz": {"BTC": [], "LTC": [], "ETH": []}}

with open('history.txt') as plik:
    data = json.load(plik)
print(data)
gui = Tk()
gui.geometry("300x120")
gui.title("Wprowadź transakcje")
Label(gui, text="Waluta").grid(row=0, sticky=W)
Label(gui, text="Ilosc").grid(row=1, sticky=W)
Label(gui, text="Cena").grid(row=2, sticky=W)
Label(gui, text="kupno/sprzedaż").grid(row=3, sticky=W)
waluta = Entry(gui)
ilosc = Entry(gui)
cena = Entry(gui)
ks = Entry(gui)

waluta.grid(row=0, column=1)
ilosc.grid(row=1, column=1)
cena.grid(row=2, column=1)
ks.grid(row=3, column=1)

butonWrite = Button(gui)
butonWrite.config(text='Zapisz', command=writeFile)
butonWrite.grid(row=8, column=1)
gui.mainloop()
