import streamlit as st
import requests

# API_BASE = "https://attendance-tracker-dp4l.onrender.com"
API_BASE = "http://127.0.0.1:8000"

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
    st.subheader("Students")
    students = requests.get(f"{API_BASE}/tasks/attendance/{selected_session_id}").json()
    
    for s in students:
        status = s['status']

        if status == 'present':
            st.markdown(f':green[{status}]')
        if status == 'late':
            st.markdown(f':yellow[{status}]')
        if status == 'absent':
            st.markdown(f':red[{status}]')
        
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
        col1.write(f"{s['name']} (Present: {s['present_count']}, Late: {s['late_count']}, Status: {s['status']})")
        if col2.button(f"Present {s['id']}"):
            requests.post(f"{API_BASE}/tasks/attendance?user_id={s['id']}&task_id={selected_session_id}&status=present")
        if col3.button(f"Late {s['id']}"):
            requests.post(f"{API_BASE}/tasks/attendance?user_id={s['id']}&task_id={selected_session_id}&status=late")
        if col4.button(f"Absent {s['id']}"):
            requests.post(f"{API_BASE}/tasks/attendance?user_id={s['id']}&task_id={selected_session_id}&status=absent")
        if col5.button(f"Delete {s['id']}"):
            requests.delete(f"{API_BASE}/users/{s['id']}")
