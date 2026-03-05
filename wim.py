# wim.py
import random
from datetime import datetime, timedelta

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from PIL import Image
from yaml.loader import SafeLoader

import utils2 as utl
from functions import (
    create_overview_columns,
    create_week_planning_team,
    get_week_details,
    update_user_csv,
)

im = Image.open("./images/wim_logo.png")
today = datetime.now()

st.set_page_config(page_title="WIM", page_icon=im, layout="wide")

streamlit_settings = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
button[title="View fullscreen"]{visibility: hidden;}
.css-z5fcl4{padding-top:1px}
.st-emotion-cache-z5fcl4{padding-top:1px}
</style>
"""
st.markdown(streamlit_settings, unsafe_allow_html=True)

# Configuration settings (kept for compatibility with existing codebase)
showWarningOnDirectExecution = False


def read_yaml() -> dict:
    with open("./config.yaml") as file:
        return yaml.load(file, Loader=SafeLoader)


# Retrieve current week and next 3 weeks (4 weeks total)
weeks = [get_week_details(week_offset=i) for i in range(4)]
(current_week_number, current_week_start, current_week_end) = weeks[0]
(next_week_number, next_week_start, next_week_end) = weeks[1]
(week3_number, week3_start, week3_end) = weeks[2]
(week4_number, week4_start, week4_end) = weeks[3]

config = read_yaml()
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
)

name, authentication_status, username = authenticator.login(location="main")

if authentication_status:
    utl.navbar_authenticated(name)
    nav = st.query_params.get("nav")

    if nav == "invullen":
        selected_weeks: list[int] = []

        current_week_selected = st.checkbox(
            label=f"Deze week (Week {current_week_number}: {current_week_start} - {current_week_end})",
            key="week0_checkbox",
        )
        next_week_selected = st.checkbox(
            label=f"Volgende week (Week {next_week_number}: {next_week_start} - {next_week_end})",
            key="week1_checkbox",
        )
        week3_selected = st.checkbox(
            label=f"Over 2 weken (Week {week3_number}: {week3_start} - {week3_end})",
            key="week2_checkbox",
        )
        week4_selected = st.checkbox(
            label=f"Over 3 weken (Week {week4_number}: {week4_start} - {week4_end})",
            key="week3_checkbox",
        )

        if current_week_selected:
            selected_weeks.append(current_week_number)
        if next_week_selected:
            selected_weeks.append(next_week_number)
        if week3_selected:
            selected_weeks.append(week3_number)
        if week4_selected:
            selected_weeks.append(week4_number)

        with st.form("my_form"):
            categories = [
                "😴 Heel Rustig",
                "🥱 Rustig",
                "✅ Goed",
                "⚡ Druk",
                "🚀 Heel druk",
                "🏖️ Afwezig",
            ]

            selected_category = st.radio(
                "Drukte",
                categories,
                index=0,
                key="category_selector",
                horizontal=False,
            )
            notes = st.text_input(label="notitie", placeholder="Hier is plek voor jouw 🥚..")
            submitted = st.form_submit_button("INVULLEN")

        if submitted:
            # Robust: works even when emojis are multiple unicode chars
            selected_category_clean = selected_category.split(" ", 1)[1]
            update_user_csv(username, selected_weeks, selected_category_clean, notes)

            st.write(
                f"{username}, bedankt voor het invullen. Je kunt ook vooruit invullen door meerdere weken aan te vinken."
            )
            st.write("Geniet van je week!")

elif nav == "overzicht":

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            ":mantelpiece_clock: Deze week",
            ":calendar: Volgende week",
            ":calendar: Over 2 weken",
            ":calendar: Over 3 weken",
        ]
    )

    # alle namen
    employees_list = [
        "alexander",
        "boran",
        "christiaan",
        "esther",
        "evert",
        "floor",
        "jasper",
        "jelle",
        "jermo",
        "joostd",
        "joosth",
        "martijn",
        "lex",
        "olof",
        "philippine",
        "sjon",
        "steven",
        "stijn",
        "sven",
        "tosca",
        "zina",
    ]

    def render_week_tab(week_number: int, week_start_date: datetime) -> None:
        week_planning, bad_employees = create_week_planning_team(
            week_number, employees_list
        )

        if not bad_employees:
            st.markdown("### HAPPY WIM :heart_eyes:")
        else:
            list_of_emotions = [
                ":pinched_fingers:",
                ":man-facepalming:",
                ":pancakes:",
                ":angry:",
                ":pensive:",
                ":unamused:",
                ":broken_heart:",
                ":thumbsdown:",
            ]
            st.markdown("### SHAME list :frog:")
            st.markdown(
                ", ".join(
                    [
                        f"{random.choice(list_of_emotions)} {bad_employee.capitalize()}"
                        for bad_employee in bad_employees
                    ]
                )
            )

        create_overview_columns(week_planning)

    # Monday of current week
    default_start = today - timedelta(days=today.weekday())

    with tab1:
        render_week_tab(current_week_number, default_start)

    with tab2:
        render_week_tab(next_week_number, default_start + timedelta(days=7))

    with tab3:
        render_week_tab(week3_number, default_start + timedelta(days=14))

    with tab4:
        render_week_tab(week4_number, default_start + timedelta(days=21))

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
