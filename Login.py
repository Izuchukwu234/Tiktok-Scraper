import streamlit as st
from auth import get_authenticator

# Page config
st.set_page_config(page_title="Login | KOMI Radar", page_icon="🔐", layout="centered")

# Page-specific CSS
st.markdown("""
    <style>
        /* Hide sidebar, header, menu */
        #MainMenu, footer, header, [data-testid="stSidebar"], button[aria-label="Toggle sidebar"] {
            display: none;
        }

        /* Reset wrappers to remove empty container at top */
        [data-testid="stForm"], [data-testid="stVerticalBlock"], [data-testid="stBlock"] {
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
            min-height: 0 !important;
            overflow: hidden !important;
        }

        /* Form container */
        .komi-login-form {
            background: #ffffff;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 123, 255, 0.1);
            margin-top: 0 !important;
            border: 2px solid #007bff; /* Temporary border to confirm form visibility */
            font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Form labels */
        .komi-login-form label {
            font-size: 1rem;
            color: #2d3748;
            font-weight: 500;
            margin-bottom: 0.4rem;
            display: block;
        }

        /* Form inputs */
        .komi-login-form input,
        .komi-login-form [data-testid="stTextInput"] input,
        .komi-login-form input[type="text"],
        .komi-login-form input[type="password"] {
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 12px 14px;
            font-size: 1rem;
            font-family: 'Inter', 'Segoe UI', sans-serif;
            background-color: #f8fafc;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
            width: 100%;
            box-sizing: border-box;
            margin-bottom: 0.8rem;
        }

        .komi-login-form input:focus,
        .komi-login-form [data-testid="stTextInput"] input:focus,
        .komi-login-form input[type="text"]:focus,
        .komi-login-form input[type="password"]:focus {
            border-color: #007bff;
            box-shadow: 0 0 8px rgba(0, 123, 255, 0.2);
            outline: none;
        }

        /* Login button */
        .komi-login-form button,
        .komi-login-form [data-testid="stButton"] button,
        .komi-login-form button[kind="primary"] {
            background: linear-gradient(to right, #007bff, #00d4ff);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 12px 24px;
            font-weight: 600;
            font-size: 1rem;
            text-transform: uppercase;
            transition: transform 0.2s ease, box-shadow 0.3s ease;
            width: 100%;
            cursor: pointer;
            margin-top: 0.8rem;
        }

        .komi-login-form button:hover,
        .komi-login-form [data-testid="stButton"] button:hover,
        .komi-login-form button[kind="primary"]:hover {
            box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
            transform: translateY(-2px);
        }

        /* Error message */
        [data-testid="stAlert"] {
            border-radius: 10px;
            padding: 1rem;
            background-color: #fff1f0;
            color: #c53030;
            font-size: 0.95rem;
            margin-top: 1rem;
        }

        /* Footer */
        .footer {
            text-align: center;
            font-size: 0.8em;
            color: #666;
            margin-top: 20px;
        }

        /* Blue text for KOMI */
        .komi-blue {
            color: #0000FF;
        }
    </style>
""", unsafe_allow_html=True)

# If already authenticated, redirect to Home
if st.session_state.get("authentication_status"):
    st.switch_page("pages/Home.py")

# Load authenticator
authenticator = get_authenticator()

# Centered logo, title, and caption using st.columns
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.image("komi_logo.png", width=120)
    st.markdown('## Welcome to <span class="komi-blue">KOMI</span> Radar 😊', unsafe_allow_html=True)
    st.caption("Powered by KOMI Insights!")

# Add horizontal line and spacing
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Login form
st.markdown('<div class="komi-login-form">', unsafe_allow_html=True)
fields = {
    "Form name": "Login",
    "Username": "Username",
    "Password": "Password",
    "Login button": "Login"
}

login_result = authenticator.login(fields=fields, location='main')

if login_result:
    name, authentication_status, username = login_result
else:
    name = authentication_status = username = None

# Handle outcomes
if authentication_status:
    st.session_state["authentication_status"] = True
    st.experimental_rerun()
elif authentication_status is False:
    st.error("Incorrect username or password")
st.markdown('</div>', unsafe_allow_html=True)

# Add line break
st.markdown("<br>", unsafe_allow_html=True)

# Add horizontal line and spacing
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class="footer">
        © 2025 KOMI Group. All rights reserved.<br>
        KOMI Radar is for internal use only.
    </div>
    """,
    unsafe_allow_html=True
)
