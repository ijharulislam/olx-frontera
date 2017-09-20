# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OlxscraperItem(scrapy.Item):
    # define the fields for your item here like:
    Title = scrapy.Field()
    ADS = scrapy.Field()
    Name = scrapy.Field()
    Phone = scrapy.Field()
    Phone_Number = scrapy.Field()
    Price = scrapy.Field()
    Description = scrapy.Field()
    Sub_category = scrapy.Field()
    Novo_Usado = scrapy.Field()
    City = scrapy.Field()
    Suburb = scrapy.Field()
    zipcode = scrapy.Field()
    Adcode = scrapy.Field()
    Image_urls = scrapy.Field()
    Main_Image_urls = scrapy.Field()
    Day = scrapy.Field()
    Month = scrapy.Field()
    Time = scrapy.Field()
    Main_Category = scrapy.Field()
    # images = scrapy.Field()
