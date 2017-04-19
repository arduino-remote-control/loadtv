# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class LoadtvItem(scrapy.Item):
    channel_id = scrapy.Field()
    hour = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    duraction = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()

    def to_json(self):
        return {
            'channel': self['channel_id'],
            'title': self['title'],
            'desc': self['desc'],
            'duraction': self['duraction'],
            'start': self['start'].isoformat(),
            'end': self['end'].isoformat()
        }

class Channel:
    def __init__(self, name="", title="", group="", group_title="", numbers=[]):
        self.name = name
        self.title = title
        self.group = group
        self.numbers = numbers
        self.group_title = group_title

    def to_json(self):
        return {
            'name': self.name,
            'title': self.title,
            'group': self.group,
            'group_title': self.group_title,
            'numbers': {x.name: x.num for x in self.numbers}
        }

class Number:
    def __init__(self, name="", num=""):
        self.name = name
        self.num = num

    def to_json(self):
        return {
            'name': self.name,
            'num': self.num
        }
