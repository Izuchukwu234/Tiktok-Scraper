import streamlit as st
from datetime import datetime
from auth import get_authenticator

# Page config
st.set_page_config(page_title="KOMI Radar | Home", page_icon="🔍", layout="centered")

# Initialize authenticator
authenticator = get_authenticator()

# CSS to hide hamburger sidebar toggle and sidebar completely before login
hide_sidebar_style = """
<style>
    /* Hide sidebar toggle button */
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
    /* Hide entire sidebar */
    .css-1d391kg {
        display: none !important;
    }
</style>
"""

# --- AUTHENTICATION ---
# Define the login form fields dictionary (per streamlit-authenticator 0.4.2 spec)
fields = {
    "Form name": "Login",
    "Username": "Username",
    "Password": "Password",
    "Login button": "Login"
}

# Only show sidebar toggle + sidebar when logged in
if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
    st.markdown(hide_sidebar_style, unsafe_allow_html=True)

    # Show logo & powered by KOMI above login
    st.image("komi_logo.png", width=120)
    st.markdown("## Welcome to KOMI Radar")
    st.caption("Powered by KOMI Insights!")

# Perform login
name, authentication_status, username = authenticator.login(fields=fields, location="main")

if authentication_status:
    # Show sidebar toggle and sidebar again after login
    # (No special CSS means default behavior)

    # Logout button on sidebar
    authenticator.logout(button_name="Logout", location="sidebar")

    # Page styles
    st.markdown("""
        <style>
            body {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', sans-serif;
            }
            .main {
                background-color: #ffffff;
                border-radius: 12px;
                padding: 2rem;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
                margin-top: 2rem;
            }
            .header-divider {
                border-top: 2px solid #e0e0e0;
                margin-top: 1rem;
                margin-bottom: 2rem;
            }
            h1 {
                color: #007bff;
            }
            .footer {
                font-size: 0.85rem;
                color: #888;
                text-align: center;
                margin-top: 3rem;
                padding-top: 1rem;
                border-top: 1px solid #ddd;
            }
        </style>
    """, unsafe_allow_html=True)

    # Logo & title (inside main content area)
    st.image("komi_logo.png", width=100)
    st.title("KOMI Radar")
    st.caption("Powered by KOMI Insights!")
    st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)

    # Main content
    st.markdown("""
    Welcome to the **KOMI Radar** – a unified platform to extract social media content from various platforms like:

    - TikTok
    - Reddit (Development of the app ongoing 😊)
    - Instagram 🕐
    - YouTube 🕐
    - Threads 🕐
    - Snapchat 🕐
    - Twitter 🕐

    Use the navigation menu (>) on the top-left to switch between platform pages.

    ---

    🚧 **Note**: This application is intended **only for internal use by KOMI Group**. Unauthorised access or distribution is prohibited.
    """)

    # Footer
    current_year = datetime.now().year
    st.markdown(f"""
        <div class="footer">
            <p>© {current_year} KOMI Group. All rights reserved.</p>
            <p>This tool is property of KOMI Group and is restricted to internal use only.</p>
        </div>
    """, unsafe_allow_html=True)

elif authentication_status is False:
    st.error("Incorrect username or password")

elif authentication_status is None:
    # Before login (show logo + welcome - already shown above, so can be empty or add here if you want)
    pass
