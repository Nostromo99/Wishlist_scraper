import scrapy
class amazon_spider(scrapy.Spider):
    name="book_depository"
    start_urls=["https://www.bookdepository.com/Vinland-Saga-1-Makoto-Yukimura/9781612624204?ref=grid-view&qid=1590090133787&sr=1"]
    def parse(self, response):
        title=response.css('h1').css("::text").extract()
        price=response.css('.sale-price').css("::text").extract()

        with open("prices.json","a") as info:
            info.write(str(title[0]))
            info.write(str(price[0]))
            info.close()
