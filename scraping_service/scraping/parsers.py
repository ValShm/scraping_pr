import requests
import codecs
from scraping.headhanter import get_jobs
from random import randint


headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/89.0.4389.86 YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36'}
]
"""
headers = {
'authority': 'scrapeme.live',
'dnt': '1',
'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp, image/apng, */*; q=0.8, application/signed-exchange; v=b3; q=0.9',
'sec-fetch-site': 'none',
'sec-fetch-mode': 'navigate',
'sec-fetch-user': '?1',
'sec-fetch-dest': 'document',
'accept-language': 'en-GB, en-US; q=0.9 , en; q=0.8',
}
"""

url = "https://spb.hh.ru/search/vacancy?text=python&from=suggest_post&area=2"

resp = requests.get(url, headers=headers)
def hh_parse():
    if resp.status_code == 200:
        jobs, errors = get_jobs()
    return jobs, errors


if __name__ == "__main__":
    jobs, errors = hh_parse()
    with codecs.open('../work.json', 'w', 'utf-8') as f:
        f.write(str(jobs))
        f.close()
