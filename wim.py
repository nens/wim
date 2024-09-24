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
today = datetime.datetime.now()

st.set_page_config(page_title="WIM", page_icon=":water:", layout="centered")

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
        categories = ["Heel Rustig", "Rustig", "Goed", "Druk", "Heel druk", "Afwezig"]
        selected_category = st.radio("Drukte", categories, index=0, key="category_selector", horizontal=False)
        notes = st.text_input(label='notitie',placeholder="Hier is plek voor jouw 🥚..")

        submitted = st.form_submit_button("INVULLEN")
        if submitted:
            update_user_data(username, week_numbers, selected_category, notes)

            
elif nav == 'overzicht':

    
    def streamlit_menu(pages):
        pages_count = len(pages)
        grid_icons = pages_count - 1
        grid_icons_list = ["grid"] * grid_icons
        icons = ["download"] + grid_icons_list

        selected = option_menu(
            menu_title=None,  # required
            options=pages,  # required
            icons= ['clock','calendar'],  # optional
            menu_icon="list-task",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": menu_colors["background"],
                },
                "icon": {"color": menu_colors["text"], "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "center",
                    "margin": "0px",
                    "--hover-color": menu_colors["active_background"],
                    "color": menu_colors["text"],
                },
                "nav-link-selected": {
                    "background-color": menu_colors["active_background"],
                    "color": menu_colors["active_text"],
                },
            },
        )

        return selected
    
    menu_colors = {
        "background": "#ffffff",
        "active_background": "#ffffff",
        "text": "#002b49",
        "active_text": "#002b49",
    }
    st.write('')
    st.write('')
    st.write('')
    st.write(' ')
    
    selected = streamlit_menu(['Deze week', 'Volgende week'])
    
    import datetime
    # op basis van weeknummer wordt bij elke werknemer de juiste rij geselecteerd
    if selected == 'Deze week':
        week_number = datetime.datetime.now().isocalendar()[1]
    elif selected == 'Volgende week':
        week_number = datetime.datetime.now().isocalendar()[1] +1
    
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
    
    df_current_week = pd.DataFrame(columns=['name', 'druk', 'note', 'color'])
    good_employees = []
    bad_employees = []
    for employee in employees_list:
        # get planning of employee
        planning_employee = read_user_data(employee)
        planning_employee_cw = planning_employee.loc[planning_employee['week'] == week_number].reset_index()            
        
        # check if it is filled in
        filled_in = planning_employee_cw['druk'].isin(['Afwezig', 'Heel rustig', 'Rustig', 'Goed', 'Druk', 'Heel druk']).any()
        
            
        if filled_in == True:
            good_employees += [employee]
            if planning_employee_cw['druk'][0] == 'heel rustig':
                color = '#9c27b0' 
            elif planning_employee_cw['druk'][0] == 'rustig':
                color = '#ec407a'
            elif planning_employee_cw['druk'][0] == 'goed':
                color = "#BDDB45"
            elif planning_employee_cw['druk'][0] == 'druk':
                color = '#fb8c00'
            elif planning_employee_cw['druk'][0] == 'te druk':
                color = '#e53935'
            else:
                color = '#81d4fa'
                
            employee_row = {'name': name.capitalize(), 'druk': planning_employee_cw['druk'][0], 'note': planning_employee_cw['note'][0], 'color': color}
            df_current_week.loc[len(df_current_week)] = employee_row
        else:
            bad_employees += [employee]
        
    # Create Horizontal bar chart
    values = ['Afwezig', 'Heel rustig', 'Rustig', 'Goed', 'Druk', 'Heel druk']

    fig = go.Figure([go.Bar(x= list(df_current_week['druk']), y=list(df_current_week['name']), 
                            orientation='h',  # Set orientation to horizontal
                            hoverinfo='text',  # Enable hover text
                            hovertext=list(df_current_week['note']),  # Custom hover text
                            textposition='auto', 
                            marker=dict(color=list(df_current_week['color'])))])  # give bar of every person a specific color based on drukte

    # Customize the layout (optional)
    fig.update_layout(title=f'Work in montoring - weeknummer {week_number}',
                      xaxis=dict(title='', side='top',  # put x-asis on top of plot
                                 tickvals=values,
                                 ticktext=values,))
    fig.update_xaxes(categoryorder='array', categoryarray= values) # zorgt ervoor dat x-axis heeft juiste volgorde



    # place graphic on right spot

    if not bad_employees:
        st.markdown("### HAPPY WIM 	:heart_eyes:")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    else:        
        #implementation of shame list
        list_of_emotions = [':pinched_fingers:', ':man-facepalming:', ':pancakes:', ':angry:', '	:pensive:', '	:unamused:', ':broken_heart:', ':thumbsdown:']
        random_emotion = random.choice(list_of_emotions)
        st.markdown("### SHAME list :frog:")
        st.markdown(", ".join([f"{random.choice(list_of_emotions)} {bad_employee.capitalize()}" for bad_employee in bad_employees]))
        
        #plot figure
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

utl.inject_custom_css()

if authentication_status:
    utl.navbar_authenticated(name)
elif authentication_status == False:
    utl.navbar_unauthenticated()
    st.error('Username/password is incorrect')
elif authentication_status == None:
    utl.navbar_unauthenticated()
    st.warning('Please enter your username and password')

