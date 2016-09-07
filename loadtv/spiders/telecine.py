from scrapy import Spider, FormRequest
from scrapy.selector import Selector
import datetime
import time
import logging
import os

from loadtv.items import LoadtvItem, Channel, Number
os.environ['TZ'] = 'America/Sao_Paulo'
time.tzset()


class TelecineSpider(Spider):
    name = "telecine"
    title = 'Telecine'
    allowed_domains = [
        "telecine.globo.com/programacao",
    ]

    def start_requests(self):
        logging.info('NOW: {}'.format(datetime.datetime.now()))
        date = datetime.datetime.today()
        url = 'http://telecine.img.estaticos.tv.br/rendered/static/grade_htmls/%s.html' % date.strftime('%d_%m_%Y')
        logging.info('URL: \'{}\''.format(url));
        return [
            FormRequest(url, callback=self.parse)
        ]

    def parse(self, response):
        items = []

        shows = response.xpath('*')[0].xpath('section')
        for s in shows:
            hour = s.xpath('span/text()').extract_first()
            for i in s.xpath('ul/li'):
                item = LoadtvItem()
                item['name'] = i.xpath('@data-canal').extract_first()
                item['title'] = i.xpath('article/strong/a/text()').extract_first()
                item['hour'] = hour
                item['desc'] = i.xpath('article/p/text()').extract_first()
                item['duraction'] = (int(i.xpath('@data-fim').extract_first()) - int(i.xpath('@data-inicio').extract_first()))/60
                logging.info(item)
                items.append(item)

        return items

    def get_channels(self):
        return [
            Channel(title='Telecine Premium', name='tcpremium', group_title=self.title, group=self.name, numbers=[Number(name='NET', num=661)]),
            Channel(title='Telecine Action', name='tcaction', group_title=self.title, group=self.name, numbers=[Number(name='NET', num=662)]),
            Channel(title='Telecine Touch', name='tctouch', group_title=self.title, group=self.name, numbers=[Number(name='NET', num=663)]),
            Channel(title='Telecine Fun', name='tcfun', group_title=self.title, group=self.name, numbers=[Number(name='NET', num=664)]),
            Channel(title='Telecine Pipoca', name='tcpipoca', group_title=self.title, group=self.name, numbers=[Number(name='NET', num=665)]),
            Channel(title='Telecine Cult', name='tccult', group_title=self.title, group=self.name, numbers=[Number(name='NET', num=666)])
        ]
