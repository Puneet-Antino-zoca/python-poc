import os
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
from app.utils.logger import logger

    
class GeoService:
    def __init__(self):
        # self.cities = gpd.read_file('data/shapefiles/places/tl_2024_13_place.shp')
        # self.blocks = gpd.read_file('data/shapefiles/blocks/tl_2024_13_tabblock20.shp')

 
        self.cities_on_google = pd.read_csv('https://rank-automation-bucket.s3.ap-south-1.amazonaws.com/test-tablock/GeorgiaOnGoogleAds.csv?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEOz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCmFwLXNvdXRoLTEiRzBFAiEA79VAU8DvcTVNcy820%2B29qpcDDCPjcQkaH%2FErYaRoqV8CIHxNHRz5I1Z8b%2F22yng2vgRjiuRSxpItISmMK2EfC7KnKuADCBUQABoMNDE4Mjk1NzAzMjU2IgzV%2FEO8o1nOuQl13f8qvQOjDd%2Fa18TxHFdBEFdEdSRZgaea7yjBUXFGKg0NqM5YHmRkwKfAr9KLQNN2zuUpqn%2BQwyDYSnA0X4SGRFLx3Y%2B9exKeH0ExhiziUrXt7Dmk9LYhyQdwQf9CjJqeHEK%2Br1iEL%2B7ABr9DrwVz4%2FFuvp6y5nUEsoyXq427JII2Yckv0OcSdI4Id%2FCEPY4B6rr2hv%2BJS2KbZWB%2FrUPe5bNtg140SF8QDMWEwq%2FX%2BELJxzyAMWERIvZPb%2Bpj3LHbb7W8B5OToJ8cXZPFixT3hIjdIjfM94qTiXY9ic%2BC6%2FKoRkCrclV%2FhIckDOEgVi%2BiBa2h%2FXH9w7Bsrzq0UNZ6Hzl1Z%2Fgyf22SEMY6jaRFQ5Bq5HkxlC%2Fjl8hxIVwEW%2B%2F%2BuEt7qxyFk3KokyZWpsEg32I8rs93Hw1wEi882Zbw5DvH79dwyw3Cn59RQKjvatMcYKm1edbsQd1leeB3%2Ffbu5dbZmAZLEGSrCsA3Q2w%2BqSFDHrHBRyyvx7hIjgVgKmrwyXauNjxjQr8DjSwv7DslL%2Bk9pcmj8hiwp%2BEHqHdVyLhYpyumkKORvYFMyV7Yhzb4N6HExJCCbhVmNq4v6r8aK8r0MJS2tr0GOuQCy6dXBeT6iDm54ZTLWVo6g3KOl%2FR99cU1KUJRyMMph%2BXIKLhcBShoRTgF7JVHqgiPyHy8NgO1%2FuZP49ImMMoGvkkWCPkL%2FTJQROzChdsM87iVpcnI33tdecwLx1mPPWflEM%2FqmiDgtzEKzrRz%2F3VO3MWK45iBxHkZScoaVhQPQrgSip%2BnScCUcQVQqZE6WfiKVdYM34OLqba0qvthiMhoON6IXU071msYgqgjEvRuMueQaAP9sbaw0xVIEO%2FEi9P3STNyXMwpP3UOWf7EM3ncUyU2dvJe8BxuQv0qe5NgiDwX47Bb2XVN47dTF8F7vnMUH2iifL2pUuWpVHorkhpzAxc05VGcTv0Xq61W2wamU%2BIyXD3lq3scwKj35pkE6l4jv%2FYopBhPNbWPegcVBLvUl2E0WqMpVMwZO9HTzs4Qgx5XPIEi%2FXcuF4AB9DMItDnCBP3iGWitw0No2pYZFrRSfj%2B7W6Q%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAWCZC543MFRZMBBWY%2F20250213%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20250213T120630Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=deb231d1d74c8fc3c0c9d2761a1e673a547d75b09c93a5d0f2587a210d2b5f67')
        self.cities = gpd.read_file('data/shapefiles/places_merged/merged.shp')
        self.blocks = gpd.read_file('data/shapefiles/blocks_merged/merged.shp')

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
        print(f"MAPPED BLOCKS:=========================================>{mapped_blocks}")
        try:
            print(f"cities:=========================================>{self.cities}")
            print(f"blocks:=========================================>{self.blocks}")
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
        
           # Calculate city factors and merge with overall population
            city_factor = pd.merge(
                city_population_within_radius,
                overall_city_population,
                how="left",
                on="NAME"
            )
            city_factor['multiplier'] = city_factor['POPINT'] / city_factor['POP20']
       
            # Filter cities that are available on Google Ads
            cities_in_radius = pd.merge(
                city_factor,
                self.cities_on_google,
                how="inner",
                left_on="NAME",
                right_on="Name"
            )
   
            # Prepare data for MongoDB
            city_data = []
            for _, row in cities_in_radius.iterrows():
                city_info = {
                    'entity_id': entity_id,
                    'intersecting_city': row['NAME'],
                    'contribution_percentage': float(row['multiplier'] * 100),  # Convert to percentage
                    'radius_miles': int(radius_miles),
                    'status': 1,
                    'intersection_population_inside_circle': float(row['POPINT']),
                    'total_population': int(row['POP20']),
                    'multiplier': float(row['multiplier']),
                    'block_data': [
                        {
                            'block_id': block['GEOID20'],
                            'percentage_contribution': float(block['intersection_percentage'])
                        }
                        for _, block in blocks_with_intersections[
                            (blocks_with_intersections['NAME'] == row['NAME']) &
                            (blocks_with_intersections['intersection_percentage'] > 0.01)
                        ].iterrows()
                    ]
                }
                city_data.append(city_info)
            
            return city_data
            
        except Exception as e:
            logger.error(f"Error in process_circle_data: {str(e)}")
            raise
    