import pymongo

class NintendoPipeline:
    def open_spider(self, spider):
        """Connexion à MongoDB lors du lancement de la spider."""
        self.client = pymongo.MongoClient("mongodb://root:example@db:27017/")
        self.client.drop_database("nintendo")  #réinitialise la base pour éviter les doublons
        self.db = self.client["nintendo"]
        self.collection = self.db["games"]

    def process_item(self, item, spider):
        """Ajoute les données dans la base MongoDB en évitant les doublons."""
        self.collection.update_one(
            {"title": item["title"]},
            {"$set": dict(item)},
            upsert=True
        )
        return item

    def close_spider(self, spider):
        """Ferme la connexion à MongoDB."""
        self.client.close()
