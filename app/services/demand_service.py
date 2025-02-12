import geopandas as gpd
import pandas as pd
from app.services.geo_service import GeoService
from app.services.mongo_service import MongoService
from config.config import Config
from app.utils.logger import logger
import os
import json
import requests

class DemandService:
    def __init__(self):
        self.geo_service = GeoService()
        self.mongo_service = MongoService()
        
    def calculate_demand(self, entity_id, lat, lng):
        """Calculate demand for given entity_id and coordinates"""
        try:
            logger.debug(f"Starting demand calculation for entity_id={entity_id}, lat={lat}, lng={lng}")
            
            mapped_blocks = self.geo_service.map_cities_to_blocks(
                self.geo_service.blocks,
                self.geo_service.cities
            )
            
            # Get circle data with mapped blocks
            city_data = self.geo_service.process_circle_data(lat, lng, mapped_blocks, entity_id)
            
            # Save to MongoDB
            self.mongo_service.save_city_data(city_data)
            
            return city_data            
        except Exception as e:
            logger.error(f"Error in calculate_demand: {str(e)}")
            raise Exception(f"Failed to calculate demand: {str(e)}")
