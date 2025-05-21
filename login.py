import streamlit as st
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

# If already authenticated, redirect to Home
if st.session_state.get("authentication_status"):
    st.switch_page("pages/Home.py")

# Load authenticator
authenticator = get_authenticator()

# Show logo and login header
st.image("komi_logo.png", width=120)
st.markdown("## KOMI Radar Login")
st.caption("Powered by KOMI Insights")

# --- LOGIN FORM ---
fields = {
    "Form name": "Login",
    "Username": "Username",
    "Password": "Password",
    "Login button": "Login"
}

login_result = authenticator.login(fields=fields, location='main')

if login_result:
    name, authentication_status, username = login_result
else:
    name = authentication_status = username = None

# --- Handle outcomes ---
if authentication_status:
    st.session_state["authentication_status"] = True
    st.experimental_rerun()  # Will rerun, and redirect at top
elif authentication_status is False:
    st.error("Incorrect username or password")
