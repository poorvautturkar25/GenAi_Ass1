import streamlit as st
import pandas as pd

st.title("CSV Explorer")

#upload a CSV  file 
data_file = st.file_uploader("Upload a CSV File", type=["csv"])
# load it as dataframe
if data_file :
    df = pd.read_csv(data_file)
    #display the dataframe
    st.datafram(df)