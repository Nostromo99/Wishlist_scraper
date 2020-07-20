import scrapy
from .. Profile import Profile
class amazon_spider(scrapy.Spider):
    name="amazon"
    start_urls=[
        "https://www.amazon.co.uk/Vinland-Saga-1-Makoto-Yukimura/dp/1612624200/ref=sr_1_1?dchild=1&keywords=vinland+saga&qid=1593526281&sr=8-1"
    ]
    def parse(self, response):
        title=response.css("#productTitle").css("::text").extract()
        price=response.css("#buyNewSection .a-text-normal").css("::text").extract()
        print(title)
        print(price)