# -*- coding: utf-8 -*-
import sys

from scrapy import optional_features
from scrapy.crawler import CrawlerProcess

from spiders.category import CategorySpider

optional_features.remove('boto')

settings = {'TELNETCONSOLE_ENABLED': False, 'COOKIES_ENABLED': False, 'ITEM_PIPELINES': {
    'pipelines.DuplicatePipeline': 200,
    'pipelines.ToRedisPipeline': 300,
    'pipelines.ToMongoPipeline': 400,
}, 'LOG_LEVEL': 'INFO', 'prefix': 'chargers',
            'base_url': 'http://www.aliexpress.com/category/100003571/chargers-docks.html'}

crawlera_settings = dict(settings)
crawlera_settings.update({'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 600},
                          'CRAWLERA_ENABLED': True,
                          'CRAWLERA_USER': sys.argv[1],
                          'CRAWLERA_PASS': '',
                          'CONCURRENT_REQUESTS': 10,
                          'CONCURRENT_REQUESTS_PER_DOMAIN': 10,
                          'AUTOTHROTTLE_ENABLED': False,
                          'DOWNLOAD_TIMEOUT': 600})

process = CrawlerProcess(settings)
process.crawl(CategorySpider, lambda rate, order: rate >= 100 or order >= 100)

# process = CrawlerProcess(crawlera_settings)
# process.crawl(ProductSpider)

# for i in xrange(100):
#     process.crawl(FeedbackSpider)
#     process.crawl(OrderSpider)
#
# process.crawl(StoreSpider)

process.start()
