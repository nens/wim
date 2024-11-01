import streamlit as st
import streamlit_authenticator as stauth
from streamlit_date_picker import date_range_picker, date_picker, PickerType
from streamlit_option_menu import option_menu
from pathlib import Path
import utils2 as utl
import yaml
from yaml.loader import SafeLoader
from datetime import datetime, timedelta
import datetime
import pandas as pd
import random
import plotly.graph_objects as go
from functions import *

from PIL import Image

im = Image.open('./images/wim_logo.png')


today = datetime.datetime.now()

st.set_page_config(page_title="WIM", page_icon=im, layout="wide")

streamlit_settings = """
        <style>
        #MainMenu {visibility: hidden; }
        header {visibility: hidden;}
        footer {visibility: hidden;}
        button[title="View fullscreen"]{
            visibility: hidden;}
        .css-z5fcl4{
            padding-top:1px
        }
        .st-emotion-cache-z5fcl4{
            padding-top:1px 
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

name, authentication_status, username = authenticator.login(location='main')

nav = st.query_params.get('nav')

if nav == 'uitloggen':
    authenticator.logout('logout', 'unrendered', 'home')
    utl.get_current_route()

if nav == 'invullen':
    st.header('')

    default_start = today - timedelta(days=today.weekday())  # Monday
    default_end = default_start + timedelta(days=4)  # Friday
    refresh_value = timedelta(days=7)

    date_range_string = date_range_picker(picker_type=PickerType.week,
                                          start=default_start, end=default_end,
                                          key='week_range_picker',
                                          refresh_button={'is_show': False, 'button_name': 'Refresh Last 1 Week',
                                                          'refresh_value': refresh_value})

    if date_range_string:
        start, end = date_range_string
        week_numbers = extract_weeks(date_range_string)

    with st.form("my_form"):
        # HTML for week selector with arrows
        categories = ["🛌 Heel Rustig", "😐 Rustig", "😎 Goed", "🐝 Druk", "🔥 Heel druk ", "🚫 Afwezig" ]
        
        selected_category = st.radio("Drukte", categories, index=0, key="category_selector", horizontal=False)
        notes = st.text_input(label='notitie',placeholder="Hier is plek voor jouw 🥚..")

        submitted = st.form_submit_button("INVULLEN")
        if submitted:
            selected_category = selected_category[2:]
            print(selected_category)
            update_user_csv(username, week_numbers, selected_category, notes)

            
elif nav == 'overzicht':
    st.write('')
    st.write('')
    st.write('')
    
    tab1, tab2 = st.tabs([":mantelpiece_clock: Deze week", ":calendar: Volgende week"])
    
    # alle namen
    employees_list = ['alexander',
             'boran',
             'eefje',
             'esther',
             'evert',
             'jan-maarten',
             'jasper',
             'jeroen',
             'joost',
             'joostH',
             'kizje',
             'leendert',
             'martijn',
             'olga',
             'olof',
             'philippine',
             'sjon',
             'steven',
             'stijn',
             'taj',
             'wessel']
    
    
    
    import datetime
    with tab1:
        current_week_number = datetime.datetime.now().isocalendar()[1]
        
        current_week_planning, bad_employees = create_week_planning_team(current_week_number, employees_list)
        #print(current_week_planning)
        graph_current_week = create_overview_graph(current_week_planning, current_week_number)
        
        # place graphic on right spot
    
        if not bad_employees:
            st.markdown("### HAPPY WIM 	:heart_eyes:")
            st.plotly_chart(graph_current_week, theme="streamlit", use_container_width=True)
        else:        
            #implementation of shame list
            #TODO: make second column for gifjes of shame
            list_of_emotions = [':pinched_fingers:', ':man-facepalming:', ':pancakes:', ':angry:', '	:pensive:', '	:unamused:', ':broken_heart:', ':thumbsdown:']
            random_emotion = random.choice(list_of_emotions)
            st.markdown("### SHAME list :frog:")
            st.markdown(", ".join([f"{random.choice(list_of_emotions)} {bad_employee.capitalize()}" for bad_employee in bad_employees]))
            
            #plot figure
            st.plotly_chart(graph_current_week, theme="streamlit", use_container_width=True)
        
    with tab2:
        next_week_number = datetime.datetime.now().isocalendar()[1] +1
        next_week_planning, bad_employees = create_week_planning_team(next_week_number, employees_list)
        graph_next_week = create_overview_graph(next_week_planning, next_week_number)
        
        # place graph or next week planning on right spot
    
        if not bad_employees:
            st.markdown("### HAPPY WIM 	:heart_eyes:")
            st.plotly_chart(graph_next_week, theme="streamlit", use_container_width=True)
        else:        
            #implementation of shame list
            list_of_emotions = [':pinched_fingers:', ':man-facepalming:', ':pancakes:', ':angry:', '	:pensive:', '	:unamused:', ':broken_heart:', ':thumbsdown:']
            random_emotion = random.choice(list_of_emotions)
            st.markdown("### SHAME list :frog:")
            st.markdown(", ".join([f"{random.choice(list_of_emotions)} {bad_employee.capitalize()}" for bad_employee in bad_employees]))
            
            #plot figure
            st.plotly_chart(graph_next_week, theme="streamlit", use_container_width=True)

utl.inject_custom_css()

if authentication_status:
    utl.navbar_authenticated(name)
elif authentication_status == False:
    utl.navbar_unauthenticated()
    st.error('Username/password is incorrect')
elif authentication_status == None:
    utl.navbar_unauthenticated()
    st.warning('Please enter your username and password')

