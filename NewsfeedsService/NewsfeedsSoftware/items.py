# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class NewsfeedssoftwareItem(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    content = Field()
    image_url = Field()
    address = Field()
    pass
