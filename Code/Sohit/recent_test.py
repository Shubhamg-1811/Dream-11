import pandas as pd
from collections import deque

# Load your dataset
df = pd.read_csv('../../CSVs/fantasy_points/Test_MatchWise_fantasy_points.csv', low_memory=False)

# Ensure the date column is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Sort the dataframe by date to ensure correct order of matches
df = df.sort_values(by='date')

# Initialize a dictionary to store sliding window (queue) for each player
player_queues = {}

# Initialize columns for recent form metrics with updated names
df['recent_batsman_total_runs_test'] = 0
df['recent_batsman_average_runs_test'] = 0.
df['recent_batsman_total_fours_test'] = 0
df['recent_batsman_total_sixes_test'] = 0
df['recent_batsman_50s_test'] = 0
df['recent_batsman_100s_test'] = 0
df['recent_bowler_average_test'] = 0
df['recent_bowler_wickets_test'] = 0
df['recent_fielder_total_catches_test'] = 0
df['recent_fielder_runouts_test'] = 0
# df['recent_strike_rate_test'] = 0
# df['recent_economy_rate_test'] = 0

# Initialize progress counter
processed_rows = 0

# Process each row in the dataset
for index, row in df.iterrows():
    player_id = row['player_id']

    # Initialize the queue for the player if it doesn't exist
    if player_id not in player_queues:
        player_queues[player_id] = {
            "runs": deque(),
            "balls": deque(),
            "fours": deque(),
            "sixes": deque(),
            "fifties": deque(),
            "hundreds": deque(),
            "runs_conceded": deque(),
            "balls_bowled": deque(),
            "wickets": deque(),
            "catches": deque(),
            "runouts": deque(),
        }

    # Get the player's queue
    queues = player_queues[player_id]

    # Calculate recent form metrics
    recent_total_runs = sum(queues["runs"])
    recent_total_balls = sum(queues["balls"])
    recent_4s = sum(queues["fours"])
    recent_6s = sum(queues["sixes"])
    recent_50s = sum(queues["fifties"])
    recent_100s = sum(queues["hundreds"])
    recent_runs_conceded = sum(queues["runs_conceded"])
    recent_balls_bowled = sum(queues["balls_bowled"])
    recent_wickets = sum(queues["wickets"])
    recent_catches = sum(queues["catches"])
    recent_runouts = sum(queues["runouts"])

    # Calculate additional metrics
    # recent_economy_rate = (recent_runs_conceded / (recent_balls_bowled / 6)) if recent_balls_bowled > 0 else 0
    recent_bowler_average = (recent_runs_conceded / recent_wickets) if recent_wickets > 0 else 0

    # Update recent form metrics in the DataFrame
    df.at[index, 'recent_batsman_total_runs_test'] = recent_total_runs
    df.at[index, 'recent_batsman_average_runs_test'] = recent_total_runs / len(queues["runs"]) if len(queues["runs"]) > 0 else 0
    df.at[index, 'recent_batsman_total_fours_test'] = recent_4s
    df.at[index, 'recent_batsman_total_sixes_test'] = recent_6s
    df.at[index, 'recent_batsman_50s_test'] = recent_50s
    df.at[index, 'recent_batsman_100s_test'] = recent_100s
    df.at[index, 'recent_bowler_average_test'] = recent_bowler_average
    df.at[index, 'recent_bowler_wickets_test'] = recent_wickets
    df.at[index, 'recent_fielder_total_catches_test'] = recent_catches
    df.at[index, 'recent_fielder_runouts_test'] = recent_runouts

    # Add current match stats to the queue after calculating recent form
    queues["runs"].append(row['runs_scored'])
    queues["balls"].append(row['balls_faced'])
    queues["fours"].append(row['no_of_fours'])
    queues["sixes"].append(row['no_of_sixes'])
    
    queues["fifties"].append(1 if row['runs_scored'] >= 50 else 0)
    queues["hundreds"].append(1 if row['runs_scored'] >= 100 else 0)
    queues["runs_conceded"].append(row['runs_conceded'])
    queues["balls_bowled"].append(row['balls_bowled'])
    queues["wickets"].append(row['wickets'])
    queues["catches"].append(row['no_of_catches'])
    queues["runouts"].append(row['runouts'])

    # Maintain the size of the queue to a maximum of 5
    if len(queues["runs"]) > 5:
        queues["runs"].popleft()
        queues["balls"].popleft()
        queues["fours"].popleft()
        queues["sixes"].popleft()
        
        queues["fifties"].popleft()
        queues["hundreds"].popleft()
        queues["runs_conceded"].popleft()
        queues["balls_bowled"].popleft()
        queues["wickets"].popleft()
        queues["catches"].popleft()
        queues["runouts"].popleft()

    # Increment the progress counter
    processed_rows += 1

    # Print progress every 10,000 rows
    if processed_rows % 10000 == 0:
        print(f"Processed {processed_rows} rows...")


drop = ['player_name', 'team_name', 'runs_scored', 'balls_faced', 'no_of_fours', 'no_of_sixes',
        'no_of_catches', 'runouts', 'balls_bowled', 'dot_balls', 'wickets', 'LBWs/Bowled',
        'runs_conceded', 'stumpings', 'out', 'date', 'venue', 'match_type', 'gender', 'fantasy_points']
df = df.drop(columns=[col for col in drop if col in df.columns])

# Save the updated DataFrame to a new CSV file
df.to_csv('../../CSVs/Final/Test/recent_test.csv', index=False)

print("Recent form metrics added to the DataFrame with optimized performance!")
