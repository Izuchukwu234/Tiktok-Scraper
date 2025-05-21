import streamlit as st
from datetime import datetime
from auth import get_authenticator

# Set page config
st.set_page_config(page_title="KOMI Radar | Home", page_icon="🔍", layout="centered")

# Hide Streamlit default UI
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION ---
authenticator = get_authenticator()

# ✅ Use only positional args — and ensure second argument is exactly one of: 'main', 'sidebar', 'unrendered'
name, authentication_status, username = authenticator.login("Login", "main")

# --- LOGIN SUCCESS ---
if authentication_status:
    authenticator.logout("Logout", "sidebar")

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

    # App Title
    st.image("komi_logo.png", width=100)
    st.title("KOMI Radar")
    st.caption("Powered by KOMI Insights!")
    st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)

    # Content
    st.markdown("""
    Welcome to the **KOMI Radar** – a unified platform to extract social media content from various platforms like:

    - TikTok
    - Reddit (Development ongoing 😊)
    - Instagram 🕐
    - YouTube 🕐
    - Threads 🕐
    - Snapchat 🕐
    - Twitter 🕐

    Use the navigation menu (☰) on the top-left to switch between platform pages.

    ---

    🚧 **Note**: This application is intended **only for internal use by KOMI Group**. Unauthorized access or distribution is prohibited.
    """)

    # Footer
    current_year = datetime.now().year
    st.markdown(f"""
        <div class="footer">
            <p>© {current_year} KOMI Group. All rights reserved.</p>
            <p>This tool is property of KOMI Group and is restricted to internal use only.</p>
        </div>
    """, unsafe_allow_html=True)

# --- LOGIN FAILED ---
elif authentication_status is False:
    st.error("Incorrect username or password")

# --- BEFORE LOGIN ---
elif authentication_status is None:
    st.image("komi_logo.png", width=120)
    st.markdown("## Welcome to KOMI Radar")
    st.caption("Powered by KOMI Insights!")
