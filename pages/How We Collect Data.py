import streamlit as st
from auth import get_authenticator
from style import inject_custom_css

st.set_page_config(page_title="How We Collect Data | KOMI Group", page_icon="📊")

inject_custom_css()

# Page-specific CSS with enhanced designs
st.markdown("""
    <style>
        .komi-data-container {
            background: linear-gradient(135deg, #ffffff, #e8f0fe);
            padding: 3rem 3.5rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            margin: 20px 0;
            font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            border: 1px solid rgba(0, 123, 255, 0.15);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .komi-data-container:hover {
            box-shadow: 0 14px 32px rgba(0, 123, 255, 0.2);
            transform: scale(1.02);
        }

        .komi-data-container h3 {
            font-size: 2rem;
            background: linear-gradient(to right, #007bff, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1.5rem;
            letter-spacing: 0.5px;
            font-weight: 700;
            text-align: center;
        }

        .komi-data-container p {
            font-size: 1.1rem;
            color: #2d3748;
            margin-bottom: 1.5rem;
            letter-spacing: 0.2px;
            line-height: 1.6;
        }

        .komi-data-container ul {
            padding-left: 0;
            margin-bottom: 1.5rem;
            list-style-type: none; /* No bullet points */
        }

        .komi-data-container ul li {
            margin-bottom: 0.8rem;
            font-size: 1.05rem;
            color: #1a202c;
            background-color: #edf5ff;
            padding: 10px 15px;
            border-radius: 10px;
            transition: background 0.3s ease, transform 0.2s ease;
            font-weight: 500; /* Slightly less bold than homepage for variety */
            display: flex;
            align-items: center;
        }

        .komi-data-container ul li::before {
            content: '📈';
            margin-right: 10px;
            font-size: 1.2rem;
        }

        .komi-data-container ul li:hover {
            background-color: #c3e0ff;
            transform: translateX(5px);
        }

        .komi-data-note {
            margin-top: 2rem;
            font-weight: 500;
            font-size: 0.98rem;
            color: #2d3748;
            background-color: #fffaf0;
            border-left: 5px solid #f6ad55;
            border-radius: 10px;
            padding: 1.2rem;
            box-shadow: 0 2px 8px rgba(246, 173, 85, 0.2);
            transition: box-shadow 0.3s ease;
        }

        .komi-data-note:hover {
            box-shadow: 0 4px 12px rgba(246, 173, 85, 0.3);
        }

        .komi-divider {
            border-top: 2px solid #e2e8f0;
            margin: 2rem 0;
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

# Check login status
if not st.session_state.get("authentication_status"):
    st.warning("🔒 Please log in first.")
    st.stop()

# --- Show logout in sidebar ---
authenticator.logout("Logout", location="sidebar")
# st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.image("logo_2.png")

# Logo and title
# st.image("komi_logo.png", width=100)
# st.title("How We Collect Data")

# Styled content container
st.markdown("""
<div class="komi-data-container">
    <h3>📡 Our Data Collection Process</h3>
    <p>We use the <strong>EnsembleData API</strong>, a third-party enterprise-grade provider, to <strong>fetch publicly available social media data</strong>. Our system does <strong>not directly scrape websites</strong>, but instead relies on secure and compliant API access to retrieve:</p>
    <ul>
        <li>Publicly available social media post metrics</li>
        <li>Metadata for content like captions, hashtags, view counts</li>
        <li>User-facing share links</li>
        <li>Historical data based on hashtags, usernames, or keywords</li>
    </ul>
    <div class="komi-data-note">
        ✅ We ensure our tools stay compliant with platform guidelines and are strictly used for <strong>internal insights and reporting</strong>.<br>
        🛡️ <strong>Disclaimer:</strong> No personal data, login credentials, or private content is ever accessed.
    </div>
</div>
<div class="komi-divider"></div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        © KOMI Group — Internal Use Only
    </div>
""", unsafe_allow_html=True)
