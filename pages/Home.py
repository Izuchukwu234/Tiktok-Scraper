import streamlit as st
from datetime import datetime
from auth import get_authenticator

# Page config
st.set_page_config(page_title="KOMI Radar | Home", page_icon="🔍", layout="centered")

# --- Page-Specific Styling ---
st.markdown("""
    <style>
        .landing-container {
            background-color: #ffffff;
            padding: 2rem 2.5rem;
            border-radius: 16px;
            box-shadow: 0 8px 28px rgba(0, 0, 0, 0.08);
            margin-top: 30px;
        }

        .header-divider {
            border-top: 2px solid #e0e0e0;
            margin: 1.5rem 0;
        }

        h1 {
            color: #007bff;
            font-size: 2.4rem;
            margin-bottom: 0.5rem;
        }

        .st-emotion-cache-1kyxreq {
            text-align: center;
        }

        .welcome-text {
            font-size: 1.05rem;
            line-height: 1.7;
            color: #333333;
        }

        ul {
            padding-left: 1.3rem;
        }

        .footer {
            font-size: 0.85rem;
            color: #888;
            text-align: center;
            margin-top: 2.5rem;
            padding-top: 1rem;
            border-top: 1px solid #ddd;
        }
    </style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION ---
authenticator = get_authenticator()

if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please log in first.")
    st.stop()

# --- Show logout in sidebar ---
authenticator.logout("Logout", location="sidebar")
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.image("logo_2.png")

# --- Logo and Title ---
st.image("komi_logo.png", width=100)
st.title("KOMI Radar")
st.caption("Powered by KOMI Insights!")
st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)

# --- CONTENT in styled container ---
with st.container():
    st.markdown("""
    <div class="landing-container">
        <div class="welcome-text">
            Welcome to the <strong>KOMI Radar</strong> – a unified platform to extract social media content from various platforms like:

            <ul>
                <li>TikTok</li>
                <li>Reddit (Development of the app ongoing 😊)</li>
                <li>Instagram 🕐</li>
                <li>YouTube 🕐</li>
                <li>Threads 🕐</li>
                <li>Snapchat 🕐</li>
                <li>Twitter 🕐</li>
            </ul>

            Use the navigation menu (>) on the top-left to switch between platform pages.

            <hr>

            🚧 <strong>Note</strong>: This application is intended <strong>only for internal use by KOMI Group</strong>.
            Unauthorised access or distribution is prohibited.
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
current_year = datetime.now().year
st.markdown(f"""
    <div class="footer">
        <p>© {current_year} KOMI Group. All rights reserved.</p>
        <p>This tool is property of KOMI Group and is restricted to internal use only.</p>
    </div>
""", unsafe_allow_html=True)
