# -*- coding: utf-8 -*-
##############################
# for items.py
from scrapy.exporters import CsvItemExporter
from scrapy.conf import settings
from fake_useragent import UserAgent


##############################
#for middlewares.py

class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()

        self.ua = UserAgent()
        self.per_proxy = crawler.settings.get('RANDOM_UA_PER_PROXY', False)
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')
        self.proxy2ua = {}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            '''Gets random UA based on the type setting (random, firefox…)'''
            return getattr(self.ua, self.ua_type)

        if self.per_proxy:
            proxy = request.meta.get('proxy')
            if proxy not in self.proxy2ua:
                self.proxy2ua[proxy] = get_ua()
                logger.debug('Assign User-Agent %s to Proxy %s'
                             % (self.proxy2ua[proxy], proxy))
            request.headers.setdefault('User-Agent', self.proxy2ua[proxy])
        else:
            request.headers.setdefault('User-Agent', get_ua())

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer

        request.headers["Proxy-Authorization"] = proxyAuth
