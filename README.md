# Wishlist_scraper

## Overview
This tkinter app uses the [Scrapy](https://scrapy.org/) module to collect pricing information for specified items.
Items are added by pasting the url into the entry box and clicking add.
Items can be removed by simply clicking the remove button attached to each entry.
The wishlist currently supports items from amazon.co.uk and bookdepository.
[image](wishlist.PNG)
## adapting for personal use
More websites can be added by simply creating a scrapy spider that collects an items':
1.title
2.price
3.image url
4.currency
5.page url
These pieces of information can then be passed to the process function provided by book_depository_spider.
Once thats' done simply run the spider at the start of update() in testing.pyw
