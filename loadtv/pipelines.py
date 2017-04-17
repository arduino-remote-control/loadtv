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
import tvshow_pb2 as tvshow
import requests
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
            buff = self.convert_pb(item, self.channel_info[item['name']]).SerializeToString()
            r = requests.post("http://localhost:8000/protobuf", data=buff)
            logging.info(r)

            logging.info('Item processed')
            return item
        except Exception as err:
            logging.error('Process Item Error: %s' % err)
            raise DropItem('Process Item Error: %s' % err)

    def convert_pb(self, item, channel):
        tv_item = tvshow.TvShow()
        tv_item.channel.group = channel.group
        tv_item.channel.group_title = channel.group_title
        tv_item.channel.name = channel.name
        tv_item.channel.title = channel.title
        tv_item.desc = item['desc']
        tv_item.title = item['title']
        tv_item.start = int(item['start'].timestamp())
        tv_item.end = int(item['end'].timestamp())
        tv_item.duraction = int(item['duraction'])
        return tv_item
