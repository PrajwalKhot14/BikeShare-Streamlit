import streamlit as st

import pandas as pd
import glob
import os

import plotly.express as px
from datetime import datetime, timedelta
from plotly.subplots import make_subplots


st.title("Map")

latlong = pd.read_csv('data/distinct_LatLong.csv')

px.set_mapbox_access_token('pk.eyJ1IjoicHJhandhbHBraG90IiwiYSI6ImNsOGxyOWZwMDA3YjgzdnVsaHhyZmpycjYifQ.SwPz8CjjBoakK3UAPKTRIA')
latlong = latlong[['Latitude_x', 'Longitude_x']]

fig = px.scatter_mapbox(latlong, lat="Latitude_x", lon="Longitude_x", color_continuous_scale=px.colors.cyclical.IceFire,zoom=12, width=800, height=800)
fig.update_layout(mapbox_style="mapbox://styles/prajwalpkhot/clgpfs21100co01nu61fwfpbp")
st.plotly_chart(fig, theme="streamlit", use_container_width=True)