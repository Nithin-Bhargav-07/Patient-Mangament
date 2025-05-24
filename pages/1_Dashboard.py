import streamlit as st
from auth import role_required
import json
import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from utils import set_background
from encryption import decrypt_data
from collections import Counter
from datetime import datetime, timedelta

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


st.subheader(" Health Trends (Last 7 Days)")
date_counts = Counter(decrypt_data(appt["date"]) for appt in appointments if "date" in appt)
dates = [(datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d") for i in reversed(range(7))]
counts = [date_counts.get(date, 0) for date in dates]
trend_df = pd.DataFrame({"Date": dates, "Appointments": counts})
st.line_chart(trend_df.set_index("Date"))

st.markdown("---")

st.subheader(" Alerts")
alerts = []
if total_patients > 90:
    alerts.append("⚠️ High occupancy rate! Consider opening additional rooms.")
if appointments_today > 20:
    alerts.append("📅 Too many appointments today. Expect delays.")

if alerts:
    for alert in alerts:
        st.warning(alert)
else:
    st.success("No critical alerts at the moment.")

st.markdown("---")

st.subheader(" Patient Summary")
patient_names = [decrypt_data(p["name"]) for p in patients]
selected_patient = st.selectbox("Select a patient", patient_names)

if selected_patient:
    selected_data = next((p for p in patients if decrypt_data(p["name"]) == selected_patient), None)
    if selected_data:
        st.write("**Patient Info:**")
        st.json({
            "Name": decrypt_data(selected_data.get("name", "Unknown")),
            "Age": decrypt_data(selected_data.get("age", "N/A")),
            "Gender": decrypt_data(selected_data.get("gender", "N/A")),
        })

        st.write("**Appointments History:**")
        history = [a for a in appointments if decrypt_data(a.get("name", "")) == selected_patient]
        if history:
            df_history = pd.DataFrame([
                {"Date": decrypt_data(h["date"]), "Reason": decrypt_data(h["reason"])} for h in history
            ])
            st.dataframe(df_history)
        else:
            st.info("No past appointments found.")

st.markdown("---")

st.subheader(" Quick Actions")
colA, colB = st.columns(2)
with colA:
    if st.button(" Add New Patient"):
        st.switch_page("2_Patient_Records")
with colB:
    if st.button(" Give Appointment"):
        st.switch_page("3_Appointments")
