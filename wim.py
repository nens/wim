import streamlit as st
import streamlit as st
import streamlit_authenticator as stauth
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

