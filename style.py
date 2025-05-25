import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
            /* GLOBAL STYLES */
            body {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', sans-serif;
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

            /* LOGIN FORM STYLING */
            div[data-testid="stForm"] {
                background-color: #ffffff;
                padding: 2.5rem;
                border-radius: 12px;
                border: 1px solid #cce0ff;
                box-shadow: 0 8px 20px rgba(0, 123, 255, 0.15);
                margin: 2rem auto;
                width: 100% !important;
                max-width: 650px;
            }

            .block-container {
                max-width: 1000px;
                padding-top: 2rem;
            }

            /* SIDEBAR CONTAINER */
            section[data-testid="stSidebar"] > div:first-child {
                background-color: #ffffff;
                border-radius: 16px;
                padding: 25px 20px;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
                margin: 15px;
            }

            /* SIDEBAR LINK STYLING */
            section[data-testid="stSidebar"] a span {
                color: #007bff !important;
                font-weight: bold !important;
                text-transform: uppercase !important;
                font-size: 14px !important;
            }

            section[data-testid="stSidebar"] a:hover span {
                color: #0056b3 !important;
                text-decoration: underline !important;
            }

            /* LOGOUT BUTTON MARGIN */
            .block-container .stButton {
                margin-bottom: 25px;
            }

            /* SIDEBAR LOGO SPACING */
            section[data-testid="stSidebar"] img {
                margin-top: 20px;
                margin-bottom: 10px;
            }
        </style>
    """, unsafe_allow_html=True)
