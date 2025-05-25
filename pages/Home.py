import streamlit as st
from datetime import datetime
from auth import get_authenticator
from style import inject_custom_css

# Page config
st.set_page_config(page_title="KOMI Radar | Home", page_icon="🔍", layout="centered")

# Inject global styles
inject_custom_css()

# Page-specific CSS with text designs
st.markdown("""
    <style>
        .komi-home-container {
            background: linear-gradient(to bottom right, #fefefe, #f2f8ff);
            padding: 2.5rem 3rem;
            border-radius: 20px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
            margin-top: 30px;
            font-family: 'Segoe UI', sans-serif;
            transition: box-shadow 0.3s ease;
        }

        .komi-home-container:hover {
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.15);
        }

        .komi-home-container h3 {
            color: #007bff;
            font-size: 1.8rem;
            margin-bottom: 1rem;
            text-shadow: 1px 1px 0 #e2eaff;
        }

        .komi-home-container p {
            font-size: 1.05rem;
            color: #333;
            margin-bottom: 1.2rem;
        }

        .komi-home-container ul {
            padding-left: 1.2rem;
            margin-bottom: 1.5rem;
            list-style-type: none; /* Remove bullet points */
        }

        .komi-home-container ul li {
            margin-bottom: 0.7rem;
            font-size: 1.02rem;
            color: #222;
            background-color: #e9f3ff;
            padding: 8px 12px;
            border-radius: 8px;
            transition: background 0.3s;
            font-weight: bold; /* Make text bold */
        }

        .komi-home-container ul li:hover {
            background-color: #d2e9ff;
            cursor: default;
        }

        .komi-home-note {
            margin-top: 2rem;
            font-weight: 500;
            font-size: 0.95rem;
            color: #444;
            border-top: 1px solid #ddd;
            padding-top: 1.2rem;
            background-color: #fff8e1;
            border-left: 4px solid #ffc107;
            padding-left: 1rem;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION ---
authenticator = get_authenticator()
if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please log in first.")
    st.stop()

# Sidebar untouched
authenticator.logout("Logout", location="sidebar")
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.image("logo_2.png")

# Logo and title
st.image("komi_logo.png", width=100)
st.title("KOMI Radar")
st.caption("Powered by KOMI Insights!")

# Beautiful styled content container
st.markdown("""
<div class="komi-home-container">
    <h3>Welcome to the KOMI Radar 👋</h3>
    <p>A unified platform to extract social media content from various platforms like:</p>
    <ul>
        <li>TikTok</li>
        <li>Reddit (Development of the app ongoing 😊)</li>
        <li>Instagram 🕐</li>
        <li>YouTube 🕐</li>
        <li>Threads 🕐</li>
        <li>Snapchat 🕐</li>
        <li>Twitter 🕐</li>
    </ul>
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
        <p>© {current_year} KOMI Group. All rights reserved.</p>
        <p>This tool is property of KOMI Group and is restricted to internal use only.</p>
    </div>
""", unsafe_allow_html=True)
