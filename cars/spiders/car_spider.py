import scrapy
from scrapy.selector import Selector
from scrapy.loader import ItemLoader, Identity
from cars.items import CarsItem
class CarSpider(scrapy.Spider):
    name = "cars"
    count = 0
    allow_domains = ["http://car.autohome.com.cn"]
    start_urls = []
    for i in xrange(300):
        start_urls.append('http://car.autohome.com.cn/pic/brand-'+str(i)+'.html')

    def parse(self,response):
        sel = Selector(response)
        links = sel.xpath('//a[contains(@title," ")]/@href').extract()
        if links:
            self.count +=1
            print 'site count',self.count
            for link in links:
                link_vec = link.split('.')
                link = link_vec[0]+'-1.'+link_vec[-1]
           # print link
                request = scrapy.Request(self.allow_domains[0]+link,callback=self.parse_brand)
                yield request
    def parse_brand(self,response):
        sel = Selector(response)
        links = sel.xpath('//div[@class="page"]/a[contains(@href,"/pic/")]/@href').extract()
        if len(links) > 0:
            links[-1] = links[-1].replace('p2','p1')
            for link in links:
             #   print link
                request = scrapy.Request(self.allow_domains[0]+link,callback=self.parse_item)
                yield request


    def parse_item(self,response):
        sel = Selector(response)
        l = ItemLoader(item =CarsItem(),response=response)
        name = sel.xpath('//div[@class="cartab-title"]/h2/a/text()').extract()[0].encode('utf-8')
        l.add_value('name',name)
        for link in sel.xpath('//a[@target="_blank"]/img/@src').extract():
            link = link.replace('t_','u_')
            l.add_value('image_urls',link)
           # print link
        return l.load_item()
