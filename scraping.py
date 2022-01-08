from bs4 import BeautifulSoup
from tkinter import Tk, LabelFrame, Button, Grid, ttk, Label, PhotoImage, messagebox
import requests
import time
import random
import json
import urllib.request
import gzip
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

root = Tk()
root.title('Crypto Price Check')
root.iconbitmap(resource_path('bitcoin_icon.ico'))
root.minsize(width=950, height=300)
root.resizable(width=0, height=0)

windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()

positionRight = int(root.winfo_screenwidth()/3 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight)

root.geometry("+{}+{}".format(positionRight, positionDown))

def populate():
    # Check IC Connection
    try:
        # GET REQUESTS
        source = requests.get('https://www.tradingview.com/markets/cryptocurrencies/prices-all/', stream=True).text
        fear_greed = requests.get('https://api.alternative.me/fng/?limit=2', stream=True)
    except:
        messagebox.showinfo("Internet Required","Please connect to the internet to use this application")
    
    fear_greed_json = fear_greed.json()
    fear_greed_index = int(fear_greed_json['data'][0]['value'])
    fear_greed_classification = fear_greed_json['data'][0]['value_classification']
    #Compile to LXML
    compiler = BeautifulSoup(source, 'lxml')

    #Finding Main Data Body
    main = compiler.find('tbody', class_='tv-data-table__tbody')

    #Take all Rows from tbody
    cryptos = main.find_all('tr', class_='tv-data-table__row tv-data-table__stroke tv-screener-table__result-row', limit=100) #limiting to 100 rows

    style = ttk.Style(root)
    # set ttk theme to "clam" which support the fieldbackground option
    style.theme_use("clam")
    #Iterate through Rows
    for crypto in cryptos:
        #Find name from a element
        crypto_name = crypto.find('a', class_='tv-screener__symbol').text
        
        #Loop through elements in crypto object and retrieve img source by selecting container div
        # crypto_img = [img['src'] for img in crypto.find_all('img')]
        # img_url = ' '.join([str(elem) for elem in crypto_img])
        # if (img_url == ''):
        #     img_url = 'https://ps.w.org/404page/assets/icon.svg?rev=2451324'
        
        #read the image retrieved to get accent color when available
        # req = urllib.request.Request(img_url)
        # with urllib.request.urlopen(req) as response:
        #     the_page = response.read()
        #     soup = BeautifulSoup(the_page, 'lxml')
        #     color_path = soup.find('path')
        #     substring = 'url'
        #     try:
        #         color=color_path['fill']
        #         if substring in color_path['fill']:
        #             color='#A5E2FF'
        #     except:
        #         pass
        
        #Find neccessary data
        crypto_data = crypto.find_all('td', class_='tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big')

        #Iterate through Array of table columns
        crypto_market_cap = crypto_data[0].text
        crypto_f_diluted_market_cap = crypto_data[1].text
        crypto_l_price = crypto_data[2].text
        crypto_avail_coins = crypto_data[3].text
        crypto_total_coins = crypto_data[4].text
        crypto_traded_vol = crypto_data[5].text

        # crypto_image_retrieved = PhotoImage(file=f'image{crypto_name}.svg')
        table.insert(parent='', index='end', values=(crypto_name, crypto_market_cap, crypto_f_diluted_market_cap, crypto_l_price, crypto_avail_coins, crypto_total_coins, crypto_traded_vol), tags=crypto_name)
        
        # print(crypto_name + f' color')
        # table.tag_configure(crypto_name, background=f"{color}")
    
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
    root.after(2000, lambda: (status_label.configure(text='')))
    
table = ttk.Treeview(frame, selectmode='browse')
vsb = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
vsb.place(x=885, y=25, height=200)

table['columns'] = ("Coin", "Market Cap", "FD. Market Cap", "Price", "Available Coins", "Total Coins", "Traded Volumes")

table.heading("#0", anchor='center')
table.heading("Coin", text="Name", anchor='center')
table.heading("Market Cap", text="Market Cap", anchor='center')
table.heading("FD. Market Cap", text="FD. Market Cap", anchor='center')
table.heading("Price", text="Price", anchor='center')
table.heading("Available Coins", text="Available Coins", anchor='center')
table.heading("Total Coins", text="Total Coins", anchor='center')
table.heading("Traded Volumes", text="Traded Volumes", anchor='center')

table.column("#0", anchor='center', width=0, minwidth=0)
table.column("Coin", anchor='w', width=120, minwidth=25)
table.column("Market Cap", anchor='center', width=120, minwidth=25)
table.column("FD. Market Cap", anchor='center', width=120, minwidth=25)
table.column("Price", anchor='center', width=120, minwidth=25)
table.column("Available Coins", anchor='center', width=120, minwidth=25)
table.column("Total Coins", anchor='center', width=120, minwidth=25)
table.column("Traded Volumes", anchor='center', width=120, minwidth=25)

populate()
table.grid(row=0, column=0, pady=10)

root.mainloop()