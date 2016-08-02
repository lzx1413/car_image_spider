#coding:utf-8
import scrapy
from scrapy.selector import Selector
from scrapy.loader import ItemLoader, Identity
from cars.items import CarsItem
class owner_car_spider(scrapy.Spider):
    name ="ownerauto"
    count = 0
    allow_domains = ["http://pic.16888.com"]
    start_urls = []
    with open('/home/zuoxin/workplace/car_image_spider/cars/spiders/16888_brand.list') as listfile:
        brandlist = listfile.readlines()
        for brand in brandlist:
            brand = brand.strip()
            start_urls.append('http://pic.16888.com'+brand+'70995/')
    def parse(self,response):
        sel = Selector(response)
        links = sel.xpath('//div[@class="page"]/a/@href').extract()
        self.count +=1
        print 'site count',self.count
        if links:
            links[-1]=links[-1].split('-')[0]+'-1'
            for link in links:
                request = scrapy.Request(self.allow_domains[0]+link,callback=self.parse_brand)
                yield request
        else:
            request = scrapy.Request(response.url,callback=self.parse_brand)
            yield request
	    
    def parse_brand(self,response):
        sel = Selector(response)
        links = sel.xpath('//div[@class="show_cars"]/ul/li/a/img/@src').extract()
        name = sel.xpath('//span[@class="ico_w"]/em/text()').extract()[0]
        name = name[:-4]
        l = ItemLoader(item =CarsItem(),response=response)
        l.add_value('name',name)
        for link in links:
            link = link.replace('120_90','800_600')
            l.add_value('image_urls',link)
        return l.load_item()

