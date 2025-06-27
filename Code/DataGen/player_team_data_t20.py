import pandas as pd

# Load the necessary datasets
designation_df = pd.read_csv('../../CSVs/Designation.csv')  # Path to the designation file
odi_matchwise_df = pd.read_csv('../../CSVs/fantasy_points/T20_MatchWise_fantasy_points.csv', low_memory=False)  # Path to the ODI match-wise data file

# Print column names to verify the presence of 'player_name'
print("ODI MatchWise Columns:", odi_matchwise_df.columns)
print("Designation Columns:", designation_df.columns)

# Ensure both 'player_id' and 'player_name' are present in both dataframes
if 'player_id' not in odi_matchwise_df.columns or 'player_name' not in odi_matchwise_df.columns:
    print("Error: 'player_id' or 'player_name' not found in ODI MatchWise data.")
    exit()

if 'player_id' not in designation_df.columns or 'player_name' not in designation_df.columns:
    print("Error: 'player_id' or 'player_name' not found in Designation data.")
    exit()

# Perform an inner join on both 'player_id' and 'player_name' to ensure accurate matches
player_match_data = odi_matchwise_df.merge(designation_df, on=['player_id', 'player_name'], how='inner')[
    ['match_id', 'player_id', 'player_name', 'fantasy_points', 'team_name', 'role', 'date']
]

# Save the resulting dataframe to a CSV file
output_file = '../../CSVs/Final/T20/player_match_data_t20.csv'
player_match_data.to_csv(output_file, index=False)

print(f"CSV file '{output_file}' created successfully!")
