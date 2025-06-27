import pandas as pd

# Load the dataset
df = pd.read_csv('../../CSVs/fantasy_points/Test_MatchWise_fantasy_points.csv')

# Ensure the date column is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Sort the dataframe by date to ensure correct accumulation
df = df.sort_values(by='date')


# Initialize a hashmap to store cumulative statistics for each player-venue combination
venue_player_stats = {}

# Initialize columns for venue-specific performance
df['venue_batsman_100s_test'] = 0
df['venue_batsman_50s_test'] = 0
df['venue_batsman_average_runs_test'] = 0
df['venue_batsman_total_runs_test'] = 0
df['venue_bowler_average_test'] = 0
df['venue_bowler_wickets_test'] = 0
df['venue_fielder_total_catches_test'] = 0
df['venue_fielder_total_runouts_test'] = 0
df['venue_batsman_total_fours_test'] = 0
df['venue_batsman_total_sixes_test'] = 0
# df['venue_batsman_strike_rate_test'] = 0
# df['venue_bowler_economy_rate_test'] = 0

# Counter for processed rows
processed_rows = 0

# Process each row in the dataset
for index, row in df.iterrows():
    player_id = row['player_id']
    venue = row['venue']
    
    # Create a unique key for the player-venue combination
    key = (player_id, venue)
    
    # If the key is not in the hashmap, initialize their stats
    if key not in venue_player_stats:
        venue_player_stats[key] = {
            "total_runs": 0,
            "total_balls": 0,
            "matches_for_average": 0,
            "hundreds": 0,
            "fifties": 0,
            "total_runs_conceded": 0,
            "total_balls_bowled": 0,
            "total_wickets": 0,
            "total_catches": 0,
            "total_runouts": 0,
            "total_4s": 0,
            "total_6s": 0,
        }

    # Get the cumulative stats for this player-venue combination
    stats = venue_player_stats[key]

    # Update the DataFrame with cumulative stats before adding the current match's data
    df.at[index, 'venue_batsman_100s_test'] = stats['hundreds']
    df.at[index, 'venue_batsman_50s_test'] = stats['fifties']
    df.at[index, 'venue_batsman_average_runs_test'] = stats['total_runs'] / stats['matches_for_average'] if stats['matches_for_average'] > 0 else 0
    df.at[index, 'venue_batsman_total_runs_test'] = stats['total_runs']
    df.at[index, 'venue_bowler_average_test'] = (stats['total_runs_conceded'] / stats['total_wickets']) if stats['total_wickets'] > 0 else 0
    df.at[index, 'venue_bowler_wickets_test'] = stats['total_wickets']
    df.at[index, 'venue_fielder_total_catches_test'] = stats['total_catches']
    df.at[index, 'venue_fielder_total_runouts_test'] = stats['total_runouts']
    df.at[index, 'venue_batsman_total_fours_test'] = stats['total_4s']
    df.at[index, 'venue_batsman_total_sixes_test'] = stats['total_6s']
    # df.at[index, 'batsman_strike_rate_at_venue'] = (stats['total_runs'] / stats['total_balls'] * 100) if stats['total_balls'] > 0 else 0
    # df.at[index, 'bowler_economy_rate_at_venue'] = (stats['total_runs_conceded'] / (stats['total_balls_bowled'] / 6)) if stats['total_balls_bowled'] > 0 else 0

    # After writing to the DataFrame, update the cumulative stats with the current match's data
    stats['total_runs'] += row['runs_scored']
    stats['total_balls'] += row['balls_faced']
    stats['matches_for_average'] += 1  # Assuming all matches are considered for average
    stats['hundreds'] += 1 if row['runs_scored'] >= 100 else 0
    stats['fifties'] += 1 if 50 <= row['runs_scored'] < 100 else 0  # Only count fifties if not hundreds
    stats['total_runs_conceded'] += row['runs_conceded']
    stats['total_balls_bowled'] += row['balls_bowled']
    stats['total_wickets'] += row['wickets']
    stats['total_catches'] += row['no_of_catches']
    stats['total_runouts'] += row['runouts']
    stats['total_4s'] += row['no_of_fours']
    stats['total_6s'] += row['no_of_sixes']

    # Increment the processed rows counter
    processed_rows += 1

    # Print progress every 10,000 rows
    if processed_rows % 10000 == 0:
        print(f"Processed {processed_rows} rows...")

drop = ['player_name', 'team_name', 'runs_scored', 'balls_faced', 'no_of_fours', 'no_of_sixes',
        'no_of_catches', 'runouts', 'balls_bowled', 'dot_balls', 'wickets', 'LBWs/Bowled',
        'runs_conceded', 'stumpings', 'out', 'date', 'venue', 'match_type', 'gender', 'fantasy_points']
df = df.drop(columns=[col for col in drop if col in df.columns])

# Save the updated DataFrame to a new CSV file
df.to_csv('../../CSVs/Final/Test/venue_test.csv', index=False)

print("Venue-specific performance added to the DataFrame with optimized performance!")
