#Pyhton script to build feature csv file from the json file
import json
import sys
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# file path
data_path = '../../data/raw/meteotrentino-weather-station-data.json'

# load the data
with open(data_path) as json_file:
    data = json.load(json_file)
print(data.keys()) #print keys

# load the grid
grid_path = '../../data/raw/trentino-grid.geojson'
df_grid = gpd.read_file(grid_path)

# extract features
data_features = gpd.GeoDataFrame(data['features'])
print(data_features.columns)

# geometry column
# data_features['geometry'] = data_features['geomPoint.geom'].apply(lambda x:Point(x['coordinates'][0], x['coordinates'][1]))
# data_features.drop(columns=['geomPoint.geom'],inplace=True)

# plot the data
# plot temperature
# plt.scatter(data_features['timestamp'], data_features['minTemperature'])
# plt.xlabel('Timestamp')
# plt.ylabel('Minimum Temperature')
# plt.title('Minimum Temperature Variation')
# plt.show()
