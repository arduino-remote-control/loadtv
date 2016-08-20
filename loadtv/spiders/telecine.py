from scrapy.spiders import Spider
from scrapy.selector import Selector

from loadtv.items import LoadtvItem, Channel, Number


class TelecineSpider(Spider):
    name = "telecine"
    title = 'Telecine'
    allowed_domains = [
        "telecine.globo.com/programacao",
    ]
    start_urls = (
        'http://www.telecine.globo.com/programacao/',
    )

    def parse(self, response):
        items = []

        xpath = '//*[@id="ProgramacaoCompleta"]/section'
        shows = Selector(response).xpath(xpath)
        for s in shows:
            hour = s.xpath('span/text()').extract_first()
            for i in s.xpath('ul/li'):
                item = LoadtvItem()
                item['name'] = i.xpath('@data-canal').extract_first()
                item['title'] = i.xpath('article/strong/a/text()').extract_first()
                item['hour'] = hour
                item['desc'] = i.xpath('article/p/text()').extract_first()
                item['duraction'] = (int(i.xpath('@data-fim').extract_first()) - int(i.xpath('@data-inicio').extract_first()))/60
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
