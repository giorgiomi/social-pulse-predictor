# Merge feature databases into a single database
import json
import sys
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Haversine distance (km) between two points specified by latitude and longitude
def haversine_distance_np(lat1, lon1, lat2, lon2):    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula    
    dlat = lat2 - lat1[:, np.newaxis]
    dlon = lon2 - lon1[:, np.newaxis]    
    a = np.sin(dlat / 2)**2 + np.cos(lat1[:, np.newaxis]) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    # Earth's radius in kilometers (6371 km)    
    radius = 6371
    return radius * c

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

# create a dataframe for the stations
df_stations = weather_features[['station', 'geomPoint.geom']]
df_stations['geometry'] = df_stations['geomPoint.geom'].apply(lambda x:Point(x['coordinates'][0], x['coordinates'][1]))
df_stations.drop(columns=['geomPoint.geom'],inplace=True)
df_stations.drop_duplicates(subset='station', keep='first', inplace=True)
df_stations = gpd.GeoDataFrame(df_stations, geometry='geometry')
#print(df_stations)

# remove unnecessary columns
twitter_features = twitter_features.drop('entities', axis=1)
twitter_features = twitter_features.drop('municipality.acheneID', axis=1)
#print(twitter_features.columns)

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

# transform the geometry
twitter_features['geometry'] = twitter_features['geomPoint.geom'].apply(lambda x:Point(x['coordinates'][0], x['coordinates'][1]))
twitter_features.drop(columns=['geomPoint.geom'],inplace=True)
twitter_features = gpd.GeoDataFrame(twitter_features, geometry='geometry')

weather_features['geometry'] = weather_features['geomPoint.geom'].apply(lambda x:Point(x['coordinates'][0], x['coordinates'][1]))
weather_features.drop(columns=['geomPoint.geom'],inplace=True)
weather_features = gpd.GeoDataFrame(weather_features, geometry='geometry')

## calculating the distance between each tweet and each station
#print(twitter_features.get_coordinates())
twitter_lat = np.array(twitter_features.get_coordinates()['y'])
twitter_lon = np.array(twitter_features.get_coordinates()['x'])
station_lat = np.array(df_stations.get_coordinates()['y'])
station_lon = np.array(df_stations.get_coordinates()['x'])

# Compute distances using NumPy (vectorized calculation)
distances = haversine_distance_np(twitter_lat, twitter_lon, station_lat, station_lon)

# Find the index of the nearest station for each Twitter point
nearest_station_index = np.argmin(distances, axis=1).flatten()
#print(type(nearest_station_index))

# Assign the nearest station to twitter_features
twitter_features['station'] = df_stations['station'].iloc[nearest_station_index].values
# print(twitter_features)
# print(weather_features)

# merge the two dataframes
df = pd.merge(twitter_features, weather_features, on=['station', 'date'], how='inner')

# add temperature column
def get_temperature(row):
    str = 'temperatures.' + row['hour_blocks']
    return row[str]
df['temperature'] = df.apply(get_temperature, axis=1)

# add precipitation column
def get_precipitation(row):
    str = 'precipitations.' + row['hour_blocks']
    return row[str]
df['precipitation'] = df.apply(get_precipitation, axis=1)

# add wind column
def get_wind(row):
    str = 'winds.' + row['hour_blocks']
    return row[str]
df['wind'] = df.apply(get_wind, axis=1)

# drop unnecessary columns
df = df.drop([col for col in df.columns if col.startswith('temperatures.')], axis=1)
df = df.drop([col for col in df.columns if col.startswith('precipitations.')], axis=1)
df = df.drop([col for col in df.columns if col.startswith('winds.')], axis=1)

#print(df[['date', 'time', 'hour_blocks', 'station', 'elevation', 'temperature', 'precipitation', 'wind']])
#print(df)

# save the dataframe
df.to_csv('../../data/processed/twitter_weather.csv', index=False)

# Plot temperature with respect to date and time
# plt.figure(figsize=(12, 6))
# df_sorted = df.sort_values('timestamp_x')
# plt.plot(df_sorted['timestamp_x'], df_sorted['temperature'], linewidth=0.5, markersize=1)
# # Plot vertical lines every 86400 time
# for i in range(0, 60):
#     plt.axvline(x=df_sorted['timestamp_x'].iloc[0] + 86400*i, color='r', linestyle='--')

# plt.xlabel('Time')
# plt.ylabel('Temperature (°C)')
# plt.title('Temperature Variation')
# plt.xticks(rotation=45)
# plt.show()

# plot temperature with respect to elevation
# plt.figure(figsize=(12, 6))
# df_sorted = df.sort_values('elevation')
# plt.scatter(df_sorted['elevation'], df_sorted['temperature'])
# plt.xlabel('Elevation (m)')
# plt.ylabel('Temperature (°C)')
# plt.title('Temperature Variation')
# plt.show()
