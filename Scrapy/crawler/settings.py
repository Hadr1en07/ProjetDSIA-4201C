# Scrapy settings for Nintendo project
"""
Code by Hadrien DEJONGHE & Esteban NABONNE:
"""

BOT_NAME = "nintendo_scraper"

SPIDER_MODULES = ["crawler.spiders"]
NEWSPIDER_MODULE = "crawler.spiders"

#Pour désactiver l'obéissance au robots.txt
ROBOTSTXT_OBEY = False

#Activer la pipeline
ITEM_PIPELINES = {
    "crawler.pipelines.NintendoPipeline": 300,
}

#Activer les middlewares
DOWNLOADER_MIDDLEWARES = {
    "crawler.middlewares.UserAgentMiddleware": 400,
}

# Réglages anti-bannissement
AUTOTHROTTLE_ENABLED = True
DOWNLOAD_DELAY = 2