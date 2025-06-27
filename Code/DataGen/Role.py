import os
import csv

# Define input and output file paths
input_csv = "./CSVs/Overall_PlayerStats.csv"
output_csv = "./CSVs/Designation.csv"

# Define thresholds for role assignment
BATSMAN_AVERAGE_RUNS_THRESHOLD = 18
ALLROUNDER_WICKETS_PER_INNINGS_THRESHOLD = 0.2
BOWLER_WICKETS_PER_INNINGS_THRESHOLD = 0.4

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# Read Overall_PlayerStats.csv and process each player's role
designation_data = []

with open(input_csv, mode="r") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        player_id = row['player_id']
        player_name = row['player_name']
        batting_innings = int(row['batting_innings'])
        bowling_innings = int(row['bowling_innings'])
        total_runs = int(row['total_runs_scored'])
        total_wickets = int(row['total_wickets'])
        total_stumpings = int(row['total_stumpings'])

        # Calculate derived metrics
        batting_average = total_runs / batting_innings if batting_innings > 0 else 0
        wickets_per_innings = total_wickets / bowling_innings if bowling_innings > 0 else 0

        # Assign role
        if total_stumpings != 0:
            role = 'Wicket-Keeper'
        elif batting_innings > 5 * bowling_innings:
            role = 'Batsman'
        elif batting_average >= BATSMAN_AVERAGE_RUNS_THRESHOLD:
            if wickets_per_innings >= ALLROUNDER_WICKETS_PER_INNINGS_THRESHOLD:
                role = 'All-Rounder'
            else:
                role = 'Batsman'
        elif wickets_per_innings > BOWLER_WICKETS_PER_INNINGS_THRESHOLD:
            role = 'Bowler'
        else:
            role = 'All-Rounder'

        # Append the result to the designation data
        designation_data.append({
            'player_id': player_id,
            'player_name': player_name,
            'Role': role
        })

# Write Designation.csv
with open(output_csv, mode="w", newline="") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=['player_id', 'player_name', 'role'])
    writer.writeheader()
    writer.writerows(designation_data)

print(f"Designation file created: {output_csv}")
