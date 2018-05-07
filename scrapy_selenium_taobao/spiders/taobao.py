# -*- coding: utf-8 -*-
import re
from time import sleep

import scrapy
from scrapy_selenium_taobao.items import TestItem

regax = re.compile(r'[1|2][9|0]\d\d[-|.|/|\w]\d\d[-|.|/|\w]\d\d')


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    keyword = ['ipad']

    def start_requests(self):
        for word in self.keyword:
            for page_num in range(self.settings.get('MAX_PAGE')):
                url = 'https://s.taobao.com/search?q={}&s={}'.format(word, str(page_num * 44))
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
        print('parse============================================================================\n')
        body = ''.join((response.body).decode('utf-8'))
        # print(body)
        print(regax.findall(body))
        print(len(regax.findall(body)))
        if len(regax.findall(body)) > 0:
            if ((regax.findall(body)).sort())[0] < '2019':
                items = TestItem()
                items['keyword'] = response.meta['keyword']
                items['url'] = response.url
                yield items
        print('parse============================================================================\n')

        # file.write(''.join(text_parts))
        # if self.regax.findall(products):
        #     if ((self.regax.findall(products)).sort())[0] < '2019':
        #         loader = TestItem()
        #         loader['keyword'] = keyword
        #         loader['title'] = response.title
        #         loader['url'] = response.url
        #         print(loader)
        #         yield loader

        # items = TestItem()
        # keyword = response.meta['keyword']
        # title = response.xpath('/html/body/div[5]/div/div[2]/div/div[1]/div[1]/div/div[1]/h1/a/text()').extract()
        # url = response.url
        #
        # items['title'] = title
        # items['keyword'] = keyword
        # items['url'] = url
        # yield items
