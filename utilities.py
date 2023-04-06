import streamlit as st
import pandas as pd
from pypdf import PdfReader,PdfWriter

#from pathlib import Path

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

    return