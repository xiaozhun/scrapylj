# -*- coding: utf-8 -*-
import scrapy
from scrapylj.items import ScrapyljItem
import re

class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    myurls =['https://bj.lianjia.com/xiaoqu/dongcheng/']
    myurls.append('https://bj.lianjia.com/xiaoqu/xicheng/')
    # myurls.append('https://bj.lianjia.com/xiaoqu/chaoyang/')
    # myurls.append('https://bj.lianjia.com/xiaoqu/haidian/')
    # myurls.append('https://bj.lianjia.com/xiaoqu/fengtai/')
    # myurls.append('https://bj.lianjia.com/xiaoqu/shijingshan/')
    # myurls.append('https://bj.lianjia.com/xiaoqu/tongzhou/')
    # myurls.append('https://bj.lianjia.com/xiaoqu/changping/')
    # myurls.append('https://bj.lianjia.com/xiaoqu/daxing/')
    # myurls.append('https://bj.lianjia.com/xiaoqu/yizhuangkaifaqu/')
    # myurls.append('https://bj.lianjia.com/xiaoqu/shunyi/')
    # myurls.append('https://bj.lianjia.com/xiaoqu/fangshan/')
    # myurls.append('https://bj.lianjia.com/xiaoqu/mentougou/')
    # myurls.append('https://bj.lianjia.com/xiaoqu/pinggu/')
    # myurls.append('https://bj.lianjia.com/xiaoqu/huairou/')
    # myurls.append('https://bj.lianjia.com/xiaoqu/miyun/')
    # myurls.append('https://bj.lianjia.com/xiaoqu/yanqing/')
    start_urls = []
    for urls in myurls:
        for i in range(1,2,1):
            start_urls.append(urls+'pg'+str(i)+'/')
    # 处理按区域查询出的小区信息
    def parse(self, response):
        house = response.xpath('//li[@class="clear xiaoquListItem"]')
        print(len(house))
        for onehouse in house:
            item = ScrapyljItem()
            titleurl = onehouse.xpath('div[@class="info"]/div[@class="title"]/a/@href').extract()[0]
            # print(titleurl)
            if onehouse.xpath('div[@class="info"]/div[@class="title"]/a/text()').extract()[0]:
                item['housename'] = onehouse.xpath('div[@class="info"]/div[@class="title"]/a/text()').extract()[0]
            else:
                continue
            # 获取成交信息
            housesale = onehouse.xpath('div[@class="info"]/div[@class="houseInfo"]').xpath('string(.)').extract()
            if housesale:
                hif = housesale[0].replace(' ','').replace('\n','').split('|')
                for one in hif:
                    if len(re.findall(r"30天成交(.+?)套",one))>0:
                        item['day30sale']=re.findall(r"30天成交(.+?)套",one)[0]
                    if len(re.findall(r"(.+?)套正在出租",one))>0:
                        item['onrentout']=re.findall(r"(.+?)套正在出租",one)[0]
                    if len(re.findall(r"共(.+?)个户型",one))>0:
                        item['housetypecount']=re.findall(r"共(.+?)个户型",one)[0]
            # 获得小区位置信息
            locationregion = onehouse.xpath('div[@class="info"]/div[@class="positionInfo"]/a[1]/text()').extract()
            if locationregion:
                item['locationregion']=locationregion[0]
            locationinfo = onehouse.xpath('div[@class="info"]/div[@class="positionInfo"]/a[2]/text()').extract()
            if locationinfo:
                item['locationinfo'] = locationinfo[0]
            tagList = onehouse.xpath('div[@class="info"]/div[@class="tagList"]/span/text()').extract()
            if tagList:
                item['tagList']=tagList[0]
            # 获取价格信息
            houseprice = onehouse.xpath('div[@class="xiaoquListItemRight"]/div[@class="xiaoquListItemPrice"]/div[@class="totalPrice"]/span/text()').extract()
            if houseprice:
                item['houseprice']=houseprice[0]
            reference = onehouse.xpath('div[@class="xiaoquListItemRight"]/div[@class="xiaoquListItemPrice"]/div[@class="priceDesc"]/text()').extract()
            if reference:
                item['reference']=reference[0].replace(' ','').replace('\n','')
            # 进入子页面继续解析
            yield scrapy.Request(titleurl, meta={'item': item}, callback=self.childparse)
    def childparse(self,response):
        item = response.meta['item']
        # 2009年建成
        buildtime = response.xpath('//div[@class="xiaoquInfo"]/div[1]/span[2]/text()').extract()[0]
        if buildtime:
            if len(re.findall(r"(.+?)年建成", buildtime)) > 0:
                item['buildtime'] = re.findall(r"(.+?)年建成", buildtime)[0]
        #塔楼/塔板结合
        housetype = response.xpath('//div[@class="xiaoquInfo"]/div[2]/span[2]/text()').extract()[0]
        if housetype:
            item['housetype'] = housetype
        # 房屋栋数
        housenumber = response.xpath('//div[@class="xiaoquInfo"]/div[6]/span[2]/text()').extract()[0]
        if housenumber:
            item['housenumber'] = housenumber
        # 房屋总数
        housecount = response.xpath('//div[@class="xiaoquInfo"]/div[7]/span[2]/text()').extract()[0]
        if housecount:
            item['housecount'] = housecount
        yield item