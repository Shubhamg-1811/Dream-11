import sys
import os
sys.path.append(os.path.abspath('../'))
from data_processing.ODI_MatchWise import ODI_MatchWise
from data_processing.fantasy_points_odi import add_fantasy_points as add_fantasy_points_odi
from data_processing.ODI import venue_ODI,recent_ODI,career_ODI
from data_processing.T20_MatchWise import T20_MatchWise
from data_processing.fantasy_points_t20 import add_fantasy_points as add_fantasy_points_t20 
from data_processing.T20 import venue_T20,recent_T20,career_T20
from data_processing.Test_MatchWise import Test_MatchWise
from data_processing.fantasy_points_test import add_fantasy_points as add_fantasy_points_test
from data_processing.Test import venue_Test,recent_Test,career_Test
from data_processing.player_match_data_odi import process_player_match_data as process_player_match_data_odi
from data_processing.player_match_data_t20 import process_player_match_data as process_player_match_data_t20
from data_processing.player_match_data_test import process_player_match_data as process_player_match_data_test


import pandas as pd
import numpy as np
from sklearn.linear_model import HuberRegressor
from sklearn.preprocessing import StandardScaler

import pickle

career_dict = {
    "match_id": "string",  # Match ID is usually a string type, as it may contain letters or special characters.
    "player_id": "string",  # Player ID could be an alphanumeric string or a number stored as a string.
    "career_batsman_total_runs_odi": "int",  # Career total runs would be numeric.
    "career_batsman_100s_odi": "int",  # Career 100s, numeric.
    "career_batsman_50s_odi": "int",  # Career 50s, numeric.
    "career_batsman_total_sixes_odi": "int",  # Career sixes, numeric.
    "career_batsman_total_fours_odi": "int",  # Career fours, numeric.
    "career_batsman_average_runs_odi": "float64",  # Career batting average, numeric.
    "career_batsman_strike_rate_odi": "float64",  # Career strike rate, numeric.
    "career_bowler_wickets_odi": "int",  # Career wickets, numeric.
    "career_bowler_average_odi": "float64",  # Career bowler average, numeric.
    "career_bowler_economy_rate_odi": "float64",  # Economy rate, numeric.
    "career_fielder_total_catches_odi": "int",  # Career catches, numeric.
    "career_fielder_total_runouts_odi": "int"  # Career runouts, numeric.
}

recent_dict = {
    "match_id": "string",  # Match ID is usually a string type, as it may contain letters or special characters.
    "player_id": "string",  # Player ID could be an alphanumeric string or a number stored as a string.
    "recent_batsman_total_runs_odi": "int",  # Recent total runs would be numeric.
    "recent_batsman_100s_odi": "int",  # Recent 100s, numeric.
    "recent_batsman_50s_odi": "int",  # Recent 50s, numeric.
    "recent_batsman_total_sixes_odi": "int",  # Recent sixes, numeric.
    "recent_batsman_total_fours_odi": "int",  # Recent fours, numeric.
    "recent_batsman_average_runs_odi": "float64",  # Recent batting average, numeric.
    "recent_batsman_strike_rate_odi": "float64",  # Recent strike rate, numeric.
    "recent_bowler_wickets_odi": "int",  # Recent wickets, numeric.
    "recent_bowler_average_odi": "float64",  # Recent bowler average, numeric.
    "recent_bowler_economy_rate_odi": "float64",  # Economy rate, numeric.
    "recent_fielder_total_catches_odi": "int",  # Recent catches, numeric.
    "recent_fielder_total_runouts_odi": "int"  # Recent runouts, numeric.
}

venue_dict = {
    "match_id": "string",  # Match ID is usually a string type, as it may contain letters or special characters.
    "player_id": "string",  # Player ID could be an alphanumeric string or a number stored as a string.
    "venue_batsman_total_runs_odi": "int",  # Venue total runs would be numeric.
    "venue_batsman_100s_odi": "int",  # Venue 100s, numeric.
    "venue_batsman_50s_odi": "int",  # Venue 50s, numeric.
    "venue_batsman_total_sixes_odi": "int",  # Venue sixes, numeric.
    "venue_batsman_total_fours_odi": "int",  # Venue fours, numeric.
    "venue_batsman_average_runs_odi": "float64",  # Venue batting average, numeric.
    "venue_batsman_strike_rate_odi": "float64",  # Venue strike rate, numeric.
    "venue_bowler_wickets_odi": "int",  # Venue wickets, numeric.
    "venue_bowler_average_odi": "float64",  # Venue bowler average, numeric.
    "venue_bowler_economy_rate_odi": "float64",  # Economy rate, numeric.
    "venue_fielder_total_catches_odi": "int",  # Venue catches, numeric.
    "venue_fielder_total_runouts_odi": "int"  # Venue runouts, numeric.
}

player_dict = {
    "match_id": "string",         # Match ID is usually alphanumeric, so it should be a string.
    "player_id": "string",        # Player ID can be alphanumeric, stored as a string.
    "player_name": "string",      # Player name is a string, which can contain spaces and special characters.
    "fantasy_points": "float64",  # Fantasy points are numeric values, represented as float.
    "team_name": "string",        # Team name is a string, as it can contain letters, numbers, and spaces.
    "role": "string",             # Player role is usually a categorical string (e.g., "Batsman", "Bowler").     
    "venue": "string"             # Venue is a string, usually the name of the stadium or city.
}



# start_date_training = "2000-01-01"
# end_date_training = "2024-06-30"
# start_date_testing= "2024-07-01"
# end_date_testing="2024-11-10"

DESIGNATION_PATH = os.path.join(os.path.dirname(__file__), '../data_ui2/interim/Designation.csv')


def generate_odi_data_training(start_date,end_date,end_train_date):

    json_dir = os.path.join(os.path.dirname(__file__), f'../data_ui2/raw/cricksheet_data'  )
    output_csv = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/ODI_MatchWise_{end_train_date}.csv' )
    ODI_MatchWise(json_dir,output_csv,start_date,end_date)

    input_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/ODI_MatchWise_{end_train_date}.csv')
    output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/ODI_MatchWise_fantasy_points_{end_train_date}.csv')
    add_fantasy_points_odi(input_file, output_file)

    input_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/ODI_MatchWise_fantasy_points_{end_train_date}.csv')
    output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/ODI/career_odi_{end_train_date}.csv')
    career_ODI(input_file, output_file)

    input_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/ODI_MatchWise_fantasy_points_{end_train_date}.csv')
    output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/ODI/recent_odi_{end_train_date}.csv')
    recent_ODI(input_file, output_file)

    input_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/ODI_MatchWise_fantasy_points_{end_train_date}.csv')
    output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/ODI/venue_odi_{end_train_date}.csv')
    venue_ODI(input_file, output_file)

    input_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/ODI_MatchWise_fantasy_points_{end_train_date}.csv')
    output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/ODI/player_match_data_odi_{end_train_date}.csv')
    process_player_match_data_odi(DESIGNATION_PATH,input_file, output_file)



def generate_t20_data_training(start_date,end_date,end_train_date):

    json_dir = os.path.join(os.path.dirname(__file__), f'../data_ui2/raw/cricksheet_data'  )
    output_csv = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/T20_MatchWise_{end_train_date}.csv' )
    T20_MatchWise(json_dir,output_csv,start_date,end_date)

    input_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/T20_MatchWise_{end_train_date}.csv')
    output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/T20_MatchWise_fantasy_points_{end_train_date}.csv')
    add_fantasy_points_t20(input_file, output_file)

    input_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/T20_MatchWise_fantasy_points_{end_train_date}.csv')
    output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/T20/career_t20_{end_train_date}.csv')
    career_T20(input_file, output_file)

    input_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/T20_MatchWise_fantasy_points_{end_train_date}.csv')
    output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/T20/recent_t20_{end_train_date}.csv')
    recent_T20(input_file, output_file)

    input_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/T20_MatchWise_fantasy_points_{end_train_date}.csv')
    output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/T20/venue_t20_{end_train_date}.csv')
    venue_T20(input_file, output_file)

    input_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/T20_MatchWise_fantasy_points_{end_train_date}.csv')
    output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/T20/player_match_data_t20_{end_train_date}.csv')
    process_player_match_data_t20(DESIGNATION_PATH,input_file, output_file)



def generate_test_data_training(start_date,end_date,end_train_date):

    json_dir = os.path.join(os.path.dirname(__file__), f'../data_ui2/raw/cricksheet_data'  )
    output_csv = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/Test_MatchWise_{end_train_date}.csv' )
    Test_MatchWise(json_dir,output_csv,start_date,end_date)

    input_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/Test_MatchWise_{end_train_date}.csv')
    output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/Test_MatchWise_fantasy_points_{end_train_date}.csv')
    add_fantasy_points_test(input_file, output_file)

    input_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/Test_MatchWise_fantasy_points_{end_train_date}.csv')
    output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/Test/career_test_{end_train_date}.csv')
    career_Test(input_file, output_file)

    input_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/Test_MatchWise_fantasy_points_{end_train_date}.csv')
    output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/Test/recent_test_{end_train_date}.csv')
    recent_Test(input_file, output_file)

    input_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/Test_MatchWise_fantasy_points_{end_train_date}.csv')
    output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/Test/venue_test_{end_train_date}.csv')
    venue_Test(input_file, output_file)

    input_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/interim/Test_MatchWise_fantasy_points_{end_train_date}.csv')
    output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/Test/player_match_data_test_{end_train_date}.csv')
    process_player_match_data_test(DESIGNATION_PATH,input_file, output_file)


def generate_odi_data_testing(start_date,end_date,end_train_date):

    file1_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/ODI/career_odi_{end_train_date}.csv')
    file2_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/ODI/recent_odi_{end_train_date}.csv')
    file3_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/ODI/venue_odi_{end_train_date}.csv')
    file4_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/ODI/player_match_data_odi_{end_train_date}.csv')

    # Load data
    df1 = pd.read_csv(file1_path, dtype=career_dict)
    df2 = pd.read_csv(file2_path, dtype=recent_dict)
    df3 = pd.read_csv(file3_path, dtype=venue_dict)
    df4 = pd.read_csv(file4_path, dtype=player_dict, parse_dates=["date"])

    # Merge datasets
    merged_df = pd.merge(df1, df2, on=['match_id', 'player_id'], how='inner')
    merged_df = pd.merge(merged_df, df3, on=['match_id', 'player_id'], how='inner')
    merged_df = pd.merge(merged_df, df4, on=['match_id', 'player_id'], how='inner')

    # Process data
    merged_df['date'] = pd.to_datetime(merged_df['date'])

    # Split the DataFrame based on the condition (date <= June 30, 2024)
    split_date = pd.to_datetime(start_date)

    merged_df_before_start_date = merged_df[merged_df['date'] <= split_date]
    merged_df_after_start_date = merged_df[merged_df['date'] > split_date]

    output_file= output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/test_data/processed/ODI/merged_odi_{end_date}.csv')
    merged_df_after_start_date.to_csv(output_file, index=False)
    




def generate_t20_data_testing(start_date,end_date,end_train_date):

    # Paths
    file1_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/T20/career_t20_{end_train_date}.csv')
    file2_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/T20/recent_t20_{end_train_date}.csv')
    file3_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/T20/venue_t20_{end_train_date}.csv')
    file4_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/T20/player_match_data_t20_{end_train_date}.csv')


    # Load data
    df1 = pd.read_csv(file1_path, dtype=career_dict)
    df2 = pd.read_csv(file2_path, dtype=recent_dict)
    df3 = pd.read_csv(file3_path, dtype=venue_dict)
    df4 = pd.read_csv(file4_path, dtype=player_dict, parse_dates=["date"])

    # Merge datasets
    merged_df = pd.merge(df1, df2, on=['match_id', 'player_id'], how='inner')
    merged_df = pd.merge(merged_df, df3, on=['match_id', 'player_id'], how='inner')
    merged_df = pd.merge(merged_df, df4, on=['match_id', 'player_id'], how='inner')

    # Process data
    merged_df['date'] = pd.to_datetime(merged_df['date'])

    # Split the DataFrame based on the condition (date <= June 30, 2024)
    split_date = pd.to_datetime(start_date)

    merged_df_before_start_date = merged_df[merged_df['date'] <= split_date]
    merged_df_after_start_date = merged_df[merged_df['date'] > split_date]

    output_file= output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/test_data/processed/T20/merged_t20_{end_date}.csv')
    merged_df_after_start_date.to_csv(output_file, index=False)



def generate_test_data_testing(start_date,end_date,end_train_date):

    # Paths
    file1_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/Test/career_test_{end_train_date}.csv')
    file2_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/Test/recent_test_{end_train_date}.csv')
    file3_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/Test/venue_test_{end_train_date}.csv')
    file4_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/Test/player_match_data_test_{end_train_date}.csv')

    # Load data
    df1 = pd.read_csv(file1_path, dtype=career_dict)
    df2 = pd.read_csv(file2_path, dtype=recent_dict)
    df3 = pd.read_csv(file3_path, dtype=venue_dict)
    df4 = pd.read_csv(file4_path, dtype=player_dict, parse_dates=["date"])

    # Merge datasets
    merged_df = pd.merge(df1, df2, on=['match_id', 'player_id'], how='inner')
    merged_df = pd.merge(merged_df, df3, on=['match_id', 'player_id'], how='inner')
    merged_df = pd.merge(merged_df, df4, on=['match_id', 'player_id'], how='inner')

    # Process data
    merged_df['date'] = pd.to_datetime(merged_df['date'])

    
    split_date = pd.to_datetime(start_date)

    merged_df_before_start_date = merged_df[merged_df['date'] <= split_date]
    merged_df_after_start_date = merged_df[merged_df['date'] > split_date]

    output_file= output_file = os.path.join(os.path.dirname(__file__), f'../data_ui2/test_data/processed/Test/merged_test_{end_date}.csv')
    merged_df_after_start_date.to_csv(output_file, index=False)


def generate_training_data_for_retraining(start_date,end_date,end_train_date):

    generate_odi_data_training(start_date,end_date,end_train_date)
    generate_t20_data_training(start_date,end_date,end_train_date)
    generate_test_data_training(start_date,end_date,end_train_date)
    
def generate_testing_data_for_retraining(start_date,end_date,end_train_date):

    generate_odi_data_testing(start_date,end_date,end_train_date)
    generate_t20_data_testing(start_date,end_date,end_train_date)
    generate_test_data_testing(start_date,end_date,end_train_date)



def train_model_odi(start_date, end_date):
    import os
    import pandas as pd
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import HuberRegressor
    import pickle

    try:
        print("Starting training process...")

        # Paths
        file1_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/ODI/career_odi_{end_date}.csv')
        file2_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/ODI/recent_odi_{end_date}.csv')
        file3_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/ODI/venue_odi_{end_date}.csv')
        file4_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/ODI/player_match_data_odi_{end_date}.csv')

        print(f"File paths:\n  {file1_path}\n  {file2_path}\n  {file3_path}\n  {file4_path}")

        # Load data
        print("Loading data...")
        df1 = pd.read_csv(file1_path, dtype=career_dict)
        print(f"Loaded career data: {df1.shape}")

        df2 = pd.read_csv(file2_path, dtype=recent_dict)
        print(f"Loaded recent data: {df2.shape}")

        df3 = pd.read_csv(file3_path, dtype=venue_dict)
        print(f"Loaded venue data: {df3.shape}")

        df4 = pd.read_csv(file4_path, dtype=player_dict, parse_dates=["date"])
        print(f"Loaded player match data: {df4.shape}")

        # Merge datasets
        print("Merging datasets...")
        merged_df = pd.merge(df1, df2, on=['match_id', 'player_id'], how='inner')
        print(f"After merging df1 and df2: {merged_df.shape}")

        merged_df = pd.merge(merged_df, df3, on=['match_id', 'player_id'], how='inner')
        print(f"After merging df3: {merged_df.shape}")

        merged_df = pd.merge(merged_df, df4, on=['match_id', 'player_id'], how='inner')
        print(f"After merging df4: {merged_df.shape}")

        # Process data
        print("Processing data...")
        merged_df['date'] = pd.to_datetime(merged_df['date'])
        print(f"Converted 'date' column to datetime.")

        # Split the DataFrame based on the condition (date <= end_date)
        split_date = pd.to_datetime(end_date)
        merged_df_before_end_date = merged_df[merged_df['date'] <= split_date]
        merged_df_after_end_date = merged_df[merged_df['date'] > split_date]
        print(f"Split data: Before end date: {merged_df_before_end_date.shape}, After end date: {merged_df_after_end_date.shape}")

        columns_to_drop = ['match_id', 'player_id', 'player_name', 'fantasy_points', 'team_name', 'role', 'date', 'venue']
        X_train = merged_df_before_end_date.drop(columns=columns_to_drop)
        y_train = merged_df_before_end_date['fantasy_points']
        print(f"Prepared training data: X_train: {X_train.shape}, y_train: {y_train.shape}")

        # Scale the features
        print("Scaling features...")
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        print("Scaling complete.")

        # Train the model
        print("Training the model...")
        model = HuberRegressor(max_iter=500)
        model.fit(X_train_scaled, y_train)
        print("Model training complete.")

        filename = os.path.join(os.path.dirname(__file__), f"../model_artifacts_ui2/ODI/model_ODI_{end_date}.pkl")
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'wb') as f:
            pickle.dump(model, f)
        print(f"Model saved successfully at {filename}.")

    except Exception as e:
        print(f"An error occurred: {e}")





def train_model_t20(start_date, end_date):
    # Paths
    file1_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/T20/career_t20_{end_date}.csv')
    file2_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/T20/recent_t20_{end_date}.csv')
    file3_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/T20/venue_t20_{end_date}.csv')
    file4_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/T20/player_match_data_t20_{end_date}.csv')

    # Load data
    df1 = pd.read_csv(file1_path, dtype=career_dict)
    df2 = pd.read_csv(file2_path, dtype=recent_dict)
    df3 = pd.read_csv(file3_path, dtype=venue_dict)
    df4 = pd.read_csv(file4_path, dtype=player_dict, parse_dates=["date"])

    # Merge datasets
    merged_df = pd.merge(df1, df2, on=['match_id', 'player_id'], how='inner')
    merged_df = pd.merge(merged_df, df3, on=['match_id', 'player_id'], how='inner')
    merged_df = pd.merge(merged_df, df4, on=['match_id', 'player_id'], how='inner')

    # Process data
    merged_df['date'] = pd.to_datetime(merged_df['date'])
    # Split the DataFrame based on the condition (date <= June 30, 2024)
    split_date = pd.to_datetime(end_date)

    merged_df_before_end_date = merged_df[merged_df['date'] <= split_date]
    merged_df_after_end_date = merged_df[merged_df['date'] > split_date]

    columns_to_drop = ['match_id', 'player_id', 'player_name', 'fantasy_points', 'team_name', 'role', 'date', 'venue']
    X_train = merged_df_before_end_date.drop(columns=columns_to_drop)
    y_train = merged_df_before_end_date['fantasy_points']
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    # Train the model
    model = HuberRegressor(max_iter=500)  # Increased max_iter
    model.fit(X_train_scaled, y_train)

    filename = os.path.join(os.path.dirname(__file__), f"../model_artifacts_ui2/T20/model_T20_{end_date}.pkl")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        pickle.dump(model, f)


def train_model_test(start_date, end_date):
    # Paths
    file1_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/Test/career_test_{end_date}.csv')
    file2_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/Test/recent_test_{end_date}.csv')
    file3_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/Test/venue_test_{end_date}.csv')
    file4_path = os.path.join(os.path.dirname(__file__), f'../data_ui2/processed/Test/player_match_data_test_{end_date}.csv')

    # Load data
    df1 = pd.read_csv(file1_path, dtype=career_dict)
    df2 = pd.read_csv(file2_path, dtype=recent_dict)
    df3 = pd.read_csv(file3_path, dtype=venue_dict)
    df4 = pd.read_csv(file4_path, dtype=player_dict, parse_dates=["date"])

    # Merge datasets
    merged_df = pd.merge(df1, df2, on=['match_id', 'player_id'], how='inner')
    merged_df = pd.merge(merged_df, df3, on=['match_id', 'player_id'], how='inner')
    merged_df = pd.merge(merged_df, df4, on=['match_id', 'player_id'], how='inner')

    # Process data
    merged_df['date'] = pd.to_datetime(merged_df['date'])
    # Split the DataFrame based on the condition (date <= June 30, 2024)
    split_date = pd.to_datetime(end_date)

    merged_df_before_end_date = merged_df[merged_df['date'] <= split_date]
    merged_df_after_end_date = merged_df[merged_df['date'] > split_date]

    columns_to_drop = ['match_id', 'player_id', 'player_name', 'fantasy_points', 'team_name', 'role', 'date', 'venue']
    X_train = merged_df_before_end_date.drop(columns=columns_to_drop)
    y_train = merged_df_before_end_date['fantasy_points']
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    # Train the model
    model = HuberRegressor(max_iter=500)  # Increased max_iter
    model.fit(X_train_scaled, y_train)

    # Save the model
    filename = os.path.join(os.path.dirname(__file__), f"../model_artifacts_ui2/Test/model_test_{end_date}.pkl")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as f:
        pickle.dump(model, f)

# Function to clean team names by replacing empty or whitespace-only strings with NaN
def clean_team_names(df):
    df['team_name'] = df['team_name'].replace(r'^\s*$', np.nan, regex=True)
    return df

def standardize_columns(df):
    df.columns = df.columns.str.strip()
    return df

def extract_match_details(df):
    match_details = df.groupby('match_id').agg({
        'date': 'first',
        'team_name': lambda x: x.dropna().unique()
    }).reset_index()
    
    # Rename columns for clarity
    match_details = match_details.rename(columns={
        'date': 'Match Date',
        'team_name': 'teams'
    })
    
    # Debug: Print the 'teams' column to inspect its contents
    print("\nTeams per match_id:")
    print(match_details[['match_id', 'teams']].head(10))
    
    # Split the 'teams' array into 'Team 1' and 'Team 2'
    # Ensure that each list has exactly two elements by padding with NaN if necessary
    match_details[['Team 1', 'Team 2']] = match_details['teams'].apply(
        lambda x: (list(x) + [np.nan, np.nan])[:2] if isinstance(x, (np.ndarray, list)) else [x, np.nan]
    ).tolist()
    
    # Drop the 'teams' column as it's no longer needed
    match_details = match_details.drop(columns=['teams'])
    
    return match_details


# Define Dream Team Calculation Logic
def calculate_dream_team_predicted(players):
    try:
        # Step 1: Pick one player from each role based on predicted fantasy points
        selected_players = []
        for role in ["Batsman", "Bowler", "Wicket-Keeper", "All-Rounder"]:
            role_players = [p for p in players if p["role"].lower() == role.lower()]
            if role_players:
                selected_players.append(max(role_players, key=lambda x: x["predicted_fantasy_points"]))

        # Step 2: Select remaining players to make a team of 11
        remaining_players = [p for p in players if p not in selected_players]
        remaining_players.sort(key=lambda x: x["predicted_fantasy_points"], reverse=True)

        while len(selected_players) < 11:
            next_player = remaining_players.pop(0)
            selected_players.append(next_player)

        # Step 3: Ensure team diversity (max 5 players from one team)
        team_counts = pd.DataFrame(selected_players)["team_name"].value_counts()
        if team_counts.max() == 11:
            # Replace the lowest fantasy point player with the highest fantasy point player from the other team
            other_team = [team for team in players[0]["team_name"].unique() if team not in team_counts.index][0]
            lowest_fantasy_player = min(selected_players, key=lambda x: x["predicted_fantasy_points"])
            replacement_player = max(
                [p for p in players if p["team_name"] == other_team and p not in selected_players],
                key=lambda x: x["predicted_fantasy_points"]
            )
            selected_players.remove(lowest_fantasy_player)
            selected_players.append(replacement_player)

        # Step 4: Sort selected players by predicted fantasy points
        selected_players.sort(key=lambda x: x["predicted_fantasy_points"], reverse=True)

        return selected_players, "Optimal"

    except Exception as e:
        print(f"Error in calculating dream team: {e}")
        return None, "Error"

# Define Dream Team Calculation Logic
def calculate_dream_team_actual(players):
    try:
        # Step 1: Pick one player from each role based on actual fantasy points
        selected_players = []
        for role in ["Batsman", "Bowler", "Wicket-Keeper", "All-Rounder"]:
            role_players = [p for p in players if p["role"].lower() == role.lower()]
            if role_players:
                selected_players.append(max(role_players, key=lambda x: x["actual_fantasy_points"]))

        # Step 2: Select remaining players to make a team of 11
        remaining_players = [p for p in players if p not in selected_players]
        remaining_players.sort(key=lambda x: x["actual_fantasy_points"], reverse=True)

        while len(selected_players) < 11:
            next_player = remaining_players.pop(0)
            selected_players.append(next_player)

        # Step 3: Ensure team diversity (max 5 players from one team)
        team_counts = pd.DataFrame(selected_players)["team_name"].value_counts()
        if team_counts.max() == 11:
            # Replace the lowest fantasy point player with the highest fantasy point player from the other team
            other_team = [team for team in players[0]["team_name"].unique() if team not in team_counts.index][0]
            lowest_fantasy_player = min(selected_players, key=lambda x: x["actual_fantasy_points"])
            replacement_player = max(
                [p for p in players if p["team_name"] == other_team and p not in selected_players],
                key=lambda x: x["actual_fantasy_points"]
            )
            selected_players.remove(lowest_fantasy_player)
            selected_players.append(replacement_player)

        # Step 4: Sort selected players by actual fantasy points
        selected_players.sort(key=lambda x: x["actual_fantasy_points"], reverse=True)

        return selected_players, "Optimal"

    except Exception as e:
        print(f"Error in calculating dream team: {e}")
        return None, "Error"
    
# Function to calculate the sum of fantasy points (with captain and vice-captain multipliers)
def calculate_team_points(team_df):
    team_df = team_df.sort_values(by='predicted_fantasy_points', ascending=False)  # Sort by predicted points (or actual, depending on case)
    
    total_points = 0
    if len(team_df) >= 1:
        # Highest points player (Captain)
        total_points += team_df.iloc[0]['predicted_fantasy_points'] * 2
    if len(team_df) >= 2:
        # Second highest points player (Vice-Captain)
        total_points += team_df.iloc[1]['predicted_fantasy_points'] * 1.5
    
    # Add the rest normally
    total_points += team_df.iloc[2:]['predicted_fantasy_points'].sum()

    return total_points

def evaluate_model_odi(end_training_date, end_testing_date):
    # Define the directory where the CSV files are located
    csv_dir = os.path.join(os.path.dirname(__file__), '../data_ui2/test_data/processed/ODI/')

    # Construct the filename using the end_testing_date
    filename = f'merged_odi_{end_testing_date}.csv'

    # Create the full file path
    file_path = os.path.join(csv_dir, filename)

    # Import the CSV file
    try:
        merged_df_test = pd.read_csv(file_path, low_memory=False)
        print(f"Successfully loaded data from {file_path}")
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} does not exist. Please check the end_testing_date and the file path.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {e}")
    
    # Specify the current working directory (if needed, adjust as per your setup)
    current_directory = os.path.dirname(__file__)
    # Replace with your actual end_date
    model_file_path = os.path.join(current_directory, f'../model_artifacts_ui2/ODI/model_ODI_{end_training_date}.pkl')

    # Ensure the model file exists
    if os.path.exists(model_file_path):
        with open(model_file_path, 'rb') as f:
            model = pickle.load(f)
        print("Model loaded successfully!")
    else:
        print(f"Model file not found at: {model_file_path}")

    
    columns_to_drop = ['match_id', 'player_id', 'player_name', 'fantasy_points', 'team_name', 'role', 'date','venue']
    X_test = merged_df_test.drop(columns=columns_to_drop)
    y_test = merged_df_test['fantasy_points']

    scaler = StandardScaler()
    X_test_scaled = scaler.fit_transform(X_test)

    # Use the trained model to make predictions on the test data
    y_pred = model.predict(X_test_scaled)

    # Create a new DataFrame with the necessary columns
    predictions_df = merged_df_test[['match_id', 'player_id', 'player_name', 'fantasy_points', 'role', 'team_name','date']].copy()

    # Add the predicted fantasy points to the DataFrame
    predictions_df['predicted_fantasy_points'] = y_pred

    # Rename the fantasy_points column to actual_fantasy_points
    predictions_df.rename(columns={'fantasy_points': 'actual_fantasy_points'}, inplace=True)

    # Save the DataFrame to a CSV file
    current_directory = os.path.dirname(__file__)
    output_file = os.path.join(current_directory, f'Results_ui2/ODI/predicted_fantasy_points_odi.csv')
    predictions_df.to_csv(output_file, index=False)

    print(f"Predictions saved to {output_file}")

    

    # Input File (Predicted Fantasy Points)
    input_file = os.path.join(current_directory, f'Results_ui2/ODI/predicted_fantasy_points_odi.csv')

    # Output File
    output_file=os.path.join(current_directory, f'Results_ui2/ODI/dream_team_with_predicted_fantasy_points.csv')

    # Columns for Output
    output_columns = [
        "match_id", "date", "player_id", "player_name", "actual_fantasy_points", "role", "team_name", "predicted_fantasy_points"
    ]

    # Read Data
    data = pd.read_csv(input_file)

    # Prepare Output Data
    output_data = []
    # Process Matches
    i = 1
    for match_id, match_group in data.groupby("match_id"):
        # Extract necessary columns (including date)
        players = match_group[['match_id', 'date', 'player_id', 'player_name', 'actual_fantasy_points', 'role', 'team_name', 'predicted_fantasy_points']].to_dict(orient="records")
        match_date = match_group['date'].iloc[0]  # Extract the date for the match

        # Calculate Dream Team
        selected_team, status = calculate_dream_team_predicted(players)

        if selected_team is None or len(selected_team) != 11:
            # If selected_team is None or doesn't have exactly 11 players, log the error
            with open("matches_where_team_could_not_be_formed.txt", 'a') as file:
                file.write(f"{status}, {match_id}, {len(selected_team) if selected_team else 'None'}, {selected_team if selected_team else 'None'}\n")
            i += 1
            continue

        # Prepare Row for Output
        for player in selected_team:
            row = [
                match_id,
                match_date,
                player["player_id"],
                player["player_name"],
                player["actual_fantasy_points"],
                player["role"],
                player["team_name"],
                player["predicted_fantasy_points"]
            ]
            output_data.append(row)

        if i % 100 == 0:
            print(f"Processed {i} matches...")
        i += 1

    # Write Output to CSV
    output_df = pd.DataFrame(output_data, columns=output_columns)
    output_df.to_csv(output_file, index=False)

    print(f"Dream Team details saved to {output_file}")

    # Input File (Predicted Fantasy Points)
    input_file = os.path.join(current_directory, f'Results_ui2/ODI/predicted_fantasy_points_odi.csv')

    # Output File
    output_file=os.path.join(current_directory, f'Results_ui2/ODI/dream_team_with_actual_fantasy_points.csv')

    # Columns for Output
    output_columns = [
        "match_id", "date", "player_id", "player_name", "actual_fantasy_points", "role", "team_name", "predicted_fantasy_points"
    ]

    # Read Data
    data = pd.read_csv(input_file)

    # Prepare Output Data
    output_data = []

    # Process Matches
    i = 1
    for match_id, match_group in data.groupby("match_id"):
        # Extract necessary columns (including date)
        players = match_group[['match_id', 'date', 'player_id', 'player_name', 'actual_fantasy_points', 'role', 'team_name', 'predicted_fantasy_points']].to_dict(orient="records")
        match_date = match_group['date'].iloc[0]  # Extract the date for the match

        # Calculate Dream Team
        selected_team, status = calculate_dream_team_actual(players)

        if selected_team is None or len(selected_team) != 11:
            # If selected_team is None or doesn't have exactly 11 players, log the error
            with open("matches_where_team_could_not_be_formed.txt", 'a') as file:
                file.write(f"{status}, {match_id}, {len(selected_team) if selected_team else 'None'}, {selected_team if selected_team else 'None'}\n")
            i += 1
            continue

        # Prepare Row for Output
        for player in selected_team:
            row = [
                match_id,
                match_date,
                player["player_id"],
                player["player_name"],
                player["actual_fantasy_points"],
                player["role"],
                player["team_name"],
                player["predicted_fantasy_points"]
            ]
            output_data.append(row)

        if i % 100 == 0:
            print(f"Processed {i} matches...")
        i += 1

    # Write Output to CSV
    output_df = pd.DataFrame(output_data, columns=output_columns)
    output_df.to_csv(output_file, index=False)

    print(f"Dream Team details saved to {output_file}")
      
    predicted_file= os.path.join(current_directory, f'Results_ui2/ODI/dream_team_with_predicted_fantasy_points.csv')
    actual_file= os.path.join(current_directory, f'Results_ui2/ODI/dream_team_with_actual_fantasy_points.csv')
    

    # Output file path
    output_file = os.path.join(current_directory, f'Results_ui2/ODI/dream_team_summary.csv')

    # Read the data from the two files
    predicted_df = pd.read_csv(predicted_file)
    actual_df = pd.read_csv(actual_file)

    # Initialize list to store the summary for each match_id
    summary_data = []

    

    # Iterate through the unique match IDs
    for match_id in predicted_df['match_id'].unique():
        # Get the predicted dream team for the current match_id
        predicted_team = predicted_df[predicted_df['match_id'] == match_id]

        # Get the actual dream team for the current match_id
        actual_team = actual_df[actual_df['match_id'] == match_id]

        # Calculate the sum of actual and predicted points for both teams
        predicted_team_points = calculate_team_points(predicted_team)
        actual_team_points_predicted = calculate_team_points(actual_team)
        
        # Add the match summary to the summary_data list
        summary_data.append({
            'match_id': match_id,
            'sum_predicted_points_predicted_team': predicted_team_points,
            'sum_predicted_points_actual_team': actual_team_points_predicted,
            'sum_actual_points_predicted_team': predicted_team['actual_fantasy_points'].sum(),
            'sum_actual_points_actual_team': actual_team['actual_fantasy_points'].sum()
        })

    # Create a DataFrame from the summary_data
    summary_df = pd.DataFrame(summary_data)

    # Write the summary data to a CSV file
    summary_df.to_csv(output_file, index=False)

    print(f"Summary saved to {output_file}")

    predicted_fp_path=os.path.join(current_directory, f'Results_ui2/ODI/dream_team_with_predicted_fantasy_points.csv')
    actual_fp_path=os.path.join(current_directory, f'Results_ui2/ODI/dream_team_with_actual_fantasy_points.csv')
    summary_path=os.path.join(current_directory, f'Results_ui2/ODI/dream_team_summary.csv')


    # Read the CSV files into pandas DataFrames
    predicted_df = pd.read_csv(predicted_fp_path)
    actual_df = pd.read_csv(actual_fp_path)
    summary_df = pd.read_csv(summary_path)

    # Apply the cleaning function to both predicted and actual DataFrames
    predicted_df = clean_team_names(predicted_df)
    actual_df = clean_team_names(actual_df)

    # Apply standardization to remove leading/trailing spaces
    predicted_df = standardize_columns(predicted_df)
    actual_df = standardize_columns(actual_df)
    summary_df = standardize_columns(summary_df)


    # Verify 'match_id' exists in all DataFrames
    for df_name, df in zip(['predicted_df', 'actual_df', 'summary_df'], [predicted_df, actual_df, summary_df]):
        if 'match_id' not in df.columns:
            raise KeyError(f"'match_id' column is missing in {df_name}")
        else:
            print(f"'match_id' found in {df_name}")

    # Assign player_number within each match_id for predicted_df and actual_df
    predicted_df['player_number'] = predicted_df.groupby('match_id').cumcount() + 1
    predicted_df['player_number'] = predicted_df['player_number'].clip(upper=11)

    actual_df['player_number'] = actual_df.groupby('match_id').cumcount() + 1
    actual_df['player_number'] = actual_df['player_number'].clip(upper=11)

    # Pivot the Predicted Fantasy Points DataFrame
    predicted_pivot = predicted_df.pivot_table(
        index='match_id',
        columns='player_number',
        values=['player_name', 'predicted_fantasy_points'],
        aggfunc='first'
    )

    # Flatten the MultiIndex columns for predicted_pivot
    predicted_pivot.columns = [
        f'Predicted Player {int(col[1])} {col[0].split("_")[1].capitalize()}' for col in predicted_pivot.columns
    ]

    # Reset the index to turn 'match_id' back into a column
    predicted_pivot = predicted_pivot.reset_index()

    # Pivot the Actual Fantasy Points DataFrame
    actual_pivot = actual_df.pivot_table(
        index='match_id',
        columns='player_number',
        values=['player_name', 'actual_fantasy_points'],
        aggfunc='first'
    )

    # Flatten the MultiIndex columns for actual_pivot
    actual_pivot.columns = [
        f'Dream Team Player {int(col[1])} {col[0].split("_")[1].capitalize()}' for col in actual_pivot.columns
    ]

    # Reset the index to turn 'match_id' back into a column
    actual_pivot = actual_pivot.reset_index()


    # Extract match details from predicted_df
    match_details = extract_match_details(predicted_df)

    # Verify the extracted match_details DataFrame
    print("\nMatch Details Sample:")
    print(match_details.head())

    # Merge predicted_pivot with match_details
    performance_summary = pd.merge(
        predicted_pivot,
        match_details,
        on='match_id',
        how='left'
    )

    # Merge with summary_df
    performance_summary = pd.merge(
        performance_summary,
        summary_df,
        on='match_id',
        how='left',
        suffixes=('', '_summary')
    )

    # Merge with actual_pivot
    performance_summary = pd.merge(
        performance_summary,
        actual_pivot,
        on='match_id',
        how='left',
        suffixes=('', '_actual')
    )

    # ================================
    # Implementing Steps 1-5
    # ================================

    # Step 1: Drop 'Predicted Player 1 Points' to 'Predicted Player 11 Points'
    predicted_points_cols = [f'Predicted Player {i} Points' for i in range(1, 12)]
    performance_summary.drop(columns=predicted_points_cols, inplace=True, errors='ignore')

    # Step 2: Drop 'Dream Team Player 1 Points' to 'Dream Team Player 11 Points'
    dream_points_cols = [f'Dream Team Player {i} Points' for i in range(1, 12)]
    performance_summary.drop(columns=dream_points_cols, inplace=True, errors='ignore')

    # Step 3: Rename 'Predicted Player X Fantasy' to 'Predicted Player X Points'
    for i in range(1, 12):
        old_col = f'Predicted Player {i} Fantasy'
        new_col = f'Predicted Player {i} Points'
        if old_col in performance_summary.columns:
            performance_summary.rename(columns={old_col: new_col}, inplace=True)

    # Step 4: Rename 'Dream Team Player X Fantasy' to 'Dream Team Player X Points'
    for i in range(1, 12):
        old_col = f'Dream Team Player {i} Fantasy'
        new_col = f'Dream Team Player {i} Points'
        if old_col in performance_summary.columns:
            performance_summary.rename(columns={old_col: new_col}, inplace=True)

    # Step 5: Reorder the columns in the specified format
    desired_columns = [
        'match_id', 'Match Date', 'Team 1', 'Team 2'
    ]

    # Add Predicted Players and Points
    for i in range(1, 12):
        predicted_name_col = f'Predicted Player {i} Name'
        predicted_points_col = f'Predicted Player {i} Points'
        desired_columns.extend([predicted_name_col, predicted_points_col])

    # Add Dream Team Players and Points
    for i in range(1, 12):
        dream_name_col = f'Dream Team Player {i} Name'
        dream_points_col = f'Dream Team Player {i} Points'
        desired_columns.extend([dream_name_col, dream_points_col])

    # Add Summary Fields (excluding 'match_id')
    summary_fields = [col for col in summary_df.columns if col != 'match_id']
    desired_columns += summary_fields

    # Add any additional columns not already included
    additional_columns = [col for col in performance_summary.columns if col not in desired_columns]
    desired_columns += additional_columns

    # Reorder the DataFrame
    try:
        performance_summary = performance_summary[desired_columns]
    except KeyError as e:
        print(f"KeyError during column reordering: {e}")
        print("Available columns:", performance_summary.columns.tolist())
        raise

    # Verify the final DataFrame structure
    print("\nPerformance Summary Sample:")
    print(performance_summary.head())

    # Export the final DataFrame to CSV

    output_file = os.path.join(current_directory, f'Results_ui2/ODI/test_data_performance_summary_odi_{end_testing_date}.csv')
    performance_summary.to_csv(output_file, index=False)

    print("\nPerformance_summary.csv has been successfully created.")

def evaluate_model_test(end_training_date, end_testing_date):
    # Define the directory where the CSV files are located
    csv_dir = os.path.join(os.path.dirname(__file__), '../data_ui2/test_data/processed/Test/')

    # Construct the filename using the end_testing_date
    filename = f'merged_test_{end_testing_date}.csv'

    # Create the full file path
    file_path = os.path.join(csv_dir, filename)

    # Import the CSV file
    try:
        merged_df_test = pd.read_csv(file_path, low_memory=False)
        print(f"Successfully loaded data from {file_path}")
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} does not exist. Please check the end_testing_date and the file path.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {e}")
    
    # Specify the current working directory (if needed, adjust as per your setup)
    current_directory = os.path.dirname(__file__)
    # Replace with your actual end_date
    model_file_path = os.path.join(current_directory, f'../model_artifacts_ui2/Test/model_test_{end_training_date}.pkl')

    # Ensure the model file exists
    if os.path.exists(model_file_path):
        with open(model_file_path, 'rb') as f:
            model = pickle.load(f)
        print("Model loaded successfully!")
    else:
        print(f"Model file not found at: {model_file_path}")

    
    columns_to_drop = ['match_id', 'player_id', 'player_name', 'fantasy_points', 'team_name', 'role', 'date','venue']
    X_test = merged_df_test.drop(columns=columns_to_drop)
    y_test = merged_df_test['fantasy_points']

    scaler = StandardScaler()
    X_test_scaled = scaler.fit_transform(X_test)

    # Use the trained model to make predictions on the test data
    y_pred = model.predict(X_test_scaled)

    # Create a new DataFrame with the necessary columns
    predictions_df = merged_df_test[['match_id', 'player_id', 'player_name', 'fantasy_points', 'role', 'team_name','date']].copy()

    # Add the predicted fantasy points to the DataFrame
    predictions_df['predicted_fantasy_points'] = y_pred

    # Rename the fantasy_points column to actual_fantasy_points
    predictions_df.rename(columns={'fantasy_points': 'actual_fantasy_points'}, inplace=True)

    # Save the DataFrame to a CSV file
    current_directory = os.path.dirname(__file__)
    output_file = os.path.join(current_directory, f'Results_ui2/Test/predicted_fantasy_points_test.csv')
    predictions_df.to_csv(output_file, index=False)

    print(f"Predictions saved to {output_file}")

    

    # Input File (Predicted Fantasy Points)
    input_file = os.path.join(current_directory, f'Results_ui2/Test/predicted_fantasy_points_test.csv')

    # Output File
    output_file=os.path.join(current_directory, f'Results_ui2/Test/dream_team_with_predicted_fantasy_points.csv')

    # Columns for Output
    output_columns = [
        "match_id", "date", "player_id", "player_name", "actual_fantasy_points", "role", "team_name", "predicted_fantasy_points"
    ]

    # Read Data
    data = pd.read_csv(input_file)

    # Prepare Output Data
    output_data = []
    # Process Matches
    i = 1
    for match_id, match_group in data.groupby("match_id"):
        # Extract necessary columns (including date)
        players = match_group[['match_id', 'date', 'player_id', 'player_name', 'actual_fantasy_points', 'role', 'team_name', 'predicted_fantasy_points']].to_dict(orient="records")
        match_date = match_group['date'].iloc[0]  # Extract the date for the match

        # Calculate Dream Team
        selected_team, status = calculate_dream_team_predicted(players)

        if selected_team is None or len(selected_team) != 11:
            # If selected_team is None or doesn't have exactly 11 players, log the error
            with open("matches_where_team_could_not_be_formed.txt", 'a') as file:
                file.write(f"{status}, {match_id}, {len(selected_team) if selected_team else 'None'}, {selected_team if selected_team else 'None'}\n")
            i += 1
            continue

        # Prepare Row for Output
        for player in selected_team:
            row = [
                match_id,
                match_date,
                player["player_id"],
                player["player_name"],
                player["actual_fantasy_points"],
                player["role"],
                player["team_name"],
                player["predicted_fantasy_points"]
            ]
            output_data.append(row)

        if i % 100 == 0:
            print(f"Processed {i} matches...")
        i += 1

    # Write Output to CSV
    output_df = pd.DataFrame(output_data, columns=output_columns)
    output_df.to_csv(output_file, index=False)

    print(f"Dream Team details saved to {output_file}")

    # Input File (Predicted Fantasy Points)
    input_file = os.path.join(current_directory, f'Results_ui2/Test/predicted_fantasy_points_test.csv')

    # Output File
    output_file=os.path.join(current_directory, f'Results_ui2/Test/dream_team_with_actual_fantasy_points.csv')

    # Columns for Output
    output_columns = [
        "match_id", "date", "player_id", "player_name", "actual_fantasy_points", "role", "team_name", "predicted_fantasy_points"
    ]

    # Read Data
    data = pd.read_csv(input_file)

    # Prepare Output Data
    output_data = []

    # Process Matches
    i = 1
    for match_id, match_group in data.groupby("match_id"):
        # Extract necessary columns (including date)
        players = match_group[['match_id', 'date', 'player_id', 'player_name', 'actual_fantasy_points', 'role', 'team_name', 'predicted_fantasy_points']].to_dict(orient="records")
        match_date = match_group['date'].iloc[0]  # Extract the date for the match

        # Calculate Dream Team
        selected_team, status = calculate_dream_team_actual(players)

        if selected_team is None or len(selected_team) != 11:
            # If selected_team is None or doesn't have exactly 11 players, log the error
            with open("matches_where_team_could_not_be_formed.txt", 'a') as file:
                file.write(f"{status}, {match_id}, {len(selected_team) if selected_team else 'None'}, {selected_team if selected_team else 'None'}\n")
            i += 1
            continue

        # Prepare Row for Output
        for player in selected_team:
            row = [
                match_id,
                match_date,
                player["player_id"],
                player["player_name"],
                player["actual_fantasy_points"],
                player["role"],
                player["team_name"],
                player["predicted_fantasy_points"]
            ]
            output_data.append(row)

        if i % 100 == 0:
            print(f"Processed {i} matches...")
        i += 1

    # Write Output to CSV
    output_df = pd.DataFrame(output_data, columns=output_columns)
    output_df.to_csv(output_file, index=False)

    print(f"Dream Team details saved to {output_file}")
      
    predicted_file= os.path.join(current_directory, f'Results_ui2/Test/dream_team_with_predicted_fantasy_points.csv')
    actual_file= os.path.join(current_directory, f'Results_ui2/Test/dream_team_with_actual_fantasy_points.csv')
    

    # Output file path
    output_file = os.path.join(current_directory, f'Results_ui2/Test/dream_team_summary.csv')

    # Read the data from the two files
    predicted_df = pd.read_csv(predicted_file)
    actual_df = pd.read_csv(actual_file)

    # Initialize list to store the summary for each match_id
    summary_data = []

    

    # Iterate through the unique match IDs
    for match_id in predicted_df['match_id'].unique():
        # Get the predicted dream team for the current match_id
        predicted_team = predicted_df[predicted_df['match_id'] == match_id]

        # Get the actual dream team for the current match_id
        actual_team = actual_df[actual_df['match_id'] == match_id]

        # Calculate the sum of actual and predicted points for both teams
        predicted_team_points = calculate_team_points(predicted_team)
        actual_team_points_predicted = calculate_team_points(actual_team)
        
        # Add the match summary to the summary_data list
        summary_data.append({
            'match_id': match_id,
            'sum_predicted_points_predicted_team': predicted_team_points,
            'sum_predicted_points_actual_team': actual_team_points_predicted,
            'sum_actual_points_predicted_team': predicted_team['actual_fantasy_points'].sum(),
            'sum_actual_points_actual_team': actual_team['actual_fantasy_points'].sum()
        })

    # Create a DataFrame from the summary_data
    summary_df = pd.DataFrame(summary_data)

    # Write the summary data to a CSV file
    summary_df.to_csv(output_file, index=False)

    print(f"Summary saved to {output_file}")

    predicted_fp_path=os.path.join(current_directory, f'Results_ui2/Test/dream_team_with_predicted_fantasy_points.csv')
    actual_fp_path=os.path.join(current_directory, f'Results_ui2/Test/dream_team_with_actual_fantasy_points.csv')
    summary_path=os.path.join(current_directory, f'Results_ui2/Test/dream_team_summary.csv')


    # Read the CSV files into pandas DataFrames
    predicted_df = pd.read_csv(predicted_fp_path)
    actual_df = pd.read_csv(actual_fp_path)
    summary_df = pd.read_csv(summary_path)

    # Apply the cleaning function to both predicted and actual DataFrames
    predicted_df = clean_team_names(predicted_df)
    actual_df = clean_team_names(actual_df)

    # Apply standardization to remove leading/trailing spaces
    predicted_df = standardize_columns(predicted_df)
    actual_df = standardize_columns(actual_df)
    summary_df = standardize_columns(summary_df)


    # Verify 'match_id' exists in all DataFrames
    for df_name, df in zip(['predicted_df', 'actual_df', 'summary_df'], [predicted_df, actual_df, summary_df]):
        if 'match_id' not in df.columns:
            raise KeyError(f"'match_id' column is missing in {df_name}")
        else:
            print(f"'match_id' found in {df_name}")

    # Assign player_number within each match_id for predicted_df and actual_df
    predicted_df['player_number'] = predicted_df.groupby('match_id').cumcount() + 1
    predicted_df['player_number'] = predicted_df['player_number'].clip(upper=11)

    actual_df['player_number'] = actual_df.groupby('match_id').cumcount() + 1
    actual_df['player_number'] = actual_df['player_number'].clip(upper=11)

    # Pivot the Predicted Fantasy Points DataFrame
    predicted_pivot = predicted_df.pivot_table(
        index='match_id',
        columns='player_number',
        values=['player_name', 'predicted_fantasy_points'],
        aggfunc='first'
    )

    # Flatten the MultiIndex columns for predicted_pivot
    predicted_pivot.columns = [
        f'Predicted Player {int(col[1])} {col[0].split("_")[1].capitalize()}' for col in predicted_pivot.columns
    ]

    # Reset the index to turn 'match_id' back into a column
    predicted_pivot = predicted_pivot.reset_index()

    # Pivot the Actual Fantasy Points DataFrame
    actual_pivot = actual_df.pivot_table(
        index='match_id',
        columns='player_number',
        values=['player_name', 'actual_fantasy_points'],
        aggfunc='first'
    )

    # Flatten the MultiIndex columns for actual_pivot
    actual_pivot.columns = [
        f'Dream Team Player {int(col[1])} {col[0].split("_")[1].capitalize()}' for col in actual_pivot.columns
    ]

    # Reset the index to turn 'match_id' back into a column
    actual_pivot = actual_pivot.reset_index()


    # Extract match details from predicted_df
    match_details = extract_match_details(predicted_df)

    # Verify the extracted match_details DataFrame
    print("\nMatch Details Sample:")
    print(match_details.head())

    # Merge predicted_pivot with match_details
    performance_summary = pd.merge(
        predicted_pivot,
        match_details,
        on='match_id',
        how='left'
    )

    # Merge with summary_df
    performance_summary = pd.merge(
        performance_summary,
        summary_df,
        on='match_id',
        how='left',
        suffixes=('', '_summary')
    )

    # Merge with actual_pivot
    performance_summary = pd.merge(
        performance_summary,
        actual_pivot,
        on='match_id',
        how='left',
        suffixes=('', '_actual')
    )

    # ================================
    # Implementing Steps 1-5
    # ================================

    # Step 1: Drop 'Predicted Player 1 Points' to 'Predicted Player 11 Points'
    predicted_points_cols = [f'Predicted Player {i} Points' for i in range(1, 12)]
    performance_summary.drop(columns=predicted_points_cols, inplace=True, errors='ignore')

    # Step 2: Drop 'Dream Team Player 1 Points' to 'Dream Team Player 11 Points'
    dream_points_cols = [f'Dream Team Player {i} Points' for i in range(1, 12)]
    performance_summary.drop(columns=dream_points_cols, inplace=True, errors='ignore')

    # Step 3: Rename 'Predicted Player X Fantasy' to 'Predicted Player X Points'
    for i in range(1, 12):
        old_col = f'Predicted Player {i} Fantasy'
        new_col = f'Predicted Player {i} Points'
        if old_col in performance_summary.columns:
            performance_summary.rename(columns={old_col: new_col}, inplace=True)

    # Step 4: Rename 'Dream Team Player X Fantasy' to 'Dream Team Player X Points'
    for i in range(1, 12):
        old_col = f'Dream Team Player {i} Fantasy'
        new_col = f'Dream Team Player {i} Points'
        if old_col in performance_summary.columns:
            performance_summary.rename(columns={old_col: new_col}, inplace=True)

    # Step 5: Reorder the columns in the specified format
    desired_columns = [
        'match_id', 'Match Date', 'Team 1', 'Team 2'
    ]

    # Add Predicted Players and Points
    for i in range(1, 12):
        predicted_name_col = f'Predicted Player {i} Name'
        predicted_points_col = f'Predicted Player {i} Points'
        desired_columns.extend([predicted_name_col, predicted_points_col])

    # Add Dream Team Players and Points
    for i in range(1, 12):
        dream_name_col = f'Dream Team Player {i} Name'
        dream_points_col = f'Dream Team Player {i} Points'
        desired_columns.extend([dream_name_col, dream_points_col])

    # Add Summary Fields (excluding 'match_id')
    summary_fields = [col for col in summary_df.columns if col != 'match_id']
    desired_columns += summary_fields

    # Add any additional columns not already included
    additional_columns = [col for col in performance_summary.columns if col not in desired_columns]
    desired_columns += additional_columns

    # Reorder the DataFrame
    try:
        performance_summary = performance_summary[desired_columns]
    except KeyError as e:
        print(f"KeyError during column reordering: {e}")
        print("Available columns:", performance_summary.columns.tolist())
        raise

    # Verify the final DataFrame structure
    print("\nPerformance Summary Sample:")
    print(performance_summary.head())

    # Export the final DataFrame to CSV

    output_file = os.path.join(current_directory, f'Results_ui2/Test/test_data_performance_summary_test_{end_testing_date}.csv')
    performance_summary.to_csv(output_file, index=False)

    print("\nPerformance_summary.csv has been successfully created.")

def evaluate_model_t20(end_training_date, end_testing_date):
    # Define the directory where the CSV files are located
    csv_dir = os.path.join(os.path.dirname(__file__), '../data_ui2/test_data/processed/T20/')

    # Construct the filename using the end_testing_date
    filename = f'merged_t20_{end_testing_date}.csv'

    # Create the full file path
    file_path = os.path.join(csv_dir, filename)

    # Import the CSV file
    try:
        merged_df_test = pd.read_csv(file_path, low_memory=False)
        print(f"Successfully loaded data from {file_path}")
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} does not exist. Please check the end_testing_date and the file path.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {e}")
    
    # Specify the current working directory (if needed, adjust as per your setup)
    current_directory = os.path.dirname(__file__)
    # Replace with your actual end_date
    model_file_path = os.path.join(current_directory, f'../model_artifacts_ui2/T20/model_T20_{end_training_date}.pkl')

    # Ensure the model file exists
    if os.path.exists(model_file_path):
        with open(model_file_path, 'rb') as f:
            model = pickle.load(f)
        print("Model loaded successfully!")
    else:
        print(f"Model file not found at: {model_file_path}")

    
    columns_to_drop = ['match_id', 'player_id', 'player_name', 'fantasy_points', 'team_name', 'role', 'date','venue']
    X_test = merged_df_test.drop(columns=columns_to_drop)
    y_test = merged_df_test['fantasy_points']

    scaler = StandardScaler()
    X_test_scaled = scaler.fit_transform(X_test)

    # Use the trained model to make predictions on the test data
    y_pred = model.predict(X_test_scaled)

    # Create a new DataFrame with the necessary columns
    predictions_df = merged_df_test[['match_id', 'player_id', 'player_name', 'fantasy_points', 'role', 'team_name','date']].copy()

    # Add the predicted fantasy points to the DataFrame
    predictions_df['predicted_fantasy_points'] = y_pred

    # Rename the fantasy_points column to actual_fantasy_points
    predictions_df.rename(columns={'fantasy_points': 'actual_fantasy_points'}, inplace=True)

    # Save the DataFrame to a CSV file
    current_directory = os.path.dirname(__file__)
    output_file = os.path.join(current_directory, f'Results_ui2/T20/predicted_fantasy_points_t20.csv')
    predictions_df.to_csv(output_file, index=False)

    print(f"Predictions saved to {output_file}")

    

    # Input File (Predicted Fantasy Points)
    input_file = os.path.join(current_directory, f'Results_ui2/T20/predicted_fantasy_points_t20.csv')

    # Output File
    output_file=os.path.join(current_directory, f'Results_ui2/T20/dream_team_with_predicted_fantasy_points.csv')

    # Columns for Output
    output_columns = [
        "match_id", "date", "player_id", "player_name", "actual_fantasy_points", "role", "team_name", "predicted_fantasy_points"
    ]

    # Read Data
    data = pd.read_csv(input_file)

    # Prepare Output Data
    output_data = []
    # Process Matches
    i = 1
    for match_id, match_group in data.groupby("match_id"):
        # Extract necessary columns (including date)
        players = match_group[['match_id', 'date', 'player_id', 'player_name', 'actual_fantasy_points', 'role', 'team_name', 'predicted_fantasy_points']].to_dict(orient="records")
        match_date = match_group['date'].iloc[0]  # Extract the date for the match

        # Calculate Dream Team
        selected_team, status = calculate_dream_team_predicted(players)

        if selected_team is None or len(selected_team) != 11:
            # If selected_team is None or doesn't have exactly 11 players, log the error
            with open("matches_where_team_could_not_be_formed.txt", 'a') as file:
                file.write(f"{status}, {match_id}, {len(selected_team) if selected_team else 'None'}, {selected_team if selected_team else 'None'}\n")
            i += 1
            continue

        # Prepare Row for Output
        for player in selected_team:
            row = [
                match_id,
                match_date,
                player["player_id"],
                player["player_name"],
                player["actual_fantasy_points"],
                player["role"],
                player["team_name"],
                player["predicted_fantasy_points"]
            ]
            output_data.append(row)

        if i % 100 == 0:
            print(f"Processed {i} matches...")
        i += 1

    # Write Output to CSV
    output_df = pd.DataFrame(output_data, columns=output_columns)
    output_df.to_csv(output_file, index=False)

    print(f"Dream Team details saved to {output_file}")

    # Input File (Predicted Fantasy Points)
    input_file = os.path.join(current_directory, f'Results_ui2/T20/predicted_fantasy_points_t20.csv')

    # Output File
    output_file=os.path.join(current_directory, f'Results_ui2/T20/dream_team_with_actual_fantasy_points.csv')

    # Columns for Output
    output_columns = [
        "match_id", "date", "player_id", "player_name", "actual_fantasy_points", "role", "team_name", "predicted_fantasy_points"
    ]

    # Read Data
    data = pd.read_csv(input_file)

    # Prepare Output Data
    output_data = []

    # Process Matches
    i = 1
    for match_id, match_group in data.groupby("match_id"):
        # Extract necessary columns (including date)
        players = match_group[['match_id', 'date', 'player_id', 'player_name', 'actual_fantasy_points', 'role', 'team_name', 'predicted_fantasy_points']].to_dict(orient="records")
        match_date = match_group['date'].iloc[0]  # Extract the date for the match

        # Calculate Dream Team
        selected_team, status = calculate_dream_team_actual(players)

        if selected_team is None or len(selected_team) != 11:
            # If selected_team is None or doesn't have exactly 11 players, log the error
            with open("matches_where_team_could_not_be_formed.txt", 'a') as file:
                file.write(f"{status}, {match_id}, {len(selected_team) if selected_team else 'None'}, {selected_team if selected_team else 'None'}\n")
            i += 1
            continue

        # Prepare Row for Output
        for player in selected_team:
            row = [
                match_id,
                match_date,
                player["player_id"],
                player["player_name"],
                player["actual_fantasy_points"],
                player["role"],
                player["team_name"],
                player["predicted_fantasy_points"]
            ]
            output_data.append(row)

        if i % 100 == 0:
            print(f"Processed {i} matches...")
        i += 1

    # Write Output to CSV
    output_df = pd.DataFrame(output_data, columns=output_columns)
    output_df.to_csv(output_file, index=False)

    print(f"Dream Team details saved to {output_file}")
      
    predicted_file= os.path.join(current_directory, f'Results_ui2/T20/dream_team_with_predicted_fantasy_points.csv')
    actual_file= os.path.join(current_directory, f'Results_ui2/T20/dream_team_with_actual_fantasy_points.csv')
    

    # Output file path
    output_file = os.path.join(current_directory, f'Results_ui2/T20/dream_team_summary.csv')

    # Read the data from the two files
    predicted_df = pd.read_csv(predicted_file)
    actual_df = pd.read_csv(actual_file)

    # Initialize list to store the summary for each match_id
    summary_data = []

    

    # Iterate through the unique match IDs
    for match_id in predicted_df['match_id'].unique():
        # Get the predicted dream team for the current match_id
        predicted_team = predicted_df[predicted_df['match_id'] == match_id]

        # Get the actual dream team for the current match_id
        actual_team = actual_df[actual_df['match_id'] == match_id]

        # Calculate the sum of actual and predicted points for both teams
        predicted_team_points = calculate_team_points(predicted_team)
        actual_team_points_predicted = calculate_team_points(actual_team)
        
        # Add the match summary to the summary_data list
        summary_data.append({
            'match_id': match_id,
            'sum_predicted_points_predicted_team': predicted_team_points,
            'sum_predicted_points_actual_team': actual_team_points_predicted,
            'sum_actual_points_predicted_team': predicted_team['actual_fantasy_points'].sum(),
            'sum_actual_points_actual_team': actual_team['actual_fantasy_points'].sum()
        })

    # Create a DataFrame from the summary_data
    summary_df = pd.DataFrame(summary_data)

    # Write the summary data to a CSV file
    summary_df.to_csv(output_file, index=False)

    print(f"Summary saved to {output_file}")

    predicted_fp_path=os.path.join(current_directory, f'Results_ui2/T20/dream_team_with_predicted_fantasy_points.csv')
    actual_fp_path=os.path.join(current_directory, f'Results_ui2/T20/dream_team_with_actual_fantasy_points.csv')
    summary_path=os.path.join(current_directory, f'Results_ui2/T20/dream_team_summary.csv')


    # Read the CSV files into pandas DataFrames
    predicted_df = pd.read_csv(predicted_fp_path)
    actual_df = pd.read_csv(actual_fp_path)
    summary_df = pd.read_csv(summary_path)

    # Apply the cleaning function to both predicted and actual DataFrames
    predicted_df = clean_team_names(predicted_df)
    actual_df = clean_team_names(actual_df)

    # Apply standardization to remove leading/trailing spaces
    predicted_df = standardize_columns(predicted_df)
    actual_df = standardize_columns(actual_df)
    summary_df = standardize_columns(summary_df)


    # Verify 'match_id' exists in all DataFrames
    for df_name, df in zip(['predicted_df', 'actual_df', 'summary_df'], [predicted_df, actual_df, summary_df]):
        if 'match_id' not in df.columns:
            raise KeyError(f"'match_id' column is missing in {df_name}")
        else:
            print(f"'match_id' found in {df_name}")

    # Assign player_number within each match_id for predicted_df and actual_df
    predicted_df['player_number'] = predicted_df.groupby('match_id').cumcount() + 1
    predicted_df['player_number'] = predicted_df['player_number'].clip(upper=11)

    actual_df['player_number'] = actual_df.groupby('match_id').cumcount() + 1
    actual_df['player_number'] = actual_df['player_number'].clip(upper=11)

    # Pivot the Predicted Fantasy Points DataFrame
    predicted_pivot = predicted_df.pivot_table(
        index='match_id',
        columns='player_number',
        values=['player_name', 'predicted_fantasy_points'],
        aggfunc='first'
    )

    # Flatten the MultiIndex columns for predicted_pivot
    predicted_pivot.columns = [
        f'Predicted Player {int(col[1])} {col[0].split("_")[1].capitalize()}' for col in predicted_pivot.columns
    ]

    # Reset the index to turn 'match_id' back into a column
    predicted_pivot = predicted_pivot.reset_index()

    # Pivot the Actual Fantasy Points DataFrame
    actual_pivot = actual_df.pivot_table(
        index='match_id',
        columns='player_number',
        values=['player_name', 'actual_fantasy_points'],
        aggfunc='first'
    )

    # Flatten the MultiIndex columns for actual_pivot
    actual_pivot.columns = [
        f'Dream Team Player {int(col[1])} {col[0].split("_")[1].capitalize()}' for col in actual_pivot.columns
    ]

    # Reset the index to turn 'match_id' back into a column
    actual_pivot = actual_pivot.reset_index()


    # Extract match details from predicted_df
    match_details = extract_match_details(predicted_df)

    # Verify the extracted match_details DataFrame
    print("\nMatch Details Sample:")
    print(match_details.head())

    # Merge predicted_pivot with match_details
    performance_summary = pd.merge(
        predicted_pivot,
        match_details,
        on='match_id',
        how='left'
    )

    # Merge with summary_df
    performance_summary = pd.merge(
        performance_summary,
        summary_df,
        on='match_id',
        how='left',
        suffixes=('', '_summary')
    )

    # Merge with actual_pivot
    performance_summary = pd.merge(
        performance_summary,
        actual_pivot,
        on='match_id',
        how='left',
        suffixes=('', '_actual')
    )

    # ================================
    # Implementing Steps 1-5
    # ================================

    # Step 1: Drop 'Predicted Player 1 Points' to 'Predicted Player 11 Points'
    predicted_points_cols = [f'Predicted Player {i} Points' for i in range(1, 12)]
    performance_summary.drop(columns=predicted_points_cols, inplace=True, errors='ignore')

    # Step 2: Drop 'Dream Team Player 1 Points' to 'Dream Team Player 11 Points'
    dream_points_cols = [f'Dream Team Player {i} Points' for i in range(1, 12)]
    performance_summary.drop(columns=dream_points_cols, inplace=True, errors='ignore')

    # Step 3: Rename 'Predicted Player X Fantasy' to 'Predicted Player X Points'
    for i in range(1, 12):
        old_col = f'Predicted Player {i} Fantasy'
        new_col = f'Predicted Player {i} Points'
        if old_col in performance_summary.columns:
            performance_summary.rename(columns={old_col: new_col}, inplace=True)

    # Step 4: Rename 'Dream Team Player X Fantasy' to 'Dream Team Player X Points'
    for i in range(1, 12):
        old_col = f'Dream Team Player {i} Fantasy'
        new_col = f'Dream Team Player {i} Points'
        if old_col in performance_summary.columns:
            performance_summary.rename(columns={old_col: new_col}, inplace=True)

    # Step 5: Reorder the columns in the specified format
    desired_columns = [
        'match_id', 'Match Date', 'Team 1', 'Team 2'
    ]

    # Add Predicted Players and Points
    for i in range(1, 12):
        predicted_name_col = f'Predicted Player {i} Name'
        predicted_points_col = f'Predicted Player {i} Points'
        desired_columns.extend([predicted_name_col, predicted_points_col])

    # Add Dream Team Players and Points
    for i in range(1, 12):
        dream_name_col = f'Dream Team Player {i} Name'
        dream_points_col = f'Dream Team Player {i} Points'
        desired_columns.extend([dream_name_col, dream_points_col])

    # Add Summary Fields (excluding 'match_id')
    summary_fields = [col for col in summary_df.columns if col != 'match_id']
    desired_columns += summary_fields

    # Add any additional columns not already included
    additional_columns = [col for col in performance_summary.columns if col not in desired_columns]
    desired_columns += additional_columns

    # Reorder the DataFrame
    try:
        performance_summary = performance_summary[desired_columns]
    except KeyError as e:
        print(f"KeyError during column reordering: {e}")
        print("Available columns:", performance_summary.columns.tolist())
        raise

    # Verify the final DataFrame structure
    print("\nPerformance Summary Sample:")
    print(performance_summary.head())

    # Export the final DataFrame to CSV

    output_file = os.path.join(current_directory, f'Results_ui2/T20/test_data_performance_summary_t20_{end_testing_date}.csv')
    performance_summary.to_csv(output_file, index=False)

    print("\nPerformance_summary.csv has been successfully created.")


def train_model_ui2(start_date_training,end_date_training,start_date_testing,end_date_testing):
    # try:
        generate_training_data_for_retraining(start_date_training,end_date_testing,end_date_training)
        generate_testing_data_for_retraining(start_date_testing,end_date_testing,end_date_training)
        train_model_odi(start_date_training,end_date_training)
        train_model_t20(start_date_training,end_date_training)
        train_model_test(start_date_training,end_date_training)
        evaluate_model_odi(end_date_training,end_date_testing)
        evaluate_model_test(end_date_training,end_date_testing)
        evaluate_model_t20(end_date_training,end_date_testing)
    # relative paths from ui/backend/main.py
        return list([f"../../model_artifacts_ui2/ODI/model_ODI_{end_date_training}.pkl",\
            f"../../model_artifacts_ui2/T20/model_T20_{end_date_training}.pkl",\
            f"../../model_artifacts_ui2/Test/model_test_{end_date_training}.pkl",\
            f"../../model/Results_ui2/ODI/test_data_performance_summary_odi_{end_date_testing}.csv",\
            f"../../model/Results_ui2/T20/test_data_performance_summary_t20_{end_date_testing}.csv",\
            f"../../model/Results_ui2/Test/test_data_performance_summary_test_{end_date_testing}.csv"])
    # except Exception as e:
    #     print(f"Error occured while training model pipeline: {e}")
    #     return []
    
# train_model_ui2(start_date_training,end_date_training,start_date_testing,end_date_testing)