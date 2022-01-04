from bs4 import BeautifulSoup
from tkinterhtml import HtmlFrame
from tkinter import Tk, LabelFrame, Button, Grid, ttk, Label, PhotoImage
import requests
import shutil
import time
import random

root = Tk()
root.title('Crypto Price Check')
root.iconbitmap('bitcoin_icon.ico')
root.minsize(width=900, height=300)
root.resizable(width=0, height=0)

html_frame = HtmlFrame(root, horizontal_scrollbar=False)

#Iterate through Rows
def populate():
    # Functions
    # GET REQUEST
    source = requests.get('https://www.tradingview.com/markets/cryptocurrencies/prices-all/', stream=True).text

    #Compile to LXML
    compiler = BeautifulSoup(source, 'lxml')

    #Finding Main Data Body
    main = compiler.find('tbody', class_='tv-data-table__tbody')

    #Take all Rows from tbody
    cryptos = main.find_all('tr', class_='tv-data-table__row tv-data-table__stroke tv-screener-table__result-row')
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
        
        on_click()
        #Print Result to Console
        # print(f'''{crypto_name} - Market Cap: {crypto_market_cap} - Fully Diluted Market Cap: {crypto_f_diluted_market_cap} - Price: {crypto_l_price} - Available Coins: {crypto_avail_coins} - Total Coins: {crypto_total_coins} - Traded Volume: {crypto_traded_vol}''')

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

status_label = Label(frame, text='')
status_label.grid(row=2, column=0)

def on_click():
    status_label["text"] = 'Refreshed.'
    root.after(1500, lambda: (status_label.configure(text='')))
    
table = ttk.Treeview(frame, selectmode='browse')
vsb = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
vsb.place(x=800, y=25, height=200)

table['columns'] = ("Coin", "FD. Market Cap", "Price", "Available Coins", "Total Coins", "Traded Volumes")

table.column("#0", width=0, minwidth=0)
table.column("Coin", anchor='w', width=120, minwidth=25)
table.column("FD. Market Cap", anchor='center', width=120, minwidth=25)
table.column("Price", anchor='center', width=120, minwidth=25)
table.column("Available Coins", anchor='center', width=120, minwidth=25)
table.column("Total Coins", anchor='center', width=120, minwidth=25)
table.column("Traded Volumes", anchor='center', width=120, minwidth=25)

table.heading("#0", anchor='center')
table.heading("Coin", text="Name", anchor='w')
table.heading("FD. Market Cap", text="FD. Market Cap", anchor='center')
table.heading("Price", text="Price", anchor='center')
table.heading("Available Coins", text="Available Coins", anchor='center')
table.heading("Total Coins", text="Total Coins", anchor='center')
table.heading("Traded Volumes", text="Traded Volumes", anchor='center')

populate()
table.grid(row=0, column=0, pady=10)
root.mainloop()