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





data = pd.DataFrame({
    'awesome cities' : ['Chicago', 'Minneapolis', 'Louisville', 'Topeka'],
    'lat' : [41.868171, 44.979840,  38.257972, 39.030575],
    'lon' : [-87.667458, -93.272474, -85.765187,  -95.702548]
})

# Adding code so we can have map default to the center of the data
midpoint = (np.average(data['lat']), np.average(data['lon']))

st.deck_gl_chart(
            viewport={
                'latitude': midpoint[0],
                'longitude':  midpoint[1],
                'zoom': 4
            },
            layers=[{
                'type': 'ScatterplotLayer',
                'data': data,
                'radiusScale': 250,
   'radiusMinPixels': 5,
                'getFillColor': [248, 24, 148],
            }]
        )


map_data = pd.read_csv("./data/countries1.csv")
map_data
st.map(map_data)