import streamlit as st
import base64

def set_background_local(image_path):
    """
    Sets a local image as the background for the Streamlit app.
    image_path: relative path to the image file
    """
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
