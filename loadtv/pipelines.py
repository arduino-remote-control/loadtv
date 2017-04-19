# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import datetime
from scrapy.exporters import BaseItemExporter
from scrapy.exceptions import DropItem
from loadtv import settings, items
import time
import os
import requests
import json
os.environ['TZ'] = 'America/Sao_Paulo'
time.tzset()

class LoadtvPipeline(BaseItemExporter):
    def open_spider(self, spider):
        try:
            logging.info('checking the channels')
            self.channel_info = {x.name: x for x in spider.get_channels()}
            logging.debug('Channels: %s' % self.channel_info)
        except Exception as err:
            logging.error('Open Spider Error: %s' % err)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        try:
            logging.info('Process item')
            date = datetime.datetime.now()
            item['start'] = date.replace(hour=int(item['hour'][:2]), minute=int(item['hour'][3:]), second=0, microsecond=0)
            item['end'] = item['start'] + datetime.timedelta(minutes=item['duraction'])
            item['channel_id'] = self.channel_info[item['name']].to_json()

            url = spider.tvshow_url if spider.tvshow_url is not None else 'http://localhost:8080/import'
            logging.info("Request to %s" % url)
            r = requests.post(url, data=json.dumps(item.to_json()))

            logging.info('Item processed')
            return item
        except Exception as err:
            raise DropItem('Process Item Error: %s' % err)
