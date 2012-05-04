from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule

from scraper.items import PageItem
from scraper.spiders.base import BaseSpider


path_patterns = [r'wiki/pve/false-god/[-\w]+/?$',
                 r'wiki/pve/false-gods/?$']
rules = []
for pattern in path_patterns:
    rules.append(Rule(SgmlLinkExtractor(allow=pattern), callback='parse_item'))


class FalseGodSpider(BaseSpider):
    name = 'falsegods'
    start_urls = ['http://elementscommunity.com/wiki/pve/false-gods/']
    rules = rules
