import streamlit as st
import requests

def get_health_data(token):
    headers = {"Authorization": f"Token {token}"}
    response = requests.get("http://localhost:8000/api/health_data/", headers=headers)
    if response.status_code == 200:
        return response.json()
    return {"error": "Unable to fetch data"}

def login(username, password):
    response = requests.post("http://localhost:8000/api-token-auth/", data={"username": username, "password": password})
    if response.status_code == 200:
        return response.json().get("token")
    return None

st.title("Health Care App")

if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state.token:
    st.success("Logged in as admin")
    if st.button("Get Health Data"):
        data = get_health_data(st.session_state.token)
        st.json(data)
else:
    st.subheader("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        token = login(username, password)
        if token:
            st.session_state.token = token
            st.success("Login successful!")
        else:
            st.error("Invalid credentials")