import requests
from bs4 import BeautifulSoup
ITEMS = 100
URL = f"https://spb.hh.ru/search/vacancy?text=python&items_on_page={ITEMS}"
headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36'
}
