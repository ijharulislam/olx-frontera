# -*- coding: utf-8 -*-

# Scrapy settings for Olxscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Olxscraper'

SPIDER_MODULES = ['Olxscraper.spiders']
NEWSPIDER_MODULE = 'Olxscraper.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Olxscraper (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS=40

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN=20
CONCURRENT_REQUESTS_PER_IP=20

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Olxscraper.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'Olxscraper.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'Olxscraper.pipelines.OlxscraperPipeline': 300,
}
# ITEM_PIPELINES = {
#     'scrapy.contrib.pipeline.images.ImagesPipeline': 1
# }

# IMAGES_EXPIRES = 180 # The amount of days until we re-download the image

# IMAGES_THUMBS = {
#     'small': (50, 50), # You can add as many of these as you want
#     'big': (300, 300)
# }

# AWS_ACCESS_KEY_ID = "AKIAI5XIVSOW5PK4JQIQ"
# AWS_SECRET_ACCESS_KEY = "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"
# IMAGES_STORE = 's3://olximages/'

# MEDIA_ALLOW_REDIRECTS = True
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'


SPIDER_MIDDLEWARES = {}
DOWNLOADER_MIDDLEWARES = {}
SPIDER_MIDDLEWARES.update({
    'frontera.contrib.scrapy.middlewares.schedulers.SchedulerSpiderMiddleware': 999
}, )
DOWNLOADER_MIDDLEWARES.update({
    'frontera.contrib.scrapy.middlewares.schedulers.SchedulerDownloaderMiddleware':
    999
})
SCHEDULER = 'frontera.contrib.scrapy.schedulers.frontier.FronteraScheduler'
FRONTERA_SETTINGS = 'Olxscraper.frontera_settings'

HTTPCACHE_ENABLED = False
REDIRECT_ENABLED = True
COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 240
RETRY_ENABLED = False
DOWNLOAD_MAXSIZE = 1*1024*1024

# auto throttling
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = False
AUTOTHROTTLE_MAX_DELAY = 3.0
AUTOTHROTTLE_START_DELAY = 0.25
RANDOMIZE_DOWNLOAD_DELAY = False

# concurrency
CONCURRENT_REQUESTS = 64
CONCURRENT_REQUESTS_PER_DOMAIN = 10
DOWNLOAD_DELAY = 0.0

LOG_LEVEL = 'DEBUG'

REACTOR_THREADPOOL_MAXSIZE = 32
DNS_TIMEOUT = 180

# SPIDER_MIDDLEWARES.update({
#     'frontera.contrib.scrapy.middlewares.seeds.file.FileSeedLoader': 650
# })

# SEEDS_SOURCE = 'Olxscraper/seeds.txt'


