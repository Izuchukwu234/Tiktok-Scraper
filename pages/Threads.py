import streamlit as st
from auth import get_authenticator

st.set_page_config(page_title="Threads Scraper | KOMI Group", page_icon="💬")

# --- AUTHENTICATION ---
authenticator = get_authenticator()

# Check login status
if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please log in first.")
    st.stop()

# --- Show logout in sidebar ---
authenticator.logout("Logout", location="sidebar")

st.image("komi_logo.png", width=100)
st.markdown("""
<div style="display: flex; align-items: center; gap: 10px;">
    <img src="https://cdn-icons-png.flaticon.com/512/12105/12105338.png" width="36">
    <h1 style="margin: 0;">Threads Scraper</h1>
</div>
""", unsafe_allow_html=True)
st.markdown("### COMING SOON!")
st.markdown("---")

st.info("This feature is under development and will be available in a future update.")

st.markdown("""
    <div style="margin-top: 50px; font-size: 0.9em; color: gray;">
        © KOMI Group — Internal Use Only
    </div>
""", unsafe_allow_html=True)
