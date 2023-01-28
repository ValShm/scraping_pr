import codecs
import os, sys
import asyncio
import datetime as dt

from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
#print(proj)
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scraping_service.settings")
#os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"
import django
django.setup()

from django.db import DatabaseError

from scraping.headhanter import *
from save_csv import save_to_csv
from scraping.models import Vacancy, City, Language, Error, Url

User = get_user_model()

file_name = 'test3.csv'
#parsers = ((get_jobs, URL),)
parsers = ((get_jobs, 'hh_work'),)

jobs, errors = [], []


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst


def get_urls(_settings):
    qs = Url.objects.all().values()
    #print(qs)
    url_dict = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    #print(url_dict)
    urls = []
    for pair in _settings:
       if pair in url_dict:
            #print(pair)
            tmp = {}
            tmp['city'] = pair[0]
            tmp['language'] = pair[1]
            url_data = url_dict.get(pair)
            if url_data:
                tmp['url_data'] = url_dict.get(pair)
                urls.append(tmp)
    #print(urls)
    return urls


async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(err)
    jobs.extend(job)


settings = get_settings()
url_list = get_urls(settings)
print(url_list)

#loop = asyncio.get_event_loop()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_list
             for func, key in parsers]
print(tmp_tasks)
# for data in url_list:
#
#     for func, key in parsers:
#         url = data['url_data'][key]
#         j, e = func(url, city=data['city'], language=data['language'])
#         jobs += j
#         errors += e
#if tmp_tasks:
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
loop.run_until_complete(tasks)
loop.close()


for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    qs = Error.objects.filter(timestamp=dt.date.today())
    if qs.exists():
        err = qs.first()
        err.data.update({'errors': errors})
        err.save()
    else:
        er = Error(data=f'errors:{errors}').save()

# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
ten_days_ago = dt.date.today() - dt.timedelta(30)
Vacancy.objects.filter(timestamp__lte=ten_days_ago).delete()

#save_to_csv(jobs, file_name)


