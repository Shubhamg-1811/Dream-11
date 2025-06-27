import pandas as pd


def process_player_match_data(designation_file, test_matchwise_file, output_file):
    """
    Merges designation data with test matchwise fantasy points data to create a player match data file which includes match_id, player_id, player_name, fantasy_points, team_name, role, date, venue.
    
    Parameters:
        designation_file (str): Path to the designation CSV file.
        test_matchwise_file (str): Path to the test matchwise fantasy points CSV file.
        output_file (str): Path to save the processed CSV file.
    """
    try:
        # Load the necessary datasets
        designation_df = pd.read_csv(designation_file)
        test_matchwise_df = pd.read_csv(test_matchwise_file, low_memory=False)

        # Print column names to verify presence of 'player_name' and 'player_id'
        print("test MatchWise Columns:", test_matchwise_df.columns)
        print("Designation Columns:", designation_df.columns)

        # Ensure both 'player_id' and 'player_name' are present in both dataframes
        required_columns = {'player_id', 'player_name'}
        if not required_columns.issubset(test_matchwise_df.columns):
            raise ValueError("'player_id' or 'player_name' not found in test MatchWise data.")
        if not required_columns.issubset(designation_df.columns):
            raise ValueError("'player_id' or 'player_name' not found in Designation data.")

        # Perform an inner join on both 'player_id' and 'player_name' to ensure accurate matches
        player_match_data = test_matchwise_df.merge(designation_df, on=['player_id', 'player_name'], how='inner')[
            ['match_id', 'player_id', 'player_name', 'fantasy_points', 'team_name', 'role', 'date','venue']
        ]

        # Save the resulting dataframe to a CSV file
        player_match_data.to_csv(output_file, index=False)
        print(f"CSV file '{output_file}' created successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")


# # Example Usage
# process_player_match_data(
#     '../data/interim/Designation.csv',
#     '../data/interim/Test_MatchWise_fantasy_points.csv',
#     '../data/processed/Test/player_match_data_test.csv'
# )
