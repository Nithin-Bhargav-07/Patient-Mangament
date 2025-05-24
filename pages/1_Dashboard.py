import streamlit as st
from auth import role_required
import json
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from utils import set_background
from encryption import decrypt_data

st.set_page_config(page_title="Hospital Dashboard", layout="wide")

set_background("images/background.jpg")  



role_required(['admin', 'doctor'])

if "username" not in st.session_state or not st.session_state.username:
    st.warning("Username not found in session. Please login first.")
    st.stop()
else:
    username = st.session_state.username.strip()
    st.title(f"Welcome, Dr. {username.capitalize()}!")
st.markdown("###  Here's your hospital overview for today.")

# Load data
def load_json_lines(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return [json.loads(line) for line in f]

patients = load_json_lines("data/patients.json")
appointments = load_json_lines("data/appointments.json")


total_patients = len(patients)
total_rooms = 100
available_rooms = max(0, total_rooms - total_patients)


today = datetime.today().strftime("%Y-%m-%d")
appointments_today = sum(
    1 for appt in appointments
    if datetime.strptime(decrypt_data(appt["date"]), "%Y-%m-%d").strftime("%Y-%m-%d") == today
)

col1, col2, col3 = st.columns(3)
col1.metric(" Total Patients", total_patients)
col2.metric(" Available Rooms", available_rooms)
col3.metric(" Appointments Today", appointments_today)

st.markdown("---")

st.subheader(" Hospital Capacity Overview")

labels = ['Occupied Rooms (Patients)', 'Available Rooms']
sizes = [total_patients, available_rooms]
colors = ['#ff9999','#66b3ff']
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax.axis('equal')
st.pyplot(fig)

st.markdown("---")


st.subheader("⚡ Quick Actions")
colA, colB = st.columns(2)
with colA:
    if st.button(" Add New Patient"):
        st.switch_page("pages/2_Add_Patient.py")
with colB:
    if st.button(" Give Appointment"):
        st.switch_page("pages/3_Give_Appointment.py")
