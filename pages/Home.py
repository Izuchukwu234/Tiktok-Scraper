import streamlit as st
from datetime import datetime
from auth import get_authenticator
from style import inject_custom_css

# Page config
st.set_page_config(page_title="KOMI Radar | Home", page_icon="🔍", layout="centered")

# Inject global styles
inject_custom_css()

# Page-specific CSS with enhanced designs
st.markdown("""
    <style>
        .komi-home-container {
            background: linear-gradient(135deg, #ffffff, #e8f0fe);
            padding: 3rem 3.5rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            margin-top: 30px;
            font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            border: 1px solid rgba(0, 123, 255, 0.15);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .komi-home-container:hover {
            box-shadow: 0 14px 32px rgba(0, 123, 255, 0.2);
            transform: scale(1.02);
        }

        .komi-home-container h3 {
            font-size: 2rem;
            background: linear-gradient(to right, #007bff, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1.2rem;
            letter-spacing: 0.5px;
            font-weight: 700;
            text-align: center;
        }

        .komi-home-container p {
            font-size: 1.1rem;
            color: #2d3748;
            margin-bottom: 1.5rem;
            letter-spacing: 0.2px;
            line-height: 1.6;
        }

        .komi-home-container ul {
            padding-left: 0;
            margin-bottom: 1.5rem;
            list-style-type: none; /* No bullet points */
        }

        .komi-home-container ul li {
            margin-bottom: 0.8rem;
            font-size: 1.05rem;
            color: #1a202c;
            background-color: #edf5ff;
            padding: 10px 15px;
            border-radius: 10px;
            transition: background 0.3s ease, transform 0.2s ease;
            font-weight: bold; /* Bold text */
            display: flex;
            align-items: center;
        }

        .komi-home-container ul li::before {
            content: '🌐';
            margin-right: 10px;
            font-size: 1.2rem;
        }

        .komi-home-container ul li:hover {
            background-color: #c3e0ff;
            transform: translateX(5px);
        }

        .komi-home-note {
            margin-top: 2rem;
            font-weight: 500;
            font-size: 0.98rem;
            color: #2d3748;
            border-top: 1px solid #e2e8f0;
            padding: 1.2rem;
            background-color: #fffaf0;
            border-left: 5px solid #f6ad55;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(246, 173, 85, 0.2);
            transition: box-shadow 0.3s ease;
        }

        .komi-home-note:hover {
            box-shadow: 0 4px 12px rgba(246, 173, 85, 0.3);
        }

        .footer {
            text-align: center;
            margin-top: 2rem;
            font-size: 0.9rem;
            color: #4a5568;
            border-top: 1px solid #e2e8f0;
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION ---
authenticator = get_authenticator()
if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please log in first.")
    st.stop()

# Sidebar
authenticator.logout("Logout", location="sidebar")
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.image("logo_2.png")

# # Logo and title
# st.image("komi_logo.png", width=100)
# st.title("KOMI Radar")
# # st.caption("Powered by KOMI Insights!")

# Beautiful styled content container
st.markdown("""
<div class="komi-home-container">
    <h3>Welcome to the KOMI Radar 👋</h3>
    st.caption("Powered by KOMI Insights!")
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
