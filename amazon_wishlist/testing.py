import shelve
import os
import requests
from tkinter import *
wishlist=Tk()
def add(url):
    try:
        check=requests.get(url)
    except:
        print("not a valid url")
        return
    if check.ok and "bookdepository" in url:
        with open("urls.txt","a") as urls:
            urls.write(url+"\n")
        update()

    else:
        print("url not valid")
def remove(row,item):
    db=shelve.open("list")
    with open("urls.txt", "r") as url:
        urls=url.readlines()
    with open("urls.txt","w") as new:
        for url in urls:
            if url.strip("\n")!=item.link:
                new.write(url)
    del db[item.name]
    db.close()
    for label in wishlist.grid_slaves():
        if int(label.grid_info()["row"]==row):
            label.grid_forget()

class geo():
    def __init__(self,profile,row):
        self.profile=profile
        self.row=row
def update():
    os.system("scrapy crawl book_depository")
    db = shelve.open("list")
    row = 0
    widgets=wishlist.grid_slaves()
    buttons=[]
    for item in widgets:
        item.destroy()
    for item in db:
        var=db[item]
        Label(master=wishlist,text=var.name+"\t").grid(row=row,column=0)
        Label(master=wishlist,text= "|current:€"+str(var.price)+"\t|").grid(row=row,column=1)
        Label(master=wishlist,text= "avg:€"+str(var.avg)+"\t|").grid(row=row,column=2)
        Label(master=wishlist,text= "min:€"+str(var.lowest)).grid(row=row,column=3)
        buttons.append(Button(master=wishlist,text="remove",command=lambda i=row ,item=var: remove(i,item)))
        buttons[row].grid(row=row,column=4)
        row+=1
    entry1=Entry(wishlist)
    entry1.grid(row=row,column=1)
    Button(wishlist,text="add",command=lambda: add(entry1.get())).grid(row=row+1,column=1)
    db.close()
update()
wishlist.mainloop()