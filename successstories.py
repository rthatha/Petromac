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

def filters():
    if wlco_choices==[]:
        areas = [Middle East, North America, Latin America, Asia, Europe, Africa]
    else:
        areas = df_casestudies["Area"].loc[df_casestudies['WL Co'].isin(wlco_choices)].unique()
    return areas






def wlco_choices_filter():
    areas = df_casestudies["Area"].loc[df_casestudies['WL Co'].isin(wlco_choices)].unique()
    return areas




wlcos = df_casestudies['WL Co'].unique()
wlco_choices = st.sidebar.multiselect('Wl Co:', wlcos, on_change = filters())

'areas = df_casestudies["Area"].loc[df_casestudies['WL Co'].isin(wlco_choices)].unique()
area_choices = st.sidebar.multiselect('Area:', filters())

countries = df_casestudies['Country'].loc[df_casestudies['WL Co'].isin(wlco_choices)].loc[df_casestudies['Area'].isin(area_choices)].unique()
country_choices = st.sidebar.multiselect('Country:', countries)

categories = df_casestudies['Category 1'].loc[df_casestudies['WL Co'].isin(wlco_choices)].loc[df_casestudies['Area'].isin(area_choices)].loc[df_casestudies['Country'].isin(country_choices)].unique()
categories_choices = st.sidebar.multiselect('Categories:', categories)

wlco_choices
area_choices
country_choices
categories_choices



if st.sidebar.button('Filter'):
          
     df_casestudies.loc[df_casestudies['WL Co'].isin(wlco_choices)].loc[df_casestudies['Area'].isin(area_choices)].loc[df_casestudies['Country'].isin(country_choices)]


"""

Filter works only downwards


"""


from rendermap import rendermap
rendermap()

map_data = pd.read_csv("./data/countries1.csv")
map_data
st.map(map_data)