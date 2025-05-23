import streamlit as st
from auth import get_authenticator

st.set_page_config(page_title="How We Collect Data | KOMI Group", page_icon="📊")

# --- AUTHENTICATION ---
authenticator = get_authenticator()

# Check login status
if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please log in first.")
    st.stop()

# --- Show logout in sidebar ---
authenticator.logout("Logout", location="sidebar")
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
st.sidebar.image("logo_2.png")

st.image("komi_logo.png", width=100)
st.title("How We Collect Data")
st.markdown("---")

st.markdown("""
### 📡 Our Data Collection Process

We use the **EnsembleData API**, a third-party enterprise-grade provider, to **fetch publicly available social media data**. Our system does **not directly scrape websites**, but instead relies on secure and compliant API access to retrieve:

- Publicly available social media post metrics
- Metadata for content like captions, hashtags, view counts
- User-facing share links
- Historical data based on hashtags, usernames, or keywords

---

✅ We ensure our tools stay compliant with platform guidelines and are strictly used for **internal insights and reporting**.

🛡️ **Disclaimer:** No personal data, login credentials, or private content is ever accessed.

""")

st.markdown("""
    <div style="margin-top: 50px; font-size: 0.9em; color: gray;">
        © KOMI Group — Internal Use Only
    </div>
""", unsafe_allow_html=True)
