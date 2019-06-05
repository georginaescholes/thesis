import pandas as pd
import geopandas as gpd #import Geopandas to create geodataframs
from shapely.geometry import Point #import Shapely to convert coordinates to point geometries
import os

weights = pd.read_csv('mean_months.csv')

#convert dataframe into geodataframe
geometry = [Point(xy) for xy in zip(weights.lng, weights.lat)]
crs = {'init':'epsg:4326'}
weights_geo = gpd.GeoDataFrame(weights, crs=crs, geometry=geometry)

mf_routes = weights_geo.groupby('RuteLabel')

#create destination folder for routes
result_folder = os.path.join('Results')
if not os.path.exists(result_folder):
    os.makedirs(result_folder)

#save individual routes as shape files
for key, values in mf_routes:
    out_name = "%s" % key.replace(" ", "_")
    out_path = os.path.join(result_folder, out_name)
    values.to_file(out_path)


