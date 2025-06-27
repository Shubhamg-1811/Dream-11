# import pandas as pd

# # Load the dataset (replace 'your_file.csv' with the actual filename)
# df_h2h_odi = pd.read_csv('CSVs/ODI_H2H.csv.csv')

# # Remove the 'wicket_type' column
# df_h2h_odi = df_h2h_odi.drop(columns=['wicket_type'])

# # Group by batsman and bowler to aggregate statistics
# combined_df = df_h2h_odi.groupby(
#     ['batsman_id', 'batsman_name', 'batsman_team', 'bowler_id', 'bowler_name', 'bowler_team']
# ).agg({
#     'runs_scored': 'sum',
#     'balls_faced': 'sum',
#     'runs_conceded': 'sum',
#     'balls_bowled': 'sum',
#     '4s': 'sum',
#     '6s': 'sum',
#     'wickets': 'sum',
#     # Optional: Include other columns if needed
# }).reset_index()

# # Display the combined dataframe
# print(combined_df)

# # Save to a new CSV if needed
# combined_df.to_csv('combined_h2h_stats.csv', index=False)
import pandas as pd

# Load the dataset (replace 'your_file.csv' with the actual filename)
df_test_h2h = pd.read_csv('../../CSVs/Test_H2H.csv')



#### ADDING DATE CUTOFF SO THAT WE DONT'T GET DISCO-LIFIED

df_test_h2h=df_test_h2h[df_test_h2h['date']<='2024-06-30']






df_test_h2h['bowled_lbw_count'] = df_test_h2h.apply(
    lambda row: (1 if row['wicket_type_1'] in ['bowled', 'lbw'] else 0) +
                (1 if row['wicket_type_2'] in ['bowled', 'lbw'] else 0),
    axis=1
)


# Group by batsman and bowler to aggregate statistics
combined_df = df_test_h2h.groupby(
    ['batsman_id', 'batsman_name', 'batsman_team', 'bowler_id', 'bowler_name', 'bowler_team']
).agg({
    'runs_scored': 'sum',
    'balls_faced': 'sum',
    'runs_conceded': 'sum',
    'balls_bowled': 'sum',
    '4s': 'sum',
    '6s': 'sum',
    'wickets': 'sum',
    'bowled_lbw_count': 'sum'  # Count of bowled or lbw dismissals
}).reset_index()

# Rename the aggregated columns with the new naming convention
column_renames = {
    'runs_scored': 'h2h_runs_scored_test',
    'balls_faced': 'h2h_balls_faced_test',
    'runs_conceded': 'h2h_runs_conceded_test',
    'balls_bowled': 'h2h_balls_bowled_test',
    '4s': 'h2h_4s_test',
    '6s': 'h2h_6s_test',
    'wickets': 'h2h_wickets_test',
    'bowled_lbw_count': 'h2h_bowled_lbw_test'
}
combined_df = combined_df.rename(columns=column_renames)

# Display the combined dataframe
print(combined_df)

# Save to a new CSV if needed
combined_df.to_csv('../../CSVs/Sohit/combined_h2h_stats_test.csv', index=False)
