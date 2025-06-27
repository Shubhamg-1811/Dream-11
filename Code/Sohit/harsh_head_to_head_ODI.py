import pandas as pd

# Load the dataset
df_h2h_odi = pd.read_csv('../../CSVs/ODI_H2H.csv',low_memory=False)

# Ensure the date column is in datetime format and filter by date
df_h2h_odi['date'] = pd.to_datetime(df_h2h_odi['date'])
df_h2h_odi = df_h2h_odi[df_h2h_odi['date'] <= '2024-06-30']

# Sort by date for proper cumulative calculations
df_h2h_odi = df_h2h_odi.sort_values(by='date')

# Initialize a hashmap (dictionary) to store cumulative stats for each batsman-bowler pair
h2h_stats = {}

# Add new columns for cumulative stats
df_h2h_odi['cum_h2h_runs_scored'] = 0
df_h2h_odi['cum_h2h_balls_faced'] = 0
df_h2h_odi['cum_h2h_runs_conceded'] = 0
df_h2h_odi['cum_h2h_balls_bowled'] = 0
df_h2h_odi['cum_h2h_4s'] = 0
df_h2h_odi['cum_h2h_6s'] = 0
df_h2h_odi['cum_h2h_wickets'] = 0


# Process each row
for index, row in df_h2h_odi.iterrows():
    pair = (row['batsman_id'], row['bowler_id'])

    # Initialize stats if pair is not in the dictionary
    if pair not in h2h_stats:
        h2h_stats[pair] = {
            'runs_scored': 0,
            'balls_faced': 0,
            'runs_conceded': 0,
            'balls_bowled': 0,
            '4s': 0,
            '6s': 0,
            'wickets': 0
            
        }

    # Get the current stats for the pair
    stats = h2h_stats[pair]

    # Add cumulative stats to the DataFrame
    df_h2h_odi.at[index, 'cum_h2h_runs_scored'] = stats['runs_scored']
    df_h2h_odi.at[index, 'cum_h2h_balls_faced'] = stats['balls_faced']
    df_h2h_odi.at[index, 'cum_h2h_runs_conceded'] = stats['runs_conceded']
    df_h2h_odi.at[index, 'cum_h2h_balls_bowled'] = stats['balls_bowled']
    df_h2h_odi.at[index, 'cum_h2h_4s'] = stats['4s']
    df_h2h_odi.at[index, 'cum_h2h_6s'] = stats['6s']
    df_h2h_odi.at[index, 'cum_h2h_wickets'] = stats['wickets']
   

    # Update the stats with the current row's data
    stats['runs_scored'] += row['runs_scored']
    stats['balls_faced'] += row['balls_faced']
    stats['runs_conceded'] += row['runs_conceded']
    stats['balls_bowled'] += row['balls_bowled']
    stats['4s'] += row['4s']
    stats['6s'] += row['6s']
    stats['wickets'] += row['wickets']
    

# Save the updated DataFrame to a new CSV file
df_h2h_odi.to_csv('../../CSVs/Sohit/harsh_cumulated_h2h_stats_odi.csv', index=False)

print("Cumulative head-to-head statistics added successfully!")
