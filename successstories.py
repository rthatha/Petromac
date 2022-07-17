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

st.write(df)

wlco = df['WL Co'].drop_duplicates()
wlco_choice = st.sidebar.selectbox('Wl Co:', wlco)

df[df['WL Co'] == wlco_choice]

area = df["Area"].loc[df['WL Co'] == wlco_choice].drop_duplicates()
area_choice = st.sidebar.selectbox('Area:', area)
df[df['Area'] == area_choice]

country = df['Country'].loc[df['WL Co'] == wlco_choice].loc[df['Area'] == area_choice].drop_duplicates()
country_choice = st.sidebar.selectbox('Country:', country)
df[df['Country'] == country_choice]

categories = df['Category 1'].drop_duplicates()



categories_choice = st.sidebar.selectbox('Categories:', categories)


