import json, os, errno, shutil, lxml.html, hashlib, glob, urlparse

import requests


template = None
with open('template.html') as f:
    template = f.read()


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


os.chdir('site')
try:
    os.makedirs('img')
except OSError as error:
    if not error.errno == errno.EEXIST: # File exists
        raise

for path in os.listdir('.'):
    if path == 'img':
        continue
    shutil.rmtree(path)

for path in glob.glob('../data/*.json'):
    with open(path) as f:
        for line in f:
            page = json.loads(line)
            url = page['url']
            title = page['title']
            print 'Generating %s page' % title
            slug = url.replace('http://elementscommunity.com/wiki/', '') \
                      .replace('http://cdn.elementscommunity.com/wiki/', '')
            node = lxml.html.fragment_fromstring(page['content'])

            node = filter_node(node, ('div.post-revisions', '.adsense',
                                      '.related', '.alert'))
            node = process_images(node, url)

            html = template.replace('{{ title }}', page['title']) \
                           .replace('{{ content }}', lxml.html.tostring(node))
            os.makedirs(slug)
            with open('%s/index.html' % slug, 'w') as f:
                f.write(html.encode('utf8'))
