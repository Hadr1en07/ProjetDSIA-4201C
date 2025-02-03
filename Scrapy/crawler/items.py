"""
Code by Hadrien DEJONGHE & Esteban NABONNE:

    Définition des items que l'on veut scraper sur le site web.
    Représente les données extraites pour un jeu vidéo particulier dans la partie Jeux du site 
    de Nintendo.
"""
import scrapy

class NintendoGameItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    age_rating = scrapy.Field()
    genre = scrapy.Field()
