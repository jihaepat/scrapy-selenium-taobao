# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
import datetime
from scrapy.loader.processors import MapCompose, Join
import re


class ProductItem(Item):
    collection = 'taobao-product-%s' % str(datetime.datetime.now())
    keyword = Field(
        output_processor=Join(),
    )
    title = Field(
        input_processor=MapCompose(str.strip),
        output_processor=Join(),
    )
    price = Field(
        output_processor=Join(),
    )
    deal = Field(
        input_processor=MapCompose(lambda i: re.search('\d+', i).group()),
        output_processor=Join(),
    )
    shop = Field(
        output_processor=Join(),
    )
    location = Field(
        output_processor=Join(),
    )
    image = Field(
        output_processor=Join(),
    )
    page = Field(
        output_processor=Join(),
    )
