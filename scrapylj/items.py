# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyljItem(scrapy.Item):
    # define the fields for your item here like:
    housename = scrapy.Field() #小区名字
    houseprice = scrapy.Field()  # 小区每平米价格
    reference = scrapy.Field()  # 价格参考时间
    onsalecount = scrapy.Field()  # 在售数量
    day30sale = scrapy.Field()  # 近30天销售数量
    onrentout = scrapy.Field()  # 正在出租数量
    housetypecount = scrapy.Field() #户型数量
    locationregion = scrapy.Field() #所属区 eg：西城
    locationinfo = scrapy.Field() #位置信息 eg: 广安门
    housetype = scrapy.Field() #建筑类型 eg:塔楼/塔板结合
    tagList = scrapy.Field() #标签信息
    buildtime = scrapy.Field() #建成时间
    housenumber = scrapy.Field() #房屋栋数
    housecount = scrapy.Field() #房屋总数


