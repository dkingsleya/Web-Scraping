from bs4 import BeautifulSoup
import requests

source = requests.get('https://www.tradingview.com/markets/cryptocurrencies/prices-all/').text

compiler = BeautifulSoup(source, 'lxml')
main = compiler.find('tbody', class_='tv-data-table__tbody')
cryptos = main.find_all('tr', class_='tv-data-table__row tv-data-table__stroke tv-screener-table__result-row')

for crypto in cryptos:
    crypto_name = crypto.find('a', class_='tv-screener__symbol').text
    crypto_price = crypto.find_all('td', class_='tv-data-table__cell tv-screener-table__cell tv-screener-table__cell--big')
    crypto_market_cap = crypto_price[0].text
    crypto_f_diluted_market_cap = crypto_price[1].text
    crypto_l_price = crypto_price[2].text
    crypto_avail_coins = crypto_price[3].text
    crypto_total_coins = crypto_price[4].text
    crypto_traded_vol = crypto_price[5].text
    print(f'''{crypto_name} - Market Cap: {crypto_market_cap} - Fully Diluted Market Cap: {crypto_f_diluted_market_cap} - Price: {crypto_l_price} - Available Coins: {crypto_avail_coins} - Total Coins: {crypto_total_coins} - Traded Volume: {crypto_traded_vol}''')


