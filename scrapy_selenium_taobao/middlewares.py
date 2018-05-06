# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from logging import getLogger
from scrapy.http import HtmlResponse

from time import sleep
import re

regax = re.compile(r'[1|2][9|0]\d\d')


class SeleniumMiddleware(object):
    def __init__(self):
        # self.logger = getLogger(__name__)
        # self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument('headless')
        # self.driver = webdriver.Chrome('/home/leehyunsoo/4TB/chromedriver/chromedriver',
        #                                options=self.chrome_options)
        self.firefox_options = webdriver.FirefoxOptions()
        self.firefox_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1')
        # self.firefox_options.add_argument('-headless')
        self.driver = webdriver.Firefox(executable_path='/home/leehyunsoo/work/scrapy-selenium-taobao/web_driver/geckodriver',
                                        firefox_options= self.firefox_options)
        self.driver.set_page_load_timeout(10)

    def __del__(self):
        self.driver.close()

    def process_request(self, request, spider):
        # scrap the website using headlesschrome
        # self.logger.debug('Headlesschrome is starting')
        try:
            self.driver.get(request.url)
            current_page_url = self.driver.current_url
            data_url = self.get_data_url()
            self.move_data(data_url)
            self.driver.get(current_page_url)
            self.driver.find_element_by_xpath('//a[@trace="srp_bottom_pagedown"]').click()
            sleep(2)
            next_page_url = self.driver.current_url
            self.driver.get(current_page_url)
            return HtmlResponse(url=next_page_url, status=200, body=self.driver.page_source, request=request,
                                encoding='utf-8')
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)

    def get_data_url(self):
        # sleep(1000)
        data = self.driver.find_elements_by_xpath(
            '//*[@class="J_ClickStat"]')

        data_url = [href.get_attribute('href') for href in data]
        print(len(data_url))
        # print(data_url)
        return data_url

    def move_data(self, data_url):
        for url in data_url:
            self.driver.get(url)
            sleep(20)
        pass


class ScrapySeleniumTaobaoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
