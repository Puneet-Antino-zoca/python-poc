import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    API_URL = os.environ.get('API_URL')
    
    # Data file paths
    BLOCKS_SHAPEFILE = 'data/shapefiles/blocks/tl_2024_13_tabblock20.shp'
    PLACES_SHAPEFILE = 'data/shapefiles/places/tl_2024_13_place.shp'
    GOOGLE_ADS_CSV = 'data/csv/GeorgiaOnGoogleAds.csv'

    # MongoDB Configuration
    MONGODB_URI = "mongodb://localhost:27017/"
    MONGODB_DB = "demand_calculator"
    MONGODB_COLLECTION = "city_contributions"
    
    # Add any additional MongoDB-specific configs like:
    MONGODB_USERNAME = "your_username"
    MONGODB_PASSWORD = "your_password"
    MONGODB_AUTH_SOURCE = "admin"