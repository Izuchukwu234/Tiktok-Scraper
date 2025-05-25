import streamlit as st
from datetime import datetime
from auth import get_authenticator
from style import inject_custom_css

# Page config
st.set_page_config(page_title="KOMI Radar | Home", page_icon="🔍", layout="centered")

# Load global styles (sidebar, buttons, etc.)
inject_custom_css()

# --- Page-Specific Styling (content only) ---
st.markdown("""
    <style>
        .komi-home-container {
            background-color: #ffffff;
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
            margin-top: 30px;
        }
        .komi-home-container h2 {
            color: #007bff;
            margin-bottom: 1rem;
        }
        .komi-home-container ul {
            padding-left: 1.2rem;
            margin-top: 0.5rem;
        }
        .komi-home-container li {
            margin-bottom: 0.4rem;
        }
        .komi-home-note {
            margin-top: 2rem;
            font-weight: 500;
            color: #444;
            border-top: 1px solid #eee;
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION ---
authenticator = get_authenticator()
if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please log in first.")
    st.stop()

# --- Sidebar content (preserved) ---
authenticator.logout("Logout", location="sidebar")
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.image("logo_2.png")

# --- Logo and Title ---
st.image("komi_logo.png", width=100)
st.title("KOMI Radar")
st.caption("Powered by KOMI Insights!")

# --- Styled Content Container ---
st.markdown('<div class="komi-home-container">', unsafe_allow_html=True)

st.markdown("### Welcome to the KOMI Radar 👋")
st.write("""
A unified platform to extract social media content from various platforms like:
""")

st.markdown("""
<ul>
    <li>TikTok</li>
    <li>Reddit (Development of the app ongoing 😊)</li>
    <li>Instagram 🕐</li>
    <li>YouTube 🕐</li>
    <li>Threads 🕐</li>
    <li>Snapchat 🕐</li>
    <li>Twitter 🕐</li>
</ul>
""", unsafe_allow_html=True)

st.markdown("""
<div class="komi-home-note">
🚧 <strong>Note:</strong> This application is intended <strong>only for internal use by KOMI Group</strong>.  
Unauthorised access or distribution is prohibited.
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
current_year = datetime.now().year
st.markdown(f"""
    <div class="footer">
        <p>© {current_year} KOMI Group. All rights reserved.</p>
        <p>This tool is property of KOMI Group and is restricted to internal use only.</p>
    </div>
""", unsafe_allow_html=True)
