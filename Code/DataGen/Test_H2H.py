import json
import csv
import os

# Define directories
json_folder = "all_json"  # Folder containing all JSON files
output_csv = "CSVs/Test_H2H.csv"  # Single CSV file to save all data

# List of fields for CSV
csv_fields = [
    'match_id', 'batsman_id', 'batsman_name', 'batsman_team', 'bowler_id', 'bowler_name', 'bowler_team',
    'runs_scored', 'balls_faced', 'runs_conceded', 'balls_bowled', '4s', '6s', 'wickets',
    'gender', 'venue', 'date', 'match_type', 'wicket_type_1', 'wicket_type_2'
]

# Ensure the output folder exists
if not os.path.exists("CSVs"):
    os.makedirs("CSVs")

# Open the CSV file in append mode (if it exists) or write mode (if it doesn't)
with open(output_csv, mode="w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_fields)
    
    # Write the header only if the CSV is empty (i.e., the file is being created for the first time)
    writer.writeheader()

    # Iterate through all JSON files in the folder
    for json_file in os.listdir(json_folder):
        if json_file.endswith(".json"):  # Process only JSON files
            input_path = os.path.join(json_folder, json_file)
            match_id = os.path.splitext(json_file)[0]  # Get match ID from file name

            # Load JSON data
            with open(input_path, "r") as f:
                match_data = json.load(f)

            # Extract match type and skip if it's not a Test or MDM match
            match_type = match_data['info']['match_type']
            if match_type.lower() == "test" or match_type.lower() == "mdm":

                # Extract match details
                match_date = match_data['info']['dates'][0]
                venue = match_data['info']['venue']
                gender = match_data['info']['gender']

                # Map player names to their IDs from the registry
                player_registry = match_data['info']['registry']['people']

                # Create a mapping of players to their teams
                player_teams = {}
                if 'players' in match_data['info']:
                    for team_name, team_players in match_data['info']['players'].items():
                        for player_name in team_players:
                            player_teams[player_name] = team_name

                # Dictionary to store aggregated stats for each batsman-bowler pair
                head_to_head_data = {}

                # Iterate through each inning in the match
                inning_index = 0
                for inning in match_data['innings']:
                    inning_index += 1
                    if 'overs' not in inning:
                        continue  # Skip this inning or handle it accordingly

                    for over in inning['overs']:
                        for delivery in over['deliveries']:
                            # Extract delivery details
                            batter = delivery['batter']
                            bowler = delivery['bowler']

                            # Generate unique key for batsman-bowler pair
                            key = (batter, bowler)

                            # Update the aggregated stats
                            if key not in head_to_head_data:
                                head_to_head_data[key] = {
                                    'batsman_id': player_registry[batter],
                                    'batsman_name': batter,
                                    'batsman_team': player_teams.get(batter, "Unknown"),
                                    'bowler_id': player_registry[bowler],
                                    'bowler_name': bowler,
                                    'bowler_team': player_teams.get(bowler, "Unknown"),
                                    'runs_scored': 0,
                                    'balls_faced': 0,
                                    'runs_conceded': 0,
                                    'balls_bowled': 0,
                                    '4s': 0,
                                    '6s': 0,
                                    'wickets': 0,
                                    'wicket_type_1': "",
                                    'wicket_type_2': ""
                                }

                            # Handle extras
                            extras = delivery.get('extras', {})
                            if 'byes' in extras:
                                head_to_head_data[key]['balls_bowled'] += 1
                                head_to_head_data[key]['balls_faced'] += 1
                                head_to_head_data[key]['runs_conceded'] += extras['byes']
                            elif 'legbyes' in extras:
                                head_to_head_data[key]['balls_bowled'] += 1
                                head_to_head_data[key]['balls_faced'] += 1
                                head_to_head_data[key]['runs_conceded'] += extras['legbyes']
                            elif 'wides' in extras:
                                head_to_head_data[key]['runs_conceded'] += extras['wides']
                                head_to_head_data[key]['balls_bowled'] += 1
                            elif 'noballs' in extras:
                                head_to_head_data[key]['runs_conceded'] += extras['noballs'] + delivery['runs']['batter']
                                head_to_head_data[key]['runs_scored'] += delivery['runs']['batter']
                                head_to_head_data[key]['balls_faced'] += 1
                                if delivery['runs']['batter'] == 4:
                                    head_to_head_data[key]['4s'] += 1
                                elif delivery['runs']['batter'] == 6:
                                    head_to_head_data[key]['6s'] += 1
                            else:
                                head_to_head_data[key]['balls_bowled'] += 1
                                head_to_head_data[key]['balls_faced'] += 1
                                head_to_head_data[key]['runs_conceded'] += delivery['runs']['total']
                                head_to_head_data[key]['runs_scored'] += delivery['runs']['total']
                                if delivery['runs']['batter'] == 4:
                                    head_to_head_data[key]['4s'] += 1
                                elif delivery['runs']['batter'] == 6:
                                    head_to_head_data[key]['6s'] += 1

                            # Process wickets
                            if 'wickets' in delivery:
                                for wicket_info in delivery['wickets']:
                                    if wicket_info['player_out'] == batter:
                                        head_to_head_data[key]['wickets'] += 1
                                        if inning_index in (1, 2):
                                            head_to_head_data[key]['wicket_type_1'] = wicket_info['kind']
                                        elif inning_index in (3, 4):
                                            head_to_head_data[key]['wicket_type_2'] = wicket_info['kind']

                # Write aggregated data to the single CSV file
                for key, stats in head_to_head_data.items():
                    stats.update({
                        'match_id': match_id,
                        'gender': gender,
                        'venue': venue,
                        'date': match_date,
                        'match_type': match_type
                    })
                    writer.writerow(stats)

print(f"Data has been written to {output_csv}")
