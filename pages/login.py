import streamlit as st
from auth import get_authenticator

st.set_page_config(page_title="Login | KOMI Radar", page_icon="🔐", layout="centered")

authenticator = get_authenticator()

st.image("komi_logo.png", width=120)
st.markdown("## Welcome to KOMI Radar")
st.caption("Powered by KOMI Insights!")

fields = {
    "Form name": "Login",
    "Username": "Username",
    "Password": "Password",
    "Login button": "Login"
}

login_result = authenticator.login(fields=fields, location="main")

if login_result:
    name, authentication_status, username = login_result
    if authentication_status:
        st.success("Login successful! Redirecting...")
        st.session_state["logged_in"] = True
        st.switch_page("Home.py")  # 🚨 Requires Streamlit >= 1.25.0
    elif authentication_status is False:
        st.error("Incorrect username or password")
else:
    st.session_state["logged_in"] = False