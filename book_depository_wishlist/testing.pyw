import shelve
import os
import requests
import PIL
from PIL import Image
from PIL import ImageTk
from tkinter import *
wishlist=Tk()
wishlist.geometry("1200x700")
scrollbar=Scrollbar(wishlist)
def bad_url(entry):
    entry.delete(0,END)
    entry.config(foreground="red",background="black")
    entry.insert(0,"invalid url")
    entry.bind("<Button-1>",lambda e:entry.config(foreground="black",background="white")or entry.delete(0,END))

def add(entry):
    url=entry.get()
    try:
        check=requests.get(url)
    except:
        bad_url(entry)
        print("hi")
        return
    if check.ok:
        with open("urls.txt","a") as urls:
            urls.write(url+"\n")
        update()

    else:
        print("HO")
        bad_url(entry)
def remove(row,item,inner_frame):
    db=shelve.open("list")
    with open("urls.txt", "r") as url:
        urls=url.readlines()
    with open("urls.txt","w") as new:
        for url in urls:
            if url.strip("\n")!=item["link"]:
                new.write(url)
    del db[item["name"]]
    db.close()
    for label in inner_frame.grid_slaves():
        if int(label.grid_info()["row"]==row):
            label.grid_forget()
    os.remove("book_depository_wishlist/images/full/"+item["file"]+".jpg")



def update():
    os.system("scrapy crawl book_depository -s LOG_ENABLED=False")
    db = shelve.open("list")
    row = 0
    widgets=wishlist.pack_slaves()
    buttons=[]
    rows=[]
    for item in widgets:
        item.destroy()
    outer_frame=Frame(wishlist)
    outer_frame.pack(fill=BOTH,expand=1)
    canvas=Canvas(outer_frame)
    canvas.pack(side=LEFT,fill=BOTH,expand=1)
    scrollbar=Scrollbar(outer_frame,command=canvas.yview)
    scrollbar.pack(side=RIGHT,fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>",lambda event:canvas.configure(scrollregion=canvas.bbox("all")))
    inner_frame=Frame(canvas)
    canvas.create_window((0,0),window=inner_frame,anchor="nw")
    canvas.bind_all("<MouseWheel>",lambda event:canvas.yview_scroll(-1*(int(event.delta/120)),"units"))
    for item in db:
        var=db[item]
        img=ImageTk.PhotoImage(PIL.Image.open("book_depository_wishlist/images/full/"+var["file"]+".jpg").resize((200,200)))
        rows.append(Frame(inner_frame))
        info_set=rows[row]
        info_set.grid(row=row,column=0,sticky=W)
        pic=Label(master=info_set, image=img)
        pic.photo=img
        pic.grid(row=row, column=0)
        Label(master=info_set,text=var["name"]+"\t").grid(row=row,column=1)
        Label(master=info_set,text= "|current:€"+str(var["price"])+"\t|").grid(row=row,column=2)
        Label(master=info_set,text= "avg:€"+str(var["avg"])+"\t|").grid(row=row,column=3)
        Label(master=info_set,text= "min:€"+str(var["lowest"])).grid(row=row,column=4)
        buttons.append(Button(master=info_set,text="remove",command=lambda i=row ,item=var ,frame=inner_frame: remove(i,item,frame)))
        buttons[row].grid(row=row,column=5)

        row+=1
    entry1=Entry(inner_frame)
    entry1.grid(row=row,column=0)
    Button(inner_frame,text="add",command=lambda: add(entry1)).grid(row=row+1,column=0,pady=5)

    db.close()
update()
wishlist.mainloop()