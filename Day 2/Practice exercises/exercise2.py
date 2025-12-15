import streamlit as st

with st.form(key="Login_Form"):
    st.header("Login Form")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    sumbit_button = st.form_submit_button(label="Login")

if sumbit_button:
    st.success(f"You Are Successfully Logged In !!!")


