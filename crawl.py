import urllib
import time
import os
import json

import requests


def crawl(url, params, crawled_pages, follow=True):
    title = params['page']
    print title
    if title in crawled_pages:
        print 'Crawled!'
        return
    crawled_pages.append(title)
    data = requests.get(api_url, params=params).text
    data = json.loads(data)
    content = data['parse']['text']['*']
    yield (title, content)
    if not follow:
        return
    for link in data['parse']['links']:
        if not link.has_key('exists'):
            continue
        for result in crawl(url, dict(params, page=link['*'].encode('utf8')),
                            crawled_pages=crawled_pages, follow=False):
            yield result


api_url = 'http://elementsthegame.wikia.com/api.php'
params = {'format': 'json', 'action': 'parse'}
base_url = 'http://elementsthegame.wikia.com/wiki/'
data_path = 'data/pages.jsonline'
crawled_pages_data_path = 'data/crawled_pages.json'
start_pages = '''
Akebono
Mark_of_Entropy
Mark_of_Death
Mark_of_Gravity
Mark_of_Earth
Mark_of_Life
Mark_of_Fire
Mark_of_Water
Mark_of_Light
Mark_of_Air
Mark_of_Time
Mark_of_Darkness
Mark_of_Aether
Others
Card_List
Card_effects_and_monster_skills
Weapon
Shields
Rares
False_Gods
'''.strip().split('\n')
crawled_pages = []
if os.path.exists(data_path):
    with open(data_path) as f:
        for line in f:
            page = json.loads(line)
            crawled_pages.append(page['title'])

f = open(data_path, 'a')
for page in start_pages:
    print '*%s*' % page
    page = urllib.unquote(page).replace('_', ' ')
    for title, content in crawl(api_url, dict(params, page=page),
                                crawled_pages=crawled_pages):
        url = base_url + urllib.quote(title.replace(' ', '_'))
        data = dict(title=title, url=url, content=content)
        f.write(json.dumps(data) + '\n')
        time.sleep(0.4)
f.close()

with open(crawled_pages_data_path, 'w') as f:
    f.write(json.dumps(crawled_pages))
