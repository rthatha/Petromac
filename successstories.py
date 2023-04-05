from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np

from pathlib import Path
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

import pypdf
from pypdf import PdfReader


@st.cache_data
def get_data():
    df_casestudies = pd.read_csv("./data/Summary.csv")
    df_jobhistory = pd.read_csv("./data/jobhistory.csv")
    return df_casestudies,df_jobhistory.set_index("Country")


def mergepdf(pagenumbers):

    cover_page = PdfFileReader("./data/PDFTemplates/coverpage.pdf")
    #jobhistory_page = PdfFileReader("./data/PDFTemplates/Jobhistory_byfilter.pdf")
    end_page = PdfFileReader("./data/PDFTemplates/endpage.pdf")
    successstories = PdfFileReader("./data/PDFTemplates/SuccessStories.pdf")
        
    pdf_writer = PdfFileWriter()

    for page in range(cover_page.getNumPages()):
            pdf_writer.addPage(cover_page.getPage(page))

    for page in pagenumbers:
        pdf_writer.addPage(successstories.getPage(page-1))

    for page in range(end_page.getNumPages()):
            pdf_writer.addPage(end_page.getPage(page))


    # Make folder for storing user uploads
    destination_folder = Path('downloads')
    destination_folder.mkdir(exist_ok=True, parents=True)
    output_path = destination_folder / f"output_filtered_successstories.pdf"

    with open(str(output_path), 'wb') as out:
        pdf_writer.write(out)

    st.download_button('Download Merged Document', output_path.read_bytes(), f"output_filtered_successstories.pdf", mime='application/pdf')

    return


df_casestudies,df_jobhistory = get_data()

df_casestudies

wlcos = df_casestudies['WL Co'].unique()
wlco_choices = st.sidebar.multiselect('Wl Co:', wlcos)

areas = df_casestudies["Area"].loc[df_casestudies['WL Co'].isin(wlco_choices)].unique()
area_choices = st.sidebar.multiselect('Area:', areas)

countries = df_casestudies['Country'].loc[df_casestudies['WL Co'].isin(wlco_choices)].loc[df_casestudies['Area'].isin(area_choices)].unique()
country_choices = st.sidebar.multiselect('Country:', countries)

categories = df_casestudies['Category 1'].loc[df_casestudies['WL Co'].isin(wlco_choices)].loc[df_casestudies['Area'].isin(area_choices)].loc[df_casestudies['Country'].isin(country_choices)].unique()
categories_choices = st.sidebar.multiselect('Categories:', categories)



if st.sidebar.button('Filter'):
    filtered_df = df_casestudies.loc[df_casestudies['WL Co'].isin(wlco_choices)].loc[df_casestudies['Area'].isin(area_choices)].loc[df_casestudies['Country'].isin(country_choices)]
    filtered_df
    pagenumbers = filtered_df['Page']
    
    mergepdf(pagenumbers)
    
    
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