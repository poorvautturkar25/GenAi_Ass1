#Q1:
#Create a Streamlit application that allows users to upload a CSV file and view its schema.
# Use an LLM to convert user questions into SQL queries, execute them on the CSV data using pandasql, 
# and explain the results in simple English.

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from pandasql import sqldf
from langchain.chat_models import init_chat_model


st.set_page_config(page_title="CSV SQL Assistant", page_icon="📊")
st.title("📊 CSV SQL Assistant with LLM")

load_dotenv()

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)


uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 CSV Preview")
    st.dataframe(df.head())

    st.subheader("🧱 CSV Schema")
    st.write(df.dtypes)

    
    data = df

    
    question = st.text_input("Ask a question about this CSV (in English)")

    if st.button("Run Query"):
        if not question:
            st.warning("Please enter a question")
        else:
            
            sql_prompt = f"""
            Table name: data
            Table schema: {df.dtypes}

            Question: {question}

            Instruction:
            Write a valid SQLite SQL query only.
            Do NOT explain.
            Output only SQL.
            """

            sql_result = llm.invoke(sql_prompt)
            sql_query = sql_result.content.strip()

            st.subheader("🧠 Generated SQL")
            st.code(sql_query, language="sql")

            try:
                
                query_result = sqldf(sql_query, {"data": data})

                st.subheader("📊 Query Result")
                st.dataframe(query_result)

                
                explain_prompt = f"""
                The user asked: {question}

                SQL result:
                {query_result.head(10).to_string(index=False)}

                Explain this result in simple English.
                """

                explanation = llm.invoke(explain_prompt)

                st.subheader("🗣️ Explanation")
                st.write(explanation.content)

            except Exception as e:
                st.error("❌ Failed to execute SQL query")
                st.write(str(e))
