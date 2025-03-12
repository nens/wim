import random
from datetime import datetime, timedelta

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from PIL import Image
from yaml.loader import SafeLoader

# from streamlit_date_picker import PickerType, date_range_picker
import utils2 as utl
from functions import (
    create_overview_graph,
    create_week_planning_team,
    get_week_details,
    update_user_csv,
)

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
    with open("./config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config


# Retrieve current and next week details
current_week_number, current_week_start, current_week_end = get_week_details()
next_week_number, next_week_start, next_week_end = get_week_details(week_offset=1)

config = read_yaml()
authenticator = stauth.Authenticate(
    config["credentials"], config["cookie"]["name"], config["cookie"]["key"]
)

name, authentication_status, username = authenticator.login(location="main")
# authentication_status = True
# name = 'kizje'
# username = "kizje"
if authentication_status:
    utl.navbar_authenticated(name)
    nav = st.query_params.get("nav")
    if nav == "invullen":
        # qoutes
        #     qoute_random = random.choice(list_bad_qoutes)
        #    qoute, auteur = qoute_random.split("–")
        #   placeholder = st.empty()
        #  placeholder1 = st.empty()
        # Loop through each letter in the text
        # for i in range(len(qoute) + 1):
        #      placeholder.header(qoute[:i])  # Update the container with the current substring
        #     time.sleep(0.03)
        # st.header(qoute)
        # for i in range(len(auteur) + 1):
        #   placeholder1.text(auteur[:i])  # Update the container with the current substring
        #  time.sleep(0.03)
        selected_weeks = []
        current_week_selected = st.checkbox(
            label=f"Deze week (Week {current_week_number}: {current_week_start} - {current_week_end})",
            key="current_week_checkbox",
        )
        next_week_selected = st.checkbox(
            label=f"Volgende week (Week {next_week_number}: {next_week_start} - {next_week_end})",
            key="next_week_checkbox",
        )

        # Add weeks to the list based on checkbox state
        if current_week_selected:
            selected_weeks.append(current_week_number)
        if next_week_selected:
            selected_weeks.append(next_week_number)
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
            update_user_csv(username, selected_weeks, selected_category, notes)
            st.write(
                f"{username}, Bedankt voor het invullen, door de datum aan te passen kan je ook voor volgende week alvast je verwachte drukte invullen."
            )
            st.write("Geniet van je week!")
        st.write("")
        st.write("")
        st.markdown("" "" "" "" "" "")
        st.markdown("")
        st.markdown("")
        st.markdown("")

    elif nav == "overzicht":
        st.write("")
        st.write("")
        st.write("")

        tab1, tab2 = st.tabs(
            [":mantelpiece_clock: Deze week", ":calendar: Volgende week"]
        )

        # alle namen
        employees_list = [
            "alexander",
            "boran",
            'christiaan'
            "eefje",
            "esther",
            "evert",
            "jasper",
            "jeroen",
            "joostd",
            "joosth",
            "kizje",
            "martijn",
            "lex",
            "olof",
            "philippine",
            "sjon",
            "steven",
            "stijn",
            "sven",
            "taj",
            "wessel",
            "zina",
        ]

        with tab1:
            current_week_number = datetime.now().isocalendar()[1]

            current_week_planning, bad_employees = create_week_planning_team(
                current_week_number, employees_list
            )
            # print(current_week_planning)
            default_start = today - timedelta(days=today.weekday())
            graph_current_week = create_overview_graph(
                current_week_planning, current_week_number, default_start
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
            start_day_next_week = default_start + timedelta(days=7)
            next_week_planning, bad_employees = create_week_planning_team(
                next_week_number, employees_list
            )
            graph_next_week = create_overview_graph(
                next_week_planning, next_week_number, start_day_next_week
            )

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
