import pandas as pd
import numpy as np

def load_data():
    """Load the necessary CSV files into DataFrames."""
    player_match_data = pd.read_csv('../../../CSVs/Final/ODI/player_match_data_odi.csv')
    career_data = pd.read_csv('../../../CSVs/Final/ODI/career_odi.csv')
    recent_data = pd.read_csv('../../../CSVs/Final/ODI/recent_odi.csv')
    venue_data = pd.read_csv('../../../CSVs/Final/ODI/venue_odi.csv')
    return player_match_data, career_data, recent_data, venue_data

def find_closest_match(player_match_data, player_id, date):
    """Find the closest match for the given player_id and date."""
    player_data = player_match_data[player_match_data['player_id'] == player_id]
    player_data['date'] = pd.to_datetime(player_data['date'])
    target_date = pd.to_datetime(date)
    closest_match_idx = (player_data['date'] - target_date).abs().idxmin()
    return player_data.loc[closest_match_idx]

def find_match_data(tournament_type, date, venue, team_name, player_id):
    """Find and combine match data from multiple sources."""
    # Load data
    player_match_data_df, career_odi_df, recent_odi_df, venue_odi_df = load_data()

    # Find closest match
    closest_match = find_closest_match(player_match_data_df, player_id, date)
    match_id = closest_match['match_id']

    # Check venue match
    if closest_match['venue'] != venue:
        return "No matching venue found for the given date and player."

    # Fetch corresponding tuples
    career_tuple = career_odi_df[(career_odi_df['match_id'] == match_id) & (career_odi_df['player_id'] == player_id)].iloc[0]
    recent_tuple = recent_odi_df[(recent_odi_df['match_id'] == match_id) & (recent_odi_df['player_id'] == player_id)].iloc[0]
    venue_tuple = venue_odi_df[(venue_odi_df['match_id'] == match_id) & (venue_odi_df['player_id'] == player_id)].iloc[0]

    # Combine the tuples
    combined_result = pd.concat([career_tuple, recent_tuple[2:], venue_tuple[2:]])

    # Return result as a tuple
    return tuple(combined_result)

# Input parameters
tournament_type = "ODI"
date = "2024-07-07"
venue = "Radlett Cricket Club, Radlett"
team_name = "Sunrisers"
player_id = "9d9edf14"

# Call the function and print the result
result = find_match_data(tournament_type, date, venue, team_name, player_id)
print(result)
