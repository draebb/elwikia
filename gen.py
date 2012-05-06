import json, os, errno, shutil, lxml.html, hashlib, glob, urlparse, re

import requests


template = None
with open('template.html') as f:
    template = f.read()

from scraper.spiders import cards, falsegods
path_patterns = cards.path_patterns + falsegods.path_patterns
re_objects = [re.compile('http://elementscommunity.com/%s' % pattern)
              for pattern in path_patterns]


def filter_node(node, selectors):
    for selector in selectors:
        node.remove(node.cssselect(selector)[0])
    return node

def process_images(node, page_url):
    for img in node.xpath('//img'):
        url = img.get('src')
        if url.startswith(('.', '/')):
            url = urlparse.urljoin(page_url, url)

        file_name = hashlib.sha1(url).hexdigest()
        path = 'img/%s' % file_name
        if not os.path.exists(path):
            response = requests.get(url)
            if response.headers['content-type'].startswith('image'):
                with open(path, 'wb') as f:
                    f.write(response.content)
        img.set('src', '/%s' % path)
    return node

def replace_links(node):
    for a in node.xpath('//a'):
        url = a.get('href')
        for o in re_objects:
            if o.match(url):
                new_url = url.replace('http://elementscommunity.com/wiki', '')
                a.set('href', new_url)
                break
    return node


os.chdir('site')
try:
    os.makedirs('img')
except OSError as error:
    if not error.errno == errno.EEXIST: # File exists
        raise

for path in os.listdir('.'):
    if path in ('img', 'assets'):
        continue
    if os.path.isdir(path):
        shutil.rmtree(path)

chosen_data = []
category_map = {'abilities': 'Ability',
                'cards': 'Card',
                'falsegods': 'False God'}
for file_path in glob.glob('../data/*.json'):
    with open(file_path) as f:
        for line in f:
            page = json.loads(line)
            url = page['url']
            title = page['title']
            print 'Generating %s page' % title
            path = url.replace('http://elementscommunity.com/wiki/', '') \
                      .replace('http://cdn.elementscommunity.com/wiki/', '')
            node = lxml.html.fragment_fromstring(page['content'])

            node = filter_node(node, ('div.post-revisions', '.adsense',
                                      '.related', '.alert'))
            node = process_images(node, url)
            node = replace_links(node)

            html = template.replace('{{ title }}', page['title']) \
                           .replace('{{ content }}', lxml.html.tostring(node))
            os.makedirs(path)
            with open('%s/index.html' % path, 'w') as f:
                f.write(html.encode('utf8'))

            file_name = os.path.basename(file_path).split('.')[0]
            category = category_map[file_name]
            chosen_data.append({'title': '%s (%s)' % (title, category),
                                'path': '/%s' % path})

with open('assets/chosen.json', 'w') as f:
    chosen_data.sort(key=lambda page: page['title'])
    f.write(json.dumps(chosen_data))

with open('index.html', 'w') as f:
    html = template.replace('{{ title }}', '') \
                   .replace('{{ content }}', '')
    f.write(html.encode('utf8'))
