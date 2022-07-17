from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np


@st.cache
def get_data():
    df_casestudies = pd.read_csv("./data/Summary.csv")
    df_jobhistory = pd.read_csv("./data/jobhistory.csv")
    return df_casestudies,df_jobhistory


df_casestudies,df_jobhistory = get_data()

df_casestudies


wlcos = df_casestudies['WL Co'].unique()
st.write(type(wlcos))
wlcos
areas = df_casestudies["Area"].drop_duplicates()
countries = df_casestudies['Country'].drop_duplicates()
categories = df_casestudies['Category 1'].drop_duplicates()


wlco_choices = st.sidebar.multiselect('Wl Co:', wlcos)
area_choices = st.sidebar.multiselect('Area:', areas)
country_choices = st.sidebar.multiselect('Country:', countries)
categories_choices = st.sidebar.multiselect('Categories:', categories)

wlco_choices
area_choices
country_choices
categories_choices


if st.sidebar.button('Filter'):
     df = df_casestudies
     
     df[(df['WL Co'] == wlco_choices) & (df['Area'] == area_choices) & (df['Country'] == country_choices) & (df['Category 1'] == categories_choices)]


"""

areas = df["Area"].loc[df['WL Co'] == wlco_choices].drop_duplicates()

country = df['Country'].loc[df['WL Co'] == wlco_choice].loc[df['Area'] == area_choice].drop_duplicates()



categories = df['Category 1'].drop_duplicates()





"""
df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=37.76,
         longitude=-122.4,
         zoom=11,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=df,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
     ],
 ))

map_data = pd.read_csv("./data/countries1.csv")
map_data
st.map(map_data)