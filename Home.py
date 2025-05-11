import streamlit as st
from datetime import datetime

# Page config
st.set_page_config(page_title="KOMI Scraper | Home", page_icon="🔍", layout="centered")

# --- STYLES ---
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

# --- LOGO & TITLE ---
st.image("komi_logo.png", width=100)
st.title("KOMI Scraper Tool")
st.caption("Built for internal use by the KOMI Group")
st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)

# --- CONTENT ---
st.markdown("""
Welcome to the **KOMI Scraper Tool** – a unified platform to extract social media content from various platforms like:

- TikTok ✅ (Finished first phase of development)
- Instagram 🕐
- YouTube 🕐
- Threads 🕐
- Snapchat 🕐
- Twitter 🕐

Use the navigation menu (>) on the top-left to switch between platform pages.

---

🚧 **Note**: This application is intended **only for internal use by KOMI Group**. Unauthorized access or distribution is prohibited.

""")

# --- FOOTER ---
current_year = datetime.now().year
st.markdown(f"""
    <div class="footer">
        <p>© {current_year} KOMI Group. All rights reserved.</p>
        <p>This tool is property of KOMI Group and is restricted to internal use only.</p>
    </div>
""", unsafe_allow_html=True)
