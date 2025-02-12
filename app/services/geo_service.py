import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
from app.utils.logger import logger

class GeoService:
    def __init__(self):
        self.cities = gpd.read_file('data/shapefiles/places/tl_2024_13_place.shp')
        self.blocks = gpd.read_file('data/shapefiles/blocks/tl_2024_13_tabblock20.shp')

    def city_population(self, blocks, pop_type):
        """
        Calculate city population based on blocks data.
        
        Parameters:
        blocks (GeoDataFrame): GeoDataFrame containing block data
        pop_type (str): Population column name to aggregate ('POP20' or 'POPINT')
        
        Returns:
        DataFrame: Aggregated population data by city
        """
        try:
            logger.debug(f"Calculating city population using {pop_type}")
            cities_population = blocks.groupby('NAME')[pop_type].sum().reset_index()
            return cities_population
        except Exception as e:
            logger.error(f"Error calculating city population: {str(e)}")
            raise

    def map_cities_to_blocks(self, blocks, cities):
        """Maps cities to blocks using spatial join"""
        try:
            logger.debug("Starting spatial join of cities and blocks")
            result = gpd.sjoin(cities, blocks, how="right", predicate="contains")
            logger.debug(f"Spatial join completed with {len(result)} results")
            return result
        except Exception as e:
            logger.error(f"Error in map_cities_to_blocks: {str(e)}")
            raise Exception(f"Failed to map cities to blocks: {str(e)}")

    def create_circle(self, lat, lon, radius_miles=5):
        """Creates a circle geometry around a point"""
        try:
            logger.debug(f"Creating circle at lat={lat}, lon={lon}, radius={radius_miles}")
            center = Point(lon, lat)
            radius_deg = radius_miles / 69.0
            circle = center.buffer(radius_deg)
            gdf = gpd.GeoDataFrame({'geometry': [circle]})
            gdf.set_crs('EPSG:4326', allow_override=True, inplace=True)
            logger.debug("Circle created successfully")
            return gdf
        except Exception as e:
            logger.error(f"Error in create_circle: {str(e)}")
            raise Exception(f"Failed to create circle: {str(e)}")

    def map_blocks_to_circle_intersections(self, blocks_with_cities, circle_gdf):
        """Calculate intersection of blocks with circle"""
        try:
            logger.debug("Starting block-circle intersection calculation")
            intersection_percentages = []
            
            for idx, block in blocks_with_cities.iterrows():
                try:
                    block_geom = block.geometry
                    intersection = block_geom.intersection(circle_gdf.geometry.iloc[0])
                    intersection_area = intersection.area if not intersection.is_empty else 0
                    block_area = block_geom.area
                    intersection_percentage = (intersection_area / block_area) * 100 if block_area > 0 else 0
                    intersection_percentages.append(intersection_percentage)
                except Exception as e:
                    logger.warning(f"Error processing block {idx}: {str(e)}")
                    intersection_percentages.append(0)
            
            # Create a copy to avoid SettingWithCopyWarning
            blocks_with_intersections = blocks_with_cities.copy()
            
            blocks_with_intersections['intersection_percentage'] = intersection_percentages
            blocks_with_intersections = blocks_with_intersections[
                blocks_with_intersections['intersection_percentage'] > 0
            ]
            
            blocks_with_intersections['POP20'] = pd.to_numeric(
                blocks_with_intersections['POP20'], 
                errors='coerce'
            )
            blocks_with_intersections['intersection_percentage'] = pd.to_numeric(
                blocks_with_intersections['intersection_percentage'], 
                errors='coerce'
            )
            
            blocks_with_intersections['POPINT'] = (
                blocks_with_intersections['POP20'] * 
                blocks_with_intersections['intersection_percentage'] / 100
            )
            
            logger.debug(f"Intersection calculation completed for {len(blocks_with_intersections)} blocks")
            return blocks_with_intersections
            
        except Exception as e:
            logger.error(f"Error in map_blocks_to_circle_intersections: {str(e)}")
            raise Exception(f"Failed to map blocks to circle intersections: {str(e)}")

    def process_circle_data(self, lat, lng, mapped_blocks, entity_id):
        """Process circle data for the given coordinates"""
        try:
            logger.debug(f"Creating circle for entity_id={entity_id}, lat={lat}, lng={lng}")
            radius_miles = 5  # Set constant radius
            circle = self.create_circle(lat, lng, radius_miles)
        
            blocks_with_intersections = self.map_blocks_to_circle_intersections(
                mapped_blocks, 
                circle
            )
        
            # Calculate city populations
            city_population_within_radius = self.city_population(blocks_with_intersections, 'POPINT')
            overall_city_population = self.city_population(mapped_blocks, 'POP20')
        
            # Prepare data for MongoDB
            city_data = []
            for _, row in city_population_within_radius.iterrows():
                city_info = {
                    'entity_id': entity_id,
                    'intersecting_city': row['NAME'],
                    'contribution_percentage': float(row['POPINT'] / overall_city_population[overall_city_population['NAME'] == row['NAME']]['POP20'].iloc[0] * 100),
                    'radius_miles': int(radius_miles),
                    'status': 1,
                    'intersection_population_inside_circle': float(row['POPINT']),
                    'total_population': int(overall_city_population[overall_city_population['NAME'] == row['NAME']]['POP20'].iloc[0])
                }
                city_data.append(city_info)
            
            return city_data
            
        except Exception as e:
            logger.error(f"Error in process_circle_data: {str(e)}")
            raise
    