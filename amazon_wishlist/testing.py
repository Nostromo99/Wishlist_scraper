import shelve
import os
import requests

def output():
    x=os.system("scrapy crawl book_depository")
    # process=CrawlerProcess()
    # process.crawl(book_depository_spider)
    # process.start()
    db=shelve.open("list")
    for item in db:
        var=db[item]
        print(var.name+"\t| current:€"+str(var.price)+"\t| avg:€"+str(var.avg)+"\t| min:€"+str(var.lowest))
    db.close()
def add():
    url=input("url? ")
    check=requests.get(url)
    if check.ok and "bookdepository" in url:
        with open("urls.txt","a") as urls:
            urls.write(url)
            print("item added to list")

    else:
        print("url not valid")
def remove():
    numbers={}
    pointer=0
    db=shelve.open("list")
    for item in db:
        pointer+=1
        profile=db[item]
        print(str(pointer)+": "+profile.name + "\t| current:€" + str(profile.price) + "\t| avg:€" + str(profile.avg) + "\t| min:€" + str(profile.lowest))
        numbers[pointer]=profile
    resonse=int(input("select the number you wish to remove: "))
    if numbers.get(resonse):
        temp=numbers[resonse]
        print(temp.name+" removed")
        with open("urls.txt", "r") as url:
            urls=url.readlines()
        with open("urls.txt","w") as new:
            for url in urls:
                if url.strip("\n")!=temp.link:
                    new.write(url)
        del db[temp.name]
        db.close()
    else:
        print("invalid input")

responses={"output":"output()","add":"add()","remove":"remove()"}
while True:
    user_in=input("input?: ")
    if user_in=="exit":
        break
    elif responses.get(user_in):
        exec(responses[user_in])
    else:
        print("unrecognised command")
