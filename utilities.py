import streamlit as st
import pandas as pd
from pypdf import PdfReader,PdfWriter
import base64

#from pathlib import Path

def show_pdf():
    with open("Petromac_SuccessStories.pdf", "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def export_report(pages=[]):    
    
    success_storiespdf = PdfReader("./data/Success_Stories.pdf")
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
    output.close()
    writer.close()
   
    

    with open("Petromac_SuccessStories.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    base64_pdf = base64.b64encode(PDFbyte).decode('utf-8')
    
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
        
    
    #show_pdf()
    st.download_button(label="Download PDF", 
                       data=PDFbyte,
                       file_name="Petromac_SuccessStories.pdf",
                       mime='application/octet-stream')

    return