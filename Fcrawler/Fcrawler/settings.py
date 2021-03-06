# -*- coding: utf-8 -*-

# Scrapy settings for Fcrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Fcrawler'

SPIDER_MODULES = ['Fcrawler.spiders']
NEWSPIDER_MODULE = 'Fcrawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Fcrawler (+http://www.yourdomain.com)'

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True

REDIS_HOST = 'localhost'
REDIS_PORT=6379

#禁止cookies,防止被ban  
COOKIES_ENABLED = False 

ITEM_PIPELINES = {  
    'Fcrawler.pipelines.FcrawlerPipeline':1  
} 

