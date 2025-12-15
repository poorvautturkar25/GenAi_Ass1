import streamlit as st
import pandas as pd
import pandasql as ps

st.title("CSV SQL Query Executor")

st.write("Upload a CSV file, write SQL query, and see the result")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded CSV Data")
    st.dataframe(df)

    st.subheader("Dataframe Column Types")
    st.write(df.dtypes)

    st.subheader("Enter SQL Query")
    st.info("Use table name as **data**")

    default_query = "SELECT * FROM data LIMIT 5"
    query = st.text_area("SQL Query", value=default_query, height=120)

    
    if st.button("Run Query"):
        try:
            result = ps.sqldf(query, {"data": df})

            st.subheader("Query Result")
            st.dataframe(result)

        except Exception as e:
            st.error("Error executing query")
            st.exception(e)

else:
    st.warning("Please upload a CSV file to continue.")
