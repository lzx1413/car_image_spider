import scrapy
from scrapy.selector import Selector
from scrapy.loader import ItemLoader, Identity
from cars.items import CarsItem
class CarSpider(scrapy.Spider):
    name = "bitauto"
    count = 0
    allow_domains = ["http://photo.bitauto.com"]
    start_urls = []
    for i in xrange(300):
        start_urls.append('http://photo.bitauto.com/master/'+str(i)+'/')

    def parse(self,response):
        sel = Selector(response)
        links = sel.xpath('//div[@class="title"]/a/@href').extract()
        if links:
            self.count +=1
            print 'site count',self.count
            for link in links:
                request = scrapy.Request(self.allow_domains[0]+link,callback=self.parse_brand)
                yield request
    def parse_brand(self,response):
        sel = Selector(response)
        links = sel.xpath('//ul[@class="title-tab"]/li/a[contains(@href,"/serial/")]/@href').extract()
        if len(links) > 0:
            for link in links:
             #   print link
                request = scrapy.Request(self.allow_domains[0]+link,callback=self.parse_year)
                yield request
    def parse_year(self,response):
        sel = Selector(response)
        links = sel.xpath('//div[@class="color-w-box"]/a[contains(@href,"/model/")]/@href').extract()
        if links:
            for link in links:
                link = link.replace('model','modelmore')
                link = self.allow_domains[0]+link[:-12]+'6/1/'+link[-12:]
                print link
                request = scrapy.Request(link,callback=self.parse_item)
                yield request
    def parse_item(self,response):
        sel = Selector(response)
        l = ItemLoader(item =CarsItem(),response=response)
        links = sel.xpath('//img/@src').extract()
        for link in links:
            link = link.replace('_1.','_16.')

            l.add_value('image_urls',link)
            print link
        name = sel.xpath('//div[@class="title-box"]/h3/text()').extract()[0].encode('utf-8')
        l.add_value('name',name)
        return l.load_item()
