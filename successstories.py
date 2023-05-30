
import streamlit as st
import pandas as pd
import altair as alt

from utilities import export_report


success_stories = pd.read_csv("./data/Succeses_Summary.csv")
jobhistory = pd.read_csv("./data/jobhistory.csv")
jobhistory.set_index("Country")

st.write(success_stories) #displays summary of success stories


categories = success_stories['Category 1'].unique()
areas = success_stories["Area"].unique()
countries = success_stories['Country'].unique()
wlcos = success_stories['WL Co'].unique()

#st.session_state['categories'] = success_stories['Category 1'].unique()
#st.session_state['areas'] = success_stories["Area"].unique()
#st.session_state['countries'] = success_stories['Country'].unique()
#st.session_state['wlcos'] = success_stories['WL Co'].unique()

def filter():
    st.write("Filtering")
    filtered_df = success_stories.loc[success_stories['Category 1'].isin(category_choices)]
    filtered_df

category_choices = st.multiselect(label ="Categories",
                                  options = categories,                       
                                  on_change=filter())



area_choices = st.multiselect('Area:', areas)
country_choices = st.multiselect('Country:', countries)
wlco_choices = st.multiselect('Wl Co:', wlcos)

export_report()
#categories = success_stories['Category 1'].loc[success_stories['WL Co'].isin(wlco_choices)].loc[success_stories['Area'].isin(area_choices)].loc[success_stories['Country'].isin(country_choices)].unique()
#areas = success_stories["Area"].loc[success_stories['WL Co'].isin(wlco_choices)].unique()
#countries = success_stories['Country'].loc[success_stories['WL Co'].isin(wlco_choices)].loc[success_stories['Area'].isin(area_choices)].unique()



if st.button('Filter'):
    filtered_df = success_stories.loc[success_stories['WL Co'].isin(wlco_choices)].loc[success_stories['Area'].isin(area_choices)].loc[success_stories['Country'].isin(country_choices)]
    filtered_df
    pagenumbers = filtered_df['Page']
    
    export_report(pages=pagenumbers)
    
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