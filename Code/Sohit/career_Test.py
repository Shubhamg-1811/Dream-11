import pandas as pd

# Load the dataset
df = pd.read_csv('../../CSVs/fantasy_points/Test_MatchWise_fantasy_points.csv', low_memory=False)

# Ensure the date column is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Sort the dataframe by date to ensure correct accumulation
df = df.sort_values(by='date')

# Initialize a hashmap (dictionary) to store cumulative statistics for each player
player_stats = {}

# Initialize columns for career statistics
df['career_batsman_100s_test'] = 0
df['career_batsman_50s_test'] = 0
df['career_batsman_average_runs_test'] = 0
df['career_batsman_total_runs_test'] = 0
df['career_bowler_average_test'] = 0
df['career_bowler_wickets_test'] = 0
df['career_fielder_total_catches_test'] = 0
df['career_fielder_total_runouts_test'] = 0
df['career_batsman_total_fours_test'] = 0
df['career_batsman_total_sixes_test'] = 0
# df['batsman_strike_rate'] = 0
# df['bowler_economy_rate'] = 0

# Counter for progress tracking
processed_rows = 0

# Process each row in the dataframe
for index, row in df.iterrows():
    player_id = row['player_id']
    
    # If the player is not in the hashmap, initialize their stats
    if player_id not in player_stats:
        player_stats[player_id] = {
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
            "total_fours": 0,
            "total_sixes": 0,
        }

    # Get the cumulative stats before adding the current match's data
    stats = player_stats[player_id]
    df.at[index, 'career_batsman_100s_test'] = stats['hundreds']
    df.at[index, 'career_batsman_50s_test'] = stats['fifties']
    df.at[index, 'career_batsman_average_runs_test'] = stats['total_runs'] / stats['matches_for_average'] if stats['matches_for_average'] > 0 else 0
    df.at[index, 'career_batsman_total_runs_test'] = stats['total_runs']
    df.at[index, 'career_bowler_average_test'] = (stats['total_runs_conceded'] / stats['total_wickets']) if stats['total_wickets'] > 0 else 0
    df.at[index, 'career_bowler_wickets_test'] = stats['total_wickets']
    df.at[index, 'career_fielder_total_catches_test'] = stats['total_catches']
    df.at[index, 'career_fielder_total_runouts_test'] = stats['total_runouts']
    df.at[index, 'career_batsman_total_fours_test'] = stats['total_fours']
    df.at[index, 'career_batsman_total_sixes_test'] = stats['total_sixes']
    # df.at[index, 'batsman_strike_rate'] = (stats['total_runs'] / stats['total_balls'] * 100) if stats['total_balls'] > 0 else 0
    # df.at[index, 'bowler_economy_rate'] = (stats['total_runs_conceded'] / (stats['total_balls_bowled'] / 6)) if stats['total_balls_bowled'] > 0 else 0

    # After writing to the DataFrame, update the cumulative stats with the current match's data
    stats['total_runs'] += row['runs_scored']
    stats['total_balls'] += row['balls_faced']
    stats['matches_for_average'] += 1 
    stats['hundreds'] += 1 if row['runs_scored'] >= 100 else 0
    stats['fifties'] += 1 if row['runs_scored'] >= 50 else 0
    stats['total_runs_conceded'] += row['runs_conceded']
    stats['total_balls_bowled'] += row['balls_bowled']
    stats['total_wickets'] += row['wickets']
    stats['total_catches'] += row['no_of_catches']
    stats['total_runouts'] += row['runouts']
    stats['total_fours'] += row['no_of_fours']
    stats['total_sixes'] += row['no_of_sixes']

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
df.to_csv('../../CSVs/Final/Test/career_test.csv', index=False)

print("Career statistics added to the DataFrame with optimized performance!")
