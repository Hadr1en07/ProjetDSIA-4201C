#from elasticsearch import Elasticsearch
#import pymongo

class NintendoPipeline:
    def process_item(self, item, spider):
        return item 

    #def open_spider(self, spider):
        #"""Connexion à MongoDB au lancement de la spider"""
        #self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        #self.db = self.client["nintendo"]
        #self.collection = self.db["games"]

    #def process_item(self, item, spider):
        #"""Ajoute les données dans la base MongoDB"""
        #self.collection.update_one(
            #{"title": item["title"]},  #pour éviter les doublons
            #{"$set": dict(item)},
            #upsert=True
        #)
        #return item

    #def close_spider(self, spider):
        #"""Ferme la connexion MongoDB"""
        #self.client.close()