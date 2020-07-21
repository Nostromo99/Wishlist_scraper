import shelve
import os

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

def output():
    x=os.system("scrapy crawl book_depository")
    db=shelve.open("list")
    for item in db:
        var=db[item]
        print(var.name+"\t| current:€"+str(var.price)+"\t| avg:€"+str(var.avg)+"\t| min:€"+str(var.lowest))
    db.close()
    print(x)
# output()
responses={"output":"output()"}
while True:
    user_in=input("input?: ")
    if user_in=="exit":
        break
    elif responses.get(user_in):
        exec(responses[user_in])
    else:
        print("unrecognised command")