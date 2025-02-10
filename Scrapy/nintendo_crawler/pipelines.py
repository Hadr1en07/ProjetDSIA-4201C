from elasticsearch import Elasticsearch
import pymongo

class NintendoPipeline:
    def open_spider(self, spider):
        """Connexion à MongoDB et à Elasticsearch lors du lancement de la spider."""
        self.client = pymongo.MongoClient("mongodb://root:example@db:27017/")
        self.client.drop_database("nintendo")  #pour repartir sur une base vide
        self.db = self.client["nintendo"]
        self.collection = self.db["games"]

        # Connexion à Elasticsearch
        self.es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200, 'scheme': 'http'}])
    
    def process_item(self, item, spider):
        """Insère le document dans MongoDB et l'indexe dans Elasticsearch."""
        self.collection.update_one(
            {"title": item["title"]},
            {"$set": dict(item)},
            upsert=True
        )
        #on indexe dans Elasticsearch également (ici, on utilise le titre comme identifiant)
        self.es.index(index="games", body=dict(item))
        return item

    def close_spider(self, spider):
        """Ferme la connexion MongoDB."""
        self.client.close()
