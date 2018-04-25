# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
from scrapy.loader import ItemLoader
from scrapy_selenium_taobao.items import ProductItem

class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['taobao.com']
    base_url = 'https://s.taobao.com/search?q='

    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            page = 1
            url = self.base_url + quote(keyword)
            yield scrapy.Request(url, callback=self.parse, meta={'keyword': keyword, 'page': page}, dont_filter=True)

    def parse(self, response):
        # parse the current page
        keyword = response.meta['keyword']
        page = response.meta['page']
        products = response.xpath('//div[@class="grid g-clearfix"]/div/div')
        for product in products:
            loader = ItemLoader(item=ProductItem())
            loader.add_value('keyword', keyword)
            loader.add_value('title', product.xpath('div[2]/div[2]/a/text()').extract())
            loader.add_value('price', product.xpath('.//*[contains(@class,"price")]/strong/text()').extract_first())
            loader.add_value('deal', product.xpath('.//*[@class="deal-cnt"]/text()').extract_first())
            loader.add_value('shop', product.xpath('.//*[@class="shop"]/a/span[2]/text()').extract_first())
            loader.add_value('location', product.xpath('.//*[@class="location"]/text()').extract_first())
            loader.add_value('image', product.xpath('.//img[contains(@class,"J_ItemPic")]/@data-src').extract_first())
            loader.add_value('page', str(page))
            yield loader.load_item()
        self.logger.info('Page %s for %s was completed' % (page, keyword))
        # go to next page
        if page < self.settings.get('MAX_PAGE'):
            page += 1
            yield scrapy.Request(url=response.url, callback=self.parse, meta={'keyword': response.meta['keyword'], 'page': page}, dont_filter=True)
