import streamlit_authenticator as stauth

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
        key='51d4f55920a4b81efb19ab690efce1dd',
        cookie_expiry_days=1
    )
# import streamlit_authenticator as stauth

# def get_authenticator():
#     credentials = {
#         "usernames": {
#             "KOMI": {
#                 "name": "Admin",
#                 "password": "$2b$12$6lfyis7EL3QBVGhWBoGNk.ORiipCK3XQ5bmgR0cYRvjU5hK.4vWUy"
#             }
#         }
#     }

#     authenticator = stauth.Authenticate(
#         credentials,
#         cookie_name='komi_app',
#         key='auth',
#         cookie_expiry_days=1
#     )

#     return authenticator, credentials
