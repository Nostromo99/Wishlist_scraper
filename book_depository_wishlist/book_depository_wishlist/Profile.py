from scrapy.item import Item, Field
class Profile(Item):

    name=Field()
    price=Field()
    link=Field()
    lowest=Field()
    avg=Field()
    image_urls = Field()
    images=Field()
    file=Field()
