import requests
from bs4 import BeautifulSoup
from random import randint

__all__ = ('extract_max_pages', 'extract_hh_job', 'get_jobs', 'URL', 'ITEMS')

ITEMS = 100
URL = f"https://spb.hh.ru/search/vacancy?text=python&items_on_page={ITEMS}"
headers = [
    {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36'
    },
    {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)  YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36'
    },
    {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86'
    }
]
def extract_max_pages(URL):
    #url_hh = "https://spb.hh.ru/search/vacancy?text=python&items_on_page=100"

    hh_requests = requests.get(URL, headers=headers[randint(0, 2)])
    # print(hh_requests)
    pages = []
    if hh_requests.status_code == 200:
        hh_soup = BeautifulSoup(hh_requests.text, 'html.parser')
        paginator = hh_soup.find_all("span", {'class' : 'pager-item-not-in-short-range'})
        for page in paginator :
            pages.append(int(page.find('a').text))
        # pages = paginator.find_all("a")
        max_page = pages[-1]
    return max_page


def extract_hh_job(html, city=None, language=None):

    title = html.find('a').text
    link = html.find('a')['href']
    company_div = html.find('div', {'class' : 'vacancy-serp-item__meta-info-company'})
    company_link = company_div.find('a')
    if company_link is None:
        company_name = 'Компания'
    else :
        company_name = company_link.text
    company_name = company_name.strip()
    location_div = html.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
    location_div = location_div.partition(',')[0]
    description_div = html.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'})
    if description_div is None:
        description = 'Нет описания'
    else :
        description = description_div.text
    """
    return {'title': title, 'company': company_name, 'city': location_div,
            'url': link, 'description': description}
    """
    return {'title' : title, 'company' : company_name,
            'url' : link, 'description' : description, 'city_id': city, 'language_id': language}


def extract_hh_jobs(last_page, URL, city=None, language=None):
    jobs = []
    errors = []
    for page in range(last_page):
        print(f'Парсинг страницы {page}')
        try:

            result = requests.get(f'{URL}&page={page}', headers=headers[randint(0, 2)])
            soup = BeautifulSoup(result.text, 'html.parser')
        except Exception as e:
            print("Error! " + str(e))
            errors.append({'url': f'{URL}&page={page}', 'title': 'Page not response'})
        #vacancy-serp-item__layout
        results = soup.find_all('div', {'class': 'vacancy-serp-item__layout'})
        if results:
            for result in results:
                job = extract_hh_job(result, city=city, language=language)
                jobs.append(job)
        else:
            errors.append({'url': f'{URL}&page={page}', 'title': "Div does not exists"})
    return jobs, errors


def get_jobs(URL, city=None, language=None):
    max_page = extract_max_pages(URL)
    jobs, errors = extract_hh_jobs(max_page, URL, city=city, language=language)
    return jobs, errors