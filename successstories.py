
import streamlit as st
import pandas as pd
import altair as alt

from pypdf import PdfReader,PdfWriter
from pathlib import Path

#from collections import namedtuple
#import math
#import numpy as np


@st.cache_data
def get_data():

    success_storiespdf = PdfReader("./data/Success_Stories.pdf")
    success_stories = pd.read_csv("./data/Succeses_Summary.csv")
    jobhistory = pd.read_csv("./data/jobhistory.csv")
    
    return success_stories, success_storiespdf,jobhistory.set_index("Country")


def export_report(success_storiespdf,pages=[]):
    
    pdf_writer = PdfWriter()
    if pages == []:

        output = open("success_storiespdf", "wb")
        pdf_writer.write(output)
        st.download_button('Export Report', output.read_bytes(), f"Petromac_SuccessStories.pdf", mime='application/pdf')

        return
    
    else:
        
        for page in range(3):
            pdf_writer.add_page(success_storiespdf.pages[page])
        
        for page in pages:       
            pdf_writer.add_page(success_storiespdf.pages[page-1])
            
        pdf_writer.add_page(success_storiespdf.pages[-1])   
        
        output = open("Petromac_SuccessStories.pdf", "wb")
        pdf_writer.write(output)
        st.download_button('Export Report', output.read_bytes(), f"Petromac_SuccessStories.pdf", mime='application/pdf')
        
        return


success_stories, success_storiespdf,jobhistory = get_data()

success_stories #displays summary of success stories

export_report(success_storiespdf)

# nofilter / category / area / wlco / nocountry

# stop filtering at every level


categories = success_stories['Category 1'].unique()

areas = success_stories["Area"].unique()
countries = success_stories['Country'].unique()

wlcos = success_stories['WL Co'].unique()

categories_choices = st.sidebar.multiselect('Categories:', categories)
area_choices = st.sidebar.multiselect('Area:', areas)
country_choices = st.sidebar.multiselect('Country:', countries)

wlco_choices = st.sidebar.multiselect('Wl Co:', wlcos)


#categories = success_stories['Category 1'].loc[success_stories['WL Co'].isin(wlco_choices)].loc[success_stories['Area'].isin(area_choices)].loc[success_stories['Country'].isin(country_choices)].unique()
#areas = success_stories["Area"].loc[success_stories['WL Co'].isin(wlco_choices)].unique()
#countries = success_stories['Country'].loc[success_stories['WL Co'].isin(wlco_choices)].loc[success_stories['Area'].isin(area_choices)].unique()



if st.sidebar.button('Filter'):
    filtered_df = success_stories.loc[success_stories['WL Co'].isin(wlco_choices)].loc[success_stories['Area'].isin(area_choices)].loc[success_stories['Country'].isin(country_choices)]
    filtered_df
    pagenumbers = filtered_df['Page']
    
    export_report(success_storiespdf,pagenumbers)
    
    #filter for wlco / client / area / country / category

    data = jobhistory.loc[country_choices]
        #data /= 1000000.0
    st.write("Number of Descents", data.sort_index())

    data = data.T.reset_index()
    data = pd.melt(data, id_vars=["index"]).rename(
        columns={"index": "Date", "value": "Successful"}
        )
    
    chart = (
        alt.Chart(data)
        .mark_area(opacity=0.3)
        .encode(
            x="Date:T",
            y=alt.Y("Successful:Q", stack=None),
            color="Country:N",
            )
            )
    st.altair_chart(chart, use_container_width=True)