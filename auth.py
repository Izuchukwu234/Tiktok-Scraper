import streamlit_authenticator as stauth

def get_authenticator():
    credentials = {
        "usernames": {
            "KOMI": {
                "name": "Admin",
                "password": "$2b$12$6lfyis7EL3QBVGhWBoGNk.ORiipCK3XQ5bmgR0cYRvjU5hK.4vWUy"  # bcrypt hash
            }
        }
    }

    # Cookie configuration
    cookie_config = {
        'cookie_name': 'komi_radar_auth',
        'key': '51d4f55920a4b81efb19ab690efce1dd',
        'expiry_days': 1
    }

    return stauth.Authenticate(
        credentials=credentials,
        cookie_name=cookie_config['cookie_name'],
        key=cookie_config['key'],
        cookie_expiry_days=cookie_config['expiry_days'],
        preauthorized=[]
    )
