import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()





# ---------------------------------
# Load DB Connection Details
# ---------------------------------
def load_connection():
    params = {}
    with open("connection.txt") as f:
        for line in f:
            key, value = line.strip().split("=")
            params[key] = value
    return params

# ---------------------------------
# Load Database Schema
# ---------------------------------
def load_schema():
    with open("db.txt") as f:
        return f.read()

# ---------------------------------
# Connect to MySQL
# ---------------------------------
def get_connection():
    params = load_connection()
    return mysql.connector.connect(
        host=params["host"],
        user=params["user"],
        password=params["password"],
        database=params["database"]
    )

# ---------------------------------
# Streamlit UI
# ---------------------------------
st.title("🧠 Natural Language to SQL (MySQL)")
st.write("Ask questions in English. The app will generate SQL and execute it.")

question = st.text_input("Enter your question:")

# ---------------------------------
# LLM Setup
# ---------------------------------
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)

schema = load_schema()

prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template="""
You are an expert MySQL assistant.

Database schema:
{schema}

Convert the following question into a valid MySQL SELECT query only.
Do NOT use INSERT, UPDATE, DELETE.

Question:
{question}

SQL Query:
"""
)

# ---------------------------------
# Run Query
# ---------------------------------
if st.button("Run Query") and question:
    try:
        sql_query = llm.predict(
            prompt.format(schema=schema, question=question)
        )

        st.subheader("📄 Generated SQL Query")
        st.code(sql_query, language="sql")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql_query)

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        st.subheader("📊 Query Results")
        st.dataframe(rows, use_container_width=True)

        # Explanation
        explain_prompt = f"""
Explain this SQL query in simple English:

{sql_query}
"""
        explanation = llm.predict(explain_prompt)

        st.subheader("📝 Explanation")
        st.write(explanation)

        cursor.close()
        conn.close()

    except Exception as e:
        st.error(f"Error: {e}")

