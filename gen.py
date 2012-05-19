import json, os, errno, shutil, lxml.html, hashlib, glob, urlparse, re, urllib

import requests


template = None
with open('template.html') as f:
    template = f.read().decode('utf8')


def filter_node(node, xpaths):
    for xpath in xpaths:
        for node_to_remove in node.xpath(xpath):
            node_to_remove.drop_tree()


def process_images(node, page_url):
    for img in node.xpath('//img'):
        url = img.get('src')
        if url.startswith(('.', '/')):
            url = urlparse.urljoin(page_url, url)

        file_name = hashlib.sha1(url).hexdigest()
        file_ext = os.path.splitext(url)[1]
        path = 'img/%s%s' % (file_name, file_ext)
        if not os.path.exists(path):
            response = requests.get(url)
            if response.headers['content-type'].startswith('image'):
                with open(path, 'w') as f:
                    f.write(response.content)
        img.set('src', '/%s' % path)


def replace_links(node, crawled_pages):
    for a in node.xpath('//a'):
        url = a.get('href')
        slug = url.replace(base_url, '').replace('_', ' ')
        slug = urllib.unquote(slug)
        if slug.decode('utf8') in crawled_pages:
            a.set('href', '/%s/' % urllib.quote(slug.replace(' ', '_'),
                                                safe='()'))


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

base_url = 'http://elementsthegame.wikia.com/wiki/'
chosen_data = []
crawled_pages = []
with open('../data/crawled_pages.json') as f:
    crawled_pages = set(json.load(f))

with open('../data/pages.jsonline') as f:
    for line in f:
        page = json.loads(line)
        url = page['url']
        title = page['title']
        content = page['content']

        print 'Generating %s page' % title
        path = url.replace(base_url, '')
        path = urllib.unquote(path.encode('utf8'))
        node = lxml.html.fragment_fromstring(content, create_parent=True)
        node.make_links_absolute(base_url=base_url)

        filter_node(node, ('//span[@class="editsection"]',
                           '//a[text()="Edit data"]'))
        process_images(node, url)
        replace_links(node, crawled_pages)

        html = template.format(title=title, content=lxml.html.tostring(node))
        os.makedirs(path)
        with open('%s/index.html' % path, 'w') as f:
            f.write(html.encode('utf8'))

        chosen_data.append({'title': title,
                            'path': '/%s/' % urllib.quote(path)})

with open('assets/chosen.json', 'w') as f:
    chosen_data.sort(key=lambda page: page['title'])
    f.write(json.dumps(chosen_data))

with open('index.html', 'w') as f:
    html = template.format(title='', content='')
    f.write(html.encode('utf8'))
