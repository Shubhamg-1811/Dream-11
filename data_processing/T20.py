import pandas as pd
from collections import deque


def career_T20(input_file, output_file):
    """
    Processes a T20 match dataset and calculates cumulative career statistics for each player, saving the results to a new CSV file.

    This function computes cumulative statistics such as total runs, average, strike rate, centuries, fifties, wickets, and more 
    for each player across all matches in the input dataset. The results are appended to the dataset and saved to a new CSV file.

    Args:
        input_file (str): Path to the input CSV file containing match data.
        output_file (str): Path to the output CSV file where the updated dataset with career stats is saved.

    Returns:
        None: The function writes the results to the specified output CSV file.
    """
    # Load the dataset
    df = pd.read_csv(input_file, low_memory=False)

    # Ensure the date column is in datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Sort the dataframe by date to ensure correct accumulation
    df = df.sort_values(by='date')

    # Initialize a hashmap (dictionary) to store cumulative statistics for each player
    player_stats = {}

    # Initialize columns for career statistics
    df['career_batsman_total_runs_t20'] = 0
    df['career_batsman_100s_t20'] = 0
    df['career_batsman_50s_t20'] = 0
    df['career_batsman_30s_t20'] = 0
    df['career_batsman_total_sixes_t20'] = 0
    df['career_batsman_total_fours_t20'] = 0
    df['career_batsman_average_runs_t20'] = 0
    df['career_batsman_strike_rate_t20'] = 0
    df['career_bowler_wickets_t20'] = 0
    df['career_bowler_average_t20'] = 0
    df['career_bowler_economy_rate_t20'] = 0
    df['career_fielder_total_catches_t20'] = 0
    df['career_fielder_total_runouts_t20'] = 0

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
                "thirties": 0,
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
        df.at[index, 'career_batsman_total_runs_t20'] = stats['total_runs']
        df.at[index, 'career_batsman_100s_t20'] = stats['hundreds']
        df.at[index, 'career_batsman_50s_t20'] = stats['fifties']
        df.at[index, 'career_batsman_30s_t20'] = stats['thirties']
        df.at[index, 'career_batsman_total_sixes_t20'] = stats['total_sixes']
        df.at[index, 'career_batsman_total_fours_t20'] = stats['total_fours']
        df.at[index, 'career_batsman_average_runs_t20'] = stats['total_runs'] / stats['matches_for_average'] if stats['matches_for_average'] > 0 else 0
        df.at[index, 'career_batsman_strike_rate_t20'] = (stats['total_runs'] / stats['total_balls'] * 100) if stats['total_balls'] > 0 else 0
        df.at[index, 'career_bowler_wickets_t20'] = stats['total_wickets']
        df.at[index, 'career_bowler_average_t20'] = (stats['total_runs_conceded'] / stats['total_wickets']) if stats['total_wickets'] > 0 else 0
        df.at[index, 'career_bowler_economy_rate_t20'] = (stats['total_runs_conceded'] / (stats['total_balls_bowled'] / 6)) if stats['total_balls_bowled'] > 0 else 0
        df.at[index, 'career_fielder_total_catches_t20'] = stats['total_catches']
        df.at[index, 'career_fielder_total_runouts_t20'] = stats['total_runouts']

        # After writing to the DataFrame, update the cumulative stats with the current match's data
        stats['total_runs'] += row['runs_scored']
        stats['total_balls'] += row['balls_faced']
        stats['matches_for_average'] += 1 if row['out'] == 'out' else 0
        
        # Update hundreds, fifties, and thirties while ensuring no overlap
        if row['runs_scored'] >= 100:
            stats['hundreds'] += 1
        elif row['runs_scored'] >= 50:
            stats['fifties'] += 1
        elif row['runs_scored'] >= 30:
            stats['thirties'] += 1

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

    # Drop unnecessary columns
    drop_columns = ['player_name', 'team_name', 'runs_scored', 'balls_faced', 'no_of_fours', 'no_of_sixes',
                    'no_of_catches', 'runouts', 'balls_bowled', 'dot_balls', 'wickets', 'LBWs/Bowled',
                    'runs_conceded', 'stumpings', 'out', 'date', 'venue', 'match_type', 'gender', 'fantasy_points']
    df = df.drop(columns=[col for col in drop_columns if col in df.columns])

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

    print("Career statistics added to the T20 DataFrame with optimized performance!")


def recent_T20(input_file, output_file):
    """
    Processes a T20 match dataset to calculate recent form metrics for each player (last 5 matches), saving the results to a new CSV file.

    This function calculates recent form statistics such as total runs, average, strike rate, hundreds, fifties, wickets, and more 
    for each player based on their last 5 matches. The results are added as new columns to the dataset and saved to a new CSV file.

    Args:
        input_file (str): Path to the input CSV file containing match data.
        output_file (str): Path to the output CSV file where the updated dataset with recent form metrics is saved.

    Returns:
        None: The function writes the results to the specified output CSV file.
    """
    # Load the dataset
    df = pd.read_csv(input_file, low_memory=False)

    # Ensure the date column is in datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Sort the dataframe by date to ensure correct order of matches
    df = df.sort_values(by='date')

    # Initialize dictionaries for sliding windows (queues)
    player_queues = {}

    # Initialize columns for recent form metrics
    df['recent_batsman_total_runs_t20'] = 0
    df['recent_batsman_100s_t20'] = 0
    df['recent_batsman_50s_t20'] = 0
    df['recent_batsman_30s_t20'] = 0
    df['recent_batsman_total_sixes_t20'] = 0
    df['recent_batsman_total_fours_t20'] = 0
    df['recent_batsman_average_runs_t20'] = 0
    df['recent_batsman_strike_rate_t20'] = 0
    df['recent_bowler_wickets_t20'] = 0
    df['recent_bowler_average_t20'] = 0
    df['recent_bowler_economy_rate_t20'] = 0
    df['recent_fielder_total_catches_t20'] = 0
    df['recent_fielder_total_runouts_t20'] = 0

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
                "thirties": deque(),
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
        recent_30s = sum(queues["thirties"])
        recent_50s = sum(queues["fifties"])
        recent_100s = sum(queues["hundreds"])
        recent_runs_conceded = sum(queues["runs_conceded"])
        recent_balls_bowled = sum(queues["balls_bowled"])
        recent_wickets = sum(queues["wickets"])
        recent_catches = sum(queues["catches"])
        recent_runouts = sum(queues["runouts"])

        # Calculate additional metrics
        recent_economy_rate = (recent_runs_conceded / (recent_balls_bowled / 6)) if recent_balls_bowled > 0 else 0
        recent_bowler_average = (recent_runs_conceded / recent_wickets) if recent_wickets > 0 else 0

        # Update recent form metrics in the DataFrame
        df.at[index, 'recent_batsman_total_runs_t20'] = recent_total_runs
        df.at[index, 'recent_batsman_100s_t20'] = recent_100s
        df.at[index, 'recent_batsman_50s_t20'] = recent_50s
        df.at[index, 'recent_batsman_30s_t20'] = recent_30s
        df.at[index, 'recent_batsman_total_sixes_t20'] = recent_6s
        df.at[index, 'recent_batsman_total_fours_t20'] = recent_4s
        df.at[index, 'recent_batsman_average_runs_t20'] = recent_total_runs / len(queues["runs"]) if len(queues["runs"]) > 0 else 0
        df.at[index, 'recent_batsman_strike_rate_t20'] = (recent_total_runs / recent_total_balls * 100) if recent_total_balls > 0 else 0
        df.at[index, 'recent_bowler_wickets_t20'] = recent_wickets
        df.at[index, 'recent_bowler_average_t20'] = recent_bowler_average
        df.at[index, 'recent_bowler_economy_rate_t20'] = recent_economy_rate
        df.at[index, 'recent_fielder_total_catches_t20'] = recent_catches
        df.at[index, 'recent_fielder_total_runouts_t20'] = recent_runouts

        # Add current match stats to the queue after calculating recent form
        queues["runs"].append(row['runs_scored'])
        queues["balls"].append(row['balls_faced'])
        queues["fours"].append(row['no_of_fours'])
        queues["sixes"].append(row['no_of_sixes'])
        queues["thirties"].append(1 if row['runs_scored'] >= 30 else 0)
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
            queues["thirties"].popleft()
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

    # Drop unnecessary columns
    drop = ['player_name', 'team_name', 'runs_scored', 'balls_faced', 'no_of_fours', 'no_of_sixes',
            'no_of_catches', 'runouts', 'balls_bowled', 'dot_balls', 'wickets', 'LBWs/Bowled',
            'runs_conceded', 'stumpings', 'out', 'date', 'venue', 'match_type', 'gender', 'fantasy_points']
    df = df.drop(columns=[col for col in drop if col in df.columns])

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

    print("Recent form metrics added to the DataFrame with optimized performance!")


def venue_T20(input_file, output_file):
    """
    Processes a T20 match dataset to calculate venue-specific performance metrics for each player, saving the results to a new CSV file.

    This function calculates cumulative performance statistics for each player at each venue, including total runs, strike rate, 
    centuries, fifties, wickets, catches, and economy rate. The results are added as new columns to the dataset and saved to a new CSV file.

    Args:
        input_file (str): Path to the input CSV file containing match data.
        output_file (str): Path to the output CSV file where the updated dataset with venue-specific performance metrics is saved.

    Returns:
        None: The function writes the results to the specified output CSV file.
    """
    # Load the dataset
    df = pd.read_csv(input_file)

    # Ensure the date column is in datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Sort the dataframe by date to ensure correct accumulation
    df = df.sort_values(by='date')

    # Initialize a hashmap to store cumulative statistics for each player-venue combination
    venue_player_stats = {}

    # Initialize columns for venue-specific performance
    df['venue_batsman_total_runs_t20'] = 0
    df['venue_batsman_100s_t20'] = 0
    df['venue_batsman_50s_t20'] = 0
    df['venue_batsman_30s_t20'] = 0
    df['venue_batsman_total_sixes_t20'] = 0
    df['venue_batsman_total_fours_t20'] = 0
    df['venue_batsman_average_runs_t20'] = 0
    df['venue_batsman_strike_rate_t20'] = 0
    df['venue_bowler_wickets_t20'] = 0
    df['venue_bowler_average_t20'] = 0
    df['venue_bowler_economy_rate_t20'] = 0
    df['venue_fielder_total_catches_t20'] = 0
    df['venue_fielder_total_runouts_t20'] = 0

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
                "thirties": 0,
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
        df.at[index, 'venue_batsman_total_runs_t20'] = stats['total_runs']
        df.at[index, 'venue_batsman_100s_t20'] = stats['hundreds']
        df.at[index, 'venue_batsman_50s_t20'] = stats['fifties']
        df.at[index, 'venue_batsman_30s_t20'] = stats['thirties']
        df.at[index, 'venue_batsman_total_sixes_t20'] = stats['total_6s']
        df.at[index, 'venue_batsman_total_fours_t20'] = stats['total_4s']
        df.at[index, 'venue_batsman_average_runs_t20'] = stats['total_runs'] / stats['matches_for_average'] if stats['matches_for_average'] > 0 else 0
        df.at[index, 'venue_batsman_strike_rate_t20'] = (stats['total_runs'] / stats['total_balls'] * 100) if stats['total_balls'] > 0 else 0
        df.at[index, 'venue_bowler_wickets_t20'] = stats['total_wickets']
        df.at[index, 'venue_bowler_average_t20'] = (stats['total_runs_conceded'] / stats['total_wickets']) if stats['total_wickets'] > 0 else 0
        df.at[index, 'venue_bowler_economy_rate_t20'] = (stats['total_runs_conceded'] / (stats['total_balls_bowled'] / 6)) if stats['total_balls_bowled'] > 0 else 0
        df.at[index, 'venue_fielder_total_catches_t20'] = stats['total_catches']
        df.at[index, 'venue_fielder_total_runouts_t20'] = stats['total_runouts']

        # After writing to the DataFrame, update the cumulative stats with the current match's data
        stats['total_runs'] += row['runs_scored']
        stats['total_balls'] += row['balls_faced']
        stats['matches_for_average'] += 1 if row['out'] == 'out' else 0
        stats['hundreds'] += 1 if row['runs_scored'] >= 100 else 0
        stats['fifties'] += 1 if 50 <= row['runs_scored'] < 100 else 0  # Only count fifties if not hundreds
        stats['thirties'] += 1 if 30 <= row['runs_scored'] < 50 else 0  # Only count thirties if not fifties
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

    # Drop unnecessary columns
    drop = ['player_name', 'team_name', 'runs_scored', 'balls_faced', 'no_of_fours', 'no_of_sixes',
            'no_of_catches', 'runouts', 'balls_bowled', 'dot_balls', 'wickets', 'LBWs/Bowled',
            'runs_conceded', 'stumpings', 'out', 'date', 'venue', 'match_type', 'gender', 'fantasy_points']
    df = df.drop(columns=[col for col in drop if col in df.columns])

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

    print("Venue-specific performance added to the DataFrame with optimized performance!")