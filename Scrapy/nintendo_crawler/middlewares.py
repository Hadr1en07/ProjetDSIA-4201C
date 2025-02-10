# Define here the models for your spider middleware
"""
Code by Hadrien DEJONGHE & Esteban NABONNE:
"""

from scrapy import signals
from scrapy.exceptions import IgnoreRequest
import logging
import time

class NintendoSpiderMiddleware:
    """ Middleware pour gérer les requêtes entrantes et sortantes de la spider. """

    @classmethod
    def from_crawler(cls, crawler):
        """ Initialise le middleware et connecte les signaux. """
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        """ Appelé pour chaque réponse reçue par la spider. """
        spider.logger.info(f"Réponse reçue: {response.url}")
        return None

    def process_spider_output(self, response, result, spider):
        """ Appelé après que la spider ait traité la réponse. """
        for item in result:
            yield item

    def process_spider_exception(self, response, exception, spider):
        """ Gère les exceptions dans la spider. """
        spider.logger.error(f"Exception dans la spider : {exception}")
        pass

    def process_start_requests(self, start_requests, spider):
        """ Appelé lors de l’envoi des requêtes initiales. """
        for request in start_requests:
            spider.logger.info(f"Requête initiale : {request.url}")
            yield request

    def spider_opened(self, spider):
        spider.logger.info(f"Spider ouverte : {spider.name}")


class NintendoDownloaderMiddleware:
    """ Middleware pour gérer les requêtes avant et après leur téléchargement. """

    @classmethod
    def from_crawler(cls, crawler):
        """ Initialise le middleware et connecte les signaux. """
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """ Modifie ou bloque les requêtes avant leur envoi. """
        spider.logger.info(f"Envoi de requête: {request.url}")
        return None

    def process_response(self, request, response, spider):
        """ Traite les réponses avant qu’elles n’atteignent la spider. """
        if response.status != 200:
            spider.logger.warning(f"Réponse {response.status} pour {response.url}")
        return response

    def process_exception(self, request, exception, spider):
        """ Gère les erreurs de téléchargement. """
        spider.logger.error(f"Erreur de téléchargement : {exception} - {request.url}")
        time.sleep(2) 
        return None 

    def spider_opened(self, spider):
        spider.logger.info(f"Spider ouverte : {spider.name}")