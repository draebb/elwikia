from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule

from scraper.items import PageItem
from scraper.spiders.base import BaseSpider


class CardSpider(BaseSpider):
    name = 'cards'
    start_urls = ['http://elementscommunity.com/wiki/elements/',
                  'http://elementscommunity.com/wiki/']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'wiki/cards-\w+/[-\w]+/?'),
                               callback='parse_item'),
        Rule(SgmlLinkExtractor(allow=r'wiki/spell/[-\w]+/?'),
                               callback='parse_item'),
        Rule(SgmlLinkExtractor(allow=r'wiki/permanent/[-\w]+/?'),
                               callback='parse_item'),
        Rule(SgmlLinkExtractor(allow=r'wiki/elements/\w+/?'),
                               callback='parse_item'),
    )
