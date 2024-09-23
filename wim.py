import streamlit as st
import streamlit_authenticator as stauth
from streamlit_date_picker import date_range_picker, date_picker, PickerType
import os
from pathlib import Path
    
import utils2 as utl
import yaml
from yaml.loader import SafeLoader
from datetime import datetime, timedelta
import datetime
import pandas as pd


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

name, authentication_status, username = authenticator.login(location='main')


nav = st.query_params.get('nav')

if nav == 'invullen':
    st.subheader(f'Hi {name}, Hoe druk ben jij?')
    default_start, default_end = datetime.datetime.now() - timedelta(days=7), datetime.datetime.now()
    refresh_value = timedelta(days=7)
    date_range_string = date_range_picker(picker_type=PickerType.week,
                                          start=default_start, end=default_end,
                                          key='week_range_picker',
                                          refresh_button={'is_show': False, 'button_name': 'Refresh Last 1 Week',
                                                          'refresh_value': refresh_value})
    if date_range_string:
        start, end = date_range_string
        st.write(f"wEEK Range Picker [{start}, {end}]")

    with st.form("my_form"):
        # HTML for week selector with arrows
        categories = ["Heel Rustig", "Rustig", "Goed", "Druk", "Heel druk", "Afwezig"]
        selected_category = st.radio("Drukte", categories, index=0, key="category_selector", horizontal=False)
        st.text_input(label='notitie',placeholder="Hier is plek voor jouw 🥚..")
        submitted = st.form_submit_button("INVULLEN")
        if submitted:
            st.write("week", week, "drukte", selected_category)


            
elif nav == 'overzicht':
    # overzichts pagina
    
    # current week number
    current_week_number = datetime.datetime.now().isocalendar()[1]
    
    folder_path = Path('input_employees')
    df_current_week = pd.DataFrame(columns=['name', 'druk', 'note'])
    
    good_employees = []
    bad_employees = []
    # Loop through files in the folder
    for file_path in folder_path.iterdir():
        # Check if it's a file
        if file_path.is_file():
            # get name
            name = file_path.name.split('.')[0]
            
            # get planning of employee
            planning_employee = pd.read_csv(file_path)
            planning_employee_cw = planning_employee.loc[planning_employee['week'] == current_week_number].reset_index()            
            
            # check if it is filled in
            #TODO: select from current onwards
            filled_in = planning_employee_cw['druk'].isin(['afwezog','heel rustig','rustig', 'goed', 'heel goed', 'te druk']).any()
            
            if filled_in == True:
                good_employees += [name]
                employee_row = {'name': name, 'druk': planning_employee_cw['druk'][0], 'note': planning_employee_cw['note'][0]}
                df_current_week.loc[len(df_current_week)] = employee_row
            else:
                bad_employees += [name]

            
            

            
            


    # ga naar input_employee path
    # get all files


    # select name of file == person name

    
    # if yes: voeg toe naar categories
    # if not: shame list







    import plotly.graph_objects as go

    # Data for the bar chart

    #TODO: deze vullen met lijst van files die zijn ingevuld 
    categories = ['Eefje', 'Sjon', 'Kizje', 'Evert', 'Martijn']




    values = ['afwezig', 'heel rustig', 'rustig', 'goed', 'heel goed', 'te druk']



    fig = go.Figure([go.Bar(x= list(df_current_week['druk']), y=list(df_current_week['name']), 
                            orientation='h',  # Set orientation to horizontal
                            hoverinfo='text',  # Enable hover text
                            hovertext=list(df_current_week['note']),  # Custom hover text
                            #text=values,  # Display values on bars
                            textposition='auto')])  # Position text on bars

    # Customize the layout (optional)
    fig.update_layout(title='Work in montoring',
                      xaxis=dict(title='', side='top', 
                                 tickvals=values,
                                 ticktext=values,))
                      #xaxis_title='Value',
                      #yaxis_title='Category')


    # place graphic on right spot
    st.write('')
    st.write('')
    st.write('')
    if not bad_employees:
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    else:
        st.write('SHAMEEEEE -  mensen die niks hebben ingevuld')
        st.write(bad_employees)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)


name, authentication_status, username = authenticator.login(location='main')

utl.navbar_unauthenticated()
utl.inject_custom_css()


if authentication_status:
    utl.navbar_authenticated(name)
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

