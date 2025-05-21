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

# Load authenticator
authenticator = get_authenticator()

# Show logo
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
    st.success("Login successful! Redirecting...")
    st.experimental_rerun()  # Rerun so session state persists
    st.switch_page("Home")   # ✅ Use page title, NOT file name
elif authentication_status is False:
    st.error("Incorrect username or password")
