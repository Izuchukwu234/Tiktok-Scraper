import streamlit as st
from datetime import datetime
from auth import get_authenticator

# Page setup
st.set_page_config(page_title="KOMI Radar | Home", page_icon="🔍", layout="centered")

# Hide default Streamlit UI
st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- AUTH ---
authenticator = get_authenticator()

# Use keyword args to avoid ambiguous signature parsing
fields = {
    "Form name": "Login",
    "Username": "Username",
    "Password": "Password",
    "Login button": "Login"
}

# 💡 This matches streamlit-authenticator v0.4.2
name, authentication_status, username = authenticator.login(
    fields=fields,
    location="main"
)

# --- After login ---
if authentication_status:
    authenticator.logout(button_name="Logout", location="sidebar")

    st.image("komi_logo.png", width=100)
    st.title("KOMI Radar")
    st.caption("Powered by KOMI Insights!")
    st.markdown("---")

    st.markdown("""
    Welcome to the **KOMI Radar** – a unified platform to extract social media content from:

    - TikTok
    - Reddit (Dev in progress 😊)
    - Instagram 🕐
    - YouTube 🕐
    - Threads 🕐
    - Snapchat 🕐
    - Twitter 🕐

    Use the sidebar navigation to access different platform tools.
    """)

    st.markdown(f"<p style='text-align: center; color: grey; font-size: 0.9rem;'>© {datetime.now().year} KOMI Group. Internal use only.</p>", unsafe_allow_html=True)

elif authentication_status is False:
    st.error("Incorrect username or password.")

elif authentication_status is None:
    st.image("komi_logo.png", width=120)
    st.markdown("## Welcome to KOMI Radar")
    st.caption("Powered by KOMI Insights!")
