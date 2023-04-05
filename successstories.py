
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


def mergepdf(success_storiespdf,jobhistory_page,pagenumbers):

    
    #jobhistory_page = PdfFileReader("./data/PDFTemplates/Jobhistory_byfilter.pdf")
     
        
    pdf_writer = PdfWriter()
    
    for page in range(3):
        pdf_writer.add_page(success_storiespdf.pages[page])

    #pdf_writer.add_page(jobhistory_page)

    for page in pagenumbers:       
        pdf_writer.add_page(success_storiespdf.pages[page-1])
    
    pdf_writer.add_page(success_storiespdf.pages[-1])   


    # Make folder for storing user uploads
    destination_folder = Path('downloads')
    destination_folder.mkdir(exist_ok=True, parents=True)
    output_path = destination_folder / f"output_filtered_successstories.pdf"

    with open(str(output_path), 'wb') as out:
        pdf_writer.write(out)

    st.download_button('Download Merged Document', output_path.read_bytes(), f"output_filtered_successstories.pdf", mime='application/pdf')

    return


success_stories, success_storiespdf,jobhistory = get_data()

success_stories #displays summary of success stories
with open(success_storiespdf, "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(label="Export_Report",
                    data=PDFbyte,
                    file_name="test.pdf",
                    mime='application/octet-stream')

# nofilter / category / area / wlco / nocountry

# stop filtering at every level



wlcos = df_successstories['WL Co'].unique()
wlco_choices = st.sidebar.multiselect('Wl Co:', wlcos)

areas = df_successstories["Area"].loc[df_successstories['WL Co'].isin(wlco_choices)].unique()
area_choices = st.sidebar.multiselect('Area:', areas)

countries = df_successstories['Country'].loc[df_successstories['WL Co'].isin(wlco_choices)].loc[df_successstories['Area'].isin(area_choices)].unique()
country_choices = st.sidebar.multiselect('Country:', countries)

categories = df_successstories['Category 1'].loc[df_successstories['WL Co'].isin(wlco_choices)].loc[df_successstories['Area'].isin(area_choices)].loc[df_successstories['Country'].isin(country_choices)].unique()
categories_choices = st.sidebar.multiselect('Categories:', categories)



if st.sidebar.button('Filter'):
    filtered_df = df_successstories.loc[df_successstories['WL Co'].isin(wlco_choices)].loc[df_successstories['Area'].isin(area_choices)].loc[df_successstories['Country'].isin(country_choices)]
    filtered_df
    pagenumbers = filtered_df['Page']
    
    mergepdf(success_storiespdf,pagenumbers)
    
    #filter for wlco / client / area / country / category

    data = df_jobhistory.loc[country_choices]
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