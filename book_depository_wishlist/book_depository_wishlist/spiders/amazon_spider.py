import scrapy
import os
from .. Profile import Profile
from scrapy.http.request import Request
from .book_depository_spider import *
import json
class amazon_spider(scrapy.Spider):
    name="amazon"
    domain="https://www.amazon.co.uk/"
    def __init__(self,param=None):
        self.param=param
    def start_requests(self):
        if self.param:
            if self.domain == re.match("h.*//.*?/", self.param).group(0):
                yield Request(self.param,self.parse)
        else:
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
            if len(price)==0:
                price = response.css("#priceblock_ourprice").css("::text").extract()
                if len(price)==0:
                    price = ["out of stock"]
        price[0]=price[0].strip("\n")

        ###################################
        #future bugs possible
        bugfix = response.css('#imgBlkFront').css("img::attr(data-a-dynamic-image)").extract()
        if len(bugfix)==0:
            bugfix = response.css('#imgTagWrapperId').css("img::attr(data-a-dynamic-image)").extract()
        image = [list(json.loads(bugfix[0]).keys())[0]]

        currency="£"
        return process(title,price,image,currency,link)