import os
import pandas as pd
from typing import List, Dict, Tuple, Any
import pickle  # Use pickle to load the model
import logging
import shap
# from pprint import pprint
from sklearn.preprocessing import StandardScaler

# Print the resolved paths for debugging
VENUE_ODI_PATH =  os.path.join(os.path.dirname(__file__), '../data/processed/ODI/venue_odi.csv')
RECENT_ODI_PATH = os.path.join(os.path.dirname(__file__), '../data/processed/ODI/recent_odi.csv')
CAREER_ODI_PATH = os.path.join(os.path.dirname(__file__), '../data/processed/ODI/career_odi.csv')
PLAYER_MATCH_DATA_ODI_PATH = os.path.join(os.path.dirname(__file__), '../data/processed/ODI/player_match_data_odi.csv')

VENUE_TEST_PATH =  os.path.join(os.path.dirname(__file__), '../data/processed/Test/venue_test.csv')
RECENT_TEST_PATH = os.path.join(os.path.dirname(__file__), '../data/processed/Test/recent_test.csv')
CAREER_TEST_PATH = os.path.join(os.path.dirname(__file__), '../data/processed/Test/career_test.csv')
PLAYER_MATCH_DATA_TEST_PATH = os.path.join(os.path.dirname(__file__), '../data/processed/Test/player_match_data_test.csv')

VENUE_T20_PATH =  os.path.join(os.path.dirname(__file__), '../data/processed/T20/venue_t20.csv')
RECENT_T20_PATH = os.path.join(os.path.dirname(__file__), '../data/processed/T20/recent_t20.csv')
CAREER_T20_PATH = os.path.join(os.path.dirname(__file__), '../data/processed/T20/career_t20.csv')
PLAYER_MATCH_DATA_T20_PATH = os.path.join(os.path.dirname(__file__), '../data/processed/T20/player_match_data_t20.csv')

MODEL_ARTIFACTS = {
    "T20":  os.path.join(os.path.dirname(__file__), '../model_artifacts/T20/model_t20_HBR.pkl'),
    "ODI":  os.path.join(os.path.dirname(__file__), '../model_artifacts/ODI/model_odi_HBR.pkl'),
    "Test":  os.path.join(os.path.dirname(__file__), '../model_artifacts/Test/model_test_HBR.pkl')
}

SHAP_VALUES_LIST_LEN = {
    "T20": (39, 13),
    "ODI": (36, 12),
    "Test": (30, 10),
}


career_dict_odi = {
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

recent_dict_odi = {
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

venue_dict_odi = {
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

player_dict_odi = {
    "match_id": "string",         # Match ID is usually alphanumeric, so it should be a string.
    "player_id": "string",        # Player ID can be alphanumeric, stored as a string.
    "player_name": "string",      # Player name is a string, which can contain spaces and special characters.
    "fantasy_points": "float64",  # Fantasy points are numeric values, represented as float.
    "team_name": "string",        # Team name is a string, as it can contain letters, numbers, and spaces.
    "role": "string",             # Player role is usually a categorical string (e.g., "Batsman", "Bowler").     
    "venue": "string"             # Venue is a string, usually the name of the stadium or city.
}


career_data_odi=pd.read_csv(CAREER_ODI_PATH,dtype=career_dict_odi)
venue_data_odi=pd.read_csv(VENUE_ODI_PATH,dtype=venue_dict_odi)
recent_data_odi=pd.read_csv(RECENT_ODI_PATH,dtype=recent_dict_odi)
player_match_data_odi=pd.read_csv(PLAYER_MATCH_DATA_ODI_PATH,dtype=player_dict_odi)

career_dict_test = {
    "match_id": "string",  # Match ID is usually a string type, as it may contain letters or special characters.
    "player_id": "string",  # Player ID could be an alphanumeric string or a number stored as a string.
    "career_batsman_total_runs_test": "int",  # Career total runs would be numeric.
    "career_batsman_100s_test": "int",  # Career 100s, numeric.
    "career_batsman_50s_test": "int",  # Career 50s, numeric.
    "career_batsman_total_sixes_test": "int",  # Career sixes, numeric.
    "career_batsman_total_fours_test": "int",  # Career fours, numeric.
    "career_batsman_average_runs_test": "float64",  # Career batting average, numeric.
    
    "career_bowler_wickets_test": "int",  # Career wickets, numeric.
    "career_bowler_average_test": "float64",  # Career bowler average, numeric.
    
    "career_fielder_total_catches_test": "int",  # Career catches, numeric.
    "career_fielder_total_runouts_test": "int"  # Career runouts, numeric.
}

recent_dict_test = {
    "match_id": "string",  # Match ID is usually a string type, as it may contain letters or special characters.
    "player_id": "string",  # Player ID could be an alphanumeric string or a number stored as a string.
    "recent_batsman_total_runs_test": "int",  # Recent total runs would be numeric.
    "recent_batsman_100s_test": "int",  # Recent 100s, numeric.
    "recent_batsman_50s_test": "int",  # Recent 50s, numeric.
    "recent_batsman_total_sixes_test": "int",  # Recent sixes, numeric.
    "recent_batsman_total_fours_test": "int",  # Recent fours, numeric.
    "recent_batsman_average_runs_test": "float64",  # Recent batting average, numeric.
    
    "recent_bowler_wickets_test": "int",  # Recent wickets, numeric.
    "recent_bowler_average_test": "float64",  # Recent bowler average, numeric.
    
    "recent_fielder_total_catches_test": "int",  # Recent catches, numeric.
    "recent_fielder_total_runouts_test": "int"  # Recent runouts, numeric.
}

venue_dict_test = {
    "match_id": "string",  # Match ID is usually a string type, as it may contain letters or special characters.
    "player_id": "string",  # Player ID could be an alphanumeric string or a number stored as a string.
    "venue_batsman_total_runs_test": "int",  # Venue total runs would be numeric.
    "venue_batsman_100s_test": "int",  # Venue 100s, numeric.
    "venue_batsman_50s_test": "int",  # Venue 50s, numeric.
    "venue_batsman_total_sixes_test": "int",  # Venue sixes, numeric.
    "venue_batsman_total_fours_test": "int",  # Venue fours, numeric.
    "venue_batsman_average_runs_test": "float64",  # Venue batting average, numeric.
    
    "venue_bowler_wickets_test": "int",  # Venue wickets, numeric.
    "venue_bowler_average_test": "float64",  # Venue bowler average, numeric.
    
    "venue_fielder_total_catches_test": "int",  # Venue catches, numeric.
    "venue_fielder_total_runouts_test": "int"  # Venue runouts, numeric.
}

player_dict_test = {
    "match_id": "string",         # Match ID is usually alphanumeric, so it should be a string.
    "player_id": "string",        # Player ID can be alphanumeric, stored as a string.
    "player_name": "string",      # Player name is a string, which can contain spaces and special characters.
    "fantasy_points": "float64",  # Fantasy points are numeric values, represented as float.
    "team_name": "string",        # Team name is a string, as it can contain letters, numbers, and spaces.
    "role": "string",             # Player role is usually a categorical string (e.g., "Batsman", "Bowler").     
    "venue": "string"             # Venue is a string, usually the name of the stadium or city.
}


career_data_test=pd.read_csv(CAREER_TEST_PATH,dtype=career_dict_test)
venue_data_test=pd.read_csv(VENUE_TEST_PATH,dtype=venue_dict_test)
recent_data_test=pd.read_csv(RECENT_TEST_PATH,dtype=recent_dict_test)
player_match_data_test=pd.read_csv(PLAYER_MATCH_DATA_TEST_PATH,dtype=player_dict_test)

career_dict_t20 = {
    "match_id": "string",  # Match ID is usually a string type, as it may contain letters or special characters.
    "player_id": "string",  # Player ID could be an alphanumeric string or a number stored as a string.
    "career_batsman_total_runs_t20": "int",  # Career total runs would be numeric.
    "career_batsman_100s_t20": "int",  # Career 100s, numeric.
    "career_batsman_50s_t20": "int",  # Career 50s, numeric.
    "career_batsman_30s_t20": "int",  # Career 30s, numeric.
    "career_batsman_total_sixes_t20": "int",  # Career sixes, numeric.
    "career_batsman_total_fours_t20": "int",  # Career fours, numeric.
    "career_batsman_average_runs_t20": "float64",  # Career batting average, numeric.
    "career_batsman_strike_rate_t20": "float64",  # Career strike rate, numeric.
    "career_bowler_wickets_t20": "int",  # Career wickets, numeric.
    "career_bowler_average_t20": "float64",  # Career bowler average, numeric.
    "career_bowler_economy_rate_t20": "float64",  # Economy rate, numeric.
    "career_fielder_total_catches_t20": "int",  # Career catches, numeric.
    "career_fielder_total_runouts_t20": "int"  # Career runouts, numeric.
}

recent_dict_t20 = {
    "match_id": "string",  # Match ID is usually a string type, as it may contain letters or special characters.
    "player_id": "string",  # Player ID could be an alphanumeric string or a number stored as a string.
    "recent_batsman_total_runs_t20": "int",  # Recent total runs would be numeric.
    "recent_batsman_100s_t20": "int",  # Recent 100s, numeric.
    "recent_batsman_50s_t20": "int",  # Recent 50s, numeric.
    "recent_batsman_30s_t20": "int",  # Career 30s, numeric.
    "recent_batsman_total_sixes_t20": "int",  # Recent sixes, numeric.
    "recent_batsman_total_fours_t20": "int",  # Recent fours, numeric.
    "recent_batsman_average_runs_t20": "float64",  # Recent batting average, numeric.
    "recent_batsman_strike_rate_t20": "float64",  # Recent strike rate, numeric.
    "recent_bowler_wickets_t20": "int",  # Recent wickets, numeric.
    "recent_bowler_average_t20": "float64",  # Recent bowler average, numeric.
    "recent_bowler_economy_rate_t20": "float64",  # Economy rate, numeric.
    "recent_fielder_total_catches_t20": "int",  # Recent catches, numeric.
    "recent_fielder_total_runouts_t20": "int"  # Recent runouts, numeric.
}

venue_dict_t20 = {
    "match_id": "string",  # Match ID is usually a string type, as it may contain letters or special characters.
    "player_id": "string",  # Player ID could be an alphanumeric string or a number stored as a string.
    "venue_batsman_total_runs_t20": "int",  # Venue total runs would be numeric.
    "venue_batsman_100s_t20": "int",  # Venue 100s, numeric.
    "venue_batsman_50s_t20": "int",  # Venue 50s, numeric.
    "venue_batsman_30s_t20": "int",  # Career 30s, numeric.
    "venue_batsman_total_sixes_t20": "int",  # Venue sixes, numeric.
    "venue_batsman_total_fours_t20": "int",  # Venue fours, numeric.
    "venue_batsman_average_runs_t20": "float64",  # Venue batting average, numeric.
    "venue_batsman_strike_rate_t20": "float64",  # Venue strike rate, numeric.
    "venue_bowler_wickets_t20": "int",  # Venue wickets, numeric.
    "venue_bowler_average_t20": "float64",  # Venue bowler average, numeric.
    "venue_bowler_economy_rate_t20": "float64",  # Economy rate, numeric.
    "venue_fielder_total_catches_t20": "int",  # Venue catches, numeric.
    "venue_fielder_total_runouts_t20": "int"  # Venue runouts, numeric.
}

player_dict_t20 = {
    "match_id": "string",         # Match ID is usually alphanumeric, so it should be a string.
    "player_id": "string",        # Player ID can be alphanumeric, stored as a string.
    "player_name": "string",      # Player name is a string, which can contain spaces and special characters.
    "fantasy_points": "float64",  # Fantasy points are numeric values, represented as float.
    "team_name": "string",        # Team name is a string, as it can contain letters, numbers, and spaces.
    "role": "string",             # Player role is usually a categorical string (e.g., "Batsman", "Bowler").     
    "venue": "string"             # Venue is a string, usually the name of the stadium or city.
}


career_data_t20=pd.read_csv(CAREER_T20_PATH,dtype=career_dict_t20)
venue_data_t20=pd.read_csv(VENUE_T20_PATH,dtype=venue_dict_t20)
recent_data_t20=pd.read_csv(RECENT_T20_PATH,dtype=recent_dict_t20)
player_match_data_t20=pd.read_csv(PLAYER_MATCH_DATA_T20_PATH,dtype=player_dict_t20)

def generate_tuple_from_data(data: pd.DataFrame, player_id: str, match_id: str) -> Tuple:
    """
    Generate a tuple from the given data based on player_id and match_id.
    If no matching data is found, return a tuple of length 10 filled with 0s.
    """
    matching_data = data[(data['player_id'] == player_id) & (data['match_id'] == match_id)]
    
    if matching_data.empty:
        print(f"No matching data found for player_id={player_id} and match_id={match_id}")  # Debugging line
        return tuple([0] * (len(data.columns) - 2))  # Return a tuple with zeros if no match is found (excluding player_id and match_id)
    
    # Extract the relevant data as a tuple (excluding player_id and match_id)
    return tuple(matching_data.iloc[0].drop(['player_id', 'match_id']).values)

def calculate_player_features_odi(player_id: str, match_date: str, venue: str, feature_names: Dict[str, List[str]]) -> List[float]:
    """
    Calculate the feature vector for a player based on player_id, match_date, and venue.
    This should return a list of features (numerical values) for the player.
    """
    # Convert the 'date' column to datetime format for easier comparison
    player_match_data_odi['date'] = pd.to_datetime(player_match_data_odi['date'])
    input_date = pd.to_datetime(match_date)
    
    # Filter player match data for the given player_id
    player_data = player_match_data_odi[player_match_data_odi['player_id'] == player_id]
    
    # Try to find the match_id with the closest date <= input date (regardless of venue)
    try:
        match_id_1 = player_data[player_data['date'] <= input_date].sort_values(by='date', ascending=False).iloc[0]['match_id']
    except IndexError:
        match_id_1 = None  # No match found for career stats
    
    # Try to find the match_id with the closest date <= input date and matching the input venue
    try:
        match_id_2 = player_data[(player_data['date'] <= input_date) & (player_data['venue'] == venue)].sort_values(by='date', ascending=False).iloc[0]['match_id']
    except IndexError:
        match_id_2 = None  # No match found for recent form or venue

    # Initialize tuples to be empty in case match_ids can't be determined
    career_tuple = tuple([0] * (14 - 2))
    recent_form_tuple = tuple([0] * (14 - 2))
    venue_tuple = tuple([0] * (14 - 2))

    # Generate the career tuple only if match_id_1 is valid
    if match_id_1:
        career_tuple = generate_tuple_from_data(career_data_odi, player_id, match_id_1)
    
    # Generate the recent form tuple only if match_id_2 is valid
        recent_form_tuple = generate_tuple_from_data(recent_data_odi, player_id, match_id_1)
    
    # Generate the venue tuple only if match_id_2 is valid (because match_id_2 is venue-specific)
    if match_id_2:
        venue_tuple = generate_tuple_from_data(venue_data_odi, player_id, match_id_2)
    
    # Combine the tuples to form the feature vector
    feature_vector = list(career_tuple) + list(recent_form_tuple) + list(venue_tuple)
    
    return feature_vector

def calculate_player_features_test(player_id: str, match_date: str, venue: str, feature_names: Dict[str, List[str]]) -> List[float]:
    """
    Calculate the feature vector for a player based on player_id, match_date, and venue.
    This should return a list of features (numerical values) for the player.
    """
    # Convert the 'date' column to datetime format for easier comparison
    player_match_data_test['date'] = pd.to_datetime(player_match_data_test['date'])
    input_date = pd.to_datetime(match_date)
    
    # Filter player match data for the given player_id
    player_data = player_match_data_test[player_match_data_test['player_id'] == player_id]
    
    # Try to find the match_id with the closest date <= input date (regardless of venue)
    try:
        match_id_1 = player_data[player_data['date'] <= input_date].sort_values(by='date', ascending=False).iloc[0]['match_id']
    except IndexError:
        match_id_1 = None  # No match found for career stats
    
    # Try to find the match_id with the closest date <= input date and matching the input venue
    try:
        match_id_2 = player_data[(player_data['date'] <= input_date) & (player_data['venue'] == venue)].sort_values(by='date', ascending=False).iloc[0]['match_id']
    except IndexError:
        match_id_2 = None  # No match found for recent form or venue

    # Initialize tuples to be empty in case match_ids can't be determined
    career_tuple = tuple([0] * (12 - 2))
    recent_form_tuple = tuple([0] * (12 - 2))
    venue_tuple = tuple([0] * (12 - 2))

    # Generate the career tuple only if match_id_1 is valid
    if match_id_1:
        career_tuple = generate_tuple_from_data(career_data_test, player_id, match_id_1)
    
    # Generate the recent form tuple only if match_id_2 is valid
        recent_form_tuple = generate_tuple_from_data(recent_data_test, player_id, match_id_1)
    
    # Generate the venue tuple only if match_id_2 is valid (because match_id_2 is venue-specific)
    if match_id_2:
        venue_tuple = generate_tuple_from_data(venue_data_test, player_id, match_id_2)
    
    # Combine the tuples to form the feature vector
    feature_vector = list(career_tuple) + list(recent_form_tuple) + list(venue_tuple)
    
    return feature_vector

def calculate_player_features_t20(player_id: str, match_date: str, venue: str, feature_names: Dict[str, List[str]]) -> List[float]:
    """
    Calculate the feature vector for a player based on player_id, match_date, and venue.
    This should return a list of features (numerical values) for the player.
    """
    # Convert the 'date' column to datetime format for easier comparison
    player_match_data_t20['date'] = pd.to_datetime(player_match_data_t20['date'])
    input_date = pd.to_datetime(match_date)
    
    # Filter player match data for the given player_id
    player_data = player_match_data_t20[player_match_data_t20['player_id'] == player_id]
    
    # Try to find the match_id with the closest date <= input date (regardless of venue)
    try:
        match_id_1 = player_data[player_data['date'] <= input_date].sort_values(by='date', ascending=False).iloc[0]['match_id']
    except IndexError:
        match_id_1 = None  # No match found for career stats
    
    # Try to find the match_id with the closest date <= input date and matching the input venue
    try:
        match_id_2 = player_data[(player_data['date'] <= input_date) & (player_data['venue'] == venue)].sort_values(by='date', ascending=False).iloc[0]['match_id']
    except IndexError:
        match_id_2 = None  # No match found for recent form or venue

    # Initialize tuples to be empty in case match_ids can't be determined
    career_tuple = tuple([0] * (15 - 2))
    recent_form_tuple = tuple([0] * (15 - 2))
    venue_tuple = tuple([0] * (15 - 2))

    # Generate the career tuple only if match_id_1 is valid
    if match_id_1:
        career_tuple = generate_tuple_from_data(career_data_t20, player_id, match_id_1)
    
    # Generate the recent form tuple only if match_id_2 is valid
        recent_form_tuple = generate_tuple_from_data(recent_data_t20, player_id, match_id_1)
    
    # Generate the venue tuple only if match_id_2 is valid (because match_id_2 is venue-specific)
    if match_id_2:
        venue_tuple = generate_tuple_from_data(venue_data_t20, player_id, match_id_2)
    
    # Combine the tuples to form the feature vector
    feature_vector = list(career_tuple) + list(recent_form_tuple) + list(venue_tuple)
    
    return feature_vector

def generate_features_for_all_players_odi(players_data: List[dict], match_date: str, venue: str) -> pd.DataFrame:
    """
    Generate feature vectors for all players based on the provided list of player data, match date, and venue.
    
    Returns:
    - a DataFrame with player_id, player_name, and corresponding feature values.
    """
    
    # Extract feature names by removing player_id and match_id
    career_feature_names = [col for col in career_data_odi.columns if col not in ['player_id', 'match_id']]
    recent_feature_names = [col for col in recent_data_odi.columns if col not in ['player_id', 'match_id']]
    venue_feature_names = [col for col in venue_data_odi.columns if col not in ['player_id', 'match_id']]
    
    # Combine all feature names
    all_feature_names = career_feature_names + recent_feature_names + venue_feature_names
    
    feature_rows = []  # List to store feature rows for DataFrame
    
    # Loop through each player in the list
    for player in players_data:
        player_id = player['player_id']
        player_name = player['player_name']
        
        # Step 1: Calculate feature vector for the player
        feature_vector = calculate_player_features_odi(player_id, match_date, venue, all_feature_names)
        
        # Step 2: Append each feature with the player_id, player_name, and corresponding feature name to feature_rows
        for i, feature_value in enumerate(feature_vector):
            feature_name = all_feature_names[i]  # Get actual feature name
            feature_rows.append({
                'player_id': player_id,
                'player_name': player_name,
                'feature_name': feature_name,
                'feature_value': feature_value
            })
    
    # Step 3: Convert the feature rows to a pandas DataFrame
    features_df = pd.DataFrame(feature_rows)

    # Pivot the DataFrame to get the desired output format: player_id, player_name, feature_1, feature_2, ...
    features_df_pivot = features_df.pivot_table(index=['player_id', 'player_name'], columns='feature_name', values='feature_value', aggfunc='first')

    # Reset index to flatten the DataFrame
    features_df_pivot.reset_index(inplace=True)

    # Explicitly reorder columns to maintain the order of features as in 'all_feature_names'
    features_df_pivot = features_df_pivot[['player_id', 'player_name'] + all_feature_names]

    return features_df_pivot

def generate_features_for_all_players_test(players_data: List[dict], match_date: str, venue: str) -> pd.DataFrame:
    """
    Generate feature vectors for all players based on the provided list of player data, match date, and venue.
    Returns a DataFrame with player_id, player_name, and corresponding feature values.
    """

    # Extract feature names by removing player_id and match_id
    career_feature_names = [col for col in career_data_test.columns if col not in ['player_id', 'match_id']]
    recent_feature_names = [col for col in recent_data_test.columns if col not in ['player_id', 'match_id']]
    venue_feature_names = [col for col in venue_data_test.columns if col not in ['player_id', 'match_id']]
    
    # Combine all feature names
    all_feature_names = career_feature_names + recent_feature_names + venue_feature_names
    
    feature_rows = []  # List to store feature rows for DataFrame
    
    # Loop through each player in the list
    for player in players_data:
        player_id = player['player_id']
        player_name = player['player_name']
        
        # Step 1: Calculate feature vector for the player
        feature_vector = calculate_player_features_test(player_id, match_date, venue, all_feature_names)
        
        # Step 2: Append each feature with the player_id, player_name, and corresponding feature name to feature_rows
        for i, feature_value in enumerate(feature_vector):
            feature_name = all_feature_names[i]  # Get actual feature name
            feature_rows.append({
                'player_id': player_id,
                'player_name': player_name,
                'feature_name': feature_name,
                'feature_value': feature_value
            })
    
    # Step 3: Convert the feature rows to a pandas DataFrame
    features_df = pd.DataFrame(feature_rows)

    # Pivot the DataFrame to get the desired output format: player_id, player_name, feature_1, feature_2, ...
    features_df_pivot = features_df.pivot_table(index=['player_id', 'player_name'], columns='feature_name', values='feature_value', aggfunc='first')

    # Reset index to flatten the DataFrame
    features_df_pivot.reset_index(inplace=True)

    # Explicitly reorder columns to maintain the order of features as in 'all_feature_names'
    features_df_pivot = features_df_pivot[['player_id', 'player_name'] + all_feature_names]

    return features_df_pivot

def generate_features_for_all_players_t20(players_data: List[dict], match_date: str, venue: str) -> pd.DataFrame:
    """
    Generate feature vectors for all players based on the provided list of player data, match date, and venue.
    Returns a DataFrame with player_id, player_name, and corresponding feature values.
    """
    
    # Extract feature names by removing player_id and match_id
    career_feature_names = [col for col in career_data_t20.columns if col not in ['player_id', 'match_id']]
    recent_feature_names = [col for col in recent_data_t20.columns if col not in ['player_id', 'match_id']]
    venue_feature_names = [col for col in venue_data_t20.columns if col not in ['player_id', 'match_id']]
    
    # Combine all feature names
    all_feature_names = career_feature_names + recent_feature_names + venue_feature_names
    
    feature_rows = []  # List to store feature rows for DataFrame
    
    # Loop through each player in the list
    for player in players_data:
        player_id = player['player_id']
        player_name = player['player_name']
        
        # Step 1: Calculate feature vector for the player
        feature_vector = calculate_player_features_t20(player_id, match_date, venue, all_feature_names)
        
        # Step 2: Append each feature with the player_id, player_name, and corresponding feature name to feature_rows
        for i, feature_value in enumerate(feature_vector):
            feature_name = all_feature_names[i]  # Get actual feature name
            feature_rows.append({
                'player_id': player_id,
                'player_name': player_name,
                'feature_name': feature_name,
                'feature_value': feature_value
            })
    
    # Step 3: Convert the feature rows to a pandas DataFrame
    features_df = pd.DataFrame(feature_rows)

    # Pivot the DataFrame to get the desired output format: player_id, player_name, feature_1, feature_2, ...
    features_df_pivot = features_df.pivot_table(index=['player_id', 'player_name'], columns='feature_name', values='feature_value', aggfunc='first')

    # Reset index to flatten the DataFrame
    features_df_pivot.reset_index(inplace=True)

    # Explicitly reorder columns to maintain the order of features as in 'all_feature_names'
    features_df_pivot = features_df_pivot[['player_id', 'player_name'] + all_feature_names]
    
    return features_df_pivot

def predict_fantasy_points_for_all_players_odi(players_df: pd.DataFrame) -> pd.DataFrame:
    """
    Predict the fantasy points for all players given their feature vectors.
    
    Args:
    - players_df (pd.DataFrame): A DataFrame containing player data (player_id, player_name, and feature columns).
    
    Returns:
    - pd.DataFrame: A DataFrame with player_id, player_name, and predicted fantasy points for each player.
    """
    try:
        # Load the pre-trained model (replace with the correct path to your model)
        with open(MODEL_ARTIFACTS["ODI"], 'rb') as model_file:
            model = pickle.load(model_file)  # Load the model using pickle

        # Extract features from the DataFrame (assuming the feature columns start from the 3rd column onward)
        feature_columns = players_df.columns[2:]  # Skip player_id and player_name

        # Predict fantasy points for all players
        scaler=StandardScaler()
        players_df[feature_columns]=scaler.fit_transform(players_df[feature_columns])
        predicted_fantasy_points = model.predict(players_df[feature_columns])

        # Add predicted fantasy points to the DataFrame
        players_df['predicted_fantasy_points'] = predicted_fantasy_points

        # Create the resulting DataFrame with only player_id, player_name, and predicted_fantasy_points
        results_df = players_df[['player_id', 'player_name', 'predicted_fantasy_points']]
        
        return results_df
    
    except Exception as e:
        
        print(f"Error while loading model or predicting fantasy points: {e}")
        return pd.DataFrame(columns=['player_id', 'player_name', 'predicted_fantasy_points'])

def predict_fantasy_points_for_all_players_test(players_df: pd.DataFrame) -> pd.DataFrame:
    """
    Predict the fantasy points for all players given their feature vectors.
    
    Args:
    - players_df (pd.DataFrame): A DataFrame containing player data (player_id, player_name, and feature columns).
    
    Returns:
    - pd.DataFrame: A DataFrame with player_id, player_name, and predicted fantasy points for each player.
    """
    try:
        # print("Starting the prediction process...")

        # Load the pre-trained model (replace with the correct path to your model)
        # print("Loading the pre-trained model...")
        with open(MODEL_ARTIFACTS["Test"], 'rb') as model_file:
            model = pickle.load(model_file)  # Load the model using pickle
        # print("Model loaded successfully.")

        # Extract features from the DataFrame (assuming the feature columns start from the 3rd column onward)
        feature_columns = players_df.columns[2:]  # Skip player_id and player_name
        # print(f"Extracted feature columns: {feature_columns}")

        # Check if the correct number of features are present
        # print(f"Number of features in input DataFrame: {len(feature_columns)}")
        # print("Input DataFrame preview:")
        # print(players_df.head())

        # Predict fantasy points for all players
        # print("Predicting fantasy points for all players...")
        scaler=StandardScaler()
        players_df[feature_columns]=scaler.fit_transform(players_df[feature_columns])
        predicted_fantasy_points = model.predict(players_df[feature_columns])
        # print(f"Predictions completed. Number of predictions: {len(predicted_fantasy_points)}")

        # Add predicted fantasy points to the DataFrame
        players_df['predicted_fantasy_points'] = predicted_fantasy_points
        # print("Predicted fantasy points added to DataFrame.")

        # Create the resulting DataFrame with only player_id, player_name, and predicted_fantasy_points
        results_df = players_df[['player_id', 'player_name', 'predicted_fantasy_points']]
        # print("Result DataFrame created with player_id, player_name, and predicted_fantasy_points.")

        # Display preview of results
        # print("Result DataFrame preview:")
        # print(results_df.head())
        
        return results_df
    
    except Exception as e:
        
        print(f"Error while loading model or predicting fantasy points: {e}")
        return pd.DataFrame(columns=['player_id', 'player_name', 'predicted_fantasy_points'])

def predict_fantasy_points_for_all_players_t20(players_df: pd.DataFrame) -> pd.DataFrame:
    """
    Predict the fantasy points for all players given their feature vectors.
    
    Args:
    - players_df (pd.DataFrame): A DataFrame containing player data (player_id, player_name, and feature columns).
    
    Returns:
    - pd.DataFrame: A DataFrame with player_id, player_name, and predicted fantasy points for each player.
    """
    try:
        # print("Starting the prediction process...")

        # Load the pre-trained model (replace with the correct path to your model)
        # print("Loading the pre-trained model...")
        with open(MODEL_ARTIFACTS["T20"], 'rb') as model_file:
            model = pickle.load(model_file)  # Load the model using pickle
        # print("Model loaded successfully.")

        # Extract features from the DataFrame (assuming the feature columns start from the 3rd column onward)
        feature_columns = players_df.columns[2:]  # Skip player_id and player_name
        # print(f"Extracted feature columns: {feature_columns}")

        # Check if the correct number of features are present
        # print(f"Number of features in input DataFrame: {len(feature_columns)}")
        # print("Input DataFrame preview:")
        # print(players_df.head())

        # Predict fantasy points for all players
        # print("Predicting fantasy points for all players...")
        scaler=StandardScaler()
        players_df[feature_columns]=scaler.fit_transform(players_df[feature_columns])
        predicted_fantasy_points = model.predict(players_df[feature_columns])
        # print(f"Predictions completed. Number of predictions: {len(predicted_fantasy_points)}")

        # Add predicted fantasy points to the DataFrame
        players_df['predicted_fantasy_points'] = predicted_fantasy_points
        # print("Predicted fantasy points added to DataFrame.")

        # Create the resulting DataFrame with only player_id, player_name, and predicted_fantasy_points
        results_df = players_df[['player_id', 'player_name', 'predicted_fantasy_points']]
        # print("Result DataFrame created with player_id, player_name, and predicted_fantasy_points.")

        # Display preview of results
        # print("Result DataFrame preview:")
        # print(results_df.head())
        
        return results_df
    
    except Exception as e:
        
        print(f"Error while loading model or predicting fantasy points: {e}")
        return pd.DataFrame(columns=['player_id', 'player_name', 'predicted_fantasy_points'])


def generate_recommended_team(players: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generate a recommended team based on predicted fantasy points and team diversity.
    The team should contain 11 players with the highest predicted fantasy points, while maintaining role diversity 
    and ensuring no more than 5 players from one team.
    
    Args:
    - players (List[Dict[str, Any]]): List of players with player_id, player_name, team_name, role, and predicted_fantasy_points.
    
    Returns:
    - List[Dict[str, Any]]: A list of 11 recommended players for the dream team, including their role and predicted fantasy points.
    """
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

        logging.debug(selected_players)
        while len(selected_players) < 11:
            next_player = remaining_players.pop(0)
            selected_players.append(next_player)
            logging.debug(next_player)

        # Step 3: Ensure team diversity (max 5 players from one team)
        team_counts = pd.DataFrame(selected_players)["team_name"].value_counts()
        if team_counts.max() == 11:

            other_team = [team for team in pd.DataFrame(selected_players)["team_name"].unique() if team not in team_counts.index][0]
            lowest_fantasy_player = min(selected_players, key=lambda x: x["predicted_fantasy_points"])
            replacement_player = max(
                [p for p in players if p["team_name"] == other_team and p not in selected_players],
                key=lambda x: x["predicted_fantasy_points"]
            )
            selected_players.remove(lowest_fantasy_player)
            selected_players.append(replacement_player)
        # Step 4: Sort selected players by predicted fantasy points
        selected_players.sort(key=lambda x: x["predicted_fantasy_points"], reverse=True)

        # Return the selected players as the final recommended team
        return selected_players

    except Exception as e:
        print(f"Error in generating recommended team: {e}")
        return []


def generate_dream_team(players_data: List[dict], match_date: str, venue: str, tournament_type: str, need_justification: bool=True) -> List[Dict[str, Any]]:
    """
    Generate the recommended dream team for a given squad, match date, venue, and tournament type.
    
    Args:
    - players_data (List[dict]): List of players with player_id, player_name, team_name, role, etc.
    - match_date (str): The match date in 'YYYY-MM-DD' format.
    - venue (str): The venue of the match.
    - tournament_type (str): Type of tournament ('ODI', 'T20', etc.)
    
    Returns:
    - List[Dict[str, Any]]: The dream team with player_name, role, predicted_points, isCaptain, isViceCaptain, and team_name.
    """
    if(tournament_type.lower()=='odi'):
        players_df = generate_features_for_all_players_odi(players_data, match_date, venue)
    elif(tournament_type.lower()=='test'):
        players_df = generate_features_for_all_players_test(players_data, match_date, venue)
    elif(tournament_type.lower()=='t20'):
        players_df = generate_features_for_all_players_t20(players_data, match_date, venue)
    # Generate player features based on the provided match date and venue
    
    players_copy = players_df.copy(deep=True)

    # Predict the fantasy points for all players
    if(tournament_type.lower()=='odi'):
        predicted_points_df = predict_fantasy_points_for_all_players_odi(players_df)
    elif(tournament_type.lower()=='test'):
        predicted_points_df = predict_fantasy_points_for_all_players_test(players_df)
    elif(tournament_type.lower()=='t20'):
        predicted_points_df = predict_fantasy_points_for_all_players_t20(players_df)
    
    # Convert players_data into a DataFrame to easily join on player_id
    players_data_df = pd.DataFrame(players_data)
    
    # Join the predicted points with players_data to get role and team_name
    merged_df = pd.merge(predicted_points_df, players_data_df[['player_id', 'role', 'team_name']], on='player_id', how='left')
    
    # Prepare the data for team generation (convert to list of dictionaries)
    players = merged_df.to_dict(orient='records')
    
    # Generate the recommended team
    recommended_team = generate_recommended_team(players)
    
    # Sort players by predicted points in descending order
    recommended_team.sort(key=lambda x: x['predicted_fantasy_points'], reverse=True)
    
    # Assign captain and vice-captain roles
    if len(recommended_team) > 0:
        recommended_team[0]['is_captain'] = True
        recommended_team[0]['is_vice_captain'] = False
    if len(recommended_team) > 1:
        recommended_team[1]['is_captain'] = False
        recommended_team[1]['is_vice_captain'] = True
    # Mark the rest of the players as False for both captain and vice-captain
    for player in recommended_team[2:]:
        player['is_captain'] = False
        player['is_vice_captain'] = False
    
    # Rename predicted_fantasy_points to predicted_points after generating the team
    for player in recommended_team:
        player['predicted_points'] = player.pop('predicted_fantasy_points')
        # ----------------------------------------------------------------------------------

    if need_justification:
        try:
            with open(MODEL_ARTIFACTS[tournament_type], 'rb') as model_file:
                model = pickle.load(model_file)
            recommended_team = generate_player_details_with_shap_values(recommended_team, players_copy, players_df,tournament_type=tournament_type, model=model)

        except Exception as e:
            logging.exception(f"generating_dream_team(): {e}")
    else:
        for player in recommended_team:
            player['shap_values'] = []
            player['career'] = [0]*13
            player['recent_form'] = []*13
            player['venue'] = []*13

    return recommended_team


def generate_player_details_with_shap_values(
    recommended_team: List[Dict[str, Any]],
    players_original: pd.DataFrame,
    players_df: pd.DataFrame,
    tournament_type: str,
    model
) -> List[Dict[str, Any]]:
    """
    Enrich each player in the recommended team with SHAP values and additional feature details.
    
    Args:
    - recommended_team (List[Dict[str, Any]]): The recommended team with basic player info.
    - players_df (pd.DataFrame): DataFrame containing all player features.
    - model: Trained model used for predicting fantasy points.
        
    Returns:
    - List[Dict[str, Any]]: The updated team with additional details.
    """
    # Define non-feature columns to exclude
    non_feature_cols = ['player_id', 'player_name', 'team_name', 'role', 'predicted_fantasy_points']
    # Define feature columns used by the model
    feature_cols = [col for col in players_original.columns if col not in non_feature_cols]
    # Extract player IDs from the recommended team
    team_player_ids = [player['player_id'] for player in recommended_team]
    
    
    try:
        # Filter the players_original for only the recommended team players
        team_features = players_original[players_original['player_id'].isin(team_player_ids)][['player_id'] + feature_cols].reset_index(drop=True)
        
        # Ensure the order of team_features matches the recommended_team
        team_features = team_features.set_index('player_id').loc[team_player_ids].reset_index(drop=True)
        
        # Initialize SHAP Explainer
        explainer = shap.KernelExplainer(model.predict, players_df[feature_cols])
            
        # Compute SHAP values for the team
        shap_values = explainer(team_features)

        # Iterate through each player in the recommended team
        for idx, player in enumerate(recommended_team):
            player_id = player['player_id']
            
            # Extract SHAP values for the player
            player_shap_values = shap_values[idx].values.tolist()
            if len(player_shap_values) != SHAP_VALUES_LIST_LEN[tournament_type][0]:
                logging.warning(f"Player ID {player_id} has {len(player_shap_values)} SHAP values instead of {SHAP_VALUES_LIST_LEN[tournament_type][0]}.")
            player['shap_values'] = [
                sum(player_shap_values[:SHAP_VALUES_LIST_LEN[tournament_type][1]]),
                sum(player_shap_values[SHAP_VALUES_LIST_LEN[tournament_type][1]: 2 * SHAP_VALUES_LIST_LEN[tournament_type][1]]),
                sum(player_shap_values[2 * SHAP_VALUES_LIST_LEN[tournament_type][1]: 3 * SHAP_VALUES_LIST_LEN[tournament_type][1]]),
                ]  # List of sum of SHAP values for career, recent_form and venue
            
            # Extract the player's feature row
            player_feature_row = team_features.iloc[idx]
            
            # Extract Career Features
            career_features = [
                float(player_feature_row[col]) for col in team_features.columns
                if col.startswith('career_')
            ]
            if len(career_features) != SHAP_VALUES_LIST_LEN[tournament_type][1]:
                logging.warning(f"Player ID {player_id} has {len(career_features)} career features instead of {SHAP_VALUES_LIST_LEN[tournament_type][1]}.")
            player['career'] = career_features  # List of career features
            
            # Extract Recent Features
            recent_features = [
                float(player_feature_row[col]) for col in team_features.columns
                if col.startswith('recent_')
            ]
            if len(recent_features) != SHAP_VALUES_LIST_LEN[tournament_type][1]:
                logging.warning(f"Player ID {player_id} has {len(recent_features)} recent features instead of {SHAP_VALUES_LIST_LEN[tournament_type][1]}.")
            player['recent_form'] = recent_features  # List of recent features
            
            # Extract Venue Features
            venue_features = [
                float(player_feature_row[col]) for col in team_features.columns
                if col.startswith('venue_')
            ]
            if len(venue_features) != SHAP_VALUES_LIST_LEN[tournament_type][1]:
                logging.warning(f"Player ID {player_id} has {len(venue_features)} venue features instead of {SHAP_VALUES_LIST_LEN[tournament_type][1]}.")
            player['venue'] = venue_features  # List of venue features

        return recommended_team
    
    except Exception as e:
        logging.exception(f"Error in generate_player_details_with_shap_values: {e}")
        return recommended_team  # Return the team without additional details in case of failure
