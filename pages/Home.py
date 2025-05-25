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

# Full HTML content
st.markdown("""
    <style>
        .komi-home-container {
            background: #f9fbff;
            padding: 30px;
            border-radius: 18px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
            margin-top: 20px;
            font-family: 'Segoe UI', sans-serif;
            text-align: center;
        }

        .komi-home-container img {
            width: 100px;
            margin-bottom: 10px;
        }

        .komi-home-container h1 {
            color: #007bff;
            margin-bottom: 5px;
        }

        .komi-home-container .caption {
            color: #555;
            font-size: 0.9rem;
            margin-bottom: 20px;
        }

        .komi-home-container h3 {
            font-size: 1.5rem;
            margin-bottom: 10px;
        }

        .komi-home-container p {
            font-weight: bold;
            font-size: 1rem;
            margin-bottom: 20px;
        }

        .custom-item {
            background-color: #e9f3ff;
            padding: 12px 18px;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            margin: 8px auto;
            max-width: 400px;
            transition: background 0.3s ease;
        }

        .custom-item:hover {
            background-color: #d0e7ff;
        }

        .komi-home-note {
            margin-top: 25px;
            padding: 16px 20px;
            background-color: #fff8e1;
            border-left: 4px solid #ffc107;
            border-radius: 8px;
            font-weight: bold;
            color: #444;
            text-align: left;
            max-width: 500px;
            margin-left: auto;
            margin-right: auto;
        }

        .footer {
            text-align: center;
            margin-top: 40px;
            color: #888;
            font-size: 0.85rem;
        }
    </style>

    <div class="komi-home-container">
        <img src="https://raw.githubusercontent.com/your-repo/komi_logo.png" alt="KOMI Logo">
        <h1>KOMI Radar</h1>
        <div class="caption">Powered by KOMI Insights!</div>

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
