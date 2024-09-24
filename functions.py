import re
import os
import pandas as pd
import pickle

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

        if week in df['week'].values:

            # Update existing week entry

            df.loc[df['week'] == week, 'druk'] = selected_category

            df.loc[df['week'] == week, 'note'] = notes



        else:

            # Append new week entry

            df = df.append({"week": week, "druk": selected_category, "note": notes}, ignore_index=True)



    # Save the updated DataFrame back to the CSV file

    df.to_csv(csv_file, index=False)



def update_user_data(username, week_numbers, selected_category, notes):

    # Define the file path based on the username

    pickle_file = f"./input_employees/{username}.pkl"



    # Initialize user data

    user_data = {'weeks': {}}



    # Check if the file exists; if so, try to load the existing data

    if os.path.exists(pickle_file):

        try:

            with open(pickle_file, 'rb') as f:

                user_data = pickle.load(f)

        except EOFError:

            # Handle the case where the file is empty or corrupted

            print("Warning: The pickle file is empty or corrupted. Starting with an empty structure.")



    # Iterate through each week number

    for week in week_numbers:

        # Update or overwrite the entry for the specific week

        user_data['weeks'][week] = {

            "druk": selected_category,

            "note": notes

        }



    # Save the updated user data back to the pickle file

    with open(pickle_file, 'wb') as f:

        pickle.dump(user_data, f)





def extract_weeks(date_range):

    week_numbers = []



    # Extract the start and end weeks

    for value in date_range:

        match = re.search(r'-(\d+)', value)

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

    pickle_file = f"./input_employees/{username}.pkl"



    # Check if the file exists

    if os.path.exists(pickle_file):

        with open(pickle_file, 'rb') as f:

            user_data = pickle.load(f)



        # Convert the stored weeks data into a DataFrame

        if 'weeks' in user_data:

            df = pd.DataFrame.from_dict(user_data['weeks'], orient='index').reset_index()

            df.columns = ['week', 'druk', 'note']  # Rename columns

            return df

        else:

            return pd.DataFrame(columns=['week', 'druk', 'note'])  # Return empty DataFrame if no weeks data



    else:

        print("No data found for this user.")

        return pd.DataFrame(columns=['week', 'druk', 'note'])  # Return empty DataFrame if file doesn't exist


