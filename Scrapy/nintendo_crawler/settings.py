# Scrapy settings for Nintendo project
"""
Code by Hadrien DEJONGHE & Esteban NABONNE:
"""

BOT_NAME = "nintendo_crawler"

SPIDER_MODULES = ["nintendo_crawler.spiders"]
NEWSPIDER_MODULE = "nintendo_crawler.spiders"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

#Pour désactiver l'obéissance au robots.txt
ROBOTSTXT_OBEY = False

#Activer la pipeline
ITEM_PIPELINES = {
    'nintendo_crawler.pipelines.NintendoPipeline': 300,
}

MONGO_URI = 'mongodb://root:example@db:27017'
MONGO_DATABASE = 'nintendo_db'

#Activer les middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,
}

# Réglages anti-bannissement
AUTOTHROTTLE_ENABLED = True
DOWNLOAD_DELAY = 2
FEED_EXPORT_ENCODING = 'utf-8'