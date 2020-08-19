import scrapy
from .. Profile import Profile
import shelve
import hashlib
from scrapy.http.request import Request
class book_depository_spider(scrapy.Spider):
    name="book_depository"
    # start_urls=["https://www.bookdepository.com/Vinland-Saga-1-Makoto-Yukimura/9781612624204?ref=grid-view&qid=1590090133787&sr=1",
    #             "https://www.bookdepository.com/Berserk-Deluxe-3-Kentaro-Miura/9781506712000?ref=grid-view&qid=1590432366045&sr=1-3"
    #             "https://www.bookdepository.com/Promised-Neverland-Vol-1-KAIU-SHIRAI/9781421597126?ref=grid-view&qid=1590432308949&sr=1-1",
    #             "https://www.bookdepository.com/20th-Century-Boys-Perfect-Edition-Vol-1-Naoki-Urasawa/9781421599618?ref=grid-view&qid=1590432410208&sr=1-1",
    #
    #
    #
    #
    #
    #
    #
    #             ]
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
        info=Profile(name=title[0],price=float(price[0]),link=str(response)[5:-1],avg=float(price[0]),lowest=float(price[0]),image_urls=image[0],file=hashlib.sha1(image[0].encode("utf-8")).hexdigest())
        try:
            sub=db[info.get("name")]
            if sub.price!=info.get("price"):
                sub["avg"] = format((sub.avg + info.get(price) / 2,".2f"))
            sub["price"]=info.get("price")

            if sub["lowest"] > info.get("price"):
                sub["lowest"] = info.get("price")
            db[info.get("name")]=sub

        except:
            db[info.get("name")]=info
        db.close()
        return info
# class Profile:
#     def __init__(self,name,price,site):
#         self.name=name
#         self.price=price
#         self.site=site
#         self.lowest=price
#         self.avg=price
