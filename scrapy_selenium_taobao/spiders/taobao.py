# -*- coding: utf-8 -*-

import scrapy
from urllib.parse import quote
from scrapy.loader import ItemLoader
from scrapy_selenium_taobao.items import TestItem


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    # allowed_domains = ['taobao.com']
    base_url = 'https://s.taobao.com/search?q='
    # base_url = 'https://s.taobao.com/search?q=ipad&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306'
    keyword = ['ipad', 'asics']

    def start_requests(self):
        for word in self.keyword:
            page = 1
            # end = '&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&style=grid'
            url = self.base_url + word
            # url = 'https://s.taobao.com/search?q=ipad&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306'
            yield scrapy.Request(url, callback=self.parse, meta={'keyword': word, 'page': page}, dont_filter=True)

    def parse(self, response):
        # parse the current page
        keyword = response.meta['keyword']
        page = response.meta['page']
        products = response.xpath('//div[@class="grid g-clearfix"]/div/div')
        for product in products:
            loader = TestItem()
            loader['keyword'] =  keyword
            loader['title'] = product.xpath('div[2]/div[2]/a/text()').extract()
            loader['price'] = product.xpath('.//*[contains(@class,"price")]/strong/text()').extract_first()
            # loader.add_value('deal', product.xpath('.//*[@class="deal-cnt"]/text()').extract_first())
            # loader.add_value('shop', product.xpath('.//*[@class="shop"]/a/span[2]/text()').extract_first())
            # loader.add_value('location', product.xpath('.//*[@class="location"]/text()').extract_first())
            # loader.add_value('image', product.xpath('.//img[contains(@class,"J_ItemPic")]/@data-src').extract_first())
            # loader.add_value('page', str(page))
            # print(loader)
            yield loader

        # self.logger.info('Page %s for %s was completed' % (page, keyword))
        # go to next page
        if page < self.settings.get('MAX_PAGE'):
            page += 1
            yield scrapy.Request(url=response.url, callback=self.parse,
                                 meta={'keyword': response.meta['keyword'], 'page': page}, dont_filter=True)
