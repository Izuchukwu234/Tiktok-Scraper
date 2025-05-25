import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
            /* Global Styling */
            body {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', sans-serif;
            }

            h1, h2 {
                color: #007bff;
                font-weight: 600;
            }

            .footer {
                font-size: 0.85rem;
                color: #888;
                text-align: center;
                margin-top: 3rem;
                padding-top: 1rem;
                border-top: 1px solid #ddd;
            }

            /* Sidebar Container */
            section[data-testid="stSidebar"] > div:first-child {
                background-color: #ffffff;
                border-radius: 16px;
                padding: 25px 20px;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
                margin: 15px;
            }

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

            section[data-testid="stSidebar"] img {
                margin-top: 20px;
                margin-bottom: 10px;
            }

            .block-container .stButton {
                margin-bottom: 25px;
            }

            /* Login Container */
            .login-container {
                background-color: #ffffff;
                padding: 3rem 2rem;
                border-radius: 12px;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
                max-width: 400px;
                margin: 3rem auto;
                text-align: center;
                animation: fadeIn 0.6s ease-in-out;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .komi-blue {
                color: #007bff;
            }

            hr {
                border: none;
                border-top: 1px solid #ddd;
                margin: 1.5rem 0;
            }
        </style>
    """, unsafe_allow_html=True)
