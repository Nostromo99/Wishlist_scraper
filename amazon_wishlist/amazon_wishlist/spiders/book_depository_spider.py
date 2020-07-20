import scrapy
from .. Profile import Profile
import shelve
class book_depository_spider(scrapy.Spider):
    name="book_depository"
    start_urls=["https://www.bookdepository.com/Vinland-Saga-1-Makoto-Yukimura/9781612624204?ref=grid-view&qid=1590090133787&sr=1",
                "https://www.bookdepository.com/Berserk-Deluxe-3-Kentaro-Miura/9781506712000?ref=grid-view&qid=1590432366045&sr=1-3"''
                "https://www.bookdepository.com/Promised-Neverland-Vol-1-KAIU-SHIRAI/9781421597126?ref=grid-view&qid=1590432308949&sr=1-1",
                "https://www.bookdepository.com/20th-Century-Boys-Perfect-Edition-Vol-1-Naoki-Urasawa/9781421599618?ref=grid-view&qid=1590432410208&sr=1-1",
                "https://www.bookdepository.com/Promised-Neverland-Vol-1-KAIU-SHIRAI/9781421597126?ref=grid-view&qid=1592335700127&sr=1-1"






                ]
    def parse(self, response):
        title=response.css('h1').css("::text").extract()
        price=response.css('.sale-price').css("::text").extract()
        db = shelve.open("list")
        for i in range(len(title)):
            price[i]=price[i].strip("€")
            price[i]=price[i].replace(",",".")
            info=Profile(title[i],float(price[i]),self.name)
            try:
                sub=db[info.name]
                if sub.price!=info.price:
                    sub.avg = (sub.avg + info.price) / 2
                sub.price=info.price

                if sub.lowest > info.price:
                    sub.lowest = info.price
                db[info.name]=sub

            except:
                db[info.name]=info
        db.close()
# class Profile:
#     def __init__(self,name,price,site):
#         self.name=name
#         self.price=price
#         self.site=site
#         self.lowest=price
#         self.avg=price
