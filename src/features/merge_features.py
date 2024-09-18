# Merge feature databases into a single database
import json
import sys
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import pandas as pd

# file path
weather_path = '../../data/raw/meteotrentino-weather-station-data.json'
twitter_path = '../../data/raw/social-pulse-trentino.geojson'

# load the data
with open(weather_path) as json_file:
    data_weather = json.load(json_file)
with open(twitter_path) as json_file:
    data_twitter = json.load(json_file)

# load the grid
grid_path = '../../data/raw/trentino-grid.geojson'
df_grid = gpd.read_file(grid_path)

# extract features
twitter_features = gpd.GeoDataFrame(data_twitter['features'])
weather_features = gpd.GeoDataFrame(data_weather['features'])

# remove unnecessary columns
twitter_features = twitter_features.drop('entities', axis=1)
twitter_features = twitter_features.drop('municipality.acheneID', axis=1)
print(twitter_features.columns)

# split date and time 
twitter_features['date'] = twitter_features['created'].str.split('T').str[0]
twitter_features['time'] = twitter_features['created'].str.split('T').str[1]
twitter_features = twitter_features.drop('created', axis=1)
twitter_features = twitter_features[['date', 'time', 'timestamp', 'user', 'geomPoint.geom', 'municipality.name', 'language']]

# keep only minutes
twitter_features['time'] = twitter_features['time'].str.rsplit(':', n=1).str[0]
#print(twitter_features)

# make blocks of 15 minutes (column: hour_blocks)
minutes = twitter_features['time'].str.rsplit(':', n=1).str[1].astype(int)
minutes = (minutes // 15)*15
minutes = minutes.astype(str)
minutes = minutes.str.zfill(2)
#print(minutes)

hours = twitter_features['time'].str.rsplit(':', n=1).str[0]

twitter_features['hour_blocks'] = hours + minutes
print(twitter_features)