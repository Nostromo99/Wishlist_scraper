import scrapy
from .. Profile import Profile
from amazon_wishlist.amazon_wishlist.spiders.book_depository_spider import book_depository_spider
from scrapy.http.request import Request

class amazon_spider(scrapy.Spider):
    name="amazon"
    start_urls=[]
    def start_requests(self):
        with open('urls.txt', "r") as urls:
            for url in urls:
                yield Request(url,self.parse)
    def parse(self, response):
        title=response.css("#productTitle").css("::text").extract()
        price=response.css("#buyNewSection .a-text-normal").css("::text").extract()
        image = response.css('#imgBlkFront').css("img::attr(src)").extract()
        currency="£"
        return book_depository_spider.process(title,price,image,response,currency)