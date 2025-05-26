import streamlit as st
from auth import get_authenticator

# Page config
st.set_page_config(page_title="Login | KOMI Radar", page_icon="🔐", layout="centered")

# Hide sidebar, header, menu
st.markdown("""
    <style>
    #MainMenu, footer, header, [data-testid="stSidebar"], button[aria-label="Toggle sidebar"] {
        display: none;
    }
    .footer {
        text-align: center;
        font-size: 0.8em;
        color: #666;
        margin-top: 20px;
    }
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

# Add line break
st.markdown("<br>", unsafe_allow_html=True)
# Add horizontal line and spacing
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


st.markdown(
    """
    <div class="footer">
        © 2025 KOMI Group. All rights reserved.<br>
        KOMI Radar is for internal use only.
    </div>
    """,
    unsafe_allow_html=True
)
