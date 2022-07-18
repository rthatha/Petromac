from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np

import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger


@st.cache
def get_data():
    df_casestudies = pd.read_csv("./data/Summary.csv")
    df_jobhistory = pd.read_csv("./data/jobhistory.csv")
    return df_casestudies,df_jobhistory


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

wlco_choices
area_choices
country_choices
categories_choices



if st.sidebar.button('Filter'):
          
     filtered_df = df_casestudies.loc[df_casestudies['WL Co'].isin(wlco_choices)].loc[df_casestudies['Area'].isin(area_choices)].loc[df_casestudies['Country'].isin(country_choices)]
     filtered_df
     pagenumbers = filtered_df['Page']
     pagenumbers


cover_page = PdfFileReader("./data/PDFTemplates/Coverpage.pdf")
#jobhistory_page = PdfFileReader("./data/PDFTemplates/Jobhistory_byfilter.pdf")
end_page = PdfFileReader("./data/PDFTemplates/Endpage.pdf")
successstories = PdfFileReader("./data/PDFTemplates/Successstories.pdf")

pdf_writer = PdfFileWriter()
for page in pagenumbers:
    pdf_writer.addPage(successstories.getPage(page))


pdf_writer.write("./data/PDFTemplates/Filtered_Successstories.pdf")

