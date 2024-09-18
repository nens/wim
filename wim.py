import streamlit as st
import streamlit as st
import streamlit_authenticator as stauth
import os
import utils2 as utl
import yaml
from yaml.loader import SafeLoader
from datetime import datetime, timedelta


st.set_page_config(page_title="WIM", page_icon=":water:", layout="wide")

streamlit_settings = """
        <style>
        #MainMenu {visibility: hidden; }
        header {visibility: hidden;}
        footer {visibility: hidden;}
        button[title="View fullscreen"]{
            visibility: hidden;}
        .css-z5fcl4{
            padding-top:0px
        }
        .st-emotion-cache-z5fcl4{
            padding-top:0px 
        }
        </style>
        """

st.markdown(streamlit_settings, unsafe_allow_html=True)

# Configuration settings
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


nav = st.query_params.get('nav')

if nav == 'invullen':
    st.title('hi hoe druk ben jij?')
    st.markdown("""
        <style>
        .week-selector {
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 24px;
            margin: 20px 0;
        }
        .week-arrow {
            padding: 10px;
            background-color: #007BFF;
            color: white;
            border-radius: 50%;
            cursor: pointer;
            margin: 0 10px;
            font-weight: bold;
            user-select: none;
        }
        .week-text {
            font-weight: bold;
            margin: 0 15px;
        }
        .category-btn {
            display: inline-block;
            padding: 10px 20px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            margin-right: 10px;
            font-size: 16px;
        }
        .submit-btn {
            display: block;
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 18px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Week selection logic
    today = datetime.now()
    selected_week_start = st.session_state.get("selected_week_start", today - timedelta(days=today.weekday()))
    selected_week_end = selected_week_start + timedelta(days=6)

    # HTML for week selector with arrows
    st.markdown(f"""
        <div class="week-selector">
            <div class="week-arrow" id="prev-week"><</div>
            <div class="week-text">Week: {selected_week_start.strftime('%d %b')} - {selected_week_end.strftime('%d %b %Y')}</div>
            <div class="week-arrow" id="next-week">></div>
        </div>
    """, unsafe_allow_html=True)

    # JavaScript to handle arrow clicks (needs to interact with Streamlit's state)
    st.markdown("""
        <script>
        document.getElementById('prev-week').onclick = function() {
            window.location.href = '/?previous=true';
        };
        document.getElementById('next-week').onclick = function() {
            window.location.href = '/?next=true';
        };
        </script>
    """, unsafe_allow_html=True)


    with st.form("my_form"):
        # HTML for week selector with arrows
        st.markdown(f"""
             <div class="week-selector">
                 <div class="week-arrow" id="prev-week"><</div>
                 <div class="week-text">Week: {selected_week_start.strftime('%d %b')} - {selected_week_end.strftime('%d %b %Y')}</div>
                 <div class="week-arrow" id="next-week">></div>
             </div>
         """, unsafe_allow_html=True)

        # JavaScript to handle arrow clicks (needs to interact with Streamlit's state)
        st.markdown("""
             <script>
             document.getElementById('prev-week').onclick = function() {
                 window.location.href = '/?previous=true';
             };
             document.getElementById('next-week').onclick = function() {
                 window.location.href = '/?next=true';
             };
             </script>
         """, unsafe_allow_html=True)

        st.subheader("Select Category")
        categories = ["Busy", "Not Busy"]
        selected_category = st.radio("", categories, index=0, key="category_selector", horizontal=True)
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("slider", slider_val, "checkbox", checkbox_val)


name, authentication_status, username = authenticator.login(location='main')

utl.navbar_unauthenticated()
utl.inject_custom_css()


if authentication_status:
    utl.navbar_authenticated(name)
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

