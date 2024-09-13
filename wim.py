import streamlit as st
import streamlit as st
import streamlit_authenticator as stauth
import os
import utils2 as utl
import yaml
from yaml.loader import SafeLoader

# Configuration settings
st.set_page_config(page_title="Droogte WVV", page_icon=":water:", layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)
showWarningOnDirectExecution = False

hashed_passwords = stauth.Hasher(['abc', 'def']).generate()

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


name, authentication_status, username = authenticator.login(location='main')

utl.navbar_unauthenticated()

if authentication_status:
    utl.navbar_authenticated(name)
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

utl.inject_custom_css()
