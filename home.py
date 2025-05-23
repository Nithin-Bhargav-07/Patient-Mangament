import streamlit as st
import os
from config import ROLES
import streamlit_authenticator as stauth

st.set_page_config(page_title="Hospital Dashboard", layout="wide")

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'role' not in st.session_state:
    st.session_state.role = None

# Login form
if not st.session_state.authenticated:
    with st.sidebar:
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ROLES)
        login_btn = st.button("Login")

        if login_btn:
            # Simulate authentication success
            st.session_state.authenticated = True
            st.session_state.role = role
            st.session_state.username = username 
            st.success(f"Logged in as {role}")
            st.experimental_rerun()

# Main app
if st.session_state.authenticated:
    st.sidebar.write(f" Role: `{st.session_state.role}`")

    #  Logout button
    if st.sidebar.button("Logout "):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("Logged out successfully!")
        st.experimental_rerun()

    # Add your main app content here (or use pages)
    st.title(" Welcome to the Hospital Management System")
    st.write("Use the sidebar to navigate between pages.")
