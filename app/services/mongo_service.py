from pymongo import MongoClient
from config.config import Config
from app.utils.logger import logger

class MongoService:
    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client[Config.MONGODB_DB]
        self.collection = self.db[Config.MONGODB_COLLECTION]

    def save_city_data(self, city_data):
        """Save city contribution data to MongoDB"""
        try:
            result = self.collection.insert_many(city_data)
            logger.debug(f"Successfully saved {len(result.inserted_ids)} city records")
            return result.inserted_ids
        except Exception as e:
            logger.error(f"Error saving to MongoDB: {str(e)}")
            raise
