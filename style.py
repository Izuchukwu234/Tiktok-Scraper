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

            /* Login Form Box */
            .login-form-wrapper {
                background: #fff;
                padding: 2.5rem 2rem;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
                box-shadow: 0 4px 20px rgba(0, 123, 255, 0.1);
                max-width: 400px;
                margin: 0 auto 3rem auto;
            }

            /* Streamlit text inputs inside form */
            .login-form-wrapper input {
                border: 1px solid #cce5ff !important;
                border-radius: 6px !important;
            }

            .login-form-wrapper input:focus {
                border: 1px solid #007bff !important;
                box-shadow: 0 0 5px rgba(0, 123, 255, 0.25) !important;
            }

            /* Login button */
            .login-form-wrapper button {
                background-color: #007bff !important;
                color: white !important;
                border-radius: 6px !important;
                font-weight: bold !important;
            }

            .login-form-wrapper button:hover {
                background-color: #0056b3 !important;
            }
        </style>
    """, unsafe_allow_html=True)
