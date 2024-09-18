#Pyhton script to build feature csv file from the json file
import json
import sys
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# file path
data_path = '../../data/raw/social-pulse-trentino.geojson'

# load the data
with open(data_path) as json_file:
    data = json.load(json_file)
#print(data.keys()) #print keys

# load the grid
grid_path = '../../data/raw/trentino-grid.geojson'
df_grid = gpd.read_file(grid_path)

# extract features
data_features = gpd.GeoDataFrame(data['features'])

# geometry column
data_features['geometry'] = data_features['geomPoint.geom'].apply(lambda x:Point(x['coordinates'][0], x['coordinates'][1]))
data_features.drop(columns=['geomPoint.geom'],inplace=True)

# plot the data
date_mask = (data_features['created'] > '2013-11-01') & (data_features['created'] < '2013-11-02')
ax = df_grid.plot()
data_features[date_mask].plot(column='timestamp', legend=True, ax = ax)
plt.show()
