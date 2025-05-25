import streamlit as st
from auth import get_authenticator

# Page config
st.set_page_config(page_title="Login | KOMI Radar", page_icon="🔐", layout="centered")

# Page-specific CSS with enhanced designs
st.markdown("""
    <style>
        /* Hide sidebar, header, menu */
        #MainMenu, footer, header, [data-testid="stSidebar"], button[aria-label="Toggle sidebar"] {
            display: none;
        }

        /* Login container */
        .komi-login-container {
            background: linear-gradient(135deg, #ffffff, #e8f0fe);
            padding: 3rem 3.5rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 123, 255, 0.1);
            margin: 20px auto;
            max-width: 500px;
            border: 1px solid rgba(0, 123, 255, 0.15);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .komi-login-container:hover {
            box-shadow: 0 14px 32px rgba(0, 123, 255, 0.2);
            transform: scale(1.02);
        }

        /* Title styling */
        .komi-login-container h2 {
            font-size: 2rem;
            background: linear-gradient(to right, #007bff, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-align: center;
            margin-bottom: 0.5rem;
        }

        /* Caption styling */
        .komi-login-container .stCaption {
            font-size: 0.95rem;
            color: #4a5568;
            text-align: center;
            margin-bottom: 2rem;
        }

        /* Form inputs */
        .komi-login-container input {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 10px;
            font-size: 1rem;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }

        .komi-login-container input:focus {
            border-color: #007bff;
            box-shadow: 0 0 8px rgba(0, 123, 255, 0.2);
            outline: none;
        }

        /* Login button */
        .komi-login-container button {
            background: linear Commodity: .komi-login-container button {
            background: linear-gradient(to right, #007bff, #00d4ff);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 600;
            font-size: 1rem;
            text-transform: uppercase;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            width: 100%;
            margin-top: 1rem;
        }

        .komi-login-container button:hover {
            box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
            transform: translateY(-2px);
        }

        /* Error message */
        .komi-login-container .stAlert {
            border-radius: 8px;
            padding: 1rem;
            background-color: #fff1f0;
            color: #c53030;
            font-size: 0.95rem;
            margin-top: 1rem;
        }

        /* Divider */
        .komi-divider {
            border-top: 2px solid #e2e8f0;
            margin: 2rem 0;
        }

        /* Footer */
        .footer {
            font-size: 0.9rem;
            color: #4a5568;
            text-align: center;
            margin-top: 2rem;
            padding: 1.2rem;
            background-color: #f8fafc;
            border-radius: 8px;
            transition: background 0.3s ease;
        }

        .footer:hover {
            background-color: #edf5ff;
        }

        /* Blue text for KOMI */
        .komi-blue {
            background: linear-gradient(to right, #007bff, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
    </style>
""", unsafe_allow_html=True)

# If already authenticated, redirect to Home
if st.session_state.get("authentication_status"):
    st.switch_page("pages/Home.py")

# Load authenticator
authenticator = get_authenticator()

# Login container
st.markdown('<div class="komi-login-container">', unsafe_allow_html=True)

# Centered logo, title, and caption using st.columns
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.image("komi_logo.png", width=120)
    st.markdown('<h2>Welcome to <span class="komi-blue">KOMI</span> Radar 😊</h2>', unsafe_allow_html=True)
    st.caption("Powered by KOMI Insights!")

# Add horizontal line and spacing
st.markdown('<div class="komi-divider"></div>', unsafe_allow_html=True)

# Login form
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

# Add horizontal line and spacing
st.markdown('<div class="komi-divider"></div>', unsafe_allow_html=True)

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
