import pandas as pd

import osmnx as ox
import networkx as nx
ox.settings.log_console=True
ox.settings.use_cache=True
import streamlit as st

import numpy as np
import requests
from geopy.geocoders import Nominatim   # get lat / long of an address
import folium                           # Mapping application
from folium import plugins              # Used to plot routes on a map
import openrouteservice                 # Used to get lat / longs in between starting and ending lat / long
from openrouteservice import convert
import geopy.distance  

from pyarrow.parquet import ParquetFile
import pyarrow as pa 
from streamlit_folium import st_folium



route = pd.read_csv('data/routes_0_1950.csv')
pf = ParquetFile('data/final_data.parquet') 
first_ten_rows = next(pf.iter_batches(batch_size = 500)) 
final_df = pa.Table.from_batches([first_ten_rows]).to_pandas() 
distinct_latlong = pd.read_csv('data/distinct_LatLong.csv')
distinct_latlong.rename(columns={"start_station_name": "Start station","end_station_name": "End station", "Latitude_x":"st_Latitude", "Longitude_x":"st_Longitude", "Latitude_y":"end_Latitude", "Longitude_y":"end_Longitude"}, inplace = True)
combined = pd.merge(final_df, distinct_latlong, on=['Start station', 'End station'])
# combined = pd.merge(combined, distinct_latlong, on='End station')
combined = combined[combined['Start station'] != combined['End station']]
sample = combined
# st.write(sample)

def generate_map(map_location, map_style, start_lat_col, start_long_col, start_color, end_lat_col, end_long_col, end_color):
    folium_map = folium.Map(location=map_location,
                            zoom_start=11,
                            tiles=map_style)
    for index, row in sample.iterrows():
        folium.CircleMarker(location=(row[start_lat_col],
                                      row[start_long_col]),
                            color=start_color,
                            radius=5,
                            weight=1,
                            fill=True).add_to(folium_map)
        folium.CircleMarker(location=(row[end_lat_col],
                                      row[end_long_col]),
                            color=end_color,
                            radius=5,
                            weight=1,
                            fill=True).add_to(folium_map)
    return folium_map


def plot_paths(paths,map_data):
    for path in paths:
        line = folium.PolyLine(
            path,
            weight=1,
            color='#0A8A9F'
        ).add_to(map_data)
    return map_data


map_data = generate_map([38.896138,-77.026000],"cartodbpositron","st_Latitude","st_Longitude",'#0A8A9F',"end_Latitude","end_Longitude",'#f68e56')
# st.write(route['route'].values.tolist())
import ast
routes = []

start_locations = distinct_latlong['Start station'].unique()
option = st.selectbox(
    'Start Location',
    start_locations)

sample = distinct_latlong[distinct_latlong['Start station']==option]
st.write(sample)
start_lat, start_long = distinct_latlong[distinct_latlong['Start station']==option]['st_Latitude'].iloc[0], distinct_latlong[distinct_latlong['Start station']==option]['st_Longitude'].iloc[0]
# st.write(start_lat)
# st.write(start_long)



for i in route[(route['st_Latitude']==start_lat) & (route['st_Longitude']==start_long)]['routes']:
    routes.append(ast.literal_eval(i))

st.write(len(routes))

# start_df = distinct_latlong[['Start station']]
# start_locations = distinct_latlong['Start station'].unique()

# st.write('You selected:', option)
# path = pd.merge(route, distinct_latlong[distinct_latlong['Start station'] == option], on=["st_Latitude", "st_Longitude"])
# path.rename(columns={"end_Latitude_x":"end_Latitude", "end_Longitude_x":"end_Longitude"}, inplace = True)
# path = path[["routes", "st_Latitude", "st_Longitude", "end_Latitude","end_Longitude"]]
# st.write(route)

# st.write(out)
st_folium(plot_paths(routes, map_data))

