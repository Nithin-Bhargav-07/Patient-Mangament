import streamlit as st
from config import ROLES

def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    role = st.sidebar.selectbox("Role", ROLES)

    if st.sidebar.button("Login"):
        if username and password:
            st.session_state['authenticated'] = True
            st.session_state['role'] = role
        else:
            st.error("Enter all login details")

def role_required(allowed_roles):
    if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
        st.error("Please login.")
        st.stop()
    elif st.session_state['role'] not in allowed_roles:
        st.error("Access Denied: Unauthorized role")
        st.stop()
