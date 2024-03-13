import pandas as pd
import geopandas as gpd

df = pd.read_csv("supermarket_sales.csv")

# Assuming you have a DataFrame 'df' with columns: 'City', 'latitude', 'longitude'
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))

gdf.to_file("myanmar_cities.geojson", driver="GeoJSON")