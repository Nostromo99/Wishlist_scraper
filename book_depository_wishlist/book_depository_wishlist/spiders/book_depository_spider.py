import scrapy
from .. Profile import Profile
import shelve
import hashlib
import re
from scrapy.http.request import Request
class book_depository_spider(scrapy.Spider):
    name="book_depository"
    domain="https://www.bookdepository.com/"
    start_urls=[]
    def start_requests(self):
        with open('urls.txt', "r") as urls:
            for url in urls:
                if self.domain==re.match("h.*//.*?/",url).group(0):
                    yield Request(url,self.parse)
    def parse(self, response):
        title=response.css('h1').css("::text").extract()
        price=response.css('.sale-price').css("::text").extract()
        image=response.css('.book-img').css("img::attr(src)").extract()
        currency="€"
        return process(title,price,image,currency,response.request.url)

def process(title,price,image,currency,link):
    db = shelve.open("list")
    price[0] = price[0].strip(currency)
    price[0] = price[0].replace(",", ".")
    info = Profile(name=title[0], price=float(price[0]), link=link, avg=(float(price[0]),2),
                   lowest=float(price[0]), image_urls=image,
                   file=hashlib.sha1(image[0].encode("utf-8")).hexdigest(),currency=currency)
    try:
        sub = db[info.get("name")]
        if sub.get("price") != info.get("price"):
            sub["avg"] = (float(format(((sub.get("avg")[0]*(sub.get("avg")[1]-1)) + info.get("price")) / sub.get("avg")[1], ".2f")), sub.get("avg")[1]+1)
        sub["price"] = info.get("price")
        if sub["lowest"] > info.get("price"):
            sub["lowest"] = info.get("price")
        db[info.get("name")] = sub
        info["image_urls"] = []


    except:
        db[info.get("name")] = info
    db.close()
    return info