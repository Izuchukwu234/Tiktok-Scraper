# import streamlit as st
# import bcrypt
# from auth import get_authenticator

# # Page config
# st.set_page_config(page_title="Login | KOMI Radar", page_icon="🔐", layout="centered")

# # Hide sidebar, header, menu
# st.markdown("""
#     <style>
#     #MainMenu, footer, header, [data-testid="stSidebar"], button[aria-label="Toggle sidebar"] {
#         display: none;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Redirect if already logged in
# if st.session_state.get("authentication_status"):
#     st.switch_page("pages/Home.py")

# # Load authenticator and credentials
# authenticator, credentials = get_authenticator()

# # --- UI ---
# st.image("komi_logo.png", width=120)
# st.markdown("## KOMI Radar Login")
# st.caption("Powered by KOMI Insights")

# # --- Manual Login Form ---
# with st.form("login_form"):
#     username_input = st.text_input("Username")
#     password_input = st.text_input("Password", type="password")
#     login_button = st.form_submit_button("Login")

#     if login_button:
#         if username_input in credentials["usernames"]:
#             stored_pw_hash = credentials["usernames"][username_input]["password"].encode("utf-8")
#             if bcrypt.checkpw(password_input.encode("utf-8"), stored_pw_hash):
#                 st.session_state["authentication_status"] = True
#                 st.session_state["username"] = username_input
#                 st.success("Login successful! Redirecting...")
#                 st.experimental_rerun()
#             else:
#                 st.error("Incorrect username or password.")
#         else:
#             st.error("Incorrect username or password.")

# import streamlit as st
# from auth import get_authenticator

# # Page config
# st.set_page_config(page_title="Login | KOMI Radar", page_icon="🔐", layout="centered")

# # Hide sidebar, header, menu
# st.markdown("""
#     <style>
#     #MainMenu, footer, header, [data-testid="stSidebar"], button[aria-label="Toggle sidebar"] {
#         display: none;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # If already authenticated, redirect to Home
# if st.session_state.get("authentication_status"):
#     st.switch_page("pages/Home.py")

# # Load authenticator
# authenticator = get_authenticator()

# # Show logo and login header
# st.image("komi_logo.png", width=120)
# st.markdown("## KOMI Radar Login")
# st.caption("Powered by KOMI Insights")

# # --- LOGIN FORM ---
# fields = {
#     "Form name": "Login",
#     "Username": "Username",
#     "Password": "Password",
#     "Login button": "Login"
# }

# login_result = authenticator.login(fields=fields, location='main')

# if login_result:
#     name, authentication_status, username = login_result
# else:
#     name = authentication_status = username = None

# # --- Handle outcomes ---
# if authentication_status:
#     st.session_state["authentication_status"] = True
#     st.experimental_rerun()  # Will rerun, and redirect at top
# elif authentication_status is False:
#     st.error("Incorrect username or password")

import streamlit as st
from auth import get_authenticator
from style import inject_custom_css

# Page config
st.set_page_config(page_title="Login | KOMI Radar", page_icon="🔐", layout="centered")

# Inject CSS
inject_custom_css()

# Hide sidebar, header, menu
st.markdown("""
    <style>
    #MainMenu, footer, header, [data-testid="stSidebar"], button[aria-label="Toggle sidebar"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# If already authenticated, redirect to Home
if st.session_state.get("authentication_status"):
    st.switch_page("pages/Home.py")

# Load authenticator
authenticator = get_authenticator()

# Centered logo, title, and caption
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.image("komi_logo.png", width=120)
    st.markdown('## Welcome to <span class="komi-blue">KOMI</span> Radar 😊', unsafe_allow_html=True)
    st.caption("Powered by KOMI Insights!")

# Spacer
st.markdown("<br>", unsafe_allow_html=True)

# Login form inside styled div
st.markdown('<div class="login-form-wrapper">', unsafe_allow_html=True)

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

if authentication_status:
    st.session_state["authentication_status"] = True
    st.experimental_rerun()
elif authentication_status is False:
    st.error("Incorrect username or password")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
    <div class="footer">
        © 2025 KOMI Group. All rights reserved.<br>
        KOMI Radar is for internal use only.
    </div>
""", unsafe_allow_html=True)
