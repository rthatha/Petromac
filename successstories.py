from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""

"""


@st.cache
def get_data():
    path = r'cars.csv'
    return pd.read_csv(path)

df = pd.read_csv("./data/Summary.csv")

df

wlco = df['WL Co'].drop_duplicates()
area = df['Area'].drop_duplicates()
country = df['Country'].drop_duplicates()
categories = df['Category 1'].drop_duplicates
wlco_choice = st.sidebar.selectbox('Wl Co:', wlco)
area_choice = st.sidebar.selectbox('Area:', area)
country_choice = st.sidebar.selectbox('Country:', country)
categories_choice = st.sidebar.selectbox('', categories)

