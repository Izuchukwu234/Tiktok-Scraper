import streamlit as st
from datetime import datetime
from auth import get_authenticator

st.set_page_config(page_title="KOMI Radar | Home", page_icon="🔍", layout="centered")

authenticator = get_authenticator()

# Hide sidebar/hamburger before login
if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
    st.markdown("""
        <style>
            /* Hide hamburger menu */
            button[aria-label="Toggle sidebar"],
            button[data-testid="stSidebarToggleButton"] {
                visibility: hidden !important;
                pointer-events: none !important;
                height: 0 !important;
                width: 0 !important;
                padding: 0 !important;
                margin: 0 !important;
                overflow: hidden !important;
                position: absolute !important;
            }
            /* Hide sidebar itself */
            .css-1d391kg {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Logo and powered by caption above login
    st.image("komi_logo.png", width=120)
    st.markdown("## Welcome to KOMI Radar")
    st.caption("Powered by KOMI Insights!")

# Perform login and unpack return values properly (v0.4.2 style)
name, authentication_status, username = authenticator.login(location='main')

if authentication_status:
    # Show logout button in sidebar after login
    authenticator.logout('Logout', location='sidebar')

    st.image("komi_logo.png", width=100)
    st.title("KOMI Radar")
    st.caption("Powered by KOMI Insights!")
    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown("""
    Welcome to the **KOMI Radar** – a unified platform to extract social media content from:

    - TikTok
    - Reddit (under development)
    - Instagram 🕐
    - YouTube 🕐
    - Threads 🕐
    - Snapchat 🕐
    - Twitter 🕐

    Use the menu on the top-left to switch between pages.

    ---

    🚧 **Note**: This application is only for internal use by KOMI Group.
    """)

    current_year = datetime.now().year
    st.markdown(f"""
        <div style="font-size:0.85rem; color:#888; text-align:center; margin-top:3rem; padding-top:1rem; border-top:1px solid #ddd;">
            © {current_year} KOMI Group. All rights reserved.<br>
            This tool is restricted to internal use only.
        </div>
    """, unsafe_allow_html=True)

elif authentication_status is False:
    st.error("Username/password is incorrect")

elif authentication_status is None:
    # User has not yet entered credentials, show nothing here as login form is rendered above
    pass
