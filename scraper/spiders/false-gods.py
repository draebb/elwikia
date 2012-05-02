from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule

from scraper.items import PageItem
from scraper.spiders.base import BaseSpider


class FalseGodSpider(BaseSpider):
    name = 'false-gods'
    start_urls = ['http://elementscommunity.com/wiki/pve/false-gods/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'wiki/pve/false-god/[-\w]+/?'),
                               callback='parse_item'),
        Rule(SgmlLinkExtractor(allow=r'wiki/pve/false-gods/?$'),
                               callback='parse_item'),
    )
