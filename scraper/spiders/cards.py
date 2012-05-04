from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule

from scraper.items import PageItem
from scraper.spiders.base import BaseSpider


path_patterns = [r'wiki/cards-\w+/[-\w]+/?$',
                 r'wiki/spell/[-\w]+/?$',
                 r'wiki/permanent/[-\w]+/?$',
                 r'wiki/elements/\w+/?$']
rules = []
for pattern in path_patterns:
    rules.append(Rule(SgmlLinkExtractor(allow=pattern), callback='parse_item'))


class CardSpider(BaseSpider):
    name = 'cards'
    start_urls = ['http://elementscommunity.com/wiki/elements/',
                  'http://elementscommunity.com/wiki/']
    rules = rules
