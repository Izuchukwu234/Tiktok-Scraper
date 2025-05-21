import streamlit as st
from datetime import datetime
import streamlit_authenticator as stauth

# Page config
st.set_page_config(page_title="KOMI Radar | Home", page_icon="🔍", layout="centered")

# --- Hide sidebar / hamburger menu initially ---
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .css-1d391kg {display:none;}  /* sidebar collapse button */
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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
st.title("KOMI Radar")
st.caption("Powered by KOMI Insights!")
st.markdown('<div class="header-divider"></div>', unsafe_allow_html=True)

# --- Authentication setup ---
credentials = {
    "usernames": {
        "user1": {
            "name": "User One",
            "password": "hashed_password_here"  # Replace with hashed password or plaintext if using plaintext=True
        },
        # Add more users here
    }
}

cookie_config = {
    'cookie_name': 'komi_radar_auth',
    'key': 'some_random_key_change_this',
    'expiry_days': 30
}

authenticator = stauth.Authenticate(
    credentials,
    cookie_config['cookie_name'],
    cookie_config['key'],
    cookie_config['expiry_days'],
    preauthorized=[]
)

# --- Login form with version-safe unpacking ---
login_return = authenticator.login("Login", location="main")

if login_return is None:
    # Newer versions (0.5.0+), no unpack, use session_state
    authentication_status = st.session_state.get("authentication_status")
    name = st.session_state.get("name")
    username = st.session_state.get("username")
else:
    # Older versions (0.4.2), unpack tuple
    name, authentication_status, username = login_return

# --- After login ---
if authentication_status:
    # Show sidebar & hamburger menu again
    show_sidebar_style = """
        <style>
            #MainMenu {visibility: visible;}
            footer {visibility: visible;}
            header {visibility: visible;}
            .css-1d391kg {display:block;}  /* sidebar collapse button */
        </style>
    """
    st.markdown(show_sidebar_style, unsafe_allow_html=True)

    # Show logout in sidebar
    authenticator.logout("Logout", location="sidebar")
    st.sidebar.title(f"Welcome, {name}")

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
else:
    if authentication_status is False:
        st.error("Username/password is incorrect")
    else:
        st.info("Please enter your username and password to login.")

# --- FOOTER ---
current_year = datetime.now().year
st.markdown(f"""
    <div class="footer">
        <p>© {current_year} KOMI Group. All rights reserved.</p>
        <p>This tool is property of KOMI Group and is restricted to internal use only.</p>
    </div>
""", unsafe_allow_html=True)
