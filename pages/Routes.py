import pandas as pd
import numpy as np
import streamlit as st
import folium
import random
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import ast
import datetime

response_route = pd.read_csv('data/response_route.csv')
grouped_df = pd.read_parquet('data/Grouped.parquet') 
grouped_df = grouped_df[['Date', 'Start station', 'Time']]

st.title("Route 2")
grouped_df['Date'] = pd.to_datetime(grouped_df['Date'], format="%Y-%m-%d").dt.date


start_locations = response_route['start_station_name'].unique()
option = st.selectbox(
    'Start Location',
    start_locations)
d = st.date_input(
    "When\'s your birthday",
    datetime.date(2019, 7, 6))

sample = response_route[(response_route['start_station_name']==option)].reset_index(drop = True)


sample = sample[['start_station_name', 'end_station_name', 'response']]
grouped_df_sample = grouped_df[(grouped_df['Date']==d)].reset_index(drop = True)
sample_combined = pd.merge(grouped_df_sample, sample, left_on='Start station', right_on='start_station_name')

size = len(sample_combined)
color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(size)]

# st.dataframe(sample_combined)
def create_map():
   # use the response
    response = ast.literal_eval(sample_combined['response'][0])
    mls = response['features'][0]['geometry']['coordinates']
    points = [(i[1], i[0]) for i in mls[0]]
    m = folium.Map(location=points[0])
    folium.Marker(points[0], popup='''<h4>'''+sample_combined['start_station_name'][0]+'''</h4>''', icon=folium.Icon(color="red")).add_to(m)
    for i, response in enumerate(sample_combined['response']):
        
        response = ast.literal_eval(response)
        # st.write(i)
        mls = response['features'][0]['geometry']['coordinates']
        points = [(i[1], i[0]) for i in mls[0]]
        # add marker for the start and ending points
        # for point in [points[0], points[-1]]:
        if points[-1] == points[0]:
            continue
        folium.Marker(points[-1], popup='''<h4>'''+sample_combined['end_station_name'][i]+'''</h4>''').add_to(m)
        # add the lines
        folium.PolyLine(points, weight=5,opacity=1).add_to(m)
        # folium.PolyLine(points, weight=5,color='red', opacity=1).add_to(m)
        # create optimal zoom
        df = pd.DataFrame(mls[0]).rename(columns={0:'Lon', 1:'Lat'})[['Lat', 'Lon']]
        sw = df[['Lat', 'Lon']].min().values.tolist()
        ne = df[['Lat', 'Lon']].max().values.tolist()
        m.fit_bounds([sw, ne])
    return m
m = create_map()
# st_folium(m)
# st_folium(folium_static(m, width=1500, height=800))
folium_static(m, height=600)



