# -*- coding: utf-8 -*-
from scrapy import Spider, FormRequest
import scrapy
import datetime
import json

from loadtv.items import LoadtvItem, Channel, Number


class WarnerSpider(Spider):
    name = "warner"
    title = 'Warner Bros'
    allowed_domains = ["www.warnerchannel.com"]

    def start_requests(self):
        date = datetime.datetime.today()
        return [
            FormRequest('http://www.warnerchannel.com/apis/schedules/getday/br/%s' % date.strftime('%Y-%m-%d'), callback=self.parse)
        ]

    def parse(self, response):
        items = []
        res = json.loads(response.body_as_unicode())

        for show in res['list']:
            item = LoadtvItem()
            item['name'] = 'warnerbros'
            item['hour'] = show['startf']
            item['title'] = "%s - %s" % (show['program'], show['title'])
            item['desc'] = show['description']
            item['duraction'] = (show['end']['sec'] - show['start']['sec'])/60
            items.append(item)

        return items

    def get_channels(self):
        return [
            Channel(title='Warner bros', name='warnerbros', group_title=self.title, group=self.name, numbers=[Number(name='NET', num=632)]),
        ]
