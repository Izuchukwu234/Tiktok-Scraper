import streamlit as st
from datetime import datetime
from auth import get_authenticator

st.set_page_config(page_title="KOMI Radar | Home", page_icon="🔍", layout="centered")

authenticator = get_authenticator()

# Hide sidebar toggle and sidebar before login
if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
    st.markdown("""
        <style>
            /* Hide sidebar toggle */
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
            /* Hide sidebar */
            .css-1d391kg {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Logo & welcome above login
    st.image("komi_logo.png", width=120)
    st.markdown("## Welcome to KOMI Radar")
    st.caption("Powered by KOMI Insights!")

# LOGIN
name, authentication_status, username = authenticator.login(location="main")

if authentication_status:
    authenticator.logout(button_name="Logout", location="sidebar")

    # Main page content, styles, footer etc.
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
    st.error("Incorrect username or password")

elif authentication_status is None:
    # No need to do anything here, logo shown above login
    pass
