import streamlit_authenticator as stauth
import bcrypt

def get_authenticator():
    credentials = {
        "usernames": {
            "KOMI": {
                "name": "Admin",
                "password": "$2b$12$6lfyis7EL3QBVGhWBoGNk.ORiipCK3XQ5bmgR0cYRvjU5hK.4vWUy"
            }
        }
    }

    return stauth.Authenticate(
        credentials,
        cookie_name='komi_app',
        key='auth',
        cookie_expiry_days=1
    )
