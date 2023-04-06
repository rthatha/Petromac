
import streamlit as st
import pandas as pd
import altair as alt

from pypdf import PdfReader,PdfWriter
from pathlib import Path


@st.cache_data
def get_data():

    success_storiespdf = PdfReader("./data/Success_Stories.pdf")
    success_stories = pd.read_csv("./data/Succeses_Summary.csv")
    jobhistory = pd.read_csv("./data/jobhistory.csv")
    
    return success_stories, success_storiespdf,jobhistory.set_index("Country")


def export_report(success_storiespdf,pages=[]):    
    
    writer = PdfWriter()
    if pages == []:
        for page in range(len(success_storiespdf.pages)):
            writer.add_page(success_storiespdf.pages[page])
            
    else:
        for page in range(3):
            writer.add_page(success_storiespdf.pages[page])     
    
        for page in pages:
            writer.add_page(success_storiespdf.pages[page])
        
        writer.add_page(success_storiespdf.pages[-1])   
        
    output = open("Petromac_SuccessStories.pdf", "wb")
    writer.write(output)
    writer.close()
    output.close()

    with open("Petromac_SuccessStories.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(label="Export Report", 
                       data=PDFbyte,
                       file_name="Petromac_SuccessStories.pdf",
                       mime='application/octet-stream')

    #st.download_button('Export Report', output.read_bytes(), f"Petromac_SuccessStories.pdf", mime='application/pdf')
    #writer.close()
    #output.close()

    return


success_stories, success_storiespdf,jobhistory = get_data()

success_stories #displays summary of success stories

export_report(success_storiespdf)




categories = success_stories['Category 1'].unique()
areas = success_stories["Area"].unique()
countries = success_stories['Country'].unique()
wlcos = success_stories['WL Co'].unique()

st.session_state['categories'] = success_stories['Category 1'].unique()
st.session_state['areas'] = success_stories["Area"].unique()
st.session_state['countries'] = success_stories['Country'].unique()
st.session_state['wlcos'] = success_stories['WL Co'].unique()

st.session_state

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
    
    export_report(success_storiespdf,pages=pagenumbers)
    
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