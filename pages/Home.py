import streamlit as st
from datetime import datetime
from auth import get_authenticator
from style import inject_custom_css

# Page config
st.set_page_config(page_title="KOMI Radar | Home", page_icon="🔍", layout="centered")

inject_custom_css()

# --- AUTHENTICATION ---
authenticator = get_authenticator()
if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please log in first.")
    st.stop()

# Sidebar
authenticator.logout("Logout", location="sidebar")
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.image("logo_2.png")

# Logo and title
st.image("komi_logo.png", width=100)
st.title("KOMI Radar")
st.caption("Powered by KOMI Insights!")

# Custom HTML container
st.markdown("""
    <style>
        .komi-home-container {
            background: #f9fbff;
            padding: 30px;
            border-radius: 18px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
            margin-top: 20px;
            font-family: 'Segoe UI', sans-serif;
        }

        .komi-home-container h3 {
            color: #007bff;
            font-size: 1.75rem;
            margin-bottom: 15px;
        }

        .komi-home-container p,
        .custom-item {
            font-size: 1.05rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 12px;
        }

        .custom-item {
            background-color: #e9f3ff;
            padding: 10px 16px;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
            transition: background 0.3s;
        }

        .custom-item:hover {
            background-color: #d2e9ff;
        }

        .komi-home-note {
            margin-top: 25px;
            padding: 16px 20px;
            background-color: #fff8e1;
            border-left: 4px solid #ffc107;
            border-radius: 8px;
            font-weight: bold;
            color: #444;
        }

        .footer {
            text-align: center;
            margin-top: 40px;
            color: #888;
            font-size: 0.9rem;
        }
    </style>

    <div class="komi-home-container">
        <h3>Welcome to the KOMI Radar 👋</h3>
        <p>A unified platform to extract social media content from various platforms like:</p>

        <div class="custom-item">TikTok</div>
        <div class="custom-item">Reddit (Development of the app ongoing 😊)</div>
        <div class="custom-item">Instagram 🕐</div>
        <div class="custom-item">YouTube 🕐</div>
        <div class="custom-item">Threads 🕐</div>
        <div class="custom-item">Snapchat 🕐</div>
        <div class="custom-item">Twitter 🕐</div>

        <div class="komi-home-note">
            🚧 <strong>Note:</strong> This application is intended <strong>only for internal use by KOMI Group</strong>.<br>
            Unauthorised access or distribution is prohibited.
        </div>
    </div>
""", unsafe_allow_html=True)

# Footer
current_year = datetime.now().year
st.markdown(f"""
    <div class="footer">
        © {current_year} KOMI Group. All rights reserved.<br>
        This tool is property of KOMI Group and is restricted to internal use only.
    </div>
""", unsafe_allow_html=True)
