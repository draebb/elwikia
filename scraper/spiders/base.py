from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider

from scraper.items import PageItem


class BaseSpider(CrawlSpider):
    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        item = PageItem(
            title=hxs.select('//h1/text()').extract()[0],
            url=response.url,
            content=hxs.select('//div[contains(@class, "format_text")]')
                       .extract()[0])
        return item
