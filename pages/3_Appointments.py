import streamlit as st
from auth import role_required
import json
import os
from datetime import datetime
from encryption import encrypt_data, decrypt_data
from utils import set_background

st.set_page_config(page_title="Hospital Dashboard", layout="wide")

set_background("images/background.jpg")  


role_required(['doctor'])

st.title("Schedule Appointment")

patients = []
if os.path.exists("data/patients.json"):
    with open("data/patients.json", "r") as f:
        for line in f:
            try:
                record = json.loads(line)
                patients.append({
                    "name": decrypt_data(record["name"]),
                    "encrypted": record
                })
            except:
                continue

if not patients:
    st.warning("No patients found. Please add a patient first.")
    st.stop()

patient_names = [p["name"] for p in patients]
selected_name = st.selectbox("Select Patient", patient_names)

appointment_date = st.date_input("Appointment Date", min_value=datetime.today())
appointment_time = st.time_input("Appointment Time")
reason = st.text_area("Reason for Appointment")

if st.button("Schedule Appointment"):
    selected_patient = next(p for p in patients if p["name"] == selected_name)

    appointment = {
        "patient": selected_patient["encrypted"]["name"],
        "date": encrypt_data(appointment_date.strftime("%Y-%m-%d")),
        "time": encrypt_data(appointment_time.strftime("%H:%M")),
        "reason": encrypt_data(reason)
    }

    os.makedirs("data", exist_ok=True)
    with open("data/appointments.json", "a") as f:
        json.dump(appointment, f)
        f.write("\n")

    st.success("Appointment scheduled successfully!")
