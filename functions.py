import os
import pickle
import re
import glob
import streamlit as st
from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objects as go

# import streamlit as st

def clear_employee_data(folder_path="./input_employees"):
    files_to_delete = glob.glob(os.path.join(folder_path, "*.csv")) + glob.glob(
        os.path.join(folder_path, "*.pkl")
    )

    if not files_to_delete:
        st.success("Geen bestanden gevonden om te verwijderen.")
        return

    for file in files_to_delete:
        os.remove(file)

    st.success(f"Alle employee data ({len(files_to_delete)} bestanden) is verwijderd!")

def update_user_csv(username, week_numbers, selected_category, notes):
    # Define the file path based on the username

    csv_file = f"./input_employees/{username}.csv"

    # Check if the file exists, if not create an empty one with the correct structure

    if not os.path.exists(csv_file):
        df = pd.DataFrame(columns=["week", "druk", "note"])

    else:
        # Load existing CSV data

        df = pd.read_csv(csv_file)

    # Iterate through each week number and update druk (busy level)

    for week in week_numbers:
        if week in df["week"].values:
            # Update existing week entry

            df.loc[df["week"] == week, "druk"] = selected_category

            df.loc[df["week"] == week, "note"] = notes

        else:
            # Append new week entry
            new_row = {
                "week": week,
                "druk": selected_category,
                "note": notes,
            }  # Example row
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    df.to_csv(csv_file, index=False)


def update_user_data(username, week_numbers, selected_category, notes):
    # Define the file path based on the username

    pickle_file = f"./input_employees/{username}.pkl"

    # Initialize user data

    user_data = {"weeks": {}}

    # Check if the file exists; if so, try to load the existing data

    if os.path.exists(pickle_file):
        try:
            with open(pickle_file, "rb") as f:
                user_data = pickle.load(f)

        except EOFError:
            # Handle the case where the file is empty or corrupted

            print(
                "Warning: The pickle file is empty or corrupted. Starting with an empty structure."
            )

    # Iterate through each week number

    for week in week_numbers:
        # Update or overwrite the entry for the specific week

        user_data["weeks"][week] = {"druk": selected_category, "note": notes}

    # Save the updated user data back to the pickle file

    with open(pickle_file, "wb") as f:
        pickle.dump(user_data, f)


def extract_weeks(date_range):
    week_numbers = []

    # Extract the start and end weeks

    for value in date_range:
        match = re.search(r"-(\d+)", value)

        if match:
            week = int(match.group(1))

            week_numbers.append(week)

    # If we have both start and end weeks, generate the range

    if len(week_numbers) == 2:
        start_week, end_week = sorted(week_numbers)

        return list(range(start_week, end_week + 1))

    return week_numbers  # Return only found weeks if less than 2


def read_user_data(username):
    # Define the file path based on the username

    csv_file = f"./input_employees/{username}.csv"

    # Check if the file exists

    if os.path.exists(csv_file):
        user_data = pd.read_csv(csv_file)

        return user_data

    else:
        print(f"No data found for {username}")

        return pd.DataFrame(
            columns=["week", "druk", "note"]
        )  # Return empty DataFrame if file doesn't exist


# checks all employees files based on list of employees and creates for selected week overview of work pressure of each employee
# if employee didn't fill form for selected week, it will be listed as bad_employee and shamed in dashboard
# @st.cache_data(
#     ttl=300, show_spinner="Je zorgen maken is de verkeerde kant op fantaseren"
# )
def create_week_planning_team(week_number, employees_list):
    # print(employees_list)
    df_current_week = pd.DataFrame(columns=["name", "druk", "note", "color"])
    good_employees = []
    bad_employees = []
    for employee in employees_list:
        # get planning of employee
        planning_employee = read_user_data(employee)
        planning_employee_cw = planning_employee.loc[
            planning_employee["week"] == week_number
        ].reset_index()

        # check if it is filled in
        filled_in = (
            planning_employee_cw["druk"]
            .isin(["Afwezig", "Heel Rustig", "Rustig", "Goed", "Druk", "Heel druk"])
            .any()
        )

        if filled_in:
            good_employees += [employee]
            if planning_employee_cw["druk"][0] == "Heel Rustig":
                color = "#9c27b0"
            elif planning_employee_cw["druk"][0] == "Rustig":
                color = "#ec407a"
            elif planning_employee_cw["druk"][0] == "Goed":
                color = "#BDDB45"
            elif planning_employee_cw["druk"][0] == "Druk":
                color = "#fb8c00"
            elif planning_employee_cw["druk"][0] == "Heel druk":
                color = "#e53935"
            else:
                color = "#81d4fa"

            employee_row = {
                "name": employee.capitalize(),
                "druk": planning_employee_cw["druk"][0],
                "note": planning_employee_cw["note"][0],
                "color": color,
            }
            df_current_week.loc[len(df_current_week)] = employee_row
        else:
            bad_employees += [employee]

    return df_current_week, bad_employees


# makes plotly bar chart of employees work planning overview for selected week
def create_overview_graph(df__week, week_number, startday_week):
    # Create Horizontal bar chart
    values = ["Afwezig", "Heel Rustig", "Rustig", "Goed", "Druk", "Heel druk"]

    fig = go.Figure(
        [
            go.Bar(
                x=list(df__week["druk"]),
                y=list(df__week["name"]),
                orientation="h",  # Set orientation to horizontal
                hoverinfo="text",  # Enable hover text
                hovertext=list(df__week["note"]),  # Custom hover text
                textposition="auto",
                marker=dict(color=list(df__week["color"])),
            )
        ]
    )  # give bar of every person a specific color based on drukte

    # Customize the layout (optional)
    endday_week = startday_week + timedelta(days=5)
    endday_week = endday_week.strftime("%d-%m-%Y")
    startday_week = startday_week.strftime("%d-%m-%Y")
    fig.update_layout(
        title=f"Work in Monitoring - weeknummer {week_number} - from {startday_week} until {endday_week}",
        xaxis=dict(
            title="",
            side="top",  # put x-asis on top of plot
            tickvals=values,
            ticktext=values,
        ),
    )
    fig.update_xaxes(
        categoryorder="array", categoryarray=values
    )  # zorgt ervoor dat x-axis heeft juiste volgorde
    return fig


def get_week_details(week_offset=0):
    """Returns the ISO week number, start date, and end date with an optional offset."""
    today = datetime.now()
    start_of_week = (
        today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    )
    end_of_week = start_of_week + timedelta(days=4)
    week_number = start_of_week.isocalendar().week
    return week_number, start_of_week.date(), end_of_week.date()
