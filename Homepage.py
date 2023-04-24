
import streamlit as st
import pandas as pd
import glob
import os

import plotly.express as px
from datetime import datetime, timedelta
from plotly.subplots import make_subplots

import plotly.graph_objects as go
from scipy import signal


st.set_page_config(layout="wide", page_title = "BikeShare")
st.title("Home Page")

climate = pd.read_csv('data/climate.csv')
seasons = pd.read_csv('data/EDA/seasons.csv') #Done
grouped_by_month = pd.read_csv('data/EDA/grouped_by_month.csv') #Done
grouped_time = pd.read_csv('data/EDA/grouped_time.csv') #Done
memberGrowth = pd.read_csv('data/EDA/memberGrowth.csv') #Done
memberTypeAll = pd.read_csv('data/EDA/memberTypeAll.csv') #Done
merged_climate = pd.read_csv('data/EDA/merged_climate.csv') #Done
montly_variation = pd.read_csv('data/EDA/montly_variation.csv') #Done


seasons_fig = px.bar(x=seasons['index'], y=seasons['SEASON'])
st.plotly_chart(seasons_fig)

grouped_by_month_fig = px.bar(x=grouped_by_month['Start date'], y=grouped_by_month['Start date.1'])
st.plotly_chart(grouped_by_month_fig)

grouped_time_fig = px.bar(x=grouped_time['date'], y=grouped_time['time']/(60*60))
st.plotly_chart(grouped_time_fig)

memberGrowth_fig = px.line(x=memberGrowth['date'], y=memberGrowth['Count'], color=memberGrowth['Member type'])
st.plotly_chart(memberGrowth_fig)

memberTypeAll_fig = px.pie(values=memberTypeAll['Member type'], names=memberTypeAll['index'], title='Member Type',
             color_discrete_map={'casual':'blue',
                                 'member':'red'})
st.plotly_chart(memberTypeAll_fig)

montly_variation_fig = px.histogram(x=montly_variation['month'], y=montly_variation['Start date'], color=montly_variation['year'], barmode='group', title="Covid Impact")
st.plotly_chart(montly_variation_fig)

# st.dataframe(climate.head())

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=merged_climate['DATE'],
    y=signal.savgol_filter(merged_climate['TAVG'],
                           7, # window size used for filtering
                           1), # order of fitted polynomial
    mode='lines',
    marker=dict(
        size=6,
        color='black',
        # symbol='triangle-up'
    ),
    name='TAVG'
))

fig.add_trace(go.Scatter(
    x=merged_climate['DATE'],
    y=signal.savgol_filter(merged_climate['TMAX'],
                           7, # window size used for filtering
                           1), # order of fitted polynomial
    mode='lines',
    marker=dict(
        size=6,
        color='red',
        # symbol='triangle-up'
    ),
    name='TMAX'
))

fig.add_trace(go.Scatter(
    x=merged_climate['DATE'],
    y=signal.savgol_filter(merged_climate['TMIN'],
                           7, # window size used for filtering
                           1), # order of fitted polynomial
    mode='lines',
    marker=dict(
        size=6,
        color='blue',
        # symbol='triangle-up'
    ),
    name='TMIN'
))

st.plotly_chart(fig)