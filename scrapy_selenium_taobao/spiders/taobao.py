# -*- coding: utf-8 -*-
import re
from time import sleep

import scrapy
from scrapy_selenium_taobao.items import TestItem

regax = re.compile(r'[1|2][9|0]\d\d[-|.|/|\w]\d\d[-|.|/|\w]\d\d')


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    keyword = ['ipad','asics','xivo']
    end_date = '2019'

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
        print(response.url)
        body = ''.join((response.body).decode('utf-8'))

        if len(regax.findall(body)) > 0:
            if (''.join(filter(str.isdigit, min(regax.findall(body))))) < self.end_date:
                items = TestItem()
                items['keyword'] = response.meta['keyword']
                items['url'] = response.url
                yield items
