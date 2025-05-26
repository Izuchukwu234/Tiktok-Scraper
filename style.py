import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
        /* Global Styling */
        body {
            background: linear-gradient(to bottom, #f5f7fa, #e8f0fe);
            font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif;
            color: #2d3748;
        }

        .main {
            background: linear-gradient(135deg, #ffffff, #f8fafc);
            border-radius: 16px;
            padding: 2.5rem;
            box-shadow: 0 8px 24px rgba(0, 123, 255, 0.1);
            margin-top: 2rem;
            transition: box-shadow 0.3s ease, transform 0.3s ease;
        }

        .main:hover {
            box-shadow: 0 12px 32px rgba(0, 123, 255, 0.15);
            transform: scale(1.01);
        }

        .header-divider {
            border-top: 2px solid #e2e8f0;
            margin-top: 1rem;
            margin-bottom: 2rem;
            transition: border-color 0.3s ease;
        }

        h1 {
            font-size: 2.5rem;
            background: linear-gradient(to right, #007bff, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-align: center;
            margin-bottom: 1rem;
        }

        .footer {
            font-size: 0.9rem;
            color: #4a5568;
            text-align: center;
            margin-top: 3rem;
            padding-top: 1.2rem;
            border-top: 1px solid #e2e8f0;
            background-color: #f8fafc;
            border-radius: 8px;
            transition: background 0.3s ease;
        }

        .footer:hover {
            background-color: #edf5ff;
        }

        /* Sidebar Container */
        section[data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(135deg, #ffffff, #e8f0fe);
            border-radius: 16px;
            padding: 30px 25px;
            box-shadow: 0 6px 20px rgba(0, 123, 255, 0.1);
            margin: 15px;
            transition: box-shadow 0.3s ease, transform 0.3s ease;
        }

        section[data-testid="stSidebar"] > div:first-child:hover {
            box-shadow: 0 10px 28px rgba(0, 123, 255, 0.2);
            transform: scale(1.02);
        }

        /* Sidebar Link Styling for <a> tags */
        section[data-testid="stSidebar"] a {
            color: #007bff !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            font-size: 14px !important;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            padding: 8px 12px;
            border-radius: 8px;
            transition: background 0.3s ease, color 0.3s ease;
        }

        /* Icons for <a> tags based on href */
        section[data-testid="stSidebar"] a[href*='login']::before {
            content: '🔐'; /* Login icon */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] a[href*='home']::before {
            content: '🏠'; /* Home icon */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] a[href*='how-we-collect-data']::before {
            content: '📊'; /* How We Collect Data icon */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] a[href*='meta']::before {
            content: '📸'; /* Meta icon */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] a[href*='reddit']::before {
            content: '👽'; /* Reddit icon */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] a[href*='snapchat']::before {
            content: '👻'; /* Snapchat icon */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] a[href*='threads']::before {
            content: '🧵'; /* Threads icon */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] a[href*='tiktok']::before {
            content: '🎵'; /* TikTok icon */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] a[href*='twitter']::before {
            content: '🐦'; /* Twitter icon */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] a[href*='youtube']::before {
            content: '📹'; /* YouTube icon */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] a:hover {
            color: #0056b3 !important;
            background-color: #edf5ff !important;
            text-decoration: none !important;
        }

        /* Fallback: Styling for radio buttons (e.g., st.sidebar.radio) */
        section[data-testid="stSidebar"] .stRadio > div > label {
            color: #007bff !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            font-size: 14px !important;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            padding: 8px 12px;
            border-radius: 8px;
            transition: background 0.3s ease, color 0.3s ease;
        }

        /* Icons for radio labels based on content */
        section[data-testid="stSidebar"] .stRadio > div > label:nth-of-type(1)::before {
            content: '🔐'; /* Login */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] .stRadio > div > label:nth-of-type(2)::before {
            content: '🏠'; /* Home */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] .stRadio > div > label:nth-of-type(3)::before {
            content: '📊'; /* How We Collect Data */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] .stRadio > div > label:nth-of-type(4)::before {
            content: '📸'; /* Meta */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] .stRadio > div > label:nth-of-type(5)::before {
            content: '👽'; /* Reddit */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] .stRadio > div > label:nth-of-type(6)::before {
            content: '👻'; /* Snapchat */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] .stRadio > div > label:nth-of-type(7)::before {
            content: '🧵'; /* Threads */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] .stRadio > div > label:nth-of-type(8)::before {
            content: '🎵'; /* TikTok */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] .stRadio > div > label:nth-of-type(9)::before {
            content: '🐦'; /* Twitter */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] .stRadio > div > label:nth-of-type(10)::before {
            content: '📹'; /* YouTube */
            margin-right: 8px;
            font-size: 1.1rem;
        }

        section[data-testid="stSidebar"] .stRadio > div > label:hover {
            color: #0056b3 !important;
            background-color: #edf5ff !important;
        }

        /* Logout Button Styling */
        section[data-testid="stSidebar"] .stButton button {
            background: linear-gradient(to right, #007bff, #00d4ff);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            font-size: 14px;
            text-transform: uppercase;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            margin-bottom: 25px;
            width: 100%;
        }

        section[data-testid="stSidebar"] .stButton button:hover {
            box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
            transform: translateY(-2px);
        }

        /* Logo Spacing and Animation */
        section[data-testid="stSidebar"] img {
            margin-top: 20px;
            margin-bottom: 10px;
            transition: transform 0.3s ease;
        }

        section[data-testid="stSidebar"] img:hover {
            transform: scale(1.1);
        }
    </style>
    """, unsafe_allow_html=True)
