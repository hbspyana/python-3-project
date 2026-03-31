import streamlit as st
import requests

# API_BASE = "http://127.0.0.1:8000"
API_BASE = "https://attendance-tracker-dp4l.onrender.com"

st.title("Attendance Tracker")

st.header("Add Student")
new_student = st.text_input("Student name")
if st.button("Add Student"):
    if new_student:
        requests.post(f"{API_BASE}/users/?name={new_student}")
        st.success(f"Added student: {new_student}")
        new_student = ""

st.header("Create Session")
new_session = st.text_input("Session title")
if st.button("Create Session"):
    if new_session:
        requests.post(f"{API_BASE}/tasks/?title={new_session}")
        st.success(f"Created session: {new_session}")
        new_session = ""

sessions = requests.get(f"{API_BASE}/tasks/").json()
session_map = {s["title"]: s["id"] for s in sessions}
selected_session_title = st.selectbox("Select Session", [""] + list(session_map.keys()))
selected_session_id = session_map.get(selected_session_title)

if selected_session_id:
    if st.button('Delete Session'):
        requests.delete(f'{API_BASE}/tasks/{selected_session_id}')
        st.success('Session deleted')
        st.rerun()

    st.subheader("Students")
    students = requests.get(f"{API_BASE}/tasks/attendance/{selected_session_id}").json()
    
    for s in students:
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])

        status = s['status']
        color = 'green' if status == 'present' else 'yellow' if status == 'late' else 'red'

        col1.markdown(f"{s['id']} {s['name']} - :{color}[{status}] (Present: {s['present_count']}, Late: {s['late_count']})")

        if col2.button("Present", key=f"present_{s['id']}"):
            requests.post(f"{API_BASE}/tasks/attendance?user_id={s['id']}&task_id={selected_session_id}&status=present")

        if col3.button("Late", key=f"late_{s['id']}"):
            requests.post(f"{API_BASE}/tasks/attendance?user_id={s['id']}&task_id={selected_session_id}&status=late")

        if col4.button("Absent", key=f"absent_{s['id']}"):
            requests.post(f"{API_BASE}/tasks/attendance?user_id={s['id']}&task_id={selected_session_id}&status=absent")

        if col5.button("🗑️", key=f"delete_{s['id']}"):
            requests.delete(f"{API_BASE}/users/{s['id']}")
