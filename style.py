import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
            body {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', sans-serif;
            }

            h1, h2 {
                color: #007bff;
            }

            .komi-blue {
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

            /* Style login form block */
            [data-testid="stForm"] {
                background-color: #ffffff;
                padding: 2rem;
                border: 1px solid #d6e4ff;
                border-radius: 12px;
                box-shadow: 0 6px 16px rgba(0, 123, 255, 0.1);
                max-width: 420px;
                margin: 0 auto 2rem auto;
            }

            /* Style inputs inside the form */
            [data-testid="stForm"] input {
                border: 1px solid #b3d7ff;
                border-radius: 6px;
                padding: 0.5rem;
            }

            [data-testid="stForm"] input:focus {
                border-color: #007bff;
                box-shadow: 0 0 6px rgba(0, 123, 255, 0.2);
            }

            /* Style the login button */
            [data-testid="stForm"] button {
                background-color: #007bff !important;
                color: white !important;
                font-weight: bold;
                border-radius: 6px;
                padding: 0.5rem 1rem;
            }

            [data-testid="stForm"] button:hover {
                background-color: #0056b3 !important;
            }
        </style>
    """, unsafe_allow_html=True)
