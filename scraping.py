from bs4 import BeautifulSoup
from tkinter import Tk, LabelFrame, Button, Grid, ttk, Label, PhotoImage
import requests
import shutil
import time
import random
import json

root = Tk()
root.title('Crypto Price Check')
root.iconbitmap('bitcoin_icon.ico')
root.minsize(width=950, height=300)
root.resizable(width=0, height=0)

def populate():
    # Functions
    # GET REQUEST
    source = requests.get('https://www.tradingview.com/markets/cryptocurrencies/prices-all/', stream=True).text
    fear_greed = requests.get('https://api.alternative.me/fng/?limit=2', stream=True)
    fear_greed_json = fear_greed.json()
    fear_greed_index = int(fear_greed_json['data'][0]['value'])
    fear_greed_classification = fear_greed_json['data'][0]['value_classification']
    #Compile to LXML
    compiler = BeautifulSoup(source, 'lxml')

    #Finding Main Data Body
    main = compiler.find('tbody', class_='tv-data-table__tbody')

    #Take all Rows from tbody
    cryptos = main.find_all('tr', class_='tv-data-table__row tv-data-table__stroke tv-screener-table__result-row')

    #Iterate through Rows
    for crypto in cryptos:
        #Find name from a element
        crypto_name = crypto.find('a', class_='tv-screener__symbol').text
        
        #Loop through elements in crypto object and retrieve img source by selecting container div
        # crypto_img = [img['src'] for img in crypto.find_all('img')]
        # img_url = ' '.join([str(elem) for elem in crypto_img])
        # if (img_url == ''):
        #     img_url = 'https://ps.w.org/404page/assets/icon.svg?rev=2451324'
        # res = requests.get(img_url, stream = True)
        # try:
        #     if res.status_code == 200:
        #         with open((f'{crypto_name}.svg'),'wb') as f:
        #             shutil.copyfileobj(res.raw, f) 
        #         print('Image sucessfully Downloaded: ', crypto_name)
        #     else:
        #         pass
        # except Exception:
        #     pass

        #Find neccessary data
        crypto_price = crypto.find_all('td', class_='tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big')

        #Iterate through Array of table columns
        crypto_market_cap = crypto_price[0].text
        crypto_f_diluted_market_cap = crypto_price[1].text
        crypto_l_price = crypto_price[2].text
        crypto_avail_coins = crypto_price[3].text
        crypto_total_coins = crypto_price[4].text
        crypto_traded_vol = crypto_price[5].text

        # crypto_image_retrieved = PhotoImage(file=f'image{crypto_name}.svg')
        table.insert(parent='', index='end', values=(crypto_name, crypto_market_cap, crypto_f_diluted_market_cap, crypto_l_price, crypto_avail_coins, crypto_total_coins, crypto_traded_vol))
    
    fear_greed_index_label = Label(frame, text=f'Fear Greed Index: {fear_greed_index}', font=("Calibri", 12))
    fear_greed_class_label = Label(frame, text=f'Classification: ', font=("Calibri", 12))
    if (fear_greed_index >= 90): colorCode = '65c64c'
    if (fear_greed_index <  90): colorCode = '79d23c'
    if (fear_greed_index <= 75): colorCode = '9bbe44'
    if (fear_greed_index <= 63): colorCode = 'c6bf22'
    if (fear_greed_index <= 54): colorCode = 'dfce60'
    if (fear_greed_index <= 46): colorCode = 'd8bc59'
    if (fear_greed_index <= 35): colorCode = 'e39d64'
    if (fear_greed_index <= 25): colorCode = 'd17339'
    if (fear_greed_index <= 10): colorCode = 'b74d34'

    fear_greed_class_label = Label(frame, text=f'{fear_greed_classification}', font=("Calibri bold italic", 12), fg=f'#{colorCode}')
    fear_greed_index_label.grid(row=2, column=0)
    fear_greed_class_label.grid(row=3, column=0)
    fear_greed_class_label.grid(row=4, column=0)
    on_click()

def refresh_data():
    table.delete(*table.get_children())
    populate()

Grid.columnconfigure(root, index=0, weight=1)
Grid.rowconfigure(root, index=0, weight=1)

frame = LabelFrame(root, text="Crypto Prices", padx=5, pady=5)
frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

Grid.columnconfigure(frame, index=0, weight=1)
Grid.rowconfigure(frame, index=0, weight=1)

refresh_btn = Button(frame, text='Refresh', command=refresh_data)
refresh_btn.grid(row=1, column=0, padx=325, pady=25, sticky='nsew')

status_label = Label(frame, text='', font=("Arial italic", 12), fg='#33da6d')
status_label.grid(row=5, column=0)

def on_click():
    status_label["text"] = 'Refreshed.'
    root.after(1500, lambda: (status_label.configure(text='')))
    
table = ttk.Treeview(frame, selectmode='browse')
vsb = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
vsb.place(x=885, y=25, height=200)

table['columns'] = ("Coin", "Market Cap", "FD. Market Cap", "Price", "Available Coins", "Total Coins", "Traded Volumes")

table.column("#0", anchor='center', width=0, minwidth=0)
table.column("Coin", anchor='center', width=120, minwidth=25)
table.column("Market Cap", anchor='center', width=120, minwidth=25)
table.column("FD. Market Cap", anchor='center', width=120, minwidth=25)
table.column("Price", anchor='center', width=120, minwidth=25)
table.column("Available Coins", anchor='center', width=120, minwidth=25)
table.column("Total Coins", anchor='center', width=120, minwidth=25)
table.column("Traded Volumes", anchor='center', width=120, minwidth=25)

table.heading("#0", anchor='center')
table.heading("Coin", text="Name", anchor='center')
table.heading("Market Cap", text="Market Cap", anchor='center')
table.heading("FD. Market Cap", text="FD. Market Cap", anchor='center')
table.heading("Price", text="Price", anchor='center')
table.heading("Available Coins", text="Available Coins", anchor='center')
table.heading("Total Coins", text="Total Coins", anchor='center')
table.heading("Traded Volumes", text="Traded Volumes", anchor='center')

populate()
table.grid(row=0, column=0, pady=10)

root.mainloop()