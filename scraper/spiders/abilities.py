from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule

from scraper.items import PageItem
from scraper.spiders.base import BaseSpider


path_patterns = [r'wiki/ability/[-\w]+/?$',
                 r'wiki/basics/abilities/?$']
rules = []
for pattern in path_patterns:
    rules.append(Rule(SgmlLinkExtractor(allow=pattern), callback='parse_item'))


class CardSpider(BaseSpider):
    name = 'abilities'
    start_urls = ['http://elementscommunity.com/wiki/basics/abilities/']
    rules = rules
