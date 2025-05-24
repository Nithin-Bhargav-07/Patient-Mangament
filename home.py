import streamlit as st
import os
from config import ROLES
import streamlit_authenticator as stauth
import base64

if st.session_state.get("logged_out"):
    st.session_state.clear()
    st.experimental_rerun()

st.set_page_config(page_title="Hospital Dashboard", layout="wide")

def set_background(image_path):
    with open(image_path, "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("images/background.jpg")


if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'role' not in st.session_state:
    st.session_state.role = None


if not st.session_state.authenticated:
    with st.sidebar:
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ROLES)
        login_btn = st.button("Login")

        if login_btn:
            st.session_state.authenticated = True
            st.session_state.role = role
            st.session_state.username = username 
            st.success(f"Logged in as {role}")
            st.rerun()

if st.session_state.authenticated:
    st.sidebar.write(f" Role: `{st.session_state.role}`")

  
    if st.sidebar.button("Logout"):
        st.session_state["logged_out"] = True
        st.rerun()



  
    st.title(" Welcome to the Hospital Management System")
   
