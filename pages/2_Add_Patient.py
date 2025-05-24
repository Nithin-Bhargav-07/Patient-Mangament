import streamlit as st
from auth import role_required
from encryption import encrypt_data
import os
import json
from utils import set_background

st.set_page_config(page_title="Hospital Dashboard", layout="wide")

set_background("images/background.jpg")  


role_required(['admin', 'doctor'])

st.title("Add New Patient Record")

name = st.text_input("Patient Name")
age = st.number_input("Age", min_value=0)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
condition = st.text_area("Medical Condition")

uploaded_file = st.file_uploader("Upload PDF/Image", type=["pdf", "png", "jpg", "jpeg"])

if st.button("Submit"):
    if name and condition:
        record = {
            "name": encrypt_data(name),
            "age": age,
            "condition": encrypt_data(condition)
        }

        # Save to JSON (simulation of DB)
        os.makedirs("data", exist_ok=True)
        with open("data/patients.json", "a") as f:
            json.dump(record, f)
            f.write("\n")

        # Save file
        if uploaded_file:
            os.makedirs("uploads", exist_ok=True)
            with open(os.path.join("uploads", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())

        st.success("Patient record added securely.")
    else:
        st.error("Please complete all fields.")
