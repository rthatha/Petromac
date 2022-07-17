from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np






@st.cache
def get_data():
    df_casestudies = pd.read_csv("./data/Summary.csv")
    return df_casestudies


df_casestudies = get_data()
df_casestudies

wlcos = df_casestudies['WL Co'].drop_duplicates()
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
     df[(df['WL Co'] == wlco_choice) & (df['Area'] == area_choice) & (df['Country'] == country_choice) & (df['Category 1'] == categories_choice)]


"""
area = df["Area"].loc[df['WL Co'] == wlco_choice].drop_duplicates()


country = df['Country'].loc[df['WL Co'] == wlco_choice].loc[df['Area'] == area_choice].drop_duplicates()



categories = df['Category 1'].drop_duplicates()





"""

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data