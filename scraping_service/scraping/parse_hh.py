from scraping.headhanter import  get_jobs, URL
from save_csv import save_to_csv


#url_hh = "https://spb.hh.ru/search/vacancy?text=python&items_on_page=100"
#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36'}
"""
headers = {
    'Host'           : 'hh.ru',
    'User-Agent'     : 'Safari',
    'Accept'         : '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection'      : 'keep-alive'

}
"""
"""
hh_requests = requests.get(url_hh, headers=headers)
#print(hh_requests)
pages = []
hh_soup = BeautifulSoup(hh_requests.text, 'html.parser')
paginator = hh_soup.find_all("span", {'class': 'pager-item-not-in-short-range'})
for page in paginator:
    pages.append(int(page.find('a').text))
#pages = paginator.find_all("a")

max_page = pages[-1]
print(pages)
"""
filename = 'test2.csv'

jobs, errors = get_jobs(URL)
save_to_csv(jobs, filename)

