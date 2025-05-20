import streamlit_authenticator as stauth
import bcrypt

usernames = ['KOMI']
hashed_passwords = ['$2b$12$6lfyis7EL3QBVGhWBoGNk.ORiipCK3XQ5bmgR0cYRvjU5hK.4vWUy']

def get_authenticator():
    return stauth.Authenticate(
        names=['Admin'],
        usernames=usernames,
        passwords=hashed_passwords,
        cookie_name='komi_app',
        key='auth',
        cookie_expiry_days=1
    )