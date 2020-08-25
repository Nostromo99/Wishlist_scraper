import scrapy
from .. Profile import Profile
import shelve
import hashlib
from scrapy.http.request import Request
class book_depository_spider(scrapy.Spider):
    name="book_depository"
    start_urls=[]
    def start_requests(self):
        with open('urls.txt', "r") as urls:
            for url in urls:
                yield Request(url,self.parse)
    def parse(self, response):
        title=response.css('h1').css("::text").extract()
        price=response.css('.sale-price').css("::text").extract()
        image=response.css('.book-img').css("img::attr(src)").extract()
        db = shelve.open("list")

        price[0]=price[0].strip("€")
        price[0]=price[0].replace(",",".")
        info=Profile(name=title[0],price=float(price[0]),link=str(response)[5:-1],avg=float(price[0]),lowest=float(price[0]),image_urls=image,file=hashlib.sha1(image[0].encode("utf-8")).hexdigest())
        try:
            sub=db[info.get("name")]
            if sub.get("price")!=info.get("price"):
                sub["avg"] = format((sub.get("avg") + (info.get("price") / 2),".2f"))
            sub["price"]=info.get("price")
            if sub["lowest"] > info.get("price"):
                sub["lowest"] = info.get("price")
            db[info.get("name")]=sub
            info["image_urls"]=[]

        except:
            db[info.get("name")]=info
        db.close()
        return info

