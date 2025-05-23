import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
            /* Global Styling */
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

            /* Sidebar Styling */
            section[data-testid="stSidebar"] > div:first-child {
                background-color: #ffffff;
                border-radius: 16px;
                padding: 25px 20px;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
                margin: 15px;
            }

            section[data-testid="stSidebar"] a span {
                color: #007bff !important;
                font-weight: 600 !important;
                font-size: 15px;
            }

            section[data-testid="stSidebar"] a:hover span {
                text-decoration: underline;
            }

            .block-container .stButton {
                margin-bottom: 25px;
            }
        </style>
    """, unsafe_allow_html=True)