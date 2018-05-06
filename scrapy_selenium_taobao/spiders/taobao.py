# -*- coding: utf-8 -*-
import re

import scrapy
from urllib.parse import quote
from scrapy_selenium_taobao.items import TestItem


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    keyword = ['ipad', 'asics']

    regax = re.compile(r'[1|2][9|0]\d\d')

    def start_requests(self):
        for word in self.keyword:
            for page_num in range(self.settings.get('MAX_PAGE')):
                url = 'https://s.taobao.com/search?q={}&s={}'.format(word,
                                                                     str(page_num * 44))

                yield scrapy.Request(url, callback=self.get_data_url, meta={'keyword': word},
                                     dont_filter=True)

    def get_data_url(self, response):
        data = response.xpath(
            '//*[@class="J_ClickStat"]/@href').extract()

        print(len(data))
        for url in data:
            yield scrapy.Request(url='https:' + url, callback=self.parse, meta={'keyword': response.meta['keyword'], },
                                 dont_filter=True)

    def parse(self, response):
        # parse the current page
        keyword = response.meta['keyword']

        products = response.xpath('//body/text()').extract()
        if self.regax.findall(products):
            if ((self.regax.findall(products)).sort())[0] < '2019':
                loader = TestItem()
                loader['keyword'] = keyword
                loader['title'] = response.title
                loader['url'] = response.url
                print(loader)
                yield loader

        # self.logger.info('Page %s for %s was completed' % (page, keyword))
        # go to next page
        # if page < self.settings.get('MAX_PAGE'):
        #     page += 1
        #     yield scrapy.Request(url=response.url, callback=self.parse,
        #                          meta={'keyword': response.meta['keyword'], 'page': page}, dont_filter=True)
