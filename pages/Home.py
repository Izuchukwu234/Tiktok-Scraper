import streamlit as st
from datetime import datetime
from auth import get_authenticator
from style import inject_custom_css

# Page config
st.set_page_config(page_title="KOMI Radar | Home", page_icon="🔍", layout="centered")
inject_custom_css()

# --- AUTHENTICATION ---
authenticator = get_authenticator()

# Check login status
if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please log in first.")
    st.stop()

# --- Show logout in sidebar ---
authenticator.logout("Logout", location="sidebar")
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.image("logo_2.png")


# --- LOGO & TITLE ---
st.image("komi_logo.png", width=100)
st.title("KOMI Radar")
st.caption("Powered by KOMI Insights!")
st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)

# --- CONTENT ---
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

# --- FOOTER ---
current_year = datetime.now().year
st.markdown(f"""
    <div class="footer">
        <p>© {current_year} KOMI Group. All rights reserved.</p>
        <p>This tool is property of KOMI Group and is restricted to internal use only.</p>
    </div>
""", unsafe_allow_html=True)
