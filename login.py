import streamlit as st
import bcrypt
from auth import get_authenticator

# Page config
st.set_page_config(page_title="Login | KOMI Radar", page_icon="🔐", layout="centered")

# Hide sidebar, header, menu
st.markdown("""
    <style>
    #MainMenu, footer, header, [data-testid="stSidebar"], button[aria-label="Toggle sidebar"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Redirect if already logged in
if st.session_state.get("authentication_status"):
    st.switch_page("pages/Home.py")

# Load authenticator and credentials
authenticator = get_authenticator()
credentials = authenticator.credentials

# --- UI ---
st.image("komi_logo.png", width=120)
st.markdown("## KOMI Radar Login")
st.caption("Powered by KOMI Insights")

# --- Manual Login Form ---
with st.form("login_form"):
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")
    login_button = st.form_submit_button("Login")

    if login_button:
        if username_input in credentials["usernames"]:
            stored_pw_hash = credentials["usernames"][username_input]["password"]
            if bcrypt.checkpw(password_input.encode(), stored_pw_hash.encode()):
                st.session_state["authentication_status"] = True
                st.session_state["username"] = username_input
                st.success("Login successful! Redirecting...")
                st.experimental_rerun()
            else:
                st.error("Incorrect username or password.")
        else:
            st.error("Incorrect username or password.")
