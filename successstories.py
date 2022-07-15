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

makes = df['make'].drop_duplicates()
years = df['year']
models = df['model']
engines = df['engine']
components = df['components']
make_choice = st.sidebar.selectbox('Select your vehicle:', makes)
year_choice = st.sidebar.selectbox('', years)
model_choice = st.sidebar.selectbox('', models)
engine_choice = st.sidebar.selectbox('', engines)

st.write('Results:', components)