# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MedicationItem(scrapy.Item):
    source = scrapy.Field()
    source_url = scrapy.Field()
    name = scrapy.Field()
    generic_name = scrapy.Field()
    description = scrapy.Field()
    warnings = scrapy.Field()
    side_effects = scrapy.Field()
    how_to_take = scrapy.Field()
    pass
