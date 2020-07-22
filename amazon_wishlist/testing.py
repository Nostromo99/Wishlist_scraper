import shelve
import os
import requests
from scrapy.crawler import CrawlerProcess
from amazon_wishlist.amazon_wishlist.spiders.book_depository_spider import book_depository_spider
# def update():
#     info=shelve.open("list")
#     db=shelve.open("database")
#     for item in info:
#         try :
#             db[item.name].avg=(db[item.name].avg+item.price)/2
#             if db[item.name].lowest<item.price:
#                 db[item.name].lowest=item.price
#         except:
#             db[info[item].name]=info[item]
#     info.close()
#     db.close()
spider=book_depository_spider
def output():
    x=os.system("scrapy crawl book_depository")
    process=CrawlerProcess()
    process.crawl(book_depository_spider)
    process.start()
    db=shelve.open("list")
    for item in db:
        var=db[item]
        print(var.name+"\t| current:€"+str(var.price)+"\t| avg:€"+str(var.avg)+"\t| min:€"+str(var.lowest))
    db.close()
    print(x)
def add():
    url=input("url?")
    check=requests.get(url)
    if check.ok and "bookdepository" in url:
        book_depository_spider.start_urls.append(url)
        print(book_depository_spider.start_urls)
    else:
        print("url not valid")
responses={"output":"output()","add":"add()"}
while True:
    user_in=input("input?: ")
    if user_in=="exit":
        break
    elif responses.get(user_in):
        exec(responses[user_in])
    else:
        print("unrecognised command")