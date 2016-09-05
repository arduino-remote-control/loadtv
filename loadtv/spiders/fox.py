from scrapy import Spider, FormRequest
from scrapy.selector import Selector
import datetime

from loadtv.items import LoadtvItem, Channel, Number

class FoxSpider(Spider):
    name = "fox"
    title = 'Fox'
    allowed_domains = ["www.foxplaybrasil.com.br"]

    def start_requests(self):
        date = datetime.datetime.today()
        return [
            FormRequest('http://www.foxplaybrasil.com.br/listings/%s/' % date.strftime('%Y-%m-%d'), callback=self.parse)
        ]

    def parse(self, response):
        k = 1
        items = []
        channels = Selector(response).xpath('//*[@id="schedule"]/ol/li')
        for c in channels:
            xpath = '//*[@id="scheduleItems"]/div[%d]/div' % k
            name = c.xpath('a/@title').extract_first()
            shows = Selector(response).xpath(xpath)
            for s in shows:
                item = LoadtvItem()
                hours = s.xpath('div/h4/text()').extract_first()
                item['name'] = name
                item['hour'] = hours[:5]
                item['title'] = s.xpath('div/h2/text()').extract_first()
                item['desc'] = ''
                item['duraction'] = self.get_duraction(hours[:5], hours[8:]).total_seconds()/60
                items.append(item)
            k += 1
        return items

    def get_duraction(self, h1, h2):
        date = datetime.datetime.now()
        dt1 = date.replace(hour=int(h1[:2]), minute=int(h1[3:]), second=0, microsecond=0)
        dt2 = date.replace(hour=int(h2[:2]), minute=int(h2[3:]), second=0, microsecond=0)
        return dt2 - dt1

    def get_channels(self):
        return [
            Channel(title='Nat Geo Wild', name='Nat Geo Wild', group_title=self.title, group=self.name, numbers=[Number('NET', 591)]),
            Channel(title='Nat Geo HD', name='Nat Geo HD', group_title=self.title, group=self.name, numbers=[Number('NET', 580)]),
            Channel(title='Nat Geo', name='Nat Geo', group_title=self.title, group=self.name, numbers=[Number('NET', 580)]),
            Channel(title='FX HD', name='FX HD', group_title=self.title, group=self.name, numbers=[Number('NET', 634)]),
            Channel(title='FX', name='FX', group_title=self.title, group=self.name, numbers=[Number('NET', 634)]),
            Channel(title='FOX HD', name='FOX HD', group_title=self.title, group=self.name, numbers=[Number('NET', 631)]),
            Channel(title='FOX', name='FOX', group_title=self.title, group=self.name, numbers=[Number('NET', 631)]),
            Channel(title='FOX1', name='FOX1', group_title=self.title, group=self.name, numbers=[Number('NET', 130)]),
            Channel(title='Fox Sports HD', name='Fox Sports HD', group_title=self.title, group=self.name, numbers=[Number('NET', 573)]),
            Channel(title='Fox Sports 2 HD', name='Fox Sports 2 HD', group_title=self.title, group=self.name, numbers=[Number('NET', 74)]),
            Channel(title='Fox Sports 2', name='Fox Sports 2', group_title=self.title, group=self.name, numbers=[Number('NET', 74)]),
            Channel(title='FOX Sports', name='FOX Sports', group_title=self.title, group=self.name, numbers=[Number('NET', 573)]),
            Channel(title='FOX Life', name='FOX Life', group_title=self.title, group=self.name, numbers=[Number('NET', 51)]),
            Channel(title='FOX Life HD', name='FOX Life HD', group_title=self.title, group=self.name, numbers=[Number('NET', 51)]),
            Channel(title='FOX Action', name='FOX Action', group_title=self.title, group=self.name, numbers=[]),
        ]
