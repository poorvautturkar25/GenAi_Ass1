import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="CSV App", layout="centered")

# ---------------- FILE NAMES ----------------
USERS_FILE = "users.csv"
FILES_FILE = "userfiles.csv"

# ---------------- CREATE CSV FILES IF NOT EXIST ----------------
if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["userid", "password"]).to_csv(USERS_FILE, index=False)

if not os.path.exists(FILES_FILE):
    pd.DataFrame(columns=["userid", "filename", "upload_datetime"]).to_csv(FILES_FILE, index=False)

# ---------------- SESSION STATE ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "userid" not in st.session_state:
    st.session_state.userid = None

if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------------- SIDEBAR MENU ----------------
with st.sidebar:
    st.title("Menu")

    if not st.session_state.authenticated:
        if st.button("Home"):
            st.session_state.page = "Home"
        if st.button("Login"):
            st.session_state.page = "Login"
        if st.button("Register"):
            st.session_state.page = "Register"
    else:
        if st.button("Explore CSV"):
            st.session_state.page = "Explore CSV"
        if st.button("See History"):
            st.session_state.page = "See History"
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.userid = None
            st.session_state.page = "Home"

# ---------------- PAGES ----------------
def home():
    st.title("Home")
    st.write("Please Login or Register to continue.")

def register():
    st.title("Register")

    userid = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        users = pd.read_csv(USERS_FILE)

        if userid in users["userid"].values:
            st.error("User already exists")
        else:
            users.loc[len(users)] = [userid, password]
            users.to_csv(USERS_FILE, index=False)
            st.success("Registration successful")

def login():
    st.title("Login")

    userid = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = pd.read_csv(USERS_FILE)

        match = users[
            (users["userid"] == userid) &
            (users["password"] == password)
        ]

        if not match.empty:
            st.session_state.authenticated = True
            st.session_state.userid = userid
            st.session_state.page = "Explore CSV"
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

def explore_csv():
    st.title("Explore CSV")

    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        history = pd.read_csv(FILES_FILE)
        history.loc[len(history)] = [
            st.session_state.userid,
            uploaded_file.name,
            datetime.now()
        ]
        history.to_csv(FILES_FILE, index=False)

        st.success("File uploaded successfully")

def see_history():
    st.title("Upload History")

    history = pd.read_csv(FILES_FILE)
    user_history = history[history["userid"] == st.session_state.userid]

    if user_history.empty:
        st.info("No history found")
    else:
        st.dataframe(user_history)

# ---------------- PAGE ROUTING ----------------
if st.session_state.page == "Home":
    home()
elif st.session_state.page == "Register":
    register()
elif st.session_state.page == "Login":
    login()
elif st.session_state.page == "Explore CSV":
    explore_csv()
elif st.session_state.page == "See History":
    see_history()
