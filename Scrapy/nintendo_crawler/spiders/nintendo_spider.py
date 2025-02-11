"""
Code by Hadrien DEJONGHE & Esteban NABONNE:
"""
import scrapy
import json
from pymongo import MongoClient
from nintendo_crawler.items import NintendoGameItem

class NintendoSpider(scrapy.Spider):
    name = "nintendo_spider"
    allowed_domains = ["nintendo.com"]
    start_urls = ['https://www.nintendo.com/fr-fr/Jeux/Jeux-347085.html']

    def parse(self, response):
        """Parcourt la liste des jeux et suit chaque lien"""
        for game in response.css("li.page-list-group-item"):
            item = NintendoGameItem()
            item["title"] = game.attrib.get("data-nt-item-title", "").strip()
            item["link"] = response.urljoin(game.css("a::attr(href)").get())
            item["image"] = game.css("img::attr(data-xs)").get()
            item["description"] = game.css(".page-description span::text").get(default="").strip()

            #aller sur la page du jeu pour récupérer prix, âge et genre
            yield response.follow(item["link"], self.parse_game_details, meta={"item": item})

    def parse_game_details(self, response):
        """Récupère les informations détaillées du jeu"""
        item = response.meta["item"]

        #extraction des prix, genre, âge
        script_text = response.xpath("//script[contains(text(), 'offdeviceProductPrice')]/text()").get()
        if script_text:
            item["price"] = self.extract_json_value(script_text, "offdeviceProductPrice") or "N/A"
            item["age_rating"] = self.extract_json_value(script_text, "gameAgeRatingValue") or "N/A"
            item["genre"] = self.extract_json_value(script_text, "gameGenre") or "N/A"
        else:
            item["price"] = "N/A"
            item["age_rating"] = "N/A"
            item["genre"] = "N/A"

        yield item

    def extract_json_value(self, script_text, key):
        """Extrait une valeur spécifique d'un JSON en texte brut"""
        import re
        match = re.search(rf'"{key}":\s*"([^"]+)"', script_text)
        return match.group(1) if match else None



