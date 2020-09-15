import scrapy
import os
from .. Profile import Profile
from scrapy.http.request import Request
from .book_depository_spider import *
class amazon_spider(scrapy.Spider):
    name="amazon"
    domain="https://www.amazon.co.uk/"

    def start_requests(self):
        with open('urls.txt', "r") as urls:
            for url in urls:
                if self.domain==re.match("h.*//.*?/",url).group(0):
                    yield Request(url,self.parse)
    def parse(self, response):
        if response.request.meta.get("redirect_urls")!=None:
            link=response.request.meta.get("redirect_urls")[0]
        else:link=response.request.url
        title=response.css("#productTitle").css("::text").extract()
        title[0]=title[0].strip("\n")
        price=response.css("#buyNewSection .a-text-normal").css("::text").extract()
        if len(price)==0:
            price=response.css("#price_inside_buybox").css("::text").extract()
            price[0]=price[0].strip("\n")
        image = response.css('#imgBlkFront').css("img::attr(src)").extract()
        if len(image)==0:
            image=response.css('#imgTagWrapperId').css("img::attr(src)").extract()
        currency="£"
        return process(title,price,image,currency,link)