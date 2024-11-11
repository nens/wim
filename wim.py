from datetime import datetime, timedelta
import random
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from PIL import Image
from streamlit_date_picker import PickerType, date_range_picker
from yaml.loader import SafeLoader
import utils2 as utl
from functions import (
    create_overview_graph,
    create_week_planning_team,
    extract_weeks,
    update_user_csv,
)
from time import time

im = Image.open("./images/wim_logo.png")


today = datetime.now()

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
showWarningOnDirectExecution = False

st.cache_resource(show_spinner=False)
def read_yaml():
    with open('./config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config


config = read_yaml()
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"]
)

name, authentication_status, username = authenticator.login(location="main")

if authentication_status:
    utl.navbar_authenticated(name)
    nav = (st.query_params.get("nav"))
    if nav == "invullen":
        st.header("")
        default_start = today -timedelta(days=today.weekday())  # Monday
        default_end = default_start - timedelta(days=4)  # Friday
        refresh_value = timedelta(days=7)
        date_range_string = date_range_picker(
            picker_type=PickerType.week,
            start=default_start,
            end=default_end,
            key="week_range_picker",
            # refresh_button={
            #     "is_show": False,
            #     "button_name": "Refresh Last 1 Week",
            #     "refresh_value": refresh_value,
            # },
        )
        if date_range_string:
            start, end = date_range_string
            week_numbers = extract_weeks(date_range_string)

        with st.form("my_form"):
            # HTML for week selector with arrows
            categories = [
                "🛌 Heel Rustig",
                "😐 Rustig",
                "😎 Goed",
                "🐝 Druk",
                "🔥 Heel druk",
                "🚫 Afwezig",
            ]

            selected_category = st.radio(
                "Drukte", categories, index=0, key="category_selector", horizontal=False
            )
            notes = st.text_input(
                label="notitie", placeholder="Hier is plek voor jouw 🥚.."
            )
            submitted = st.form_submit_button("INVULLEN")
        if submitted:
            selected_category = selected_category[2:]
            update_user_csv(username, week_numbers, selected_category, notes)
            st.write(
                f'{username}, Bedankt voor het invullen, door de datum aan te passen kan je ook voor volgende week alvast je verwachte drukte invullen.')
            st.write('Geniet van je week!')

    elif nav == "overzicht":
        st.write("")
        st.write("")
        st.write("")

        tab1, tab2 = st.tabs([":mantelpiece_clock: Deze week", ":calendar: Volgende week"])

        # alle namen
        employees_list = [
            "alexander",
            "boran",
            "eefje",
            "esther",
            "evert",
            "jan-maarten",
            "jasper",
            "jeroen",
            "joostD",
            "joostH",
            "kizje",
            "leendert",
            "martijn",
            "mats",
            "olga",
            "olof",
            "philippine",
            "sjon",
            "steven",
            "stijn",
            "sven",
            "taj",
            "wessel",
        ]

        with tab1:
            current_week_number = datetime.now().isocalendar()[1]

            current_week_planning, bad_employees = create_week_planning_team(
                current_week_number, employees_list
            )
            # print(current_week_planning)
            graph_current_week = create_overview_graph(
                current_week_planning, current_week_number
            )

            # place graphic on right spot

            if not bad_employees:
                st.markdown("### HAPPY WIM 	:heart_eyes:")
                st.plotly_chart(
                    graph_current_week, theme="streamlit", use_container_width=True
                )
            else:
                # implementation of shame list
                # TODO: make second column for gifjes of shame
                list_of_emotions = [
                    ":pinched_fingers:",
                    ":man-facepalming:",
                    ":pancakes:",
                    ":angry:",
                    "	:pensive:",
                    "	:unamused:",
                    ":broken_heart:",
                    ":thumbsdown:",
                ]
                random_emotion = random.choice(list_of_emotions)
                st.markdown("### SHAME list :frog:")
                st.markdown(
                    ", ".join(
                        [
                            f"{random.choice(list_of_emotions)} {bad_employee.capitalize()}"
                            for bad_employee in bad_employees
                        ]
                    )
                )

                # plot figure
                st.plotly_chart(
                    graph_current_week, theme="streamlit", use_container_width=True
                )

        with tab2:
            next_week_number = datetime.now().isocalendar()[1] + 1
            next_week_planning, bad_employees = create_week_planning_team(
                next_week_number, employees_list
            )
            graph_next_week = create_overview_graph(next_week_planning, next_week_number)

            # place graph or next week planning on right spot

            if not bad_employees:
                st.markdown("### HAPPY WIM 	:heart_eyes:")
                st.plotly_chart(
                    graph_next_week, theme="streamlit", use_container_width=True
                )
            else:
                # implementation of shame list
                list_of_emotions = [
                    ":pinched_fingers:",
                    ":man-facepalming:",
                    ":pancakes:",
                    ":angry:",
                    "	:pensive:",
                    "	:unamused:",
                    ":broken_heart:",
                    ":thumbsdown:",
                ]
                random_emotion = random.choice(list_of_emotions)
                st.markdown("### SHAME list :frog:")
                st.markdown(
                    ", ".join(
                        [
                            f"{random.choice(list_of_emotions)} {bad_employee.capitalize()}"
                            for bad_employee in bad_employees
                        ]
                    )
                )

                # plot figure
                st.plotly_chart(
                    graph_next_week, theme="streamlit", use_container_width=True
                )

    elif nav == "uitloggen":
        authenticator.logout("logout", "unrendered", "home")
        utl.get_current_route()
elif authentication_status is False:
    utl.navbar_unauthenticated()
    st.error("Username/password is incorrect")
elif authentication_status is None:
    utl.navbar_unauthenticated()
    st.warning("Please enter your username and password")


utl.inject_custom_css()

